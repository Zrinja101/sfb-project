from sfb.combat.combat import CombatSystem
from sfb.core.map import HexMap
from sfb.units.drone import Drone


def test_find_closest_target():
    ship = Drone("Player", (0, 0))
    t1 = Drone("T1", (5, 0))
    t2 = Drone("T2", (2, 0))
    t3 = Drone("T3", (10, 0))

    closest = CombatSystem.find_closest_target(ship, [t1, t2, t3])
    assert closest is t2


def test_fire_phaser_affects_target(monkeypatch):
    ship = Drone("Player", (0, 0))
    target = Drone("Target", (1, 0))
    m = HexMap()

    # patch Phaser.fire to avoid randomness
    from sfb.combat.phaser import Phaser
    monkeypatch.setattr(Phaser, "fire", lambda self, r: 2)

    CombatSystem.fire_phaser(ship, target, m)
    assert target.hp == 2
    assert target.alive

    CombatSystem.fire_phaser(ship, target, m)
    assert target.hp == 0
    assert not target.alive
