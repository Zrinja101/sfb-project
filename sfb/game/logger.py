"""
Game event logger and output system for scenario playback and UI.
Tracks events (move, fire, damage) and map state snapshots.
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field
from sfb.core.map import HexMap


@dataclass
class MapSnapshot:
    """Snapshot of map state at a particular moment."""
    turn: int
    impulse: int
    phase: str
    entities: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self):
        """Convert snapshot to dictionary for serialization."""
        return {
            'turn': self.turn,
            'impulse': self.impulse,
            'phase': self.phase,
            'entities': self.entities
        }


@dataclass
class GameEvent:
    """Represents a single game event (move, fire, or damage)."""
    event_type: str  # 'move', 'turn', 'fire', 'damage', 'destroyed'
    turn: int
    impulse: int
    phase: str
    actor: str  # Entity performing action
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        """Convert event to dictionary for serialization."""
        return {
            'event_type': self.event_type,
            'turn': self.turn,
            'impulse': self.impulse,
            'phase': self.phase,
            'actor': self.actor,
            'details': self.details
        }


class GameLogger:
    """Captures game events and map snapshots for logging and playback."""

    def __init__(self, engine):
        self.engine = engine
        self.impulse_logs = []  # List of ImpulseLog objects
        self.current_impulse_log = None
        self.all_events = []  # Flat list of all events
        self.snapshots = []  # Map snapshots

        # Register as event listener
        self.engine.add_event_listener(self.on_event)

        # Create initial impulse log
        self.start_impulse()

    def start_impulse(self):
        """Start logging a new impulse."""
        self.current_impulse_log = ImpulseLog(
            turn=self.engine.turn,
            impulse=self.engine.impulse,
            events=[]
        )
        self.impulse_logs.append(self.current_impulse_log)

    def end_impulse(self):
        """Finalize current impulse log and take snapshot."""
        if self.current_impulse_log:
            # Take snapshot at end of impulse
            snapshot = self.take_snapshot()
            self.snapshots.append(snapshot)

    def on_event(self, event_type: str, data: Dict[str, Any] = None):
        """Handle event from engine event listener."""
        if data is None:
            data = {}

        # Create event record
        event = GameEvent(
            event_type=event_type,
            turn=self.engine.turn,
            impulse=self.engine.impulse,
            phase=self.engine.current_phase.name,
            actor=data.get('actor', 'Unknown'),
            details=data
        )

        # Add to logs
        self.all_events.append(event)
        if self.current_impulse_log:
            self.current_impulse_log.events.append(event)

    def take_snapshot(self) -> MapSnapshot:
        """Take a snapshot of current map state."""
        entities_data = []
        for entity in self.engine.map.entities:
            entity_info = {
                'name': entity.name,
                'hex': entity.hex,
                'facing': entity.facing,
                'hp': entity.hp,
                'alive': entity.alive
            }
            entities_data.append(entity_info)

        snapshot = MapSnapshot(
            turn=self.engine.turn,
            impulse=self.engine.impulse,
            phase=self.engine.current_phase.name,
            entities=entities_data
        )
        return snapshot

    def get_impulse_logs(self) -> List['ImpulseLog']:
        """Get all impulse logs."""
        return self.impulse_logs

    def get_current_impulse_log(self) -> 'ImpulseLog':
        """Get current impulse log."""
        return self.current_impulse_log

    def get_all_events(self) -> List[GameEvent]:
        """Get all events recorded."""
        return self.all_events

    def format_impulse_log(self, impulse_log: 'ImpulseLog' = None) -> str:
        """Format impulse log for display."""
        if impulse_log is None:
            impulse_log = self.current_impulse_log

        if not impulse_log:
            return ""

        output = []
        output.append(
            f"Turn {impulse_log.turn}, Impulse {impulse_log.impulse}:")

        if not impulse_log.events:
            output.append("  [No events]")
        else:
            for event in impulse_log.events:
                event_str = self._format_event(event)
                output.append(f"  {event_str}")

        return "\n".join(output)

    def _format_event(self, event: GameEvent) -> str:
        """Format a single event for display."""
        details = event.details

        if event.event_type == 'ship_moved':
            from_hex = details.get('from')
            to_hex = details.get('to')
            return f"🚀 {event.actor} moved from {from_hex} to {to_hex}"

        elif event.event_type == 'ship_turned':
            direction = details.get('direction')
            from_facing = details.get('from')
            to_facing = details.get('to')
            return f"↻ {event.actor} turned {direction} from {from_facing} to {to_facing}"

        elif event.event_type == 'combat_result':
            target = details.get('target')
            damage = details.get('damage_dealt')
            if details.get('target_destroyed'):
                return f"⚡ {event.actor} fired at {target}: {damage} damage - DESTROYED!"
            else:
                return f"⚡ {event.actor} fired at {target}: {damage} damage"

        elif event.event_type == 'phase_changed':
            new_phase = details.get('new_phase')
            return f"→ Phase changed to {new_phase}"

        elif event.event_type == 'impulse_changed':
            new_turn = details.get('new_turn')
            new_impulse = details.get('new_impulse')
            return f"→ New impulse - Turn {new_turn}, Impulse {new_impulse}"

        else:
            return f"[{event.event_type}] {event.actor}: {details}"

    def format_turn_summary(self, turn_num: int = None) -> str:
        """Format all impulses in a turn."""
        if turn_num is None:
            turn_num = self.engine.turn

        output = []
        output.append(f"\n{'='*60}")
        output.append(f"TURN {turn_num} SUMMARY")
        output.append(f"{'='*60}\n")

        # Filter impulse logs for this turn
        turn_logs = [log for log in self.impulse_logs if log.turn == turn_num]

        if not turn_logs:
            output.append("No impulses recorded for this turn")
        else:
            for log in turn_logs:
                output.append(self.format_impulse_log(log))
                output.append("")  # Blank line between impulses

        return "\n".join(output)

    def format_full_log(self) -> str:
        """Format complete game log."""
        output = []
        output.append(f"\n{'='*60}")
        output.append("COMPLETE GAME LOG")
        output.append(f"{'='*60}\n")

        current_turn = None
        for log in self.impulse_logs:
            if current_turn != log.turn:
                if current_turn is not None:
                    output.append("")  # Blank line between turns
                output.append(f"\n--- TURN {log.turn} ---")
                current_turn = log.turn

            output.append(self.format_impulse_log(log))

        return "\n".join(output)


@dataclass
class ImpulseLog:
    """Log of all events that occurred during a single impulse."""
    turn: int
    impulse: int
    events: List[GameEvent] = field(default_factory=list)

    def to_dict(self):
        """Convert to dictionary for serialization."""
        return {
            'turn': self.turn,
            'impulse': self.impulse,
            'events': [e.to_dict() for e in self.events]
        }
