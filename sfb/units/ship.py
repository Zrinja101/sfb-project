"""
Player/AI-controlled ship entity with movement controls.
"""

from sfb.core.entity import Entity
from sfb.movement.movement import turn_left, turn_right, move_forward


class Ship(Entity):
    def __init__(self, name, hex, facing):
        super().__init__(name=name, hex=hex, facing=facing)

    def move(self, game_map):
        move_forward(self, game_map)

    def turn_left(self):
        self.facing = turn_left(self.facing)

    def turn_right(self):
        self.facing = turn_right(self.facing)
