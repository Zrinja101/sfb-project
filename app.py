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
    Interactive mode where user makes decisions.
    """
    print("USER INPUT mode - Not yet implemented")
    print("This will allow players to make tactical decisions interactively")


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
