from dataclasses import dataclass


@dataclass
class Entity:
    """
    Base entity class representing game objects with position and state.
    
    Attributes:
        name: str - The entity's identifier
        hex: tuple[int, int] - (q, r) axial hex coordinates on game map
        facing: str | None - Optional facing direction (A-F) for ships
        alive: bool - Living state flag (default True)
    """
    name: str
    hex: tuple[int, int]  # (q, r) axial hex coords
    facing: str | None = None  # A-F for ships
    alive: bool = True

    def move_to(self, new_hex: tuple[int, int]):
        """
        Moves entity to specified hex coordinates.
        
        Args:
            new_hex: tuple[int, int] - Target hex coordinates (q, r)
        """
        self.hex = new_hex