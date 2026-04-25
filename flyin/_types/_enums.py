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
