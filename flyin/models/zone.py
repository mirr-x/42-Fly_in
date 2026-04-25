"""
    This Module is defeining a Zone represents a location on the map
"""
from typing import Optional, Tuple
from enum import Enum

class TypeZone(Enum):
    """
        This andicate the type of Zone
    """
    NORMAL = 'normal'
    BLOCKED = 'blocked'
    RESTRICTED = 'restricted'
    PRIORITY = 'priority'


class RoleZone(Enum):
    """
        This andicate the Role of Zone
    """
    STARTING = 'starting'
    REGULAR = 'regular'
    ENDING = 'ending'


class Zone:
    def __init__(self,
                name: str,
                cord: Tuple[int, int],
                max_drones: int,
                color: Optional[str] = None,
                _type: TypeZone = TypeZone.NORMAL) -> None:
        self._type = _type
        self.name = name
        self.cord = cord
        self.max_drones = max_drones
        self.color = color
