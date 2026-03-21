#!/usr/bin/env python3
"""
Star Fleet Battles Simulator

Command-line interface for running SFB scenarios with different execution modes.
"""

import argparse
from sfb.core.map import HexMap
from sfb.core.engine import Engine
from sfb.combat.combat import CombatSystem
from sfb.scenarios import load_scenario
from sfb.scenarios.victory import VictoryChecker
from sfb.units.ship import Ship
from sfb.units.drone import Drone


def run_scenario(scenario_path: str, max_turns: int = 20):
    """
    Run a scenario with victory conditions.
    """
    print(f"Loading scenario: {scenario_path}")
    scenario = load_scenario(scenario_path)

    print(f"🎯 {scenario.name}")
    if scenario.description:
        print(f"📖 {scenario.description}")
    print(f"🚀 Player: {scenario.player_ship.name} at {scenario.player_ship.hex}")
    print(f"🎯 Enemies: {', '.join(f'{s.name} at {s.hex}' for s in scenario.enemy_ships)}")

    if scenario.victory_conditions:
        vc = scenario.victory_conditions
        print(f"🏆 Victory: {vc.get('description', vc.get('type', 'Unknown'))}")

    print("=" * 50)

    # Setup game
    game_map = HexMap()
    game_map.add_entity(scenario.player_ship)
    for enemy in scenario.enemy_ships:
        game_map.add_entity(enemy)

    engine = Engine(game_map, scenario.player_ship, scenario.enemy_ships)

    # Run game loop
    for turn in range(max_turns):
        print(f"\n--- Turn {engine.turn} ---")

        # Run 8 impulses per turn
        for impulse in range(8):
            print(f"Impulse {engine.impulse}: ", end="")
            engine.step()

            # Check victory conditions after each impulse
            result = VictoryChecker.check_victory(engine, scenario.victory_conditions)
            if result["victory"] or result["defeat"]:
                print(f"\n{result['message']}")
                return result["victory"]

        # Check victory at end of turn
        result = VictoryChecker.check_victory(engine, scenario.victory_conditions)
        if result["victory"] or result["defeat"]:
            print(f"\n{result['message']}")
            return result["victory"]

    # Timeout
    result = VictoryChecker.check_victory(engine, scenario.victory_conditions)
    if result["defeat"]:
        print(f"\n{result['message']}")
    else:
        print(f"\n⏰ Scenario timed out after {max_turns} turns")
    return False


def run_static_scenario(max_turns=20):
    """
    Run scenario in static mode (current behavior).
    Automated execution with no user interaction.
    """
    print("Running Scenario #1 in STATIC mode")
    print("=" * 40)

    game_map = HexMap()

    ship = Ship("Cadet Ship", (0, 0), "A")

    drone1 = Drone("Drone 1", (3, 0))
    drone2 = Drone("Drone 2", (5, -1))

    game_map.add_entity(ship)
    game_map.add_entity(drone1)
    game_map.add_entity(drone2)

    engine = Engine(game_map, ship, [drone1, drone2])

    for turn in range(max_turns):
        print(f"\n--- Turn {turn + 1} ---")
        engine.step()

        # Check for victory condition (all enemies destroyed)
        if not any(target.alive for target in [drone1, drone2]):
            print(f"\n🎉 VICTORY! All enemies destroyed in {turn + 1} turns!")
            break
    else:
        print(f"\n⏰ Scenario ended after {max_turns} turns (maximum reached)")


def run_user_input_scenario():
    """
    Run scenario with user input mode.
    Interactive mode where user makes tactical decisions at each phase.
    """
    print("🎮 USER INPUT mode - Interactive Tactical Combat")
    print("=" * 50)

    # Setup game state
    game_map = HexMap()
    ship = Ship("USS Enterprise", (0, 0), "A")
    drone1 = Drone("Klingon Drone 1", (3, 0))
    drone2 = Drone("Klingon Drone 2", (5, -1))

    game_map.add_entity(ship)
    game_map.add_entity(drone1)
    game_map.add_entity(drone2)

    engine = Engine(game_map, ship, [drone1, drone2])

    print(f"🚀 Starting Scenario #1")
    print(f"📍 Your ship: {ship.name} at {ship.hex}, facing {ship.facing}")
    print(
        f"🎯 Enemies: {drone1.name} at {drone1.hex}, {drone2.name} at {drone2.hex}")
    print()

    while True:
        # Check victory/defeat conditions
        alive_enemies = [t for t in [drone1, drone2] if t.alive]
        if not alive_enemies:
            print("🎉 VICTORY! All enemies destroyed!")
            break
        if not ship.alive:
            print("💀 DEFEAT! Your ship has been destroyed!")
            break

        print(f"\n--- Turn {engine.turn}, Impulse {engine.impulse} ---")
        print(f"📍 Position: {ship.hex}, Facing: {ship.facing}, HP: {ship.hp}")
        print(f"🎯 Remaining enemies: {len(alive_enemies)}")

        # Interactive phase execution
        try:
            if not execute_phase_interactive(engine, alive_enemies):
                break  # User chose to quit
        except KeyboardInterrupt:
            print("\n👋 Game interrupted by user.")
            break
        except Exception as e:
            print(f"❌ Error during phase execution: {e}")
            continue

        # Auto-advance to next impulse
        engine._next_impulse()


