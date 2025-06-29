# Data Profiling CLI

[![PyPI version](https://img.shields.io/pypi/v/dataprof.svg)](https://pypi.org/project/dataprof)  
[![Build Status](https://github.com/your-org/dataprof/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/dataprof/actions)  
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A **fast**, **extensible** command-line tool for generating HTML (and JSON) profiling reports on CSV or table-like data, powered by [ydata-profiling](https://github.com/ydataai/ydata-profiling) and with optional Great Expectations validation stubs.

## Features

- **Fast sampling**: reservoir or fractional sampling for huge files  
- **Chunked summaries**: per-chunk JSON + final consolidated HTML  
- **Validation stub**: drop-in Great Expectations suite with non-zero exit  
- **Run-history**: stores profiling runtimes in `runs.db` and scatter-plots trends  
- **Shell completion**: `bash`, `zsh`, `fish` out of the box  

## Installation

```bash
# via Poetry:
poetry add dataprof

# or with pip:
pip install dataprof
Usage

# basic profile
dataprof profile data.csv --out reports

# reservoir sampling
dataprof profile data.csv --reservoir-size 5000 --out rpt

# generate & validate stub suite
dataprof profile data.csv --expectations --minimal

# plot historical runtimes
dataprof plot-trends --db runs.db

# aggregate chunk summaries
dataprof aggregate-chunks reports --out summary.json
```

# Contributing
```bash
git clone ... && cd dataprof

poetry install

pre-commit install (if using pre-commit)

pytest
```
MIT © rken

---

### Next

1. **Swap in** the above files.  
2. Run the pip‐install smoke test in a clean venv to confirm the entry point works.  
3. If all good, you’re ready to publish to PyPI or wire up your CI workflow.