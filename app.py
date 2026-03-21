#!/usr/bin/env python3
"""
Star Fleet Battles Simulator

Command-line interface for running SFB scenarios with different execution modes.
"""

import argparse
from sfb.core.map import HexMap
from sfb.core.engine import Engine
from sfb.units.ship import Ship
from sfb.units.drone import Drone


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
    print(f"🎯 Enemies: {drone1.name} at {drone1.hex}, {drone2.name} at {drone2.hex}")
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
        print(f"  Movement points used: {ship.hexes_moved_since_turn}/{ship.turn_mode}")
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
                print(f"🎯 Movement: {ship.hexes_moved_since_turn}/{ship.turn_mode}")
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
            print(f"  {i}. {enemy.name} at {enemy.hex} (distance: {distance}, HP: {enemy.hp})")

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
                            print(f"💥 {target.name} has {target.hp} HP remaining")
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


def run_multiplayer_scenario():
    """
    Run scenario in multiplayer mode.
    Multiple human players each controlling a side.
    """
    print("MULTIPLAYER mode - Not yet implemented")
    print("This will support multiple human players")


def main():
    parser = argparse.ArgumentParser(
        description="Star Fleet Battles Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Modes:
  static      - Automated execution (current default behavior)
  user-input  - Interactive user input for tactical decisions
  ai          - AI-controlled ship tactics
  multiplayer - Multiple human players

Examples:
  python app.py                    # Run static scenario
  python app.py -m static -t 10    # Run static for 10 turns
  python app.py -m user-input      # Interactive mode (future)
        """
    )

    parser.add_argument(
        "-m", "--mode",
        choices=["static", "user-input", "ai", "multiplayer"],
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
        default="scenario1",
        help="Scenario to run (default: scenario1, future: more options)"
    )

    args = parser.parse_args()

    # Dispatch to appropriate mode
    if args.mode == "static":
        run_static_scenario(args.turns)
    elif args.mode == "user-input":
        run_user_input_scenario()
    elif args.mode == "ai":
        run_ai_scenario()
    elif args.mode == "multiplayer":
        run_multiplayer_scenario()


if __name__ == "__main__":
    main()
