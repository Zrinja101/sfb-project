---
name: sfb-repo
description: |
  Enforce repository coding standards: full module documentation, tests for all modules (unit or integration), and Python best practices.
  Use this sheet for all code modifications in this repository.
applyTo: "**/*.py"
---

# GitHub Copilot Instructions for SFB

This workspace-level instruction is authoritative for the Star Fleet Battles simulator repo.

## Requirements

1. Documentation for all code:
   - Every public module/class/function/method must have docstring.
   - Prefer standard Python style (PEP 257) and short module-level summary in each module.
   - Keep docs in docstrings and in README where useful.

2. Tests:
   - Every module must have associated tests in `tests/`.
   - Use `pytest` (or `unittest` only if required; prefer pytest).
   - For deterministic behavior, use dependency injection, monkeypatching, seeded RNG, or fixed fixtures.
   - Cover at least:
     - happy path
     - edge case(s)
     - failure path(s) where applicable

3. Style and best practices:
   - Use PEP8 formatting (line length <= 88 preferably, explicit imports, no wildcard imports).
   - Use typing hints for function signatures when feasible (“strictness” optional but encouraged).
   - Avoid side effects in module import time (no random state or file reads during import).
   - Make logic functions pure when possible (separate I/O from computation).

4. Setup checks:
   - Ensure the repository has `pytest.ini` or equivalent so tests import `sfb` properly.
   - Ensure `README.md` includes commands to activate venv and run tests.

## Workflow

- For every file edit, run:
  ```bash
  source .venv/bin/activate
  python -m pip install -r requirements.txt
  python -m pytest -q
  ```
- If test or import path fails, update `pytest.ini` with `pythonpath = .`.

## Non-goals

- Do not modify behavior beyond bugfix / feature request.
- Avoid adding unrelated experiments if the request focuses on doc/tests.

## Quick checks

- `sfb/core`, `sfb/combat`, `sfb/ships`, `sfb/units`, `sfb/dac`, `sfb/io`, `sfb/utils`, `app.py` are all covered by tests.
- New code should ideally include small inline examples when behavior is non-trivial.
