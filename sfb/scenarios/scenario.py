from dataclasses import dataclass
from typing import List, Dict, Any
from sfb.units.ship import Ship


@dataclass
class Scenario:
    name: str
    player_ship: Ship
    enemy_ships: List[Ship]
    weapon: str
    victory_conditions: Dict[str, Any] = None
    description: str = ""


@dataclass
class ScenarioInfo:
    description: str
    ruleset: str
