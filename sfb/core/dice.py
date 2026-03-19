"""
Dice module for SFB simulator.

Provides deterministic or random dice rolling.
"""

import random
from typing import Optional


class Dice:
    """
    Dice roller supporting deterministic testing via seed injection.
    """

    def __init__(self, seed: Optional[int] = None):
        self._rng = random.Random(seed)

    def d6(self) -> int:
        """Roll a single six-sided die."""
        return self._rng.randint(1, 6)

    def roll_2d6(self) -> int:
        """
        Roll two six-sided dice.

        Returns:
            int: Value from 2–12 (bell curve distribution)
        """
        return self.d6() + self.d6()
