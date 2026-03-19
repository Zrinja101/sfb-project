class DamageBox:
    """
    Represents a single damageable box on a Ship System Display (SSD).

    Each box corresponds to a specific ship system (warp, hull, weapon, etc.)
    and can be destroyed exactly once.

    Attributes
    ----------
    system_type : str
        Type of system this box represents.
    destroyed : bool
        Whether the box has been destroyed.
    """

    def __init__(self, system_type: str):
        self.system_type = system_type
        self.destroyed = False

    def destroy(self) -> None:
        """
        Destroy this box if it has not already been destroyed.
        """
        if not self.destroyed:
            self.destroyed = True
