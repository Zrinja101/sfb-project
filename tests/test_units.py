from sfb.units.drone import Drone
from sfb.units.ship import Ship


def test_drone_takes_damage():
    d = Drone("D", (0, 0))
    d.take_damage(2)
    assert d.hp == 2
    assert d.alive
    d.take_damage(2)
    assert d.hp == 0
    assert not d.alive


def test_ship_turning():
    s = Ship("S", (0, 0), "A", turn_mode=1)
    # cannot turn before moving at least one hex in turn_mode 1
    try:
        s.turn_right()
        assert False, "Expected ValueError when turning before moving"
    except ValueError:
        pass

    # simulate movement and then turn
    s.hex = (1, 0)
    s.hexes_moved_since_turn = 1
    s.turn_right()
    assert s.facing == "B"
    assert s.hexes_moved_since_turn == 0
    s.hexes_moved_since_turn = 1
    s.turn_left()
    assert s.facing == "A"
