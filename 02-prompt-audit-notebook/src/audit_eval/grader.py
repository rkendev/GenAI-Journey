from __future__ import annotations

import sqlite3
import time
import uuid
from pathlib import Path

from prompt_audit.client import run_prompt
from prompt_audit.templating import build_messages

# --------------------------------------------------------------------------- #
# Lazy, per-process SQLite connection
# --------------------------------------------------------------------------- #
_OUT_DIR = Path(__file__).parents[2] / "outputs"
_OUT_DIR.mkdir(exist_ok=True)


def _get_conn() -> sqlite3.Connection:
    """
    Create (once per Python process) a SQLite database named run_<epoch>.sqlite
    and cache the connection for the remainder of the process.
    """
    if not hasattr(_get_conn, "_conn"):
        db_path = _OUT_DIR / f"run_{int(time.time())}.sqlite"
        conn = sqlite3.connect(db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS eval (
              id TEXT PRIMARY KEY,
              question TEXT,
              reference TEXT,
              answer TEXT,
              judge TEXT,
              passed INT,
              latency REAL,
              cost_usd REAL
            )
            """
        )
        _get_conn._conn = conn
    return _get_conn._conn


# --------------------------------------------------------------------------- #
# Single-row grader
# --------------------------------------------------------------------------- #
_RUBRIC = """
You are a strict grader but may allow brief additional context.
• PASS if the answer clearly contains the correct fact (case-insensitive).
• FAIL if the answer is missing or contradicts the reference.
Reply with exactly PASS or FAIL.
""".strip()


def grade_row(question: str, reference: str, temperature: float = 0.0) -> bool:
    """
    Ask the main model to answer `question`, then ask an LLM judge (GPT-4-o) to
    evaluate.  Returns True (PASS) or False (FAIL) and logs the result.
    """
    conn = _get_conn()

    # 1) Get model answer
    start = time.time()
    answer = run_prompt(build_messages(question), temperature=temperature)
    latency = time.time() - start

    # 2) Cheap exact-string shortcut (saves cost if obvious match)
    if reference.lower() in answer.lower():
        passed = True
        verdict = "PASS (exact match shortcut)"
    else:
        judge_msg = [
            {"role": "system", "content": _RUBRIC},
            {
                "role": "user",
                "content": (
                    f"Q: {question}\n" f"Reference: {reference}\n" f"Answer: {answer}"
                ),
            },
        ]
        verdict = run_prompt(judge_msg, temperature=0).strip()
        passed = verdict.upper().startswith("PASS")

    # 3) Naïve cost placeholder (replace with usage.metadata if desired)
    cost = 0.000_002 * len(answer.split())

    conn.execute(
        "INSERT INTO eval VALUES (?,?,?,?,?,?,?,?)",
        (
            str(uuid.uuid4()),
            question,
            reference,
            answer,
            verdict,
            int(passed),
            latency,
            cost,
        ),
    )
    conn.commit()
    return passed
