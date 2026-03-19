from typing import Dict
from .system_track import SystemTrack


class ShipSSD:
    """
    Represents a ship's system display.

    This contains all system tracks and shields for a ship.

    Attributes
    ----------
    name : str
        Ship name.
    system_tracks : Dict[str, SystemTrack]
        Mapping of system types to tracks.
    shields : list[int]
        Shield strength values for each facing.
    """

    def __init__(self, name: str):
        self.name = name
        self.system_tracks: Dict[str, SystemTrack] = {}
        self.shields = []

    def add_track(self, system_type: str, count: int) -> None:
        """
        Add a system track to the ship.

        Parameters
        ----------
        system_type : str
        count : int
        """
        self.system_tracks[system_type] = SystemTrack(system_type, count)

    def apply_damage(self, system_type: str) -> bool:
        """
        Apply damage to a specific system.

        Parameters
        ----------
        system_type : str

        Returns
        -------
        bool
            True if damage was applied.
        """
        track = self.system_tracks.get(system_type)

        if track is None:
            return False

        return track.destroy_box()
