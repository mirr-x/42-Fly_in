"""This file is for internal usage its for Enums"""

from enum import Enum


class TypeZone(Enum):
    """This andicate the type of Zone"""

    BLOCKED = 0
    NORMAL = 1
    RESTRICTED = 2
    PRIORITY = 'priority'


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