def execute_phase_interactive(engine, alive_enemies):
    """
    Execute one phase interactively, getting user input.
    Returns False if user wants to quit.
    """
    current_phase = engine.state.step

    print(f"\n🔄 Phase: {current_phase.name.replace('_', ' ').title()}")

    if current_phase.name == "MOVE_SHIPS":
        return handle_movement_phase(engine)
    elif current_phase.name == "MOVE_SEEKING_WEAPONS":
        print("🔍 Seeking weapons phase - no weapons to move")
        engine.state.next_step()
        return True
    elif current_phase.name == "FIRE_WEAPONS":
        return handle_combat_phase(engine, alive_enemies)
    elif current_phase.name == "DAMAGE":
        print("💥 Damage resolution phase - automatic")
        engine.state.next_step()
        return True
    else:
        print(f"⚠️  Unknown phase: {current_phase}")
        engine.state.next_step()
        return True


def handle_movement_phase(engine):
    """Handle user input for movement phase."""
    ship = engine.ship

    while True:
        print(f"\n🚀 Movement Options:")
        print(f"  Current: {ship.hex}, Facing: {ship.facing}")
        print(
            f"  Movement points used: {ship.hexes_moved_since_turn}/{ship.turn_mode}")
        print()
        print("Commands:")
        print("  move - Move forward one hex")
        print("  turn left - Turn left (if eligible)")
        print("  turn right - Turn right (if eligible)")
        print("  status - Show current status")
        print("  end - End movement phase")
        print("  quit - Quit game")

        try:
            cmd = input("\n🎯 Movement command: ").strip().lower()

            if cmd == "quit":
                return False
            elif cmd == "status":
                print(f"📍 Position: {ship.hex}, Facing: {ship.facing}")
                print(f"❤️  HP: {ship.hp}")
                print(
                    f"🎯 Movement: {ship.hexes_moved_since_turn}/{ship.turn_mode}")
                continue
            elif cmd == "end":
                print("✅ Ending movement phase")
                break
            elif cmd == "move":
                if ship.can_turn():
                    print("⚠️  Cannot move: must turn first (turn mode requirement)")
                    continue
                ship.move(engine.map)
                print(f"🚀 Moved to {ship.hex}")
            elif cmd == "turn left":
                ship.turn_left()
                print(f"↺ Turned left, now facing {ship.facing}")
            elif cmd == "turn right":
                ship.turn_right()
                print(f"↻ Turned right, now facing {ship.facing}")
            else:
                print("❌ Unknown command. Type 'status' for help.")

        except ValueError as e:
            print(f"❌ {e}")
        except EOFError:
            return False

    engine.state.next_step()
    return True


def handle_combat_phase(engine, alive_enemies):
    """Handle user input for combat phase."""
    ship = engine.ship

    while True:
        print(f"\n⚔️  Combat Phase")
        print(f"📍 Your position: {ship.hex}, Facing: {ship.facing}")

        # Show available targets
        print("🎯 Available targets:")
        for i, enemy in enumerate(alive_enemies, 1):
            distance = engine.map.distance(ship.hex, enemy.hex)
            print(
                f"  {i}. {enemy.name} at {enemy.hex} (distance: {distance}, HP: {enemy.hp})")

        print()
        print("Commands:")
        print("  fire <number> - Fire phaser at target (e.g., 'fire 1')")
        print("  status - Show current status")
        print("  end - End combat phase")
        print("  quit - Quit game")

        try:
            cmd = input("\n🎯 Combat command: ").strip().lower()

            if cmd == "quit":
                return False
            elif cmd == "status":
                print(f"📍 Position: {ship.hex}, Facing: {ship.facing}")
                print(f"❤️  HP: {ship.hp}")
                continue
            elif cmd == "end":
                print("✅ Ending combat phase")
                break
            elif cmd.startswith("fire "):
                try:
                    target_num = int(cmd.split()[1]) - 1
                    if 0 <= target_num < len(alive_enemies):
                        target = alive_enemies[target_num]
                        print(f"⚡ Firing at {target.name}...")
                        CombatSystem.fire_phaser(ship, target, engine.map)

                        if not target.alive:
                            print(f"💥 {target.name} destroyed!")
                            alive_enemies.remove(target)
                        else:
                            print(
                                f"💥 {target.name} has {target.hp} HP remaining")
                    else:
                        print("❌ Invalid target number")
                except (IndexError, ValueError):
                    print("❌ Invalid fire command. Use 'fire <number>'")
            else:
                print("❌ Unknown command. Type 'status' for help.")

        except EOFError:
            return False

    engine.state.next_step()
    return True


def run_ai_scenario():
    """
    Run scenario with AI input mode.
    AI makes decisions for ship movement and combat.
    """
    print("AI mode - Not yet implemented")
    print("This will feature AI-controlled ship tactics")


