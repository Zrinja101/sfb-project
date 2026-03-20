# Contributor Guide

## Setup

1. Create and activate your venv:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install -r requirements.txt
```

## Testing

```bash
python -m pytest --cov=sfb --cov-report=term-missing
```

## Linting

```bash
pre-commit run --all-files
ruff check .
black --check .
isort --check .
mypy sfb
```

## Code standards

- `PEP8` / `PEP257`
- Keep modules small and testable.
- Add docstrings on all public methods.
