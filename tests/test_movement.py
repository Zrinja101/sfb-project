from sfb.core.entity import Entity
from sfb.core.map import HexMap
from sfb.movement.movement import turn_left, turn_right, move_forward


def test_turning():
    assert turn_left("A") == "F"
    assert turn_right("F") == "A"


def test_move_forward():
    m = HexMap()
    e = Entity(name="E2", hex=(0, 0), facing="A")
    m.add_entity(e)

    move_forward(e, m)
    assert e.hex == (1, 0)
