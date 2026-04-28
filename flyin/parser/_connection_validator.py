"""Helper validation function for Connction Zones"""

from flyin.parser import _errors


def _get_zone_a_and_b(val: str, line_n: int) -> list[str]: # TODO:  forgrt to include meta data nex time inpire from _validate_hup_values() will help
    val = val.strip()
    parts = val.split('-')
    l_parts = len(parts)
    if l_parts != 2:
        raise _errors.InvalidFormatError(
            f'Missing dash seprator in line {line_n}'
        )
    parts[0] = (parts[0].strip()).lower()
    parts[1] = (parts[1].strip()).lower()
    if not parts[0] or not parts[1]:
        raise _errors.InvalidFormatError(
            f'missing format <zone_A>-<zone_B> in line {line_n}')
    return parts
