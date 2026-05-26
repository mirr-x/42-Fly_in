"""This module defines a Zone that represents a location on the map."""


from flyin._types import RoleZone, ZoneCategory, Cord, ColorZone
from flyin.parser import _errors


class Zone:
    """Represents a location (zone) on the map.

    Attributes:
        name: The zone s identifier (unique, human readable string).
        coordinates: A tuple (x, y) representing the zone s position.
        role: The zone s role (e.g., STARTING, REGULAR, or ENDING).
        max_drones: Optional[Maximum number of drones allowed in this zone]
        color: Optional color code (e.g., '#FF0000') for map rendering.
        zone_cost: Optional[type of zone NORMAL, BLOCKED, RESTRICTED, PRIORITY]
    """

    def __init__(
                self,
                name: str,
                cord: Cord,
                role: RoleZone,
                max_drones: int = 1,
                color: ColorZone = ColorZone.BLUE,
                category: ZoneCategory = ZoneCategory.NORMAL
                ) -> None:
        self.name = name
        self.cord = cord
        self.role = role
        self.max_drones = max_drones
        self.color = color
        self.category = category

    def get_movement_cost(self) -> float:
        """Return the movement category associated with this zone."""

        if self.role is RoleZone.STARTING:
            return 0
        if self.category is ZoneCategory.PRIORITY:
            return 1
        if self.category is ZoneCategory.NORMAL:
            return 1
        if self.category is ZoneCategory.RESTRICTED:
            return 2
        raise _errors.InvalidValueError(
            f"Unknown zone category for '{self.name}'"
        )

    def is_blocked(self) -> bool:
        """Return True if this zone is blocked."""

        return self.category is ZoneCategory.BLOCKED

    def __repr__(self) -> str:
        return f'{self.name}'
