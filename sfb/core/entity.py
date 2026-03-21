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
        hp: int - Hit points (default 0 for indestructible)
    """
    name: str
    hex: tuple[int, int]  # (q, r) axial hex coords
    facing: str | None = None  # A-F for ships
    alive: bool = True
    hp: int = 0

    def move_to(self, new_hex: tuple[int, int]):
        """
        Moves entity to specified hex coordinates.
        
        Args:
            new_hex: tuple[int, int] - Target hex coordinates (q, r)
        """
        self.hex = new_hex

    def take_damage(self, damage: int):
        """
        Apply damage to the entity.
        
        Args:
            damage: int - Amount of damage to apply
        """
        if self.hp > 0:
            self.hp -= damage
            if self.hp <= 0:
                self.alive = False