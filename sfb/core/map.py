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
