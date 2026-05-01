"""Graph Module is the Module gonna store all data of the map and map itself"""

from flyin.models import Zone, Connection
from flyin.parser import _errors


class Graph:
    """Graph class store all info of the map"""

    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connection: list[Connection] = []
        self.adjacency_map: dict[Zone, list[Zone]] = {}

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
        self.connection.append(connection)

    def _build_adjacency(self) -> None:
        for zone in self.zones.values():
            self.adjacency_map[zone] = []
        # 2 TODO: Then loop thou connections then linking start : needs Fixing totaly wrong
        for conn in self.connection:
            if conn.zone_b not in self.adjacency_map[conn.zone_a]:
                self.adjacency_map[conn.zone_a].append(conn.zone_b)
            if conn.zone_a not in self.adjacency_map[conn.zone_b]:
                self.adjacency_map[conn.zone_b].append(conn.zone_a)
        print(self.adjacency_map)
