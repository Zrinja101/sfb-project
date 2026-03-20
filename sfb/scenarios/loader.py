from pathlib import Path
from typing import List

from sfb.utils.loader import load_yaml
from sfb.scenarios.scenario import Scenario
from sfb.units.ship import Ship


def _build_ship(cfg: dict) -> Ship:
    return Ship(
        name=cfg["name"],
        hex=tuple(cfg["hex"]),
        facing=cfg["facing"],
        turn_mode=cfg.get("turn_mode", 1),
    )


def load_scenario(path: str) -> Scenario:
    file = Path(path)
    data = load_yaml(str(file))

    player_ship_cfg = data["player_ship"]
    enemy_cfgs = data.get("enemy_ships")

    if enemy_cfgs is None and "enemy_ship" in data:
        enemy_cfgs = [data["enemy_ship"]]

    player_ship = _build_ship(player_ship_cfg)
    enemy_ships = [_build_ship(s) for s in (enemy_cfgs or [])]

    return Scenario(
        name=data.get("scenario_name", file.stem),
        player_ship=player_ship,
        enemy_ships=enemy_ships,
        weapon=data.get("weapon", "sfb/data/weapons/phaser_1.yaml"),
    )
