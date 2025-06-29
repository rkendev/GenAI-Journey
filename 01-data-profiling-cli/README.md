# Data Profiling CLI

[![PyPI version](https://img.shields.io/pypi/v/dataprof.svg)](https://pypi.org/project/dataprof)
[![GitHub Actions CI](https://github.com/rkendev/dataprof/actions/workflows/ci.yml/badge.svg)](https://github.com/rkendev/dataprof/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A fast, extensible command-line interface for profiling tabular data.  
Supports chunk-wise sampling, reservoir sampling, minimal vs. full reports,  
and optional Great Expectations expectation-suite stubs.

## Features

- **Fast profiling** via [YData-Profiling](https://github.com/ydataai/ydata-profiling)  
- **Chunked ingestion** with on-the-fly sampling or reservoir sampling  
- **HTML & JSON** output formats  
- **Data-quality stubs** (Great Expectations suite) and non-zero exit on failures  
- **Built-in trend plotting** and chunk-aggregation utilities  
- **Shell completion** for Bash, Zsh, Fish  

## Installation

```bash
# From PyPI
pip install dataprof

# Or from local source
poetry install
poetry run pip install .
```

# Quickstart

# Profile a CSV with minimal report
dataprof profile data.csv --minimal --out reports/

# Generate a Great Expectations stub and fail on validation
dataprof profile data.csv --expectations

# Plot runtime vs. sample fraction
dataprof plot-trends --db runs.db

# Aggregate per-chunk summaries
dataprof aggregate-chunks reports/ --out summary.json
```

# Contributing
We use pre-commit hooks to enforce formatting and linting:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Please open issues or pull requests on GitHub.

© 2025 rken — MIT License
---
