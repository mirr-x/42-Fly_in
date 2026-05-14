"""Helper validation function for Connction Zones"""

from flyin.parser import _errors
from flyin._types import MetaData
from flyin.parser._zone_validators import _validate_missing_key_val
from flyin.models.zone import Zone
from flyin.models.connection import Connection


def _get_max_link_capacity(val: str, line_n: int) -> int:
    try:
        v = int(val)
    except ValueError as exc:
        raise _errors.InvalidValueError(
            f'max link capacity of drones should be included in line {line_n}'
        ) from exc
    if v <= 0:
        raise _errors.InvalidValueError(
            f'max link capacity cannot be <= 0 At line {line_n}'
        )
    return v


def _validate_meta_data_con(val: str, line_n: int) -> MetaData:
    if not (val.startswith('[') and val.endswith(']')):
        raise _errors.InvalidFormatError(
                'connction invalid format <zone_A>-<zone_B> '
                f'optional[metadata] At line {line_n}')
    val = val[1:-1]
    if not val.strip():
        raise _errors.InvalidFormatError(f'Empty metaData At line {line_n}')
    parts = val.split(" ")
    meta_data = {}
    for i in parts:
        key, _val = _validate_missing_key_val(i, '=', line_n)
        if key == 'max_link_capacity':
            meta_data['max_link_capacity'] = _get_max_link_capacity(
                _val, line_n)
        else:
            raise _errors.InvalidFormatError(
                f'Unknowun metadata At line {line_n}'
            )
    return meta_data


def _get_zone_a_and_b(val: str, line_n: int) -> tuple[str, str]:
    val = val.strip()
    parts = val.split('-')
    l_parts = len(parts)
    if l_parts != 2:
        raise _errors.InvalidFormatError(
            f'Missing dash seprator in line {line_n}'
        )
    parts[0] = parts[0].strip()
    parts[1] = parts[1].strip()
    if not parts[0] or not parts[1]:
        raise _errors.InvalidFormatError(
            f'missing format <zone_A>-<zone_B> in line {line_n}')
    return (parts[0], parts[1])


def _is_zone_a_b_exist(zone_a: str, zone_b: str, zones: list[Zone]) -> bool:
    zones_names = list(map(lambda a: a.name, zones))
    return zone_a in zones_names and zone_b in zones_names


def _is_connections_duplucate(
                                zone_a: str,
                                zone_b: str,
                                conn: list[Connection]
                            ) -> bool:
    connctions = [frozenset([i.zone_a.name, i.zone_b.name]) for i in conn]
    return frozenset([zone_a, zone_b]) in connctions


def _parse_connec_vals(
                        val: str,
                        zones: list[Zone],
                        connections: list[Connection],
                        line_n: int
                    ) -> tuple[Zone, Zone, MetaData | None]:
    parts = val.split(' ', maxsplit=1)  # <zone_A>-<zone_B> [metadata]
    l_parts = len(parts)
    if l_parts not in (1, 2):
        raise _errors.InvalidFormatError(
            'connction invalid formal zone_A>-<zone_B> '
            f'optional[metadata] At line {line_n}')
    zone_a, zone_b = _get_zone_a_and_b(parts[0].strip(), line_n)
    if zone_a == zone_b:
        raise _errors.DuplacateConnectionError(
            f'zone cant link to it self {zone_a}-{zone_b} At line {line_n}'
        )
    if not _is_zone_a_b_exist(zone_a, zone_b, zones):
        raise _errors.InvalidValueError(
            f'zones {zone_a}-{zone_b} dosent exist At line {line_n}!!'
        )
    if _is_connections_duplucate(zone_a, zone_b, connections):
        raise _errors.DuplacateConnectionError(
            f'duplucate connection detected {zone_a}-{zone_b} At line {line_n}'
        )
    meta_data = None
    if l_parts == 2:
        meta_data = _validate_meta_data_con(parts[1].strip(), line_n)
    zone_obj_a = next(filter(lambda a: a if a.name == zone_a else None, zones))
    zone_obj_b = next(filter(lambda a: a if a.name == zone_b else None, zones))
    return (zone_obj_a, zone_obj_b, meta_data)
