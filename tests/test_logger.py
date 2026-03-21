"""
Tests for game logging and output system.
"""

from sfb.core.map import HexMap
from sfb.core.engine import Engine
from sfb.game.logger import GameLogger, GameEvent
from sfb.game.visualizer import MapVisualizer
from sfb.units.ship import Ship
from sfb.units.drone import Drone


def test_logger_creation():
    """Test that logger can be created and attached to engine."""
    game_map = HexMap()
    ship = Ship("Player", (0, 0), "A")
    drone = Drone("Enemy", (3, 0))

    game_map.add_entity(ship)
    game_map.add_entity(drone)

    engine = Engine(game_map, ship, [drone])
    logger = GameLogger(engine)

    assert logger is not None
    assert logger.engine == engine
    assert len(logger.impulse_logs) > 0


def test_logger_event_capture():
    """Test that logger captures events from engine."""
    game_map = HexMap()
    ship = Ship("Player", (0, 0), "A")
    drone = Drone("Enemy", (3, 0))

    game_map.add_entity(ship)
    game_map.add_entity(drone)

    engine = Engine(game_map, ship, [drone])
    logger = GameLogger(engine)

    # Simulate an event
    engine.notify_listeners('ship_moved', {
        'from': (0, 0),
        'to': (1, 0),
        'actor': 'Player'
    })

    # Check that event was captured
    assert len(logger.all_events) > 0
    event = logger.all_events[0]
    assert event.event_type == 'ship_moved'
    assert event.details['from'] == (0, 0)


def test_map_snapshot():
    """Test that map snapshots are taken correctly."""
    game_map = HexMap()
    ship = Ship("Player", (0, 0), "A")
    drone = Drone("Enemy", (3, 0))

    game_map.add_entity(ship)
    game_map.add_entity(drone)

    engine = Engine(game_map, ship, [drone])
    logger = GameLogger(engine)

    # Take snapshot
    snapshot = logger.take_snapshot()

    assert snapshot is not None
    assert snapshot.turn == 1
    assert snapshot.impulse == 1
    assert len(snapshot.entities) == 2


def test_impulse_log():
    """Test impulse log formatting."""
    game_map = HexMap()
    ship = Ship("Player", (0, 0), "A")
    drone = Drone("Enemy", (3, 0))

    game_map.add_entity(ship)
    game_map.add_entity(drone)

    engine = Engine(game_map, ship, [drone])
    logger = GameLogger(engine)

    # Add some events
    engine.notify_listeners('ship_moved', {
        'from': (0, 0),
        'to': (1, 0),
        'actor': 'Player'
    })

    # Format log
    log_text = logger.format_impulse_log()
    assert "Turn" in log_text or "Impulse" in log_text
    assert "moved" in log_text or "Player" in log_text


def test_map_visualizer():
    """Test map visualization."""
    game_map = HexMap()
    ship = Ship("Player", (0, 0), "A")
    drone = Drone("Enemy", (3, 0))

    game_map.add_entity(ship)
    game_map.add_entity(drone)

    engine = Engine(game_map, ship, [drone])
    logger = GameLogger(engine)

    snapshot = logger.take_snapshot()
    visual = MapVisualizer.format_snapshot(snapshot)

    assert visual is not None
    assert len(visual) > 0
    assert "Player" in visual or "P" in visual
