import math


class HexMap:
    """
    Axial hex grid (q, r)
    """

    # Directions A-F (clockwise)
    DIRECTIONS = {
        "A": (1, 0),
        "B": (1, -1),
        "C": (0, -1),
        "D": (-1, 0),
        "E": (-1, 1),
        "F": (0, 1),
    }

    @staticmethod
    def facing_to_angle(facing: str) -> int:
        """Convert facing direction to angle in degrees."""
        angles = {"A": 0, "B": 60, "C": 120, "D": 180, "E": 240, "F": 300}
        return angles[facing]

    @staticmethod
    def bearing_direction(a: tuple[int, int], b: tuple[int, int]) -> str:
        """
        Get the primary hex direction from a to b.
        Returns the direction letter A-F.
        """
        dq = b[0] - a[0]
        dr = b[1] - a[1]

        if dq > 0:
            return "B" if dr < 0 else "A"
        elif dq < 0:
            return "E" if dr > 0 else "D"
        else:  # dq == 0
            if dr < 0:
                return "C"
            elif dr > 0:
                return "F"
            else:
                return "A"  # same position

    def __init__(self):
        self.entities = []

    def add_entity(self, entity):
        self.entities.append(entity)

    def move_entity(self, entity, direction):
        dq, dr = self.DIRECTIONS[direction]
        q, r = entity.hex
        entity.move_to((q + dq, r + dr))

    @staticmethod
    def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
        """
        Hex distance (axial)
        """
        aq, ar = a
        bq, br = b
        return int((abs(aq - bq) + abs(aq + ar - bq - br) + abs(ar - br)) / 2)
