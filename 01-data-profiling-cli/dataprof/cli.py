# dataprof/cli.py

import glob
import json
import os
import re
import sqlite3
import time
from pathlib import Path
from random import random
from typing import Any, Dict, Iterator, Union

import matplotlib.pyplot as plt
import pandas as pd
import typer
import yaml
from click import get_current_context
from matplotlib.lines import Line2D
from ydata_profiling import ProfileReport

app = typer.Typer(
    help="🛠️  **Data Profiling CLI**: generate profiling reports and monitor performance trends.",
    add_completion=True,
    rich_markup_mode="markdown",
)
cli = app  # alias for the entry point


def load_data(
    filepath: Path,
    reader_kwargs: Dict[str, Any],
    chunksize: Union[int, None] = None,
) -> Iterator[pd.DataFrame]:
    """
    Yield DataFrame chunks—or a single DataFrame—for CSV, Parquet, Excel.
    """
    ext = filepath.suffix.lower()
    if ext == ".csv":
        yield from pd.read_csv(filepath, chunksize=chunksize, **reader_kwargs)
    elif ext in {".parquet", ".pq"}:
        yield pd.read_parquet(filepath, **reader_kwargs)
    elif ext in {".xls", ".xlsx"}:
        yield pd.read_excel(filepath, **reader_kwargs)
    else:
        typer.secho(f"❓ Unsupported format: {ext}", fg=typer.colors.RED)
        raise typer.Exit(1)


