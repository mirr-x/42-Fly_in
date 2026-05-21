"""Module for managing simulation state and drone zone allocation."""

from collections import defaultdict

from flyin.models.zone import Zone
from flyin.models.drone import Drone
from flyin.models.connection import Connection


class StateGraph:
    """Track occupied zones and connection usage in the simulation."""

    def __init__(self) -> None:
        self.occupied_zones: defaultdict[Zone | Connection, list[Drone]] = (
            defaultdict(list)
        )
        self.connection_usage: defaultdict[Connection, list[Drone]] = (
            defaultdict(list)
        )

    def reserve_zone(
            self, zone: Zone | None | Connection, drone: Drone
            ) -> bool:
        """reserve a zone by a drone

        Args:
            zone (Zone): zone from the map
            drone (Drone): drone from the map

        Returns:
            bool: return true after reserving the zone
        """

        if not zone:
            return False
        if zone not in self.occupied_zones:
            self.occupied_zones[zone] = []
        self.occupied_zones[zone].append(drone)
        return True

    def is_zone_occupied(self, zone: Zone | Connection | None) -> bool:
        """Validate if zone is free to use or not

        Args:
            zone (Zone): zone from the map

        Returns:
            bool: True if zone is occupied, False zone not found or not free
        """

        if zone is None:
            return False
        drones_in_zone = self.occupied_zones.get(zone, None)
        if drones_in_zone:
            if isinstance(zone, Connection):
                if len(drones_in_zone) >= zone.max_link_capacity:
                    return True
            if (isinstance(zone, Zone) and
                    len(drones_in_zone) >= zone.max_drones):
                return True
        return False

    def free_zone(self, zone: Zone | Connection, drone: Drone) -> bool:
        """Remove a drone from a zone.

        Args:
            zone (Zone): zone from the map
            drone (Drone): drone from the map

        Returns:
            bool: True if the drone was removed successfully, False otherwise
        """

        drones = self.occupied_zones.get(zone)
        if not drones or drone not in drones:
            return False
        drones.remove(drone)
        return True

    def reserve_connection(
            self,
            connection: Connection | None,
            drone: Drone
            ) -> bool:
        """reserve a connection by a drone

        Args:
            connection (Connection): connection from the map between two zones
            drone (Drone): drone from the map

        Returns:
            bool: return true after reserving the zone
        """

        if not connection:
            return False
        if connection not in self.connection_usage:
            self.connection_usage[connection] = []
        self.connection_usage[connection].append(drone)
        return True

    def is_connection_occupied(self, connection: Connection | None) -> bool:
        """Validate if connection is free to use or not

        Args:
            connection (Connection): connection from the map

        Returns:
            bool: True if connection is used, False connection not free
        """

        if connection is None:
            return False
        drones_in_zone = self.connection_usage.get(connection)
        if drones_in_zone:
            if len(drones_in_zone) >= connection.max_link_capacity:
                return True
        return False

    def reset_connection_usage(self) -> None:
        """Reset all connection usages."""
        self.connection_usage = defaultdict(list)
