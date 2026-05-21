"""Graph Module is the Module gonna store all data of the map and map itself"""

from flyin.models.zone import Zone
from flyin.models.connection import Connection
from flyin.models.drone import Drone
from flyin.parser import _errors
from flyin._types import RoleZone


class Graph:
    """Graph class store all info of the map"""

    def __init__(self) -> None:
        self.drones: list[Drone]
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.adjacency_map: dict[Zone, list[Zone]] = {}
        self.dijkstra_paths: list[tuple[float, list[Zone]]] | None = None

    def add_zone(self, zone: Zone) -> None:
        """Add zone to the zones dict <ZoneRole>: Zone

        Args:
            zone (Zone): zone to be add

        Raises:
            _errors.InsaneError: raised when not adding Zone
        """

        if not isinstance(zone, Zone):
            raise _errors.InsaneError('should append zones only!!!')
        self.zones[zone.name] = zone

    def add_connection(self, connection: Connection) -> None:
        """Add connection to the connection list

        Args:
            connection (Connection): connection to be add

        Raises:
            _errors.InsaneError: raised when not adding connection
        """

        if not isinstance(connection, Connection):
            raise _errors.InsaneError('should append zones only!!!')
        self.connections.append(connection)

    def build_adjacency(self) -> None:
        """Build the adjacency map by assigning neighbors to each zone."""

        for zone in self.zones.values():
            self.adjacency_map[zone] = []
        for conn in self.connections:
            if conn.zone_b not in self.adjacency_map[conn.zone_a]:
                self.adjacency_map[conn.zone_a].append(conn.zone_b)
            if conn.zone_a not in self.adjacency_map[conn.zone_b]:
                self.adjacency_map[conn.zone_b].append(conn.zone_a)

    def get_neighbors(self, zone: Zone) -> list[Zone]:
        """return zones that you can accses from given zone

        Args:
            zone (Zone): Zone object

        Returns:
            list[Zone]: zones objects you can accses
        """

        try:
            return self.adjacency_map[zone]
        except KeyError as ecx:
            raise _errors.ElementNotFoundError(
                f'zone {zone.name} not found from get_neighbors()'
            ) from ecx

    def get_connection(self, zone_a: Zone, zone_b: Zone) -> Connection | None:
        """Get the connection between two zones.

        Args:
            zone_a (Zone): First zone
            zone_b (Zone): Second zone

        Returns:
            Connection: Connection object between the two zones
        """
        conn = next(
            (
                conn
                for conn in self.connections
                if conn.zone_a == zone_a and conn.zone_b == zone_b
            ), None)
        return conn

    def get_start_zone(self) -> Zone | None:
        """Get the start zone from the zones dictionary.

        Returns:
            Zone | None: The start zone if it exists, None otherwise
        """
        for zone in self.zones.values():
            if zone.role is RoleZone.STARTING:
                return zone
        return None
