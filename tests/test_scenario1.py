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


def test_scenario1_victory():
    """Test that scenario victory conditions work correctly."""
    from sfb.scenarios.victory import VictoryChecker
    from sfb.core.engine import Engine

    scenario = load_scenario("sfb/data/scenarios/scenario_1.yaml")
    game_map = HexMap()
    game_map.add_entity(scenario.player_ship)
    for enemy in scenario.enemy_ships:
        game_map.add_entity(enemy)

    engine = Engine(game_map, scenario.player_ship, scenario.enemy_ships)

    # Initially no victory
    result = VictoryChecker.check_victory(engine, scenario.victory_conditions)
    assert not result["victory"]
    assert not result["defeat"]

    # Test timeout defeat (before destroying enemy)
    scenario_timeout = scenario.victory_conditions.copy()
    scenario_timeout["max_impulses"] = 1
    engine.state._impulse = 5  # Simulate time passing
    result = VictoryChecker.check_victory(engine, scenario_timeout)
    assert not result["victory"]
    assert result["defeat"]
    assert "Time limit exceeded" in result["message"]

    # Now destroy enemy within time limit
    enemy = scenario.enemy_ships[0]
    enemy.take_damage(100)  # Destroy enemy
    engine.state._impulse = 1  # Reset to within time limit

    # Should be victory (within time limit)
    result = VictoryChecker.check_victory(engine, scenario.victory_conditions)
    assert result["victory"]
    assert not result["defeat"]
    assert "VICTORY" in result["message"]
