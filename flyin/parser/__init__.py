# flyin/parser/__init__.py

'''Internal file for exporting validation functions.'''

from flyin.parser import _zone_validators, _connection_validator


__all__ = [
    '_validate_missing_key_val',
    '_get_corect_role',
    '_validate_hup_val',
    '_get_max_drones',
    '_validate_drones',
    '_get_zone_a_and_b'
]

_validate_missing_key_val = getattr(
    _zone_validators, '_validate_missing_key_val'
)
_get_corect_role = getattr(_zone_validators, '_get_corect_role')
_validate_hup_val = getattr(_zone_validators, '_validate_hup_values')
_get_max_drones = getattr(_zone_validators, '_get_max_drones')
_validate_drones = getattr(_zone_validators, '_validate_drones')
_get_zone_a_and_b = getattr(_connection_validator, '_get_zone_a_and_b')
