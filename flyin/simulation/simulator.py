"""Simulator module for simulating drone movement."""

from flyin.models.drone import Drone
from flyin.graph.graph import Graph


class Simulator:
    """Manages drone simulation and movement on a graph.

    Attributes:
        dronnes (list[Drone]): list of drones in the map
        graph (Graph): current graph obj has all map info
    """

    def __init__(self, drones: list[Drone], graph: Graph) -> None:
        self.drones = drones
        self.graph = graph

    def _all_delivered(self) -> bool:
        return all(map(lambda d: d.is_delivered(), self.drones))

    def _process_turn(self, counter: int) -> str:
        movements = []
        for drone in self.drones:
            # TODO: well check if its valid for a drone to go to next zone
            # next_zone = drone.next_zone()
            # if next_zone
            # TODO: add new attr to zone andicate if zone occupide by drone
            drone.move_next()
            movements.append(
                f'{drone.id}-{drone.current_zone}'
            )
        return f'turn {counter}: ' + ' '.join(movements)

    def run(self) -> None:
        """Run the simulation."""

        counter = 1
        while not self._all_delivered():
            print(self._process_turn(counter))
            counter += 1
