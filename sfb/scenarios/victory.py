"""
Victory condition checking for scenarios.
"""

from typing import Dict, Any, List
from sfb.units.ship import Ship
from sfb.core.engine import Engine


class VictoryChecker:
    """Checks victory conditions for scenarios."""

    @staticmethod
    def check_victory(engine: Engine, victory_conditions: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if victory conditions are met.

        Args:
            engine: Game engine with current state
            victory_conditions: Victory condition configuration

        Returns:
            Dict with 'victory' (bool), 'defeat' (bool), and 'message' (str)
        """
        if not victory_conditions:
            return {"victory": False, "defeat": False, "message": ""}

        condition_type = victory_conditions.get("type", "destroy_all_enemies")
        max_impulses = victory_conditions.get("max_impulses")

        # Check defeat conditions first
        if not engine.ship.alive:
            return {
                "victory": False,
                "defeat": True,
                "message": "Player ship destroyed - DEFEAT!"
            }

        # Check victory conditions
        if condition_type == "destroy_all_enemies":
            alive_enemies = [
                target for target in engine.targets if target.alive]
            if not alive_enemies:
                total_impulses = (engine.turn - 1) * 8 + engine.impulse
                if max_impulses and total_impulses > max_impulses:
                    return {
                        "victory": False,
                        "defeat": True,
                        "message": f"All enemies destroyed but took {total_impulses} impulses (limit: {max_impulses}) - DEFEAT!"
                    }
                else:
                    return {
                        "victory": True,
                        "defeat": False,
                        "message": f"All enemies destroyed in {total_impulses} impulses - VICTORY!"
                    }

        # Check timeout defeat (only if enemies still alive)
        if max_impulses:
            total_impulses = (engine.turn - 1) * 8 + engine.impulse
            if total_impulses >= max_impulses:
                alive_enemies = [
                    target for target in engine.targets if target.alive]
                if alive_enemies:  # Only defeat if enemies are still alive
                    return {
                        "victory": False,
                        "defeat": True,
                        "message": f"Time limit exceeded ({total_impulses}/{max_impulses} impulses) - DEFEAT!"
                    }

        return {"victory": False, "defeat": False, "message": ""}
