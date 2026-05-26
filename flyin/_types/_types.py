"""This file for Type define"""

from flyin._types import ZoneCategory, TypeAlias, ColorZone

Cord: TypeAlias = tuple[int, int]
MetaData: TypeAlias = dict[str, ZoneCategory | ColorZone | int]
