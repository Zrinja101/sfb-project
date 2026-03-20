from sfb.utils.loader import load_yaml
from sfb.units.ship import Ship


def load_scenario1(path: str):
    data = load_yaml(path)

    player_config = data["player_ship"]
    enemy_config = data["enemy_ship"]

    player_ship = Ship(
        name=player_config["name"],
        hex=tuple(player_config["hex"]),
        facing=player_config["facing"],
        turn_mode=player_config.get("turn_mode", 1),
    )

    enemy_ship = Ship(
        name=enemy_config["name"],
        hex=tuple(enemy_config["hex"]),
        facing=enemy_config["facing"],
        turn_mode=enemy_config.get("turn_mode", 1),
    )

    return {
        "name": data.get("scenario_name", "Scenario 1"),
        "player_ship": player_ship,
        "enemy_ship": enemy_ship,
        "weapon": data.get("weapon", "sfb/data/weapons/phaser_1.yaml"),
    }
