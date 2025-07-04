"""Prompt-audit library stubs."""

from __future__ import annotations

import time
import uuid
from typing import Any, Dict

__all__ = ["run_prompt", "log_call"]


def run_prompt(client, prompt: str, **completion_kwargs) -> str:
    """Wrap an LLM client call (stub)."""
    start = time.time()
    response = client.chat.completions.create(  # type: ignore
        messages=[{"role": "user", "content": prompt}],
        **completion_kwargs,
    )
    duration = time.time() - start
    log_call(prompt, response, duration)
    return response.choices[0].message.content  # type: ignore


def log_call(prompt: str, response: Any, latency: float) -> None:
    """Persist call metadata (stub)."""
    meta: Dict[str, Any] = {
        "id": str(uuid.uuid4()),
        "prompt": prompt,
        "latency_s": latency,
        "tokens_in": getattr(response, "usage", {}).get("prompt_tokens", None),
        "tokens_out": getattr(response, "usage", {}).get("completion_tokens", None),
    }
    print("[prompt-audit]", meta)
