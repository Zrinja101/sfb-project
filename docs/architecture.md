# Architecture Overview

## Design Philosophy

The system is data-driven and rule-based:

- YAML defines game data
- Python enforces rules
- Engine executes turns

## Layers

### Core
Turn engine, map, movement

### Combat
Weapon resolution and targeting

### Rules
SFB-specific mechanics (damage, arcs, etc.)

### Data
External YAML files

## Key Principles

- No hardcoded tables
- Deterministic logic where possible
- Testable subsystems
