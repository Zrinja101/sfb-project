"""
Movement utilities (turning and forward motion) for hex ships.
"""

FACINGS = ["A", "B", "C", "D", "E", "F"]


def turn_left(facing: str) -> str:
    idx = FACINGS.index(facing)
    return FACINGS[(idx - 1) % 6]


def turn_right(facing: str) -> str:
    idx = FACINGS.index(facing)
    return FACINGS[(idx + 1) % 6]


def move_forward(entity, game_map):
    if entity.facing is None:
        raise ValueError("Entity has no facing")

    game_map.move_entity(entity, entity.facing)
