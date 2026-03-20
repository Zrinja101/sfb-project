from enum import Enum, auto


class GameStep(Enum):
    MOVE_SHIPS = auto()
    MOVE_SEEKING_WEAPONS = auto()
    FIRE_WEAPONS = auto()
    DAMAGE = auto()


class GameState:
    """Track turn/impulse/step progression according to SFB basic impulse sequence."""

    STEPS = [
        GameStep.MOVE_SHIPS,
        GameStep.MOVE_SEEKING_WEAPONS,
        GameStep.FIRE_WEAPONS,
        GameStep.DAMAGE,
    ]

    def __init__(self, turn: int = 1, impulse: int = 1):
        self.turn = turn
        self.impulse = impulse
        self.step_index = 0

    @property
    def step(self) -> GameStep:
        return self.STEPS[self.step_index]

    def next_step(self):
        self.step_index += 1
        if self.step_index >= len(self.STEPS):
            self.step_index = 0
            self.next_impulse()

    def next_impulse(self):
        self.impulse += 1
        if self.impulse > 8:
            self.impulse = 1
            self.turn += 1

    def reset(self):
        self.turn = 1
        self.impulse = 1
        self.step_index = 0
