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
    s = Ship("S", (0, 0), "A")
    s.turn_right()
    assert s.facing == "B"
    s.turn_left()
    assert s.facing == "A"
