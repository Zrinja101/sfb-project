from sfb.combat.phaser import Phaser


def test_phaser_damage_range():
    phaser = Phaser("sfb/data/weapons/phaser_1.yaml")

    for _ in range(50):
        dmg = phaser.fire(3)
        assert 0 <= dmg <= 7
