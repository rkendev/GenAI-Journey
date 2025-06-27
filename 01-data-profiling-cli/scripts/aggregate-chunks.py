#!/usr/bin/env python3
import os
import json
import click
import pandas as pd

@click.command()
@click.option(
    "--root",
    default="reports",
    show_default=True,
    help="Root directory containing per-chunk JSON summaries (will recurse into subdirs).",
)
@click.option(
    "--out",
    default="all_chunks_summary.csv",
    show_default=True,
    help="Path for the aggregated CSV output",
)
def main(root: str, out: str):
    """
    Recursively aggregate statistics from each chunk_{i:03d}.json under ROOT into one CSV.
    """
    records = []

    # Walk through all subdirectories
    for dirpath, dirnames, filenames in os.walk(root):
        for fname in sorted(filenames):
            if not (fname.startswith("chunk_") and fname.endswith(".json")):
                continue

            full_path = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(full_path, root)

            with open(full_path, "r") as f:
                data = json.load(f)

            # 1) Table-level stats
            table = data.get("table", {})
            n_rows = table.get("n_rows", table.get("n", None))
            n_vars = table.get("n_vars", table.get("n_columns", None))
            p_cells_missing = table.get("p_cells_missing")  # global % missing cells
            p_unique = table.get("p_unique")               # global fraction unique rows

            # 2) Legacy 'missing': average pct missing per variable
            missing_info = data.get("missing", {}).get("p_missing_var", {})
            p_missing_var_mean = missing_info.get("mean")

            # 3) Fallback: compute avg % missing across variables
            if p_missing_var_mean is None:
                var_dict = data.get("variables", {})
                pct_list = []
                for v in var_dict.values():
                    mp = v.get("p_cells_missing") or v.get("p_missing") or v.get("p_missing_var")
                    if isinstance(mp, (int, float)):
                        pct_list.append(mp)
                if pct_list:
                    p_missing_var_mean = sum(pct_list) / len(pct_list)

            # 4) Fallback for unique fraction via duplicates,
            #    but only if 'duplicates' is a dict
            if p_unique is None:
                dup = data.get("duplicates", {})
                if isinstance(dup, dict):
                    dup_info = dup.get("p_unique", {})
                    if isinstance(dup_info, dict):
                        # try the 'mean' field inside
                        p_unique = dup_info.get("mean")

            records.append({
                "chunk_path":            rel_path,
                "n_rows":                n_rows,
                "n_vars":                n_vars,
                "pct_cells_missing":     p_cells_missing,
                "pct_missing_per_var_avg": p_missing_var_mean,
                "pct_unique":            p_unique,
            })

    # Guard: no chunk files found
    if not records:
        raise click.ClickException(
            f"No chunk summary JSON files found under '{root}'.\n"
            "Make sure you've generated per-chunk reports (i.e. ran without --reservoir-size)."
        )

    # Build DataFrame
    df = pd.DataFrame(records)

    # Guard: missing expected column
    if "chunk_path" not in df.columns:
        raise click.ClickException(
            "Expected column 'chunk_path' not found in the aggregated data."
        )

    # Sort by chunk_path and write out
    df = df.sort_values("chunk_path").reset_index(drop=True)
    df.to_csv(out, index=False)
    click.echo(f"✅ Aggregated {len(df)} chunk files into '{out}'")

if __name__ == "__main__":
    main()
