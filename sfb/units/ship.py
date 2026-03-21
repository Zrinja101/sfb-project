"""
Player/AI-controlled ship entity with movement controls.
"""

from sfb.core.entity import Entity
from sfb.movement.movement import turn_left, turn_right, move_forward


class Ship(Entity):
    def __init__(self, name, hex, facing, turn_mode=1, hp=10):
        super().__init__(name=name, hex=hex, facing=facing, hp=hp)
        self.turn_mode = turn_mode
        self.hexes_moved_since_turn = 0

    def move(self, game_map):
        move_forward(self, game_map)
        self.hexes_moved_since_turn += 1

    def can_turn(self) -> bool:
        return self.hexes_moved_since_turn >= self.turn_mode

    def reset_turn_counter(self):
        self.hexes_moved_since_turn = 0

    def turn_left(self):
        if not self.can_turn():
            raise ValueError("Cannot turn yet: turn mode requirement not met")
        self.facing = turn_left(self.facing)
        self.reset_turn_counter()

    def turn_right(self):
        if not self.can_turn():
            raise ValueError("Cannot turn yet: turn mode requirement not met")
        self.facing = turn_right(self.facing)
        self.reset_turn_counter()

    def take_damage(self, amount: int):
        """Take damage and update alive status."""
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
