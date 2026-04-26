"""This file is for internal usage its for Enums"""

from enum import Enum


class TypeZone(Enum):
    """This andicate the type of Zone"""

    NORMAL = 'normal'
    BLOCKED = 'blocked'
    RESTRICTED = 'restricted'
    PRIORITY = 'priority'


class RoleZone(Enum):
    """This andicate the Role of Zone"""

    STARTING = 'starting'
    REGULAR = 'regular'
    ENDING = 'ending'


class colorZone(Enum):
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
