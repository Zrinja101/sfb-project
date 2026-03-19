from sfb.ships.ship_ssd import ShipSSD


def test_ship_damage():

    ship = ShipSSD("Test Ship")

    ship.add_track("warp", 2)

    assert ship.apply_damage("warp")
    assert ship.apply_damage("warp")

    assert not ship.apply_damage("warp")
