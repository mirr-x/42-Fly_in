"""Simulator module for simulating drone movement."""

from flyin.models.drone import Drone
from flyin.graph.graph import Graph
from flyin.simulation.state import StateGraph
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

    def _all_delivered(self) -> bool:
        return all(map(lambda d: d.is_delivered(), self.drones))

    def _process_turn(self, counter: int) -> str:
        movements = []
        for drone in self.drones:
            next_zone = drone.next_zone()
            curr_conn = self.graph.get_connection(
                drone.current_zone, next_zone
            )
            if self.state.is_connection_occupied(curr_conn):
                continue
            if drone.is_delivered():
                continue
            if self.state.is_zone_occupied(next_zone):
                drone.set_status(DroneState.WAITING)
                continue
            # TODO: FIX alot of bugs here use ai  like free at end of turn 
            self.state.free_zone(drone.current_zone, drone)
            self.state.free_connection(curr_conn, drone)
            self.state.reserve_zone(next_zone, drone)
            self.state.reserve_connection(curr_conn, drone)
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

    def run(self) -> None:
        """Run the simulation."""

        counter = 1
        while not self._all_delivered():
            self._process_turn(counter)
            counter += 1
