"""Helper functions for renderer: drone grouping and positioning."""

import math
from typing import Dict, List, Tuple

from flyin.models.drone import Drone
from flyin.models.zone import Zone
from flyin.models.connection import Connection
from flyin.visual.graph_layout import GraphLayout

ZoneOrConn = Zone | Connection


def get_drone_base_position(
    layout: GraphLayout,
    drone: Drone,
) -> Tuple[float, float]:
    """Return base screen position for a drone."""

    zone = drone.current_zone
    if isinstance(zone, Zone):
        return layout.to_screen(zone)
    if isinstance(zone, Connection):
        x1, y1 = layout.to_screen(zone.zone_a)
        x2, y2 = layout.to_screen(zone.zone_b)
        return (x1 + x2) / 2, (y1 + y2) / 2
    return 0.0, 0.0


def get_drone_offset_position(
    layout: GraphLayout,
    drone: Drone,
    drones_in_group: List[Drone],
    radius: float = 12.0,
) -> Tuple[float, float]:
    """Return a circular offset position for a drone in a crowded spot."""

    if len(drones_in_group) <= 1:
        return get_drone_base_position(layout, drone)

    try:
        index = drones_in_group.index(drone)
    except ValueError:
        index = 0

    angle = index * (2 * math.pi / len(drones_in_group))
    base_x, base_y = get_drone_base_position(layout, drone)
    offset_x = math.cos(angle) * radius
    offset_y = math.sin(angle) * radius
    return base_x + offset_x, base_y + offset_y


def get_drone_positions(
    layout: GraphLayout,
    drones: List[Drone],
) -> Dict[str, Tuple[float, float]]:
    """Return current screen positions for all drones (with offsets)."""

    grouped_drones: Dict[ZoneOrConn, List[Drone]] = {}
    for drone in drones:
        zone = drone.current_zone
        if isinstance(zone, (Zone, Connection)):
            grouped_drones.setdefault(zone, []).append(drone)

    for drones_in_group in grouped_drones.values():
        drones_in_group.sort(key=lambda drone: drone.id)

    positions: Dict[str, Tuple[float, float]] = {}
    for drone in drones:
        zone = drone.current_zone
        if not isinstance(zone, (Zone, Connection)):
            continue
        drones_in_group = grouped_drones[zone]
        positions[drone.id] = get_drone_offset_position(
            layout, drone, drones_in_group
        )

    return positions
