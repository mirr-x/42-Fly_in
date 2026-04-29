"""Graph Module is the Module gonna store all data of the map and map itself"""

from flyin.models import Zone, Connection
from flyin.parser import _errors


class Graph:
    """Graph class store all info of the map"""

    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connection: list[Connection] = []

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
