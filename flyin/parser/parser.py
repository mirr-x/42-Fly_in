"""This Module is used to handle All parsing in Fly-in project"""


from flyin.models import Zone
from flyin.graph import Graph
from flyin.parser import _errors
from flyin._types import TypeZone, RoleZone, MapsTool
from flyin.parser import (
    _validate_missing_key_val,
    _get_corect_role,
    _validate_hup_val,
    _get_max_drones,
    _validate_drones,
    _get_zone_a_and_b
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
                        role = _get_corect_role(key, line_n)
                        name, cord, meta_data = _validate_hup_val(val, line_n)
                        max_drones, color, _type = None, None, TypeZone.NORMAL
                        if meta_data:
                            max_drones = _get_max_drones(meta_data, line_n)
                            color = meta_data.get('color', None)
                            _type = meta_data.get('type', TypeZone.NORMAL)
                        temp_zone = Zone(
                            name=name,
                            cord=cord,
                            role=role,
                            max_drones=max_drones,
                            color=color,
                            _type=_type
                        )
                        self.graph.add_zone(temp_zone)
                    elif key == MapsTool.CONNECTION.value:
                        zone_a, zone_b = _get_zone_a_and_b(val, line_n)
                        # TODO: CONTIMIUE VALIDATING THIS connction
                        # temp_connection = Connection(zone_a, zone_b)
                    else:
                        raise _errors.InvalidFormatError(
                            f'Unknowun key At line {line_n}')
        except OSError as exc:
            raise _errors.ParserFileNotFoundError(
                f'cannot open file {self.file_path}'
            ) from exc
