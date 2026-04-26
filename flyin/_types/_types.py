"""This file for Type define"""

from typing import TypeAlias
from flyin._types import TypeZone, colorZone

Cord: TypeAlias = tuple[int, int]
MetaData: TypeAlias = dict[str, TypeZone | colorZone | int]
