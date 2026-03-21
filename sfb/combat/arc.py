"""
Firing arc calculations and validation for weapons.
"""

from sfb.core.map import HexMap


# Direction indices: A=0, B=1, C=2, D=3, E=4, F=5
DIRECTION_TO_INDEX = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5}

# Firing arcs as relative direction indices (0 = forward, clockwise)
ARC_INDICES = {
    "forward": [5, 0, 1],  # -30° to 30° (indices 5,0,1)
    "forward-port": [1, 2],
    "aft-port": [2, 3],
    "aft": [3, 4],
    "aft-starboard": [4, 5],
    "forward-starboard": [5, 0],  # 270°-330°, indices 5,0
}


def is_in_arc(ship_hex: tuple[int, int], ship_facing: str, target_hex: tuple[int, int], arc: str) -> bool:
    """
    Check if target is within the specified firing arc from the ship.

    Args:
        ship_hex: Ship's hex coordinates (q, r)
        ship_facing: Ship's facing direction ("A", "B", etc.)
        target_hex: Target's hex coordinates (q, r)
        arc: Arc name ("forward", "aft", etc.)

    Returns:
        True if target is in the arc, False otherwise.
    """
    if ship_hex == target_hex:
        return False

    bearing_dir = HexMap.bearing_direction(ship_hex, target_hex)
    bearing_index = DIRECTION_TO_INDEX[bearing_dir]
    facing_index = DIRECTION_TO_INDEX[ship_facing]

    relative_index = (bearing_index - facing_index) % 6

    return relative_index in ARC_INDICES[arc]


def can_fire_at(ship_hex: tuple[int, int], ship_facing: str, target_hex: tuple[int, int], allowed_arcs: list[str]) -> bool:
    """
    Check if the ship can fire at the target given the weapon's allowed arcs.

    Args:
        ship_hex: Ship's hex coordinates
        ship_facing: Ship's facing
        target_hex: Target's hex coordinates
        allowed_arcs: List of allowed arc names for the weapon

    Returns:
        True if target is in at least one allowed arc.
    """
    if ship_facing is None:
        return True  # No facing, no arc restrictions
    return any(is_in_arc(ship_hex, ship_facing, target_hex, arc) for arc in allowed_arcs)