from flyin.models.zone import Zone
from flyin.models.zone import Drone
from flyin.models.connection import Connection


class StateGraph:
    def __init__(self) -> None:
        self.occupied_zones: dict[Zone, list[Drone]] = {}
        self.connection_usage: dict[Connection, int]

    def reserve_zone(self) -> bool:
        raise NotImplementedError

    def is_zone_occupied(self) -> bool:
        raise NotImplementedError

    def free_zone(self) -> bool:
        raise NotImplementedError
