# Data Profiling CLI

[![PyPI version](https://img.shields.io/pypi/v/dataprof.svg)](https://pypi.org/project/dataprof)
[![GitHub Actions CI](https://github.com/rkendev/dataprof/actions/workflows/ci.yml/badge.svg)](https://github.com/rkendev/dataprof/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A fast, extensible command-line interface for profiling tabular data.  
Supports chunk-wise sampling, reservoir sampling, minimal vs. full reports,  
and optional Great Expectations expectation-suite stubs.

## Installation

```bash
# From PyPI
pip install dataprof

# Or from source
poetry install
poetry run pip install .
Quickstart

# 1) Generate a minimal HTML profile
dataprof profile data.csv --minimal --out reports/

# 2) Emit a GE expectation stub and fail on validation
dataprof profile data.csv --expectations

# 3) Plot runtime vs. sample fraction
dataprof plot-trends --db runs.db

# 4) Aggregate per-chunk summaries into one JSON
dataprof aggregate-chunks reports/ --out summary.json
```

---

## 5. End-to-End Commands

Run these in your project root **after** committing the above files:

```bash
# 1. Re-lock & install
poetry lock
poetry install          # now installs both main+dev thanks to group.dev

# 2. Pre-commit checks & formatting
pre-commit install
pre-commit run --all-files

# 3. Run tests
poetry run pytest -q

# 4. Smoke-test locally
poetry run dataprof --version
echo -e "x,y\n1,2" > sample.csv
poetry run dataprof profile sample.csv --minimal --out demo
ls demo

# 5. Build for release (you’ll publish later)
poetry build

```
