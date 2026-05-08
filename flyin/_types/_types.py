"""This file for Type define"""

from flyin._types import CostZone, ColorZone, TypeAlias

Cord: TypeAlias = tuple[int, int]
MetaData: TypeAlias = dict[str, CostZone | ColorZone | int]
