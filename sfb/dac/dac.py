"""
Damage Allocation Chart (DAC) engine.
"""

from typing import List, Dict, Optional
from sfb.core.dice import Dice
from sfb.core.ship import Ship


class DAC:
    """
    Implements SFB DAC logic:
    - 2d6 row selection
    - left-to-right system resolution
    - once-per-volley tracking
    """

    def __init__(self, table: List[List[Dict]], dice: Dice):
        self.table = table
        self.dice = dice
        self.once_hits = set()

    def new_volley(self):
        """Reset once-per-volley tracking."""
        self.once_hits.clear()

    def select_row(self) -> List[Dict]:
        """Select a row using 2d6."""
        roll = self.dice.roll_2d6()
        return self.table[roll - 2]

    def resolve_hit(self, ship: Ship) -> Optional[str]:
        """
        Resolve a single point of internal damage.
        """
        row = self.select_row()

        for entry in row:
            system = entry["type"]
            once = entry.get("once", False)

            entry_id = entry["id"]
            if once and system in self.once_hits:
                continue

            resolved = self._resolve_system(system, ship)

            if resolved:
                if once:
                    self.once_hits.add(entry_id)
                return resolved

        return None

    def _resolve_system(self, system: str, ship: Ship) -> Optional[str]:
        """Handle special DAC entries."""
        if system == "ANY_WEAPON":
            return self._resolve_any_weapon(ship)

        if system == "ANY_WARP":
            return self._resolve_any_warp(ship)

        if system == "EXCESS":
            if ship.apply_damage("A_HULL"):
                return "A_HULL"
            return None

        if ship.apply_damage(system):
            return system

        return None

    def _resolve_any_weapon(self, ship: Ship) -> Optional[str]:
        for s in ["PHASER", "TORPEDO", "DRONE"]:
            if ship.apply_damage(s):
                return s
        if ship.apply_damage("A_HULL"):
            return "A_HULL"
        return None

    def _resolve_any_warp(self, ship: Ship) -> Optional[str]:
        for s in ["WARP_LEFT", "WARP_RIGHT", "WARP_CENTER"]:
            if ship.apply_damage(s):
                return s
        if ship.apply_damage("A_HULL"):
            return "A_HULL"
        return None
