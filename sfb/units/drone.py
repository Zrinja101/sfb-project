"""
Drone unit (weak/flying/moving target) for combat simulation.
"""

from sfb.core.entity import Entity


class Drone(Entity):
    def __init__(self, name, hex):
        super().__init__(name=name, hex=hex, facing=None)
        self.hp = 4

    def take_damage(self, amount: int):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
