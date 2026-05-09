from flyin.models.zone import Zone


def can_move_to_zone() -> None:
    pass


def is_zone_full() -> None:
    pass


def can_use_connection() -> None:
    pass


def movement_cost(zone: Zone) -> float:
    """Gets turn cost"""
    return zone.get_movement_cost()
