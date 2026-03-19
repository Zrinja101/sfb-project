"""
Ship module representing system boxes and damage handling.
"""

from typing import Dict


class Ship:
    """
    Represents a ship with system box counts.
    """

    def __init__(self, systems: Dict[str, int]):
        self.systems = systems.copy()

    def has(self, system: str) -> bool:
        """Check if system has remaining boxes."""
        return self.systems.get(system, 0) > 0

    def apply_damage(self, system: str) -> bool:
        """
        Apply damage to a system.

        Returns:
            bool: True if damage applied, False otherwise.
        """
        if self.has(system):
            self.systems[system] -= 1
            return True
        return False
