# Star Fleet Battles Simulator (SFB)

A Python-based simulation engine for Star Fleet Battles, focused on:

- Accurate rule modeling
- YAML-driven data (ships, weapons, scenarios)
- Extensible combat engine

## Goals

- Fully simulate Cadet Training Scenarios
- Support Federation, Klingon, Romulan, Gorn ships
- Provide both CLI and future UI interfaces

## Project Structure

- `sfb/core` – engine, map, turn system
- `sfb/combat` – weapons and combat resolution
- `sfb/units` – ships and drones
- `sfb/data` – YAML definitions
- `tests` – unit tests

## Setup (Dev Container)

1. Open in VSCode
2. Run: `Dev Containers: Reopen in Container`

## Run

```bash
python app.py
```

## Testing

Before running tests, activate the virtual environment:

```bash
# POSIX
source .venv/bin/activate
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

Confirm dependencies then run:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Roadmap
- [ ] Scenario #1 full implementation
- [ ] YAML-driven scenarios
- [ ] Real DAC system
- [ ] Power allocation

---
