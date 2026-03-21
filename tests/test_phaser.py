from sfb.combat.phaser import Phaser
from sfb.units.ship import Ship
from sfb.core.map import HexMap
from sfb.combat.combat import CombatSystem


def test_phaser_damage_range():
    phaser = Phaser("sfb/data/weapons/phaser_1.yaml")

    for _ in range(50):
        dmg = phaser.fire(3)
        assert 0 <= dmg <= 7


def test_phaser_arcs():
    phaser = Phaser("sfb/data/weapons/phaser_1.yaml")
    assert phaser.arcs == ["forward"]


def test_fire_phaser_in_arc():
    game_map = HexMap()
    ship = Ship("USS Test", (0, 0), "A")
    target = Ship("Enemy", (1, 0), "A")  # In forward arc
    target.hp = 10

    CombatSystem.fire_phaser(ship, target, game_map)

    # Should have taken damage
    assert target.hp < 10


def test_fire_phaser_out_of_arc():
    game_map = HexMap()
    ship = Ship("USS Test", (0, 0), "A")
    target = Ship("Enemy", (-1, 0), "A")  # In aft arc, not forward
    target.hp = 10

    CombatSystem.fire_phaser(ship, target, game_map)

    # Should not have taken damage
    assert target.hp == 10


def test_fire_phaser_different_facing():
    """Test firing with ship facing different directions."""
    game_map = HexMap()
    ship = Ship("USS Test", (0, 0), "D")  # Facing 180°
    target = Ship("Enemy", (-1, 0), "A")  # Now in forward arc for D facing
    target.hp = 10

    CombatSystem.fire_phaser(ship, target, game_map)

    # Should have taken damage
    assert target.hp < 10


def test_fire_phaser_at_max_range():
    """Test firing at maximum effective range."""
    import random

    game_map = HexMap()
    ship = Ship("USS Test", (0, 0), "A")
    target = Ship("Enemy", (6, 0), "A")  # Range 6 (max for phaser-1)
    target.hp = 10

    # Seed global random for guaranteed damage
    random.seed(1)
    CombatSystem.fire_phaser(ship, target, game_map)

    # Should have taken damage at max range
    assert target.hp < 10


def test_fire_phaser_at_zero_damage_range():
    """Test firing at range where damage table shows 0."""
    game_map = HexMap()
    ship = Ship("USS Test", (0, 0), "A")
    target = Ship("Enemy", (10, 0), "A")  # Range beyond table (should be 0)
    target.hp = 10

    # Mock the phaser to return 0 damage
    from unittest.mock import patch
    with patch('sfb.combat.phaser.Phaser.fire', return_value=0):
        CombatSystem.fire_phaser(ship, target, game_map)

    # Should not have taken damage
    assert target.hp == 10


def test_fire_phaser_destroyed_target():
    """Test firing at already destroyed target."""
    game_map = HexMap()
    ship = Ship("USS Test", (0, 0), "A")
    target = Ship("Enemy", (1, 0), "A")
    target.hp = 0  # Already destroyed
    target.alive = False  # Mark as destroyed

    CombatSystem.fire_phaser(ship, target, game_map)

    # Should remain destroyed (no additional damage)
    assert target.hp == 0
    assert not target.alive
