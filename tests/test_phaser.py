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
