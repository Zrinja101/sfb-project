from sfb.core.map import HexMap


def test_hex_distance():
    m = HexMap()

    # Adjacent hexes (range 1)
    assert m.distance((0, 0), (1, 0)) == 1  # A direction
    assert m.distance((0, 0), (1, -1)) == 1  # B direction
    assert m.distance((0, 0), (0, -1)) == 1  # C direction
    assert m.distance((0, 0), (-1, 0)) == 1  # D direction
    assert m.distance((0, 0), (-1, 1)) == 1  # E direction
    assert m.distance((0, 0), (0, 1)) == 1  # F direction

    # Range 2
    assert m.distance((0, 0), (2, 0)) == 2
    assert m.distance((0, 0), (1, 1)) == 2
    assert m.distance((0, 0), (0, 2)) == 2

    # Range 3
    assert m.distance((0, 0), (3, 0)) == 3
    assert m.distance((0, 0), (2, 1)) == 3

    # Same position
    assert m.distance((0, 0), (0, 0)) == 0
