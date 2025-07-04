# src/prompt_audit/client.py
from __future__ import annotations

import json
import time
import uuid
from typing import Iterator, List

from openai import OpenAI  # >= 1.90
from tenacity import retry, stop_after_attempt, wait_random_exponential  # type: ignore

from .settings import Settings
from .utils import LOGGER, count_tokens

CFG = Settings()
client = OpenAI(api_key=CFG.openai_api_key, timeout=CFG.request_timeout)


def _log(meta: dict) -> None:
    LOGGER.info(json.dumps(meta, default=str))


def _meta(prompt_tokens: int) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "model": CFG.openai_model,
        "prompt_tokens": prompt_tokens,
        "ts": time.time(),
    }


@retry(
    wait=wait_random_exponential(multiplier=1, max=20),
    stop=stop_after_attempt(CFG.max_retries),
)
def run_prompt(
    messages: List[dict], stream: bool = False, **kwargs
) -> str | Iterator[str]:
    """High-level helper that retries on rate-limit / 5xx and logs cost."""
    prompt_tokens = count_tokens(messages, CFG.openai_model)
    meta = _meta(prompt_tokens)

    if stream:
        # stream chunks back to caller
        chunk_iter = client.chat.completions.create(
            model=CFG.openai_model,
            messages=messages,
            stream=True,
            **kwargs,
        )

        def generator():
            completion_tokens = 0
            full = []
            for chunk in chunk_iter:
                delta = chunk.choices[0].delta.content or ""
                completion_tokens += len(delta)
                full.append(delta)
                yield delta
            meta.update(
                {
                    "completion_tokens": completion_tokens,
                    "total_tokens": prompt_tokens + completion_tokens,
                }
            )
            _log(meta)

        return generator()

    # non-stream call
    resp = client.chat.completions.create(
        model=CFG.openai_model,
        messages=messages,
        stream=False,
        **kwargs,
    )
    completion_tokens = (
        resp.usage.completion_tokens
    )  # field always present :contentReference[oaicite:7]{index=7}
    meta.update(
        {
            "completion_tokens": completion_tokens,
            "total_tokens": resp.usage.total_tokens,
        }
    )
    _log(meta)
    return resp.choices[0].message.content
