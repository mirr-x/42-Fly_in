"""This module defines a connections between two zones"""

from flyin.models.zone import Zone


class Connection:
    """Connection bettwen two zones zone_a and zone_b

    Attrbutes:
        zone_a: Zone object in map
        zone_b: Zone object in map
    """

    def __init__(
                self,
                zone_a: Zone,
                zone_b: Zone,
                max_link_capacity: int = 1
            ) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity

    def __repr__(self) -> str:
        return f"{self.zone_a}-{self.zone_b}"
