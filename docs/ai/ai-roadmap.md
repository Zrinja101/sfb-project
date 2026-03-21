# AI Roadmap for SFB Simulator

This document serves as a reference for future single-player AI development. It assumes you already have:

- map + hex distance
- ship movement + turn mode
- weapon fire resolution
- scenario/task execution engine
- data-driven scenario definitions (YAML)

## 1. High-level architecture

1. `ai/` module handles ship decision logic.
2. `Engine` should call AI for each AI-controlled unit during the behavior steps in an impulse.
3. Keep AI pure, deterministic, easily testable.

## 2. Data-driven AI profiles

Add AI settings to scenario YAML:

```yaml
ai_profile:
  mode: "balanced"  # passive/aggressive/evasive
  firing_preference: ["phaser", "torpedo"]
  target_weights:
    hp: 0.7
    distance: 0.2
    threat: 0.1
  retreat_threshold: 0.25  # unit HP fraction
```

## 3. Behavior layers

1. Movement State
   - `CanTurn`: based on `turn_mode` and distance moved.
   - `MoveGoal`: closest-seeking vs maintain-distance.
2. Combat State
   - `SelectTarget` via weighted score.
   - `SelectWeapon` based on range/available.
   - `FireDecision` (do we fire this impulse?).
3. Tactical Layer
   - `Engage`, `Evade`, `Defend`, `Regroup`.
   - Transition via triggers (HP low, enemy too close, line-of-fire clear).

## 4. Scenario objectives

- Scenario #1: single enemy ship, win by destroying enemy.
- Later scenarios: multiple enemies, objectives, defense points.

## 5. AI utilities

- `ai/pathfinding.py`: generate legal moves based on ship facing and turn mode.
- `ai/threat_map.py`: evaluate enemy firing arcs / likely damage fields.
- `ai/trigger.py`: easy event conditions from scenario rules.

## 6. Testing AI

- unit tests on decision functions
- scenario tests with deterministic RNG seed
- assertions on expected state transitions

## 7. Future ML/learning options (optional)

- store replay logs from human play for heuristic tuning
- connect to `ai/learning.py` for reinforcement or imitation if needed

## 8. files to create

- `sfb/ai/controller.py`
- `sfb/ai/profile.py`
- `sfb/ai/utils.py`
- `sfb/ai/__init__.py`

## 9. CI integration

- tests in `tests/test_ai_behavior.py` using scenario YAMLs
- include `ai` code paths in coverage
