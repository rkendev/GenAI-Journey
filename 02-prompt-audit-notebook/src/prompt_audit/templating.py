from pathlib import Path
from typing import Dict, List

import jinja2
import yaml

_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates"),
    autoescape=False,  # plaintext prompts
    trim_blocks=True,
    lstrip_blocks=True,
)


def build_messages(
    question: str,
    context: str | None = None,
    persona: str | None = None,
    format: str | None = None,
) -> List[Dict]:
    data = {
        "question": question,
        "context": context or "",
        "persona": persona,
        "format": format,
        "max_tokens_answer": 120,
    }

    system = _ENV.get_template("system.j2").render(data)
    user = _ENV.get_template("user.j2").render(data)

    # prepend few-shot examples
    examples = yaml.safe_load(
        (Path(__file__).parent / "templates" / "examples.yml").read_text()
    )

    return [
        {"role": "system", "content": system},
        *examples,
        {"role": "user", "content": user},
    ]