def run_gui_simulation():
    """
    Simulate GUI mode - demonstrates how GUI integration would work.
    Shows event-driven updates and state queries.
    """
    print("🎨 GUI SIMULATION mode - Event-driven gameplay")
    print("=" * 50)

    # Setup game state
    game_map = HexMap()
    ship = Ship("USS Enterprise", (0, 0), "A")
    drone1 = Drone("Klingon Drone 1", (3, 0))
    drone2 = Drone("Klingon Drone 2", (5, -1))

    game_map.add_entity(ship)
    game_map.add_entity(drone1)
    game_map.add_entity(drone2)

    engine = Engine(game_map, ship, [drone1, drone2])

    # GUI Event Listener (simulates GUI updates)
    def gui_event_handler(event_type, data=None):
        if event_type == 'ship_moved':
            print(
                f"🎨 GUI UPDATE: Ship moved from {data['from']} to {data['to']}")
        elif event_type == 'ship_turned':
            print(
                f"🎨 GUI UPDATE: Ship turned {data['direction']} from {data['from']} to {data['to']}")
        elif event_type == 'combat_result':
            print(
                f"🎨 GUI UPDATE: Combat - {data['target']} took {data['damage_dealt']} damage")
            if data['target_destroyed']:
                print(f"🎨 GUI UPDATE: {data['target']} destroyed!")
        elif event_type == 'phase_changed':
            print(f"🎨 GUI UPDATE: Phase changed to {data['new_phase']}")
        elif event_type == 'impulse_changed':
            print(
                f"🎨 GUI UPDATE: New impulse - Turn {data['new_turn']}, Impulse {data['new_impulse']}")

    engine.add_event_listener(gui_event_handler)

    print("🚀 Starting GUI simulation...")
    print("🎮 This demonstrates how a GUI would interact with the game engine")
    print()

    # Simulate GUI-driven gameplay (simplified demonstration)
    print(f"\n--- Turn {engine.turn} ---")

    # Demonstrate GUI integration concepts
    print("🔄 Impulse 1")

    # Movement Phase
    print("🚀 Movement Phase:")
    state = engine.get_game_state_data()
    print(
        f"   Position: {state['player_ship']['position']}, Facing: {state['player_ship']['facing']}")

    actions = engine.get_available_actions()
    print(f"   Available actions: {[a['label'] for a in actions]}")

    print("   → Clicking 'Move Forward' button")
    engine.execute_player_move()

    print("   → Clicking 'End Movement Phase'")
    engine.advance_phase()

    # Skip seeking weapons
    engine.advance_phase()

    # Combat Phase
    print("\n⚔️ Combat Phase:")
    actions = engine.get_available_actions()
    print(
        f"   Available targets: {[a['label'] for a in actions if a['type'] == 'fire']}")

    if actions and any(a['type'] == 'fire' for a in actions):
        print("   → Clicking 'Fire at Klingon Drone 1'")
        engine.execute_player_fire(0)

    print("   → Clicking 'End Combat Phase'")
    engine.advance_phase()

    # Damage Phase
    print("\n💥 Damage Phase:")
    print("   → Clicking 'Continue'")
    engine.advance_phase()

    print("\n🎮 GUI simulation complete!")
    print("💡 This demonstrates how a GUI would:")
    print("   • Query game state for display")
    print("   • Get available actions for buttons/menus")
    print("   • Execute actions via method calls")
    print("   • Receive events for UI updates")


def main():
    parser = argparse.ArgumentParser(
        description="Star Fleet Battles Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Modes:
  static          - Automated execution with victory conditions
  user-input      - Interactive user input for tactical decisions
  ai              - AI-controlled ship tactics
  multiplayer     - Multiple human players
  gui-simulation  - Simulate GUI integration (demonstrates event-driven gameplay)

Examples:
  python app.py                                    # Run scenario 1 with victory conditions
  python app.py -s sfb/data/scenarios/scenario_1.yaml  # Run specific scenario
  python app.py -m user-input                       # Interactive mode
  python app.py -m gui-simulation                   # GUI integration demo
        """
    )

    parser.add_argument(
        "-m", "--mode",
        choices=["static", "user-input", "ai",
                 "multiplayer", "gui-simulation"],
        default="static",
        help="Execution mode (default: static)"
    )

    parser.add_argument(
        "-t", "--turns",
        type=int,
        default=20,
        help="Maximum number of turns to run (default: 20)"
    )

    parser.add_argument(
        "-s", "--scenario",
        default="sfb/data/scenarios/scenario_1.yaml",
        help="Scenario file to run (default: sfb/data/scenarios/scenario_1.yaml)"
    )

    args = parser.parse_args()

    # Dispatch to appropriate mode
    if args.mode == "static":
        run_scenario(args.scenario, args.turns)
    elif args.mode == "user-input":
        run_user_input_scenario()
    elif args.mode == "ai":
        run_ai_scenario()
    elif args.mode == "multiplayer":
        run_multiplayer_scenario()
    elif args.mode == "gui-simulation":
        run_gui_simulation()


if __name__ == "__main__":
    main()
