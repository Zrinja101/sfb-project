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
- Game state machine implemented (turn/impulse/step flow)
- Data-driven scenarios loaded from YAML
- Turn mode and turn-point validation implemented

## 4. Implementation tasks
1. ✅ `game/state.py`: helper state machine
2. ✅ `data/scenarios/scenario_1.yaml`: initial scenario data (positions, facing, turn mode)
3. ✅ `sfb/scenarios/loader.py`: generic data-driven scenario loader
4. ✅ `core/ship.py`: turn mode + turn-point state
5. ✅ `combat/arc.py`: firing arc helpers
6. ✅ `engine.py`: integrate play sequence
7. ✅ `tests/test_scenario1.py`: scenario success logic

## 5. Test driven design
- `pytest` as the primary testing framework
- ✅ `test_step_sequence` → enforce ordering (test_game_state.py)
- ✅ `test_turn_mode` → must move N hex before turn
- `test_range_formula` → match D1.4
- ✅ `test_fire_phaser_life` → hit in/out arc (test_arc.py, test_phaser.py)
- `test_scenario1_victory` → target destroyed in N impulses

## 6. Next steps
1. Add range calculation validation - D1.4 true range formula
2. Implement scenario victory conditions - target destroyed in N impulses
3. Add phaser firing tests - hit in/out of arc validation (if needed)

## 7. Data fixtures
- `data/scenarios/scenario1.yaml`:
  - player ship position, facing, turn mode
  - enemy ship position, shields

## 8. Output for UI
- 8-impulse log per turn
- event list (move, fire, damage)
- map snapshots for each step

## 9. Non-goal for now
- seeking weapons, drones, tractor beams (later scenario #??)
- cloaking, sensor effects
- full power allocation
