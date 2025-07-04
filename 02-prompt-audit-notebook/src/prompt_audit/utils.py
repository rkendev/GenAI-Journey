# src/prompt_audit/utils.py
from __future__ import annotations

import logging
from typing import List

import tiktoken

LOGGER = logging.getLogger("prompt-audit")
if not LOGGER.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)

ENC_CACHE: dict[str, tiktoken.Encoding] = {}


def count_tokens(messages: List[dict], model: str) -> int:
    # cache encoding for speed
    enc = ENC_CACHE.setdefault(model, tiktoken.encoding_for_model(model))
    num_tokens = 0
    for m in messages:
        num_tokens += 4  # every message overhead (see cookbook)
        for v in m.values():
            num_tokens += len(enc.encode(v))
    num_tokens += 2  # assistant priming
    return num_tokens
