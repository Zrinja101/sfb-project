from sfb.core.ship import Ship


def test_ship_system_damage():
    ship = Ship({"PHASER": 2})
    assert ship.has("PHASER")
    assert ship.apply_damage("PHASER")
    assert ship.has("PHASER")
    assert ship.apply_damage("PHASER")
    assert not ship.has("PHASER")
    assert not ship.apply_damage("PHASER")
