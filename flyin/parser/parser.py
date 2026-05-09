"""This Module is used to handle All parsing in Fly-in project"""


from flyin.models.zone import Zone
from flyin.models.connection import Connection
from flyin.graph.graph import Graph
from flyin.models.drone import Drone
from flyin.parser import _errors
from flyin._types import ZoneCategory, RoleZone, MapsTool
from flyin.parser import (
    _validate_missing_key_val,
    _get_role_and_validate_it,
    _parse_zone_val,
    _get_max_drones,
    _validate_drones,
    _parse_connec_vals
)


class Parser:
    """Parses raw map files into zone and connection objects

    Attrbutes:
        file_path: full path to the map file
        graph: map graph for the drones
    """

    def __init__(self, file_path: str, map_graph: Graph) -> None:
        self.file_path = file_path
        self.graph = map_graph
        self.nb_drones = 0
        self.start_zone: Zone
        self.end_zone: Zone

    def creat_drones(self) -> None:
        """Create drones for the graph based on the number specified."""
        self.graph.drones = list(
            map(
                lambda i: Drone(
                    _id=i + 1,
                    current_zone=self.start_zone,
                    path=self.graph.dijkstra_path
                ),
                range(self.nb_drones)
            )
        )

    def _handle_zones(self, key: str, val: str, line_n) -> None:
        list_zones = list(self.graph.zones.values())
        role = _get_role_and_validate_it(key, list_zones, line_n)
        name, cord, meta_data = _parse_zone_val(val, list_zones, line_n)
        max_drones, color, category = 1, None, ZoneCategory.NORMAL
        if meta_data:
            max_drones = _get_max_drones(meta_data, line_n)
            color = meta_data.get('color', None)
            category = meta_data.get('category', ZoneCategory.NORMAL)
        temp_zone = Zone(
            name=name,
            cord=cord,
            role=role,
            max_drones=max_drones,
            color=color,
            category=category
        )
        self.graph.add_zone(temp_zone)

    def _handle_connctions(self, val: str, line_n) -> None:
        zones = list(self.graph.zones.values())
        connec = self.graph.connections
        zone_a, zone_b, data = _parse_connec_vals(val, zones, connec, line_n)
        max_capacity = 1
        if data:
            max_capacity = data.get('max_link_capacity', 1)
        tmp_conction = Connection(zone_a, zone_b, max_capacity)
        self.graph.add_connection(tmp_conction)

    def parsing(self) -> None:
        """Parse the map file, validate entries, and extract map data.

        Raises:
            _errors.ParserFileNotFoundError: raised when file cannot be opened
        """

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line_n, line in enumerate(f, start=1):
                    striped = line.strip()
                    if not striped or striped.startswith('#'):
                        continue
                    key, val = _validate_missing_key_val(striped, ':', line_n)
                    if key == 'nb_drones':
                        self.nb_drones = _validate_drones(val, line_n)
                    elif key in RoleZone:
                        self._handle_zones(key, val, line_n)
                    elif key == MapsTool.CONNECTION.value:
                        self._handle_connctions(val, line_n)
                    else:
                        raise _errors.InvalidFormatError(
                            f'Unknowun key At line {line_n}')
                self.start_zone = self.graph.zones['start']
                self.end_zone = self.graph.zones.get('goal')  # type: ignore
                if self.end_zone is None:
                    self.end_zone = self.graph.zones['impossible_goal']
        except OSError as exc:
            raise _errors.ParserFileNotFoundError(
                f'cannot open file {self.file_path}'
            ) from exc
        except KeyError as exc:
            raise _errors.ElementNotFoundError(
                'start_hub/end_hub not found'
            ) from exc
        else:
            self.graph.build_adjacency()
