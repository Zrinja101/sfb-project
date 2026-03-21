"""
Tests for firing arc calculations.
"""

import pytest
from sfb.combat.arc import is_in_arc, can_fire_at


def test_forward_arc():
    # Ship at (0,0) facing A (0 degrees)
    ship_hex = (0, 0)
    facing = "A"

    # Target at (1,0) - direction A, should be in forward arc
    assert is_in_arc(ship_hex, facing, (1, 0), "forward")

    # Target at (-1,0) - direction D (180), should not be in forward
    assert not is_in_arc(ship_hex, facing, (-1, 0), "forward")

    # Target at (1,-1) - direction B (60), should be in forward
    assert is_in_arc(ship_hex, facing, (1, -1), "forward")

    # Target at (0,1) - direction F (300), should be in forward
    assert is_in_arc(ship_hex, facing, (0, 1), "forward")


def test_aft_arc():
    ship_hex = (0, 0)
    facing = "A"

    # Target at (-1,0) - aft, should be in aft arc
    assert is_in_arc(ship_hex, facing, (-1, 0), "aft")

    # Target at (1,0) - forward, should not
    assert not is_in_arc(ship_hex, facing, (1, 0), "aft")


def test_can_fire_at():
    ship_hex = (0, 0)
    facing = "A"
    target_hex = (1, 0)  # Forward

    # Phaser with forward arc can fire
    assert can_fire_at(ship_hex, facing, target_hex, ["forward"])

    # Phaser with aft arc cannot
    assert not can_fire_at(ship_hex, facing, target_hex, ["aft"])

    # Phaser with multiple arcs
    assert can_fire_at(ship_hex, facing, target_hex, ["forward", "aft"])


def test_different_facing():
    ship_hex = (0, 0)
    facing = "D"  # 180 degrees

    # Target at (-1,0) - now forward for D facing
    assert is_in_arc(ship_hex, facing, (-1, 0), "forward")

    # Target at (1,0) - now aft
    assert is_in_arc(ship_hex, facing, (1, 0), "aft")