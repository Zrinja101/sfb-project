from sfb.scenarios.scenario1 import load_scenario1
from sfb.combat.combat import CombatSystem
from sfb.core.map import HexMap


def test_scenario1_loading():
    s = load_scenario1("sfb/data/scenarios/scenario_1.yaml")
    player = s["player_ship"]
    enemy = s["enemy_ship"]

    assert player.name == "Cadet Ship"
    assert enemy.name == "Enemy Ship"
    assert player.hex == (0, 0)
    assert enemy.hex == (3, 0)


def test_scenario1_phaser_firing():
    s = load_scenario1("sfb/data/scenarios/scenario_1.yaml")
    player = s["player_ship"]
    enemy = s["enemy_ship"]
    game_map = HexMap()

    assert game_map.distance(player.hex, enemy.hex) == 3

    # minimal smoke test for CombatSystem: it should select the closest target
    best = CombatSystem.find_closest_target(player, [enemy])
    assert best is enemy
