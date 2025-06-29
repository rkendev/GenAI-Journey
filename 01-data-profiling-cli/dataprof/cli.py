# dataprof/cli.py

import glob
import json
import os
import re
import sqlite3
import time
from pathlib import Path
from random import random

import matplotlib.pyplot as plt
import pandas as pd
import typer
from click import get_current_context
from matplotlib.lines import Line2D
from ydata_profiling import ProfileReport

app = typer.Typer(
    help="🛠️  **Data Profiling CLI**: generate profiling reports and monitor performance trends.",
    add_completion=True,
    rich_markup_mode="markdown",
)
cli = app  # alias for poetry entry point


def reservoir_sample(
    filepath: Path, k: int, chunksize: int, reader_kwargs: dict
) -> pd.DataFrame:
    """Perform reservoir sampling of size k over the CSV at filepath."""
    reservoir, total = [], 0
    for chunk in pd.read_csv(filepath, chunksize=chunksize, **reader_kwargs):
        for row in chunk.itertuples(index=False):
            total += 1
            if len(reservoir) < k:
                reservoir.append(row)
            else:
                r = int(random() * total)
                if r < k:
                    reservoir[r] = row
    cols = reservoir[0]._fields if reservoir else reader_kwargs.get("usecols", [])
    return pd.DataFrame(reservoir, columns=cols)


@app.command("profile", no_args_is_help=True)
def profile(
    # ─── I/O Options ─────────────────────────────────────────────────────────
    filepath: Path = typer.Argument(
        ...,
        exists=True,
        help="📄 **Path** to the input CSV or table file.",
    ),
    out: Path = typer.Option(
        Path("reports"),
        "--out",
        "-o",
        dir_okay=True,
        file_okay=False,
        help="📂 **Output directory** for reports (will be created).",
    ),
    # ─── Sampling Options ─────────────────────────────────────────────────────
    sample: float = typer.Option(
        None,
        "--sample",
        help="🎲 Random fraction _0–1_ to sample each chunk (ignored if `--reservoir-size`).",
    ),
    reservoir_size: int = typer.Option(
        None,
        "--reservoir-size",
        help="🌀 One-pass reservoir sample size (takes precedence over `--sample`).",
    ),
    chunksize: int = typer.Option(
        10_000,
        "--chunksize",
        help="📑 Number of rows per read chunk for large files.",
    ),
    # ─── Quality Options ───────────────────────────────────────────────────────
    expectations: bool = typer.Option(
        False,
        "--expectations",
        help="✅ Auto-generate & validate a Great Expectations suite (stub).",
    ),
    # ─── Miscellaneous Options ─────────────────────────────────────────────────
    minimal: bool = typer.Option(
        True,
        "--minimal/--full",
        help="⚙️ Use **minimal** (fast) or **full** profiling report.",
    ),
    json_out: bool = typer.Option(
        False,
        "--json-out",
        help="📦 Also emit a JSON version of the final report.",
    ),
):
    """
    Generate fast HTML (and optional JSON) profiling reports,
    with optional data-quality stubs.
    """
    os.makedirs(out, exist_ok=True)
    start = time.time()

    # Build reader kwargs (ignore any "extra" column)
    reader_kwargs = {
        "usecols": [c for c in pd.read_csv(filepath, nrows=0).columns if c != "extra"]
    }

    # Ingest & sample
    if reservoir_size:
        df = reservoir_sample(filepath, reservoir_size, chunksize, reader_kwargs)
        typer.echo(f"🌀 Reservoir sample of {len(df)} rows drawn in one pass")
    else:
        parts = []
        datetime_re = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
        for i, chunk in enumerate(
            pd.read_csv(filepath, chunksize=chunksize, **reader_kwargs)
        ):
            if sample and 0 < sample < 1:
                chunk = chunk.sample(frac=sample)
            # datetime sanity check
            for col in chunk.select_dtypes(include=["object"]).columns:
                if datetime_re.match(str(chunk[col].iat[0])):
                    invalid = chunk[~chunk[col].astype(str).str.match(datetime_re)]
                    if not invalid.empty:
                        typer.secho(
                            f"⚠️ Invalid datetime in chunk {i}, col {col}",
                            fg=typer.colors.YELLOW,
                        )
            mini = ProfileReport(chunk, explorative=True, minimal=True)
            mini_path = out / f"chunk_{i:03d}.json"
            mini.to_file(mini_path)
            typer.echo(f"➡️ Chunk {i} summary written to {mini_path}")
            parts.append(chunk)
        df = pd.concat(parts, ignore_index=True)

    # Full profiling report
    report = ProfileReport(
        df, title="Data Profiling Report", explorative=True, minimal=minimal
    )
    html_path = out / "report.html"
    report.to_file(html_path)
    typer.secho(f"✅ HTML report written to {html_path}", fg=typer.colors.GREEN)

    if json_out:
        json_path = out / "report.json"
        report.to_file(json_path)
        typer.echo(f"📦 JSON report written to {json_path}")

    # Expectations stub
    if expectations:
        suite_path = out / "expectations.json"
        with open(suite_path, "w") as f:
            json.dump({"expectations": []}, f, indent=2)
        typer.secho(
            f"🧪 Expectations suite written to {suite_path}",
            fg=typer.colors.CYAN,
            err=True,
        )
        get_current_context().exit(1)

    # Persist run metadata
    duration = time.time() - start
    conn = sqlite3.connect("runs.db")
    conn.execute(
        """
      CREATE TABLE IF NOT EXISTS runs (
        file       TEXT PRIMARY KEY,
        duration   REAL,
        sample     REAL,
        chunksize  INTEGER,
        reservoir  INTEGER DEFAULT 0,
        timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    """
    )
    conn.execute(
        """
      INSERT INTO runs (file, duration, sample, chunksize, reservoir)
      VALUES (?, ?, ?, ?, ?)
      ON CONFLICT(file) DO UPDATE SET
        duration  = excluded.duration,
        sample    = excluded.sample,
        chunksize = excluded.chunksize,
        reservoir = excluded.reservoir
    """,
        (str(filepath), duration, sample or 0.0, chunksize, reservoir_size or 0),
    )
    conn.commit()
    conn.close()

    typer.echo(f"⏱  Completed in {duration:.2f}s")


