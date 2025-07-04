from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table

OUT_DIR = Path("outputs")
candidates = sorted(OUT_DIR.glob("run_*.sqlite"), reverse=True)

# Grab the newest DB **that actually contains rows**
for db_path in candidates:
    df = pd.read_sql("SELECT * FROM eval", sqlite3.connect(db_path))
    if not df.empty:
        break
else:
    raise SystemExit("❌  No non-empty evaluation runs found in outputs/")

accuracy = df["passed"].mean() * 100
table = Table(title=f"Evaluation run {db_path.name} — Accuracy {accuracy:.1f}%")

for col in ["question", "answer", "passed"]:
    table.add_column(col, overflow="fold")

for _, row in df.iterrows():
    table.add_row(
        row["question"],
        row["answer"][:80] + ("…" if len(row["answer"]) > 80 else ""),
        "✅" if row["passed"] else "❌",
    )

Console().print(table)

# Write Markdown snapshot for Git history / diff
md_path = db_path.with_suffix(".sqlite.md")
df.to_markdown(md_path, index=False)
