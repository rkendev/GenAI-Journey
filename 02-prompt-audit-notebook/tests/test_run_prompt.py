from unittest.mock import MagicMock, patch

from prompt_audit.client import run_prompt
from prompt_audit.templating import build_messages


def _dummy_resp(text: str = "Hello"):
    choice = MagicMock(message=MagicMock(content=text))
    usage = MagicMock(completion_tokens=len(text), total_tokens=len(text) + 4)
    return MagicMock(choices=[choice], usage=usage)


@patch("prompt_audit.client.client.chat.completions.create")
def test_run_prompt_offline(mock_create):
    mock_create.return_value = _dummy_resp()

    output = run_prompt(
        [{"role": "user", "content": "Say hello in one word."}],
        temperature=0,
        stream=False,
    )
    assert output == "Hello"
    mock_create.assert_called_once()


def test_template_minimal():
    msgs = build_messages("Ping?")
    assert msgs[0]["role"] == "system"
    assert "Ping?" in msgs[-1]["content"]
