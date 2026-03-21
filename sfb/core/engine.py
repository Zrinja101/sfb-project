"""
Game engine orchestration for turn/impulse processing.
"""

from sfb.combat.combat import CombatSystem
from sfb.game.state import GameState, GameStep


class Engine:
    def __init__(self, game_map, player_ship, targets):
        self.map = game_map
        self.ship = player_ship
        self.targets = targets
        self.state = GameState()

    @property
    def turn(self):
        return self.state.turn

    @property
    def impulse(self):
        return self.state.impulse

    def execute_current_phase(self):
        """
        Execute only the current phase (for interactive mode).
        Returns a description of what happened.
        """
        phase = self.state.step
        result = ""

        if phase == GameStep.MOVE_SHIPS:
            # Movement is handled interactively, not automatically
            result = "Movement phase - awaiting player input"
            
        elif phase == GameStep.MOVE_SEEKING_WEAPONS:
            result = "Seeking weapons phase - no action required"
            
        elif phase == GameStep.FIRE_WEAPONS:
            # Combat is handled interactively, not automatically
            result = "Combat phase - awaiting player input"
            
        elif phase == GameStep.DAMAGE:
            result = "Damage resolution phase - automatic"
            
        return result

    def step(self):
        # Execute a complete impulse (all defined steps) in one call
        for _ in range(len(self.state.STEPS)):
            print(f"\nTurn {self.state.turn}, Impulse {self.state.impulse} ({self.state.step.name})")

            if self.state.step == GameStep.MOVE_SHIPS:
                self.ship.move(self.map)
                print(f"{self.ship.name} moves to {self.ship.hex} facing {self.ship.facing}")

            elif self.state.step == GameStep.MOVE_SEEKING_WEAPONS:
                print("Seek weapons phase (no action)")

            elif self.state.step == GameStep.FIRE_WEAPONS:
                target = CombatSystem.find_closest_target(self.ship, self.targets)
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
