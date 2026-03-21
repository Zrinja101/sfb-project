"""
Game engine orchestration for turn/impulse processing.
"""

from sfb.combat.combat import CombatSystem
from sfb.combat.arc import can_fire_at
from sfb.game.state import GameState, GameStep


class Engine:
    def __init__(self, game_map, player_ship, targets):
        self.map = game_map
        self.ship = player_ship
        self.targets = targets
        self.state = GameState()
        self.event_listeners = []  # For GUI event notifications

    def add_event_listener(self, listener):
        """Add a listener for game events (useful for GUI)."""
        self.event_listeners.append(listener)

    def notify_listeners(self, event_type, data=None):
        """Notify all listeners of game events."""
        for listener in self.event_listeners:
            listener(event_type, data)

    @property
    def turn(self):
        return self.state.turn

    @property
    def impulse(self):
        return self.state.impulse

    @property
    def total_impulses(self):
        """Total impulses elapsed (turns * 8 + current impulse)."""
        return (self.state.turn - 1) * 8 + self.state.impulse

    @property
    def current_phase(self):
        return self.state.step

    def get_available_actions(self):
        """Get available actions for current phase (for GUI)."""
        phase = self.state.step

        if phase == GameStep.MOVE_SHIPS:
            actions = []
            if not self.ship.can_turn():  # Can move if turn requirement not met
                actions.append({'type': 'move', 'label': 'Move Forward'})
            actions.extend([
                {'type': 'turn_left', 'label': 'Turn Left'},
                {'type': 'turn_right', 'label': 'Turn Right'},
                {'type': 'end_phase', 'label': 'End Movement Phase'}
            ])
            return actions

        elif phase == GameStep.FIRE_WEAPONS:
            actions = []
            alive_targets = [t for t in self.targets if t.alive]
            for i, target in enumerate(alive_targets):
                distance = self.map.distance(self.ship.hex, target.hex)
                actions.append({
                    'type': 'fire',
                    'target_index': i,
                    'label': f'Fire at {target.name} (dist: {distance})'
                })
            actions.append({'type': 'end_phase', 'label': 'End Combat Phase'})
            return actions

        elif phase == GameStep.DAMAGE:
            return [{'type': 'end_phase', 'label': 'Continue'}]

        return []

    @property
    def turn(self):
        return self.state.turn

    @property
    def impulse(self):
        return self.state.impulse

    def execute_player_move(self):
        """Execute player movement (for GUI automation)."""
        if self.state.step == GameStep.MOVE_SHIPS:
            old_pos = self.ship.hex
            self.ship.move(self.map)
            self.notify_listeners('ship_moved', {
                'from': old_pos,
                'to': self.ship.hex,
                'facing': self.ship.facing
            })
            return True
        return False

    def execute_player_turn(self, direction):
        """Execute player turn: 'left' or 'right'."""
        if self.state.step == GameStep.MOVE_SHIPS:
            old_facing = self.ship.facing
            if direction == 'left':
                self.ship.turn_left()
            elif direction == 'right':
                self.ship.turn_right()
            else:
                return False

            self.notify_listeners('ship_turned', {
                'from': old_facing,
                'to': self.ship.facing,
                'direction': direction
            })
            return True
        return False

    def execute_player_fire(self, target_index):
        """Execute player firing at specified target index."""
        if self.state.step == GameStep.FIRE_WEAPONS:
            if 0 <= target_index < len(self.targets):
                target = self.targets[target_index]
                if target.alive:
                    old_hp = target.hp
                    CombatSystem.fire_phaser(self.ship, target, self.map)

                    self.notify_listeners('combat_result', {
                        'target': target.name,
                        'damage_dealt': old_hp - target.hp,
                        'target_destroyed': not target.alive,
                        'target_hp': target.hp
                    })
                    return True
        return False

    def advance_phase(self):
        """Advance to the next phase (for GUI control)."""
        self.state.next_step()
        self.notify_listeners('phase_changed', {
            'new_phase': self.state.step.name
        })

    def advance_impulse(self):
        """Advance to the next impulse."""
        self.state.next_impulse()
        self.notify_listeners('impulse_changed', {
            'new_turn': self.state.turn,
            'new_impulse': self.state.impulse
        })

    def get_game_state_data(self):
        """Get current game state data for GUI rendering."""
        return {
            'turn': self.state.turn,
            'impulse': self.state.impulse,
            'phase': self.state.step.name,
            'player_ship': {
                'position': self.ship.hex,
                'facing': self.ship.facing,
                'hp': self.ship.hp,
                'movement_used': self.ship.hexes_moved_since_turn,
                'turn_mode': self.ship.turn_mode
            },
            'enemies': [
                {
                    'name': target.name,
                    'position': target.hex,
                    'hp': target.hp,
                    'alive': target.alive
                }
                for target in self.targets
            ]
        }

    def get_available_actions(self):
        """Get list of available actions for current phase (for GUI buttons)."""
        actions = []

        if self.state.step == GameStep.MOVE_SHIPS:
            # Movement actions
            if not self.ship.can_turn():  # Can move forward
                actions.append({
                    'type': 'move',
                    'label': 'Move Forward',
                    'action': 'move'
                })
            else:  # Must turn
                actions.append({
                    'type': 'turn',
                    'label': 'Turn Left',
                    'action': 'turn_left'
                })
                actions.append({
                    'type': 'turn',
                    'label': 'Turn Right',
                    'action': 'turn_right'
                })

        elif self.state.step == GameStep.FIRE_WEAPONS:
            # Combat actions
            alive_targets = [t for t in self.targets if t.alive]
            for i, target in enumerate(alive_targets):
                distance = self.map.distance(self.ship.hex, target.hex)
                # For now, allow firing at any alive target (simplified)
                actions.append({
                    'type': 'fire',
                    'label': f'Fire at {target.name}',
                    'action': 'fire',
                    'target_index': i,
                    'target': target.name,
                    'distance': distance
                })

        # Always add end phase action
        phase_names = {
            GameStep.MOVE_SHIPS: 'End Movement Phase',
            GameStep.FIRE_WEAPONS: 'End Combat Phase',
            GameStep.DAMAGE: 'Continue'
        }
        if self.state.step in phase_names:
            actions.append({
                'type': 'end_phase',
                'label': phase_names[self.state.step],
                'action': 'end_phase'
            })

        return actions

    def step(self):
        # Execute a complete impulse (all defined steps) in one call
        for _ in range(len(self.state.STEPS)):
            print(
                f"\nTurn {self.state.turn}, Impulse {self.state.impulse} ({self.state.step.name})")

            if self.state.step == GameStep.MOVE_SHIPS:
                self.ship.move(self.map)
                print(
                    f"{self.ship.name} moves to {self.ship.hex} facing {self.ship.facing}")

            elif self.state.step == GameStep.MOVE_SEEKING_WEAPONS:
                print("Seek weapons phase (no action)")

            elif self.state.step == GameStep.FIRE_WEAPONS:
                target = CombatSystem.find_closest_target(
                    self.ship, self.targets)
                if target:
                    print(f"Firing at {target.name}...")
                    CombatSystem.fire_phaser(self.ship, target, self.map)
                else:
                    print("No targets remaining")

            elif self.state.step == GameStep.DAMAGE:
                print("Damage resolution phase")

            self.state.next_step()

    def _next_impulse(self):
        self.state.next_impulse()