def reservoir_sample(
    filepath: Path, k: int, chunksize: int, reader_kwargs: dict
) -> pd.DataFrame:
    """Perform reservoir sampling of size k over the file at filepath."""
    reservoir, total = [], 0
    for chunk in load_data(filepath, reader_kwargs, chunksize):
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
    # ─── I/O Options ───────────────────────────────────────────────
    filepath: Path = typer.Argument(
        ...,
        exists=True,
        help="📄 Path to a CSV, Parquet or Excel file.",
    ),
    out: Path = typer.Option(
        Path("reports"),
        "--out",
        "-o",
        dir_okay=True,
        file_okay=False,
        help="📂 Output directory (will be created).",
    ),
    config: Path = typer.Option(
        None,
        "--config",
        help="🔧 YAML file with extra ProfileReport parameters.",
    ),
    # ─── Sampling Options ───────────────────────────────────────────
    sample: float = typer.Option(
        None,
        "--sample",
        help="🎲 Random fraction 0–1 per chunk (ignored if --reservoir-size).",
    ),
    reservoir_size: int = typer.Option(
        None,
        "--reservoir-size",
        help="🌀 Size for one-pass reservoir sampling.",
    ),
    chunksize: int = typer.Option(
        10_000,
        "--chunksize",
        help="📑 Rows per chunk for large files.",
    ),
    # ─── Quality Options ────────────────────────────────────────────
    expectations: bool = typer.Option(
        False,
        "--expectations",
        help="✅ Emit GE stub and exit non-zero.",
    ),
    # ─── Miscellaneous Options ───────────────────────────────────────
    minimal: bool = typer.Option(
        True,
        "--minimal/--full",
        help="⚙️ Minimal (fast) or full profiling report.",
    ),
    json_out: bool = typer.Option(
        False,
        "--json-out",
        help="📦 Also emit JSON report.",
    ),
):
    """
    Generate HTML (and optional JSON) profiling reports,
    with sampling, custom configs, and GE stubs.
    """
    os.makedirs(out, exist_ok=True)

    # 1) Expectations‐stub mode
    if expectations:
        suite = {"expectations": []}
        stub = out / "expectations.json"
        with open(stub, "w") as f:
            json.dump(suite, f, indent=2)
        typer.secho(
            f"🧪 Expectations stub written to {stub}", fg=typer.colors.CYAN, err=True
        )
        get_current_context().exit(1)

    start = time.time()

    # 2) Build reader kwargs (ignore "extra" column if present)
    reader_kwargs: Dict[str, Any] = {}
    if filepath.suffix.lower() == ".csv":
        cols = pd.read_csv(filepath, nrows=0).columns
        reader_kwargs["usecols"] = [c for c in cols if c != "extra"]

    # 3) Load optional ProfileReport config
    report_kwargs: Dict[str, Any] = {
        "title": "Data Profiling Report",
        "explorative": True,
        "minimal": minimal,
    }
    if config:
        with open(config) as cf:
            report_kwargs.update(yaml.safe_load(cf))

    # 4) Ingest & sample
    if reservoir_size:
        df = reservoir_sample(filepath, reservoir_size, chunksize, reader_kwargs)
        typer.echo(f"🌀 Reservoir sample of {len(df)} rows")
    else:
        parts = []
        dt_re = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
        for i, chunk in enumerate(load_data(filepath, reader_kwargs, chunksize)):
            if sample and 0 < sample < 1:
                chunk = chunk.sample(frac=sample)
            # datetime sanity
            for col in chunk.select_dtypes(include=["object"]):
                if dt_re.match(str(chunk[col].iat[0])):
                    bad = chunk[~chunk[col].astype(str).str.match(dt_re)]
                    if not bad.empty:
                        typer.secho(
                            f"⚠️ Invalid datetime in chunk {i}, col {col}",
                            fg=typer.colors.YELLOW,
                        )
            mini = ProfileReport(chunk, **report_kwargs)
            mini_path = out / f"chunk_{i:03d}.json"
            mini.to_file(mini_path)
            typer.echo(f"➡️ Chunk {i} summary → {mini_path}")
            parts.append(chunk)
        df = pd.concat(parts, ignore_index=True)

    # 5) Full profiling
    report = ProfileReport(df, **report_kwargs)
    html = out / "report.html"
    report.to_file(html)
    typer.secho(f"✅ HTML report → {html}", fg=typer.colors.GREEN)

    if json_out:
        jpath = out / "report.json"
        report.to_file(jpath)
        typer.echo(f"📦 JSON report → {jpath}")

    # 6) Persist metadata
    dur = time.time() - start
    conn = sqlite3.connect("runs.db")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS runs (
          file TEXT PRIMARY KEY, duration REAL,
          sample REAL, chunksize INTEGER,
          reservoir INTEGER, timestamp DATETIME
            DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        INSERT INTO runs(file,duration,sample,chunksize,reservoir)
        VALUES(?,?,?,?,?)
        ON CONFLICT(file) DO UPDATE SET
          duration=excluded.duration,
          sample=excluded.sample,
          chunksize=excluded.chunksize,
          reservoir=excluded.reservoir
        """,
        (str(filepath), dur, sample or 0.0, chunksize, reservoir_size or 0),
    )
    conn.commit()
    conn.close()

    typer.echo(f"⏱ Completed in {dur:.2f}s")


@app.command("plot-trends")
def plot_trends(
    db: Path = typer.Option(Path("runs.db"), "--db", help="SQLite DB of past runs.")
):
    """Scatter runtime vs. sample‐fraction (red=reservoir, blue=full)."""
    conn = sqlite3.connect(db)
    df = pd.read_sql("SELECT timestamp,duration,sample,reservoir FROM runs", conn)
    conn.close()

    df["sample"] = df["sample"].fillna(0).astype(float)
    fig, ax = plt.subplots()
    ax.scatter(
        df["sample"],
        df["duration"],
        c=(df["reservoir"] > 0).map({True: "red", False: "blue"}),
        alpha=0.7,
    )
    ax.set(xlabel="Sample Fraction", ylabel="Duration (s)", title="Duration vs. Sample")
    ax.legend(
        handles=[
            Line2D(
                [], [], marker="o", color="w", label="Reservoir", markerfacecolor="red"
            ),
            Line2D(
                [], [], marker="o", color="w", label="Full Data", markerfacecolor="blue"
            ),
        ]
    )
    plt.tight_layout()
    plt.savefig("runtime_vs_sample.png")
    typer.secho("📈 Scatter saved → runtime_vs_sample.png", fg=typer.colors.GREEN)


@app.command("aggregate-chunks")
def aggregate_chunks(
    reports_dir: Path = typer.Argument(..., exists=True, file_okay=False),
    out: Path = typer.Option(Path("summary.json"), help="Aggregated JSON output"),
):
    """
    Combine all chunk_*.json into one JSON.
    """
    files = sorted(glob.glob(str(reports_dir / "chunk_*.json")))
    if not files:
        typer.secho(f"⚠️ No chunks in {reports_dir}", fg=typer.colors.YELLOW)
        raise typer.Exit(0)

    agg = []
    for path in files:
        with open(path) as f:
            agg.append({"chunk_file": Path(path).name, "profile": json.load(f)})

    with open(out, "w") as f:
        json.dump({"chunks": agg}, f, indent=2)

    typer.secho(f"🔗 Aggregated {len(agg)} chunks → {out}", fg=typer.colors.GREEN)


def main():
    app()


if __name__ == "__main__":
    main()
