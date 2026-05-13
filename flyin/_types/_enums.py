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

    WHITE = 'white'
    RED = 'red'
    YELLOW = 'yellow'
    CYAN = 'cyan'
    GREEN = 'green'
    BLUE = 'blue'
    MAGENTA = 'magenta'
    BLACK = 'black'
    GRAY = 'gray'
    ORANGE = 'orange'
    PURPLE = 'purple'
    PINK = 'pink'
    BROWN = 'brown'
    LIME = 'lime'
    NAVY = 'navy'
    TEAL = 'teal'
    OLIVE = 'olive'
    GOLD = 'gold'
    MAROON = 'maroon'
    DARKRED = 'darkred'
    VIOLET = 'violet'
    CRIMSON = 'crimson'
    RAINBOW = 'rainbow'


class MapsTool(Enum):
    """Used for diffrent enums in maps that dosent has groped enum"""
    CONNECTION = 'connection'


class DroneState(Enum):
    """Possible states for a drone."""
    MOVING = 'moving'
    IN_TRANSIT = 'in_transit'
    WAITING = 'waiting'
    DELIVERED = 'delivered'
