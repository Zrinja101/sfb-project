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


def test_forward_port_arc():
    ship_hex = (0, 0)
    facing = "A"

    # Target at (1,-1) - direction B (60°), should be in forward-port
    assert is_in_arc(ship_hex, facing, (1, -1), "forward-port")

    # Target at (1,0) - direction A (0°), should not be in forward-port
    assert not is_in_arc(ship_hex, facing, (1, 0), "forward-port")

    # Target at (-1,0) - direction D (180°), should not be in forward-port
    assert not is_in_arc(ship_hex, facing, (-1, 0), "forward-port")


def test_aft_port_arc():
    ship_hex = (0, 0)
    facing = "A"

    # Target at (0,-1) - direction C (120°), should be in aft-port
    assert is_in_arc(ship_hex, facing, (0, -1), "aft-port")

    # Target at (1,0) - direction A (0°), should not be in aft-port
    assert not is_in_arc(ship_hex, facing, (1, 0), "aft-port")


def test_aft_starboard_arc():
    ship_hex = (0, 0)
    facing = "A"

    # Target at (-1,1) - direction E (240°), should be in aft-starboard
    assert is_in_arc(ship_hex, facing, (-1, 1), "aft-starboard")

    # Target at (1,0) - direction A (0°), should not be in aft-starboard
    assert not is_in_arc(ship_hex, facing, (1, 0), "aft-starboard")


def test_forward_starboard_arc():
    ship_hex = (0, 0)
    facing = "A"

    # Target at (0,1) - direction F (300°), should be in forward-starboard
    assert is_in_arc(ship_hex, facing, (0, 1), "forward-starboard")

    # Target at (0,-1) - direction C (120°), should not be in forward-starboard
    assert not is_in_arc(ship_hex, facing, (0, -1), "forward-starboard")


def test_all_arcs_comprehensive():
    """Test all arcs with ship facing A (0°)"""
    ship_hex = (0, 0)
    facing = "A"

    test_cases = [
        # (target_hex, expected_arcs)
        ((1, 0), ["forward", "forward-starboard"]),  # A direction
        ((1, -1), ["forward", "forward-port"]),  # B direction
        ((0, -1), ["forward-port", "aft-port"]),  # C direction
        ((-1, 0), ["aft-port", "aft"]),  # D direction
        ((-1, 1), ["aft", "aft-starboard"]),  # E direction
        ((0, 1), ["forward", "aft-starboard", "forward-starboard"]),  # F direction
    ]

    for target_hex, expected_arcs in test_cases:
        for arc in ["forward", "forward-port", "aft-port", "aft", "aft-starboard", "forward-starboard"]:
            should_be_in_arc = arc in expected_arcs
            assert is_in_arc(ship_hex, facing, target_hex, arc) == should_be_in_arc, \
                f"Target {target_hex} should {'be' if should_be_in_arc else 'not be'} in {arc} arc"