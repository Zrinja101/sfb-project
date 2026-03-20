"""
Phaser weapon behavior and damage lookup from YAML data.
"""

import random
from sfb.utils.loader import load_yaml


class Phaser:
    def __init__(self, yaml_path: str):
        data = load_yaml(yaml_path)

        self.name = data["name"]
        self.damage_table = data["damage_table"]

    def fire(self, range_to_target: int) -> int:
        roll = random.randint(1, 6)

        r = min(range_to_target, max(self.damage_table.keys()))
        r = max(r, min(self.damage_table.keys()))

        damage = self.damage_table[r][roll - 1]

        print(f"{self.name} fired at range {range_to_target} (roll {roll}) → {damage} damage")

        return damage