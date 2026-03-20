from sfb.scenarios import load_scenario
from sfb.combat.combat import CombatSystem
from sfb.core.map import HexMap


def test_scenario1_loading():
    scenario = load_scenario("sfb/data/scenarios/scenario_1.yaml")

    assert scenario.name == "Scenario 1"
    assert scenario.player_ship.name == "Cadet Ship"
    assert scenario.enemy_ships[0].name == "Enemy Ship"
    assert scenario.player_ship.hex == (0, 0)
    assert scenario.enemy_ships[0].hex == (3, 0)


def test_scenario1_phaser_firing():
    scenario = load_scenario("sfb/data/scenarios/scenario_1.yaml")
    player = scenario.player_ship
    enemy = scenario.enemy_ships[0]
    game_map = HexMap()

    assert game_map.distance(player.hex, enemy.hex) == 3

    best = CombatSystem.find_closest_target(player, [enemy])
    assert best is enemy
