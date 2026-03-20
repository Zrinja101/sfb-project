from sfb.scenarios.loader import load_scenario


def load_scenario1(path: str):
    """Legacy wrapper for loading Scenario #1 data from YAML."""
    scenario = load_scenario(path)
    return {
        "name": scenario.name,
        "player_ship": scenario.player_ship,
        "enemy_ship": scenario.enemy_ships[0] if scenario.enemy_ships else None,
        "weapon": scenario.weapon,
    }
