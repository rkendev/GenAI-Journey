# Contributing to Data Profiling CLI

Thank you for your interest in contributing to Data Profiling CLI! We welcome contributions of all kinds—bug reports, feature requests, documentation improvements, and code enhancements.

Filing Issues

We use GitHub's issue templates to streamline bug reports and feature requests. Please select the appropriate template and provide as much detail as possible.

## Bug reports

Use the Bug report template.

Include:

A clear, descriptive title.

Steps to reproduce the issue.

Expected vs. actual behavior.

Environment details:

dataprof --version

Python version (python --version)

Operating system.

## Feature requests

Use the Feature request template.

### Describe:

- The problem you’re trying to solve.

- Your proposed solution or desired behavior.

- Any relevant examples or references.

- Your First Code Contribution

### Fork the repository on GitHub: https://github.com/rkendev/dataprof.

Clone your fork locally:
```bash
git clone git@github.com:<your-username>/dataprof.git
cd dataprof

Install dependencies (including dev and docs groups):

poetry install --with dev,docs

Set up pre-commit hooks for formatting and linting:

pre-commit install
pre-commit run --all-files
````

## Code Style & Quality

We follow these tools to maintain code consistency:

[Black] for code formatting

[Ruff] for linting

[isort] for import sorting

### Run them locally before committing:
```bash
pre-commit run --all-files

Running Tests & Coverage

We use pytest with pytest-cov to ensure code correctness and coverage.

Run all tests:

poetry run pytest -q

Run tests with coverage:

poetry run pytest --cov=dataprof --cov-report=term-missing
```

## Documentation

Documentation source files are under docs/source/. We use Sphinx with the ReadTheDocs theme.

Build the docs locally:
```bash
poetry run sphinx-build -b html docs/source docs/_build/html
open docs/_build/html/index.html

Edit or add new .rst files as needed.

Pull Request Guidelines

Create a new branch from main:

git checkout -b feat/my-feature  

Make your changes, ensuring new features have tests and documentation.

Commit with clear, conventional-style messages.

Push your branch and open a Pull Request against main.

The CI will run linting, formatting checks, tests, and coverage.

Address any review feedback.
```

## Code of Conduct

This project follows the Contributor Covenant. By participating, you agree to abide by its terms.

Thank you for helping make Data Profiling CLI better! We appreciate your time and effort.