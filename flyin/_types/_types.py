"""This file for Type define"""

from flyin._types import TypeZone, ColorZone, TypeAlias

Cord: TypeAlias = tuple[int, int]
MetaData: TypeAlias = dict[str, TypeZone | ColorZone | int]
