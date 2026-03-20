from sfb.core.map import HexMap


def test_hex_distance():
    m = HexMap()

    assert m.distance((0, 0), (1, 0)) == 1
    assert m.distance((0, 0), (2, 0)) == 2
