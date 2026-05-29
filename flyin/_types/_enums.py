"""This file is for internal usage its for Enums"""

from enum import Enum


class ZoneCategory(Enum):
    """This andicate the category of Zone"""

    PRIORITY = 'priority'
    NORMAL = 'normal'
    RESTRICTED = 'restricted'
    BLOCKED = 'blocked'


class RoleZone(Enum):
    """This andicate the Role of Zone"""

    STARTING = 'start_hub'
    REGULAR = 'hub'
    ENDING = 'end_hub'


class ColorZone(Enum):
    """This andicate the color of Zone"""

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    MAGENTA = (255, 0, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 192, 203)
    BROWN = (165, 42, 42)
    LIME = (50, 205, 50)
    NAVY = (0, 0, 128)
    TEAL = (0, 128, 128)
    OLIVE = (128, 128, 0)
    GOLD = (255, 215, 0)
    MAROON = (128, 0, 0)
    DARKRED = (139, 0, 0)
    VIOLET = (238, 130, 238)
    CRIMSON = (220, 20, 60)
    RAINBOW = (255, 141, 161)


class MapsTool(Enum):
    """Used for diffrent enums in maps that dosent has groped enum"""
    CONNECTION = 'connection'


class DroneState(Enum):
    """Possible states for a drone."""
    MOVING = 'moving'
    IN_TRANSIT = 'in_transit'
    WAITING = 'waiting'
    DELIVERED = 'delivered'
