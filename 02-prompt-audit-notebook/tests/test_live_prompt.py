# tests/test_live_prompt.py
import pytest
from openai import AuthenticationError, RateLimitError
from prompt_audit.client import run_prompt
from prompt_audit.templating import build_messages


@pytest.mark.live  # you can skip these in CI if you like
def test_rlhf_two_bullets():
    try:
        messages = build_messages("Explain RLHF in two bullets")
        out = run_prompt(messages, temperature=0.4, top_p=0.9)
    except (RateLimitError, AuthenticationError):
        pytest.skip("API quota/auth issue")
    assert "•" in out or "-" in out  # crude sanity-check
