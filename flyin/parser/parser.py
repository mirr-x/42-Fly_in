"""This Module is used to handle All parsing in Fly-in project"""

from flyin._types import TypeZone, colorZone, RoleZone, Cord, MetaData
from flyin.models import Zone


class Parser:
    """Parses raw map files into zone and connection objects

        Attrbutes:
            file_path: full path to the map file
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.nb_drones = 0

    @staticmethod  # Err method
    def _validate_drones(val: str, line_n: int) -> int:
        try:
            v = int(val)
        except ValueError as exc:
            raise ValueError(
                f'Error: number of drones should be included in line {line_n}'
            ) from exc
        if v <= 0:
            raise ValueError(f'Error: drons cannot be <= 0 At line {line_n}')
        return v

    @staticmethod  # Err method
    def _validate_missing_key_val(s: str, line_n: int) -> list[str]:
        parts = s.split(':', 1)
        if len(parts) != 2:
            raise ValueError(f'Error: Missing colon seprator in line {line_n}')
        parts[0] = (parts[0].strip()).lower()
        parts[1] = (parts[1].strip()).lower()
        if not parts[0] or not parts[1]:
            raise ValueError(
                f'Error: missing format <key>: <val> in line {line_n}')
        return parts

    @staticmethod  # Err method
    def _validate_cords(x: str, y: str, line_n: int) -> Cord:
        try:
            v1 = int(x)
            v2 = int(y)
        except ValueError as exc:
            raise ValueError(
                f'Error: Cords should be included At line {line_n}'
            ) from exc
        if v1 <= 0 or v2 <= 0:
            raise ValueError(f'Error: Cords cannot be <= 0 At line {line_n}')
        return (v1, v2)

    @staticmethod
    def _get_corect_zone(_type: str, line_n: int) -> TypeZone:
        try:
            return TypeZone(_type)
        except ValueError as exc:
            raise ValueError(
                f'Error: Unknowun zone type At line {line_n}'
            ) from exc

    @staticmethod
    def _get_corect_color(color: str, line_n: int) -> colorZone:
        try:
            return colorZone(color)
        except ValueError as exc:
            raise ValueError(
                f'Error: Unknowun color type At line {line_n}'
            ) from exc

    @staticmethod
    def _validate_meta_data(val: str, line_n: int) -> MetaData:
        if not (val.startswith('[') and val.endswith(']')):
            raise ValueError(
                f'Error: ivalid metaData format At line {line_n}')  # *: HANDLE val ERR
        val = val[1:-1]
        if not val.strip():
            raise ValueError(f'Error: Empty metaData At line {line_n}')
        parts = val.split(" ")
        meta_data = {}
        for i in parts:
            key, _val = Parser._validate_missing_key_val(i, line_n)
            if key == 'zone':
                meta_data['zone'] = Parser._get_corect_zone(_val, line_n)
            elif key == 'color':
                meta_data['color'] = Parser._get_corect_color(_val, line_n)
            elif key == 'max_drones':
                meta_data['max_drones'] = Parser._validate_drones(_val, line_n)
            else:
                raise ValueError(f'Error: Unknowun metadata At line {line_n}')
        return meta_data

    @staticmethod  # Err method
    def _validate_hup_values(
                            val: str,
                            line_n: int
                        ) -> tuple[str, Cord, MetaData]:
        parts = val.split(' ', 3)  # <name> <x> <y> [metadata]
        if not 3 <= len(parts) <= 4:
            raise ValueError(
                'hub Error: invalid formal <name> <x> <y> '
                f'optional[metadata] At line {line_n}')
        name = parts[0].strip()
        cord = Parser._validate_cords(
                                parts[1].strip(),
                                parts[2].strip(),
                                line_n
                            )  # *: HANDLE val ERR
        meta_data = Parser._validate_meta_data(parts[3], line_n)
        return (name, cord, meta_data)

    @staticmethod
    def _get_corect_role(role: str, line_n: int) -> RoleZone:
        try:
            return RoleZone(role)
        except ValueError as exc:
            raise ValueError(
                f'Error: Unknowun role type At line {line_n}') from exc

    @staticmethod
    def _get_max_drones(meta_data: MetaData, line_n) -> int:
        max_drones_val = meta_data.get('max_drones', 1)
        if not isinstance(max_drones_val, int):
            raise ValueError(
                f'Error: invalid max_drones At line {line_n}'
            )
        return max_drones_val

    def parsing(self) -> None:
        hups = ('start_hub', 'end_hub', 'hub')
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line_n, line in enumerate(f, start=1):
                    striped = line.strip()
                    if not striped or striped.startswith('#'):
                        continue
                    key, val = self._validate_missing_key_val(striped, line_n)  # *: HANDLE FALIURE
                    if key == 'nb_drones':
                        self.nb_drones = self._validate_drones(val, line_n)  # *: HANDLE FALIURE
                    elif key in hups:
                        role = Parser._get_corect_role(key, line_n)
                        name, cord, meta_data = Parser._validate_hup_values(
                                                                        val,
                                                                        line_n
                                                                    )
                        max_drones_val = Parser._get_max_drones(
                                                        meta_data, line_n)
                        temp = Zone(
                            name=name,
                            cord=cord,
                            role=role,
                            max_drones=max_drones_val,
                            color=
                        )
        except OSError as exc:
            raise ValueError(f'Error: cannot open file {self.file_path}') from exc


