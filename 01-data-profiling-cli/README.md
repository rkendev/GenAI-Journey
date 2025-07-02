# Data Profiling CLI

[![PyPI version](https://img.shields.io/pypi/v/dataprof.svg)](https://pypi.org/project/dataprof)  
[![GitHub Actions CI](https://github.com/rkendev/dataprof/actions/workflows/ci.yml/badge.svg)](https://github.com/rkendev/dataprof/actions)  
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

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
Quickstart

1️⃣ Minimal profiling
dataprof profile data.csv \
  --minimal \
  --out reports/

2️⃣ Reservoir sampling
dataprof profile data.csv \
  --reservoir-size 1000 \
  --minimal \
  --out reports/

3️⃣ Great Expectations stub
dataprof profile data.csv \
  --expectations
# writes expectations.json then exits non-zero

4️⃣ Trend plotting
dataprof plot-trends --db runs.db

5️⃣ Chunk aggregation
dataprof aggregate-chunks reports/ \
  --out summary.json
Configuration via YAML
You can customize ProfileReport parameters with a config.yaml:

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

poetry run dataprof profile test.csv \
  --config config.yaml \
  --minimal \
  --out demo-cfg
End-to-End
From project root after committing:


# 1. Lock & install all deps (main + dev + docs)
poetry lock
poetry install --with dev,docs

# 2. Pre-commit checks
pre-commit install
pre-commit run --all-files

# 3. Test suite
poetry run pytest -q

# 4. Smoke test
echo -e "x,y\n1,2" > sample.csv
poetry run dataprof profile sample.csv \
  --minimal \
  --out demo
ls demo

# 5. Build packages
poetry build
Supported Formats
CSV (default)

Parquet (.parquet, .pq; requires pyarrow or fastparquet)

Excel (.xls, .xlsx; requires openpyxl)

Example:
poetry run dataprof profile test.parquet \
  --full \
  --out demo-parquet

poetry run dataprof profile test.xlsx \
  --minimal \
  --out demo-xlsx
```

# Development & Contribution
We welcome issues and PRs!

```bash
Fork & clone

poetry install --with dev,docs

Implement & add tests in tests/

pre-commit run --all-files → pytest -q

Open a PR
```

Please see CONTRIBUTING.md for full guidelines.

© 2025 rken — MIT License
