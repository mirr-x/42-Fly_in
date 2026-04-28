"""Graph Module is the Module gonna store all data of the map and map itself"""

from flyin.models import Zone
from flyin.parser import _errors


class Graph:
    """Graph class store all info of the map"""

    def __init__(self) -> None:
        self.zones = {}

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
