"""This module contains the Drone class which represents a drone entity."""

from typing import TYPE_CHECKING

from flyin._types._enums import DroneState
from flyin.models.zone import Zone
from flyin.models.connection import Connection
from flyin._types._enums import ZoneCategory

if TYPE_CHECKING:
    from flyin.graph.graph import Graph


class Drone:
    """Represents a drone and its delivery state.

    Attributes:
        id (str): Unique identifier for the drone.
        current_zone (Zone): Current zone of the drone.
        path (list[Zone]): Planned path for the drone.
        path_index (int): Index of the current position in the path.
        state (DroneState): Current state of the drone.
    """

    def __init__(
            self,
            _id: int,
            current_zone: Zone | Connection,
            path: list['Zone'] | None,
            state: DroneState = DroneState.WAITING
    ) -> None:
        self.id = f'D{_id}'
        self.current_zone = current_zone
        self.path = path
        self.path_index = 0
        self.state = state

    def next_zone(self, graph: 'Graph') -> Zone | Connection | None:
        """Return the next zone in the planned path, if available."""
        if self.path is None or self.path_index + 1 >= len(self.path):
            return None
        zone = self.path[self.path_index + 1]
        if (zone.category == ZoneCategory.RESTRICTED
                and self.state != DroneState.IN_TRANSIT):
            if isinstance(self.current_zone, Zone):
                return graph.get_connection(self.current_zone, zone)
            return None
        return zone

    def move_next(self, next_zone: Zone | Connection | None) -> None:
        "Move to next zone in the planned path"

        if next_zone:
            self.current_zone = next_zone
            if isinstance(next_zone, Connection):
                self.set_status(DroneState.IN_TRANSIT)
            else:
                self.path_index += 1
                self.set_status(DroneState.MOVING)
        else:
            self.set_status(DroneState.DELIVERED)

    def is_delivered(self) -> bool:
        """Return True if the drone has reached the delivered state."""
        return self.state == DroneState.DELIVERED

    def set_status(self, status: DroneState) -> None:
        """Set the drone's state to the specified status."""
        self.state = status

    def __repr__(self) -> str:
        return (
            f"Drone(id={self.id!r}, current_zone={self.current_zone!r}, "
            f"path={self.path!r}, path_index={self.path_index!r}, "
            f"state={self.state})"
        )
