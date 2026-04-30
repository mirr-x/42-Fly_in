# flyin/parser/__init__.py

'''Internal file for exporting validation functions.'''

from flyin.parser import _zone_validators, _connection_validator


__all__ = [
    '_validate_missing_key_val',
    '_get_role_and_validate_it',
    '_parse_zone_val',
    '_get_max_drones',
    '_validate_drones',
    '_parse_connec_vals'
]

_validate_missing_key_val = getattr(
    _zone_validators, '_validate_missing_key_val'
)
_get_role_and_validate_it = getattr(
    _zone_validators, '_get_role_and_validate_it'
)
_parse_zone_val = getattr(_zone_validators, '_parse_zone_values')
_get_max_drones = getattr(_zone_validators, '_get_max_drones')
_validate_drones = getattr(_zone_validators, '_validate_drones')
_parse_connec_vals = getattr(
    _connection_validator, '_parse_connec_vals'
)
