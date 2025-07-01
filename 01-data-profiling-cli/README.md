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
```

# Quickstart

# 1️⃣ Generate a minimal HTML profile
dataprof profile data.csv --minimal --out reports/

# 2️⃣ Emit a GE expectation stub and fail on validation
dataprof profile data.csv --expectations

# 3️⃣ Plot runtime vs. sample fraction
dataprof plot-trends --db runs.db

# 4️⃣ Aggregate per-chunk summaries into one JSON
dataprof aggregate-chunks reports/ --out summary.json


---

## 5. End-to-End Commands

Run these from your project root to lock, install, lint, test, smoke-test and build:

```bash
# 1. Update lock and install all deps (main+dev):
poetry lock
poetry install

# 2. Set up and run pre-commit hooks:
pre-commit install
pre-commit run --all-files

# 3. Execute the test suite:
poetry run pytest -q

# 4. Smoke-test the CLI locally:
echo -e "x,y\n1,2" > sample.csv
poetry run dataprof profile sample.csv --minimal --out demo
ls demo
```bash


### 5.1 For cown excel files
```bash
# 1) Reservoir sampling
dataprof profile large.csv --reservoir-size 100 --out reports/

# 2) Chunk-wise minimal profiling
dataprof profile data.csv --sample 0.1 --minimal --out reports/

# 3) Plotting trends
dataprof plot-trends --db runs.db

# 4) Aggregating chunks
dataprof aggregate-chunks reports/ --out summary.json
```


# 5. Build distributable packages:
poetry build