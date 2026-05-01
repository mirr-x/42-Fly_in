"""This module defines a Zone that represents a location on the map."""

from flyin._types import Optional
from flyin._types import RoleZone, TypeZone, Cord


class Zone:
    """Represents a location (zone) on the map.

    Attributes:
        name: The zone s identifier (unique, human readable string).
        coordinates: A tuple (x, y) representing the zone s position.
        role: The zone s role (e.g., STARTING, REGULAR, or ENDING).
        max_drones: Optional[Maximum number of drones allowed in this zone]
        color: Optional color code (e.g., '#FF0000') for map rendering.
        zone_type: Optional[type of zone NORMAL, BLOCKED, RESTRICTED, PRIORITY]
    """

    def __init__(
                self,
                name: str,
                cord: Cord,
                role: RoleZone,
                max_drones: Optional[int] = 1,
                color: Optional[str] = None,
                _type: TypeZone = TypeZone.NORMAL
                ) -> None:
        self.name = name
        self.cord = cord
        self.role = role
        self.max_drones = max_drones
        self.color = color
        self._type = _type

    def __repr__(self) -> str:
        return f'{self.name}'

    # def __repr__(self) -> str:
    #     return (f'Zone(name={self.name}, cord={self.cord}, role={self.role}, '
    #             f'max_drones={self.max_drones}, color={self.color}, '
    #             f'type={self._type})')