@app.command("plot-trends")
def plot_trends(
    db: Path = typer.Option(
        Path("runs.db"), "--db", help="SQLite DB file containing profiling runs."
    ),
):
    """Plot runtime vs. sample-fraction trends from the runs table."""
    conn = sqlite3.connect(db)
    df = pd.read_sql(
        "SELECT timestamp, duration, sample, reservoir FROM runs ORDER BY timestamp",
        conn,
    )
    conn.close()

    df["sample"] = df["sample"].fillna(0).astype(float)
    fig, ax = plt.subplots()
    ax.scatter(
        df["sample"],
        df["duration"],
        c=(df["reservoir"] > 0).map({True: "red", False: "blue"}),
        alpha=0.7,
    )
    ax.set_xlabel("Sample Fraction")
    ax.set_ylabel("Duration (s)")
    ax.set_title("Duration vs. Sample Fraction")
    legend_elems = [
        Line2D(
            [0],
            [0],
            marker="o",
            label="Reservoir run",
            markerfacecolor="red",
            markersize=8,
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            label="Full-data run",
            markerfacecolor="blue",
            markersize=8,
        ),
    ]
    ax.legend(handles=legend_elems)
    plt.tight_layout()
    plt.savefig("runtime_vs_sample.png")
    typer.secho("📈 Scatter plot saved to runtime_vs_sample.png", fg=typer.colors.GREEN)


@app.command("aggregate-chunks")
def aggregate_chunks(
    reports_dir: Path = typer.Argument(
        ..., exists=True, file_okay=False, help="Directory with `chunk_*.json` files."
    ),
    out: Path = typer.Option(
        Path("summary.json"), help="Output JSON file for aggregated summary."
    ),
):
    """
    Aggregate all per-chunk JSON summaries in REPORTS_DIR into a single JSON file.
    """
    pattern = reports_dir / "chunk_*.json"
    files = sorted(glob.glob(str(pattern)))
    if not files:
        typer.secho(
            f"⚠️ No chunk JSON files found in {reports_dir}", fg=typer.colors.YELLOW
        )
        raise typer.Exit(0)

    aggregated = []
    for path in files:
        with open(path) as f:
            data = json.load(f)
        aggregated.append({"chunk_file": os.path.basename(path), "profile": data})

    with open(out, "w") as f:
        json.dump({"chunks": aggregated}, f, indent=2)

    typer.secho(
        f"🔗 Aggregated {len(aggregated)} chunk summaries into {out}",
        fg=typer.colors.GREEN,
    )


def main():
    app()


if __name__ == "__main__":
    main()
