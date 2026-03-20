"""
Game engine orchestration for turn/impulse processing.
"""

from sfb.combat.combat import CombatSystem


class Engine:
    def __init__(self, game_map, player_ship, targets):
        self.map = game_map
        self.ship = player_ship
        self.targets = targets

        self.turn = 1
        self.impulse = 1

    def step(self):
        print(f"\nTurn {self.turn}, Impulse {self.impulse}")

        # Movement
        self.ship.move(self.map)
        print(f"{self.ship.name} moves to {self.ship.hex} facing {self.ship.facing}")

        # Combat (auto-fire for now)
        target = CombatSystem.find_closest_target(self.ship, self.targets)

        if target:
            print(f"Firing at {target.name}...")
            CombatSystem.fire_phaser(self.ship, target, self.map)
        else:
            print("No targets remaining")

        self._next_impulse()

    def _next_impulse(self):
        self.impulse += 1
        if self.impulse > 8:
            self.impulse = 1
            self.turn += 1
