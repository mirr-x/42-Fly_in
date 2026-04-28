"""This file containe internal helper functions for validation Parsing"""

from flyin._types import TypeZone, ColorZone, RoleZone, Cord, MetaData
from flyin.parser import _errors


def _validate_drones(val: str, line_n: int) -> int:
    try:
        v = int(val)
    except ValueError as exc:
        raise _errors.InvalidValueError(
            f'number of drones should be included in line {line_n}'
        ) from exc
    if v <= 0:
        raise _errors.InvalidValueError(
            f'drons cannot be <= 0 At line {line_n}'
        )
    return v


def _validate_missing_key_val(s: str, sep: str, line_n: int) -> list[str]:
    parts = s.split(sep, 1)
    if len(parts) != 2:
        raise _errors.InvalidFormatError(
            f'Missing colon seprator in line {line_n}'
        )
    parts[0] = (parts[0].strip()).lower()
    parts[1] = (parts[1].strip()).lower()
    if not parts[0] or not parts[1]:
        raise _errors.InvalidFormatError(
            f'missing format <key>: <val> in line {line_n}')
    return parts


def _validate_cords(x: str, y: str, line_n: int) -> Cord:
    try:
        v1 = int(x)
        v2 = int(y)
    except ValueError as exc:
        raise _errors.InvalidCordsError(
            f'Cords should be included At line {line_n}'
        ) from exc
    if v1 < 0 or v2 < 0:
        raise _errors.InvalidCordsError(
            f'Cords cannot be >= 0 At line {line_n}'
        )
    return (v1, v2)


def _get_corect_zone(_type: str, line_n: int) -> TypeZone:
    try:
        return TypeZone(_type)
    except ValueError as exc:
        raise _errors.InvalidValueError(
            f'Unknowun zone type At line {line_n}'
        ) from exc


def _get_corect_color(color: str, line_n: int) -> ColorZone:
    try:
        return ColorZone(color)
    except ValueError as exc:
        raise _errors.InvalidValueError(
            f'Unknowun color type At line {line_n}'
        ) from exc


def _validate_meta_data(val: str, line_n: int) -> MetaData:
    if not (val.startswith('[') and val.endswith(']')):
        raise _errors.InvalidFormatError(
                'hub invalid formal <name> <x> <y> '
                f'optional[metadata] At line {line_n}')
    val = val[1:-1]
    if not val.strip():
        raise _errors.InvalidFormatError(f'Empty metaData At line {line_n}')
    parts = val.split(" ")
    meta_data = {}
    for i in parts:
        key, _val = _validate_missing_key_val(i, '=', line_n)
        if key == 'zone':
            meta_data['zone'] = _get_corect_zone(_val, line_n)
        elif key == 'color':
            meta_data['color'] = _get_corect_color(_val, line_n)
        elif key == 'max_drones':
            meta_data['max_drones'] = _validate_drones(_val, line_n)
        else:
            raise _errors.InvalidFormatError(
                f'Unknowun metadata At line {line_n}'
            )
    return meta_data


def _validate_hup_values(
                        val: str,
                        line_n: int
                    ) -> tuple[str, Cord, MetaData | None]:
    parts = val.split(' ', 3)  # <name> <x> <y> [metadata]
    l_parts = len(parts)
    if not 3 <= l_parts:
        raise _errors.InvalidFormatError(
            'hub invalid formal <name> <x> <y> '
            f'optional[metadata] At line {line_n}')
    name = parts[0].strip()
    if '-' in name:
        raise _errors.InvalidValueError('dashes forbiden in <name>')
    cord = _validate_cords(
                            parts[1].strip(),
                            parts[2].strip(),
                            line_n
                        )
    meta_data = None
    if l_parts == 4:
        meta_data = _validate_meta_data(parts[3], line_n)
    return (name, cord, meta_data)


def _get_corect_role(role: str, line_n: int) -> RoleZone:
    try:
        return RoleZone(role)
    except ValueError as exc:
        raise _errors.InvalidValueError(
            f'Unknowun role type At line {line_n}') from exc


def _get_max_drones(meta_data: MetaData, line_n) -> int:
    max_drones = meta_data.get('max_drones', 1)
    if not isinstance(max_drones, int):
        raise _errors.InvalidValueError(
            f'invalid max_drones At line {line_n}'
        )
    return max_drones
