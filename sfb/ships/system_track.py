from typing import List
from .damage_box import DamageBox


class SystemTrack:
    """
    Represents a track of damage boxes for a specific ship system.

    For example, warp engines may have 30 boxes, hull may have 40.

    Attributes
    ----------
    system_type : str
        Type of system.
    boxes : List[DamageBox]
        List of damage boxes belonging to this system.
    """

    def __init__(self, system_type: str, count: int):
        self.system_type = system_type
        self.boxes: List[DamageBox] = [
            DamageBox(system_type) for _ in range(count)
        ]

    def remaining(self) -> int:
        """
        Count how many boxes remain intact.

        Returns
        -------
        int
        """
        return sum(not b.destroyed for b in self.boxes)

    def destroy_box(self) -> bool:
        """
        Destroy the next available box.

        Returns
        -------
        bool
            True if a box was destroyed, False if no boxes remain.
        """
        for box in self.boxes:
            if not box.destroyed:
                box.destroy()
                return True
        return False
