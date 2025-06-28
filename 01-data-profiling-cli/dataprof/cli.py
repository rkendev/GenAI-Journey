# dataprof/cli.py

import click
from click import get_current_context
import pandas as pd
from ydata_profiling import ProfileReport
import re
import sqlite3
import time
import os
import glob
import json
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from random import random

@click.group()
def cli():
    """Data Profiling CLI: generate profiling reports and monitor performance trends."""
    pass

def reservoir_sample(filepath, k, chunksize, reader_kwargs):
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

@cli.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("--out", default="reports", help="Directory to write the report(s)")
@click.option("--sample", type=float, default=None, help="Ignored if --reservoir-size is used")
@click.option("--reservoir-size", type=int, default=None, help="Reservoir-sample this many rows")
@click.option("--chunksize", type=int, default=10000, help="CSV read chunk size")
@click.option("--usecols", type=str, default=None, help="Comma-separated list of columns to load")
@click.option("--minimal/--full", default=True, help="Minimal vs. full profiling")
@click.option(
    "--expectations",
    is_flag=True,
    default=False,
    help="(optional) auto-generate & signal a GE expectation suite (stub)"
)
@click.option("--json-out", is_flag=True, default=False, help="Also write JSON report")
def profile(filepath, out, sample, reservoir_size, chunksize,
            usecols, minimal, expectations, json_out):
    """Generate fast HTML (and optional JSON) profiling reports."""
    os.makedirs(out, exist_ok=True)
    start = time.time()

    # Build reader kwargs
    datetime_re = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
    reader_kwargs = {}
    if usecols:
        reader_kwargs["usecols"] = [c.strip() for c in usecols.split(",")]
    else:
        reader_kwargs["usecols"] = [
            col for col in pd.read_csv(filepath, nrows=0).columns if col != "extra"
        ]

    # Ingest & sample
    if reservoir_size:
        df = reservoir_sample(filepath, reservoir_size, chunksize, reader_kwargs)
        click.echo(f"🌀 Reservoir sample of {len(df)} rows drawn in one pass")
    else:
        parts = []
        for i, chunk in enumerate(pd.read_csv(filepath, chunksize=chunksize, **reader_kwargs)):
            if sample and 0 < sample < 1:
                chunk = chunk.sample(frac=sample)
            # Simple datetime sanity check
            for col in chunk.select_dtypes(include=["object"]).columns:
                if datetime_re.match(str(chunk[col].iloc[0])):
                    invalid = chunk[~chunk[col].astype(str).str.match(datetime_re)]
                    if not invalid.empty:
                        click.echo(f"⚠️  Invalid datetime in chunk {i}, col {col}")
            mini = ProfileReport(chunk, explorative=True, minimal=True)
            mini_path = os.path.join(out, f"chunk_{i:03d}.json")
            mini.to_file(mini_path)
            click.echo(f"➡️ Chunk {i} summary written to {mini_path}")
            parts.append(chunk)
        df = pd.concat(parts, ignore_index=True)

    # Full YData profiling report
    report = ProfileReport(df, title="Data Profiling Report", explorative=True, minimal=minimal)
    html_path = os.path.join(out, "report.html")
    report.to_file(html_path)
    click.echo(f"✅ HTML report written to {html_path}")

    if json_out:
        json_path = os.path.join(out, "report.json")
        report.to_file(json_path)
        click.echo(f"📦 JSON report written to {json_path}")

    # --- Expectations stub: always write the file, then exit non-zero ---
    if expectations:
        suite_path = os.path.join(out, "expectations.json")
        with open(suite_path, "w") as f:
            # a minimal stub suite
            json.dump({"expectations": []}, f, indent=2)
        click.echo(f"🧪 Expectations suite written to {suite_path}", err=True)
        # exit with non-zero to signal failure
        ctx = get_current_context()
        ctx.exit(1)

    # Persist run metadata
    duration = time.time() - start
    conn = sqlite3.connect("runs.db")
    conn.execute("""
      CREATE TABLE IF NOT EXISTS runs (
        file       TEXT PRIMARY KEY,
        duration   REAL,
        sample     REAL,
        chunksize  INTEGER,
        reservoir  INTEGER DEFAULT 0,
        timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    """)
    conn.execute("""
      INSERT INTO runs (file, duration, sample, chunksize, reservoir)
      VALUES (?, ?, ?, ?, ?)
      ON CONFLICT(file) DO UPDATE SET
        duration  = excluded.duration,
        sample    = excluded.sample,
        chunksize = excluded.chunksize,
        reservoir = excluded.reservoir
    """, (filepath, duration, sample or 0.0, chunksize, reservoir_size or 0))
    conn.commit()
    conn.close()

    click.echo(f"⏱  Completed in {duration:.2f}s")

@cli.command(name="plot-trends")
@click.option("--db", default="runs.db", help="SQLite DB with profiling runs")
def plot_trends(db):
    """Plot profiling runtime trends from the runs table."""
    conn = sqlite3.connect(db)
    df = pd.read_sql("""
      SELECT timestamp, duration, sample, reservoir
      FROM runs ORDER BY timestamp
    """, conn)
    conn.close()

    df["sample"] = df["sample"].fillna(0).astype(float)
    fig, ax = plt.subplots()
    ax.scatter(
        df["sample"],
        df["duration"],
        c=(df["reservoir"] > 0).map({True: "red", False: "blue"}),
        alpha=0.7
    )
    ax.set_xlabel("Sample Fraction")
    ax.set_ylabel("Duration (s)")
    ax.set_title("Duration vs. Sample Fraction")

    legend_elements = [
        Line2D([0], [0], marker="o", color="w", label="Reservoir run",
               markerfacecolor="red", markersize=8),
        Line2D([0], [0], marker="o", color="w", label="Full-data run",
               markerfacecolor="blue", markersize=8),
    ]
    ax.legend(handles=legend_elements)
    plt.tight_layout()
    plt.savefig("runtime_vs_sample.png")
    click.echo("📈 Scatter plot saved to runtime_vs_sample.png")

@cli.command(name="aggregate-chunks")
@click.argument("reports_dir", type=click.Path(exists=True, file_okay=False))
@click.option("--out", default="summary.json", help="Output JSON file for aggregated summary")
def aggregate_chunks(reports_dir, out):
    """
    Aggregate all per-chunk JSON summaries in REPORTS_DIR into a single JSON.
    """
    pattern = os.path.join(reports_dir, "chunk_*.json")
    files = sorted(glob.glob(pattern))
    if not files:
        click.echo(f"⚠️  No chunk JSON files found in {reports_dir}")
        return

    aggregated = []
    for path in files:
        with open(path, "r") as f:
            data = json.load(f)
            aggregated.append({
                "chunk_file": os.path.basename(path),
                "profile": data
            })

    with open(out, "w") as fout:
        json.dump({"chunks": aggregated}, fout, indent=2)

    click.echo(f"🔗 Aggregated {len(aggregated)} chunk summaries into {out}")

if __name__ == "__main__":
    cli()
