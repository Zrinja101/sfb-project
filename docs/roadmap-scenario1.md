# Scenario #1 Roadmap

This file maps the STARS FLEET BATTLES Cadet Training Handbook Scenario #1 requirements into implementation steps.

## 1. Scenario #1 goal
- Learn ship maneuvering (turning)
- Weapon fire mechanics (phasers)
- Move vs fire tactical choices

## 2. Required rule sets from handbook (page 6-8)
- (B2.0) sequence of play: turn/impulse/steps
- (C3.0) turning and turn mode
- (D1.4) range calculation (true range = hex count incl target)
- (D2.0) firing arcs

## 3. Current code status
- Hex map / distance built
- Ship basic movement built
- Combat phaser + DAC built
- No full step sequence engine

## 4. Implementation tasks
1. `game/state.py`: helper state machine
2. `game/scenario1.py`: initial positioning
3. `core/ship.py`: turn mode + turn-point state
4. `combat/arc.py`: firing arc helpers
5. `engine.py`: integrate play sequence
6. `tests/test_scenario1.py`: scenario success logic

## 5. Test driven design
- `test_step_sequence` → enforce ordering
- `test_turn_mode` → must move N hex before turn
- `test_range_formula` → match D1.4
- `test_fire_phaser_life` → hit in/out arc
- `test_scenario1_victory` → target destroyed in N impulses

## 6. Data fixtures
- `data/scenarios/scenario1.yaml`:
  - player ship position, facing, turn mode
  - enemy ship position, shields

## 7. Output for UI
- 8-impulse log per turn
- event list (move, fire, damage)
- map snapshots for each step

## 8. Non-goal for now
- seeking weapons, drones, tractor beams (later scenario #??)
- cloaking, sensor effects
- full power allocation
