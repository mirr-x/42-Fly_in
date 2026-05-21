"""Simulator module for simulating drone movement."""

from flyin.parser import _errors
from flyin.models.drone import Drone
from flyin.models.connection import Connection
from flyin.models.zone import Zone
from flyin.graph.graph import Graph
from .state import StateGraph
from flyin._types._enums import DroneState


class Simulator:
    """Manages drone simulation and movement on a graph.

    Attributes:
        dronnes (list[Drone]): list of drones in the map
        graph (Graph): current graph obj has all map info
    """

    def __init__(self, drones: list[Drone], graph: Graph) -> None:
        self.drones = drones
        self.graph = graph
        self.state = StateGraph()
        self._init_all_drones_at_start_zone()
        self._assign_paths_to_drones(self.drones)

    def _all_delivered(self) -> bool:
        return all(map(lambda d: d.is_delivered(), self.drones))

    def _get_correct_cur_conn(
            self, drone: Drone, next_zone: Zone | Connection | None
            ) -> Connection | None:
        if drone.state == DroneState.IN_TRANSIT:
            if isinstance(drone.current_zone, Connection):
                return drone.current_zone
            return None
        if isinstance(next_zone, Connection):
            return next_zone
        if isinstance(drone.current_zone, Zone) and isinstance(
            next_zone, Zone
        ):
            return self.graph.get_connection(drone.current_zone, next_zone)
        return None

    def _process_turn(self, counter: int) -> None:
        movements = []
        for drone in self.drones:
            if drone.is_delivered():
                continue
            next_zone = drone.next_zone(self.graph)
            cur_conn = self._get_correct_cur_conn(drone, next_zone)
            if self.state.is_connection_occupied(cur_conn):
                continue
            if self.state.is_zone_occupied(next_zone):
                drone.set_status(DroneState.WAITING)
                continue
            self.state.free_zone(drone.current_zone, drone)
            self.state.reserve_zone(next_zone, drone)
            self.state.reserve_connection(cur_conn, drone)
            drone.move_next(next_zone)

            if next_zone:
                movements.append(
                    f'{drone.id}-{drone.current_zone}'
                )
        if movements:
            print(f'turn {counter}: ' + ' '.join(movements))

    def _init_all_drones_at_start_zone(self) -> None:
        start_zone = self.graph.get_start_zone()
        for drone in self.drones:
            self.state.reserve_zone(start_zone, drone)

    def _assign_paths_to_drones(self, drones: list[Drone]) -> None:
        """Assign precomputed shortest paths to each drone."""

        paths = self.graph.dijkstra_paths
        if paths is None:
            raise _errors.InvalidPathError('No path data available')
        l_paths = len(paths)
        i = 0
        for dron in drones:
            if i == l_paths:
                i = 0
            dron.path = paths[i][1]
            i += 1

    def run(self) -> None:
        """Run the simulation."""

        counter = 1
        while not self._all_delivered():
            self._process_turn(counter)
            self.state.reset_connection_usage()
            counter += 1
