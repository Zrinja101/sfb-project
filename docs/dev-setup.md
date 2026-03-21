# Development Setup

This document covers development practices and automation for the SFB project.

## Pre-commit Hooks

The project uses pre-commit hooks to maintain code quality:

- **Black**: Code formatting
- **Ruff**: Linting and fixing
- **isort**: Import sorting
- **pydocstyle**: Docstring style checking
- **check-init-files**: Ensures all Python packages have `__init__.py` files

## Automatic __init__.py Creation

All Python packages must have `__init__.py` files. This is enforced by a pre-commit hook.

### Manual Creation

If you need to add missing `__init__.py` files manually:

```bash
python scripts/add_init_files.py
```

This script will:
- Scan the project for Python packages (directories containing `.py` files)
- Create `__init__.py` files with appropriate docstrings
- Skip excluded directories (`.venv`, `__pycache__`, etc.)

### Pre-commit Check

The pre-commit hook will prevent commits if any Python packages are missing `__init__.py` files. If this happens:

1. Run `python scripts/add_init_files.py` to add missing files
2. Stage and commit the new `__init__.py` files

## Development Workflow

1. Create new Python modules/packages as needed
2. Run `python scripts/add_init_files.py` to ensure proper package structure
3. Commit changes - pre-commit hooks will catch any issues

## VSCode Configuration

The project includes VSCode settings (`.vscode/settings.json`) for:
- Python interpreter configuration
- Pylance import resolution
- Code formatting and import organization

These settings are not committed to git as they may be user-specific.