from sfb.core.engine import Engine
from sfb.core.map import HexMap
from sfb.units.ship import Ship
from sfb.units.drone import Drone


def test_engine_next_impulse():
    m = HexMap()
    ship = Ship("Ship", (0, 0), "A")
    engine = Engine(m, ship, [])

    assert engine.turn == 1
    assert engine.impulse == 1

    for _ in range(8):
        engine._next_impulse()

    assert engine.turn == 2
    assert engine.impulse == 1


def test_engine_step_moves_and_fires(monkeypatch):
    m = HexMap()
    ship = Ship("Ship", (0, 0), "A")
    target = Drone("Target", (1, 0))
    m.add_entity(ship)
    m.add_entity(target)

    engine = Engine(m, ship, [target])

    # avoid random by overriding CombatSystem.fire_phaser
    from sfb.combat.combat import CombatSystem
    monkeypatch.setattr(CombatSystem, "fire_phaser", lambda s, t, g: target.take_damage(1))

    engine.step()
    assert ship.hex == (1, 0)
    assert target.hp == 3
