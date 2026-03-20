from dataclasses import dataclass
from typing import List
from sfb.units.ship import Ship


@dataclass
class Scenario:
    name: str
    player_ship: Ship
    enemy_ships: List[Ship]
    weapon: str


@dataclass
class ScenarioInfo:
    description: str
    ruleset: str
