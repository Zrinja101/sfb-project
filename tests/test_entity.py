from sfb.core.entity import Entity


def test_entity_move_to():
    e = Entity(name="E1", hex=(0, 0), facing="A")
    e.move_to((2, -1))
    assert e.hex == (2, -1)
