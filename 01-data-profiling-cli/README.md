# Data Profiling CLI

[![PyPI version](https://img.shields.io/pypi/v/dataprof.svg)](https://pypi.org/project/dataprof)  
[![GitHub Actions CI](https://github.com/rkendev/dataprof/actions/workflows/ci.yml/badge.svg)](https://github.com/rkendev/dataprof/actions)  
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Codecov Coverage](https://img.shields.io/codecov/c/gh/rkendev/dataprof/main.svg?label=coverage)](https://app.codecov.io/gh/rkendev/dataprof)  

A **fast**, **extensible** command-line interface for profiling tabular data, with:

- Chunk-wise sampling & reservoir sampling  
- Minimal vs. full (explorative) HTML/JSON reports  
- Optional Great Expectations expectation-suite stubs  
- Support for CSV, Parquet, and Excel inputs  
- Trend plotting and chunk aggregation utilities  
- Custom profiler config via YAML

---

## Installation

```bash
# From PyPI
pip install dataprof

# Or from source
poetry install
poetry run pip install .
```

## Quickstart
1️⃣ Minimal profiling
```bash

dataprof profile data.csv \
  --minimal \
  --out reports/
2️⃣ Reservoir sampling


dataprof profile data.csv \
  --reservoir-size 1000 \
  --minimal \
  --out reports-reservoir/

3️⃣ Great Expectations stub
Generates an empty expectations.json and exits non-zero:
dataprof profile data.csv \
  --expectations

4️⃣ Trend plotting
Produces runtime_vs_sample.png:
dataprof plot-trends --db runs.db
# then open runtime_vs_sample.png

5️⃣ Chunk aggregation
Merges per-chunk JSON into one summary.json:
dataprof aggregate-chunks reports/ \
  --out summary.json

Sample structure of summary.json:

{
  "chunks": [
    { "chunk_file": "chunk_000.json", "profile": { /* … */ } },
    { "chunk_file": "chunk_001.json", "profile": { /* … */ } }
  ]
}

6️⃣ Custom configuration
Use your own YAML to tweak profiling parameters. For example, create config.yaml:

# config.yaml
title: "🔍 Custom Data Profiler Report"
explorative: false
minimal: true
pool_size: 2
progress_bar: false
correlations:
  pearson:
    calculate: true
  spearman:
    calculate: true
missing_diagrams:
  bar: true
  matrix: true
  heatmap: false
Then run:

poetry run dataprof profile data.csv \
  --config config.yaml \
  --minimal \
  --out reports-config/
End-to-End Workflow
From your project root (after committing all changes):


# 1. Lock & install all deps (main + dev + docs)
poetry lock
poetry install --with dev,docs

# 2. Pre-commit checks
pre-commit install
pre-commit run --all-files

# 3. Run tests
poetry run pytest -q

# 4. Smoke test
echo -e "x,y\n1,2" > sample.csv
poetry run dataprof profile sample.csv \
  --minimal \
  --out demo
ls demo
```

# 5. Build distributable packages
```bash
poetry build
Supported Formats
CSV (default)

Parquet (.parquet, .pq) — requires pyarrow or fastparquet

Excel (.xls, .xlsx) — requires openpyxl

Examples:
poetry run dataprof profile test.parquet \
  --full \
  --out demo-parquet

poetry run dataprof profile test.xlsx \
  --minimal \
  --out demo-xlsx
Development & Contribution
We welcome issues and PRs!

# 1. Fork & clone
# 2. Install dependencies
poetry install --with dev,docs

# 3. Implement & add tests under tests/
pre-commit run --all-files
pytest -q
```

# 4. Open a PR!
Please see CONTRIBUTING.md for full guidelines.

© 2025 rken — MIT License