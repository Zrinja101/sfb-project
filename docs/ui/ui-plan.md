# UI Roadmap for SFB Simulator

This file outlines a phased plan for building the UI after core engine and scenario flow are working.

## 1. Goals
- Visualize map and ships on hex grid
- Allow player commands (move, turn, fire)
- Display game state: turn/impulse/step values
- Support replay/step play for training

## 2. Architecture
- `sfb/ui/` module handles platform-specific rendering/input.
- `sfb/engine.py` remains model layer (non-UI).
- Use events for animation: `MoveEvent`, `FireEvent`, `DamageEvent`.
- Keep data-driven scene definitions (scenarios + UI options in YAML).

## 3. Phases

### 3.1 Phase 1 - Proof of concept
- simple Tkinter or command-line visualization.
- render board and element positions.
- trigger engine step from keyboard.

### 3.2 Phase 2 - Interactive board
- use PyGame for smooth hex display.
- draw hex grid + ship facing + health.
- click target and action buttons.
- show firing arcs and valid movement hexes.

### 3.3 Phase 3 - Scenario controls
- scenario chooser (from `data/scenarios/*.yaml`).
- AI on/off toggle.
- rewind / replay / step through impulses.

### 3.4 Phase 4 - polish
- animations for movement/firing.
- tooltips for ship stats.
- map zoom/pan and HUD with mission info.

## 4. Tools
- **PyGame**: primary for board+gameplay.
- **DearPyGui** or **Tkinter** for debugging panels (logs, network). 
- **PyInstaller** for cross-platform builds (optional).

## 5. Suggested folder structure
- `sfb/ui/__init__.py`
- `sfb/ui/base.py` (interface for renderers)
- `sfb/ui/pygame_ui.py` (main implementation)
- `sfb/ui/controller.py`
- `sfb/ui/hud.py`

## 6. User interaction model
- select ship, choose command (turn/move/fire) with UI actions.
- validate command with engine rule checks.
- show immediate feedback and logs.
- support AI behavior and manual player toggle.

## 7. Testing
- unit tests for UI command translation (no graphics dependency): `tests/test_ui_controller.py`.
- integration tests with_engine and mock render.

## 8. Data-driven options
Add to scenario YAML:
- `ui.mode`: `arc-highlight`, `hex-highlight`, `text-only`
- `ui.starting_camera` depends on map
- `ui.hints` for training

## 9. Next steps
1. create initial `sfb/ui` modules and sample scripts
2. add docs + quickstart `docs/ui/get-started.md`
3. integrate with CI (non-graphical tests + lint)

