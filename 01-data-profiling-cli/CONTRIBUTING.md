# Contributing to Data Profiling CLI

Thank you for your interest in contributing!  Please take a moment to read through this guide.

## Filing Issues

- **Bug reports**: Use the “Bug report” template. Include:
  - A clear description of the problem.
  - Steps to reproduce.
  - Expected vs. actual behavior.
  - Your environment (`dataprof --version`, Python, OS).

- **Feature requests**: Use the “Feature request” template. Describe:
  - The use-case for the new feature.
  - Any relevant examples or links.

## Getting the Code

```bash
# Clone your fork, then install all deps:
git clone git@github.com:<your-user>/dataprof.git
cd dataprof
poetry install --with dev,docs
Code Style
We follow Black, Ruff, and isort.

Before pushing, run:

pre-commit install
pre-commit run --all-files
Running Tests

# Run entire suite:
poetry run pytest -q

# Run a single test file:
poetry run pytest tests/test_cli.py -q
```

## Documentation
Your doc sources live under docs/source/.

To build:

```bash
poetry run sphinx-build -b html docs/source docs/_build/html
open docs/_build/html/index.html
```bash

## Pull Request Guidelines
Create a new branch: git checkout -b feat/my-feature

Make your changes, adding tests where appropriate.

Update docs if you’ve added or changed functionality.

Ensure all hooks and tests pass locally.

Push your branch and open a PR against main.