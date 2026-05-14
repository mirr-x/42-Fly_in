"""Implements Dijkstra's algorithm for finding shortest paths in a graph."""

import heapq
import itertools


from flyin.models.zone import Zone
from flyin.graph.graph import Graph
from flyin.parser import _errors
from flyin._types._enums import ZoneCategory


class Dijkstra:
    """Finds the lowest category path from a src node to all other nodes or to
    a specific dest node."""

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def run(self, start: Zone, end: Zone) -> list[Zone]:
        """Return the shortest costing path from start to end.

        Args:
            start: Starting zone.
            end: Destination zone.

        Returns:
            A list of zones representing the shortest path.
        """

        if start == end:
            return [start]
        _map = self.find_all_posible_paths(start, end)
        if _map is None:
            raise _errors.InvalidPathError('no Path couldnt be found !!!')
        self.graph.dijkstra_paths = _map
        return _map

    def _get_neighbors_and_sort(self, zone: Zone) -> list[Zone]:
        zones = self.graph.get_neighbors(zone)
        return list(
            sorted(
                zones,
                key=lambda a: 0 if a.category is ZoneCategory.PRIORITY else 1
            )
        )

    def _valid_path_add(
            self,
            paths_results: list[tuple[int, list[Zone]]],
            cur_cost: int,
            cur_path: list[Zone]
            ) -> bool:
        if paths_results and cur_cost != paths_results[0][0]:
            return False
        paths_results.append((cur_cost, cur_path))
        return True

    def find_all_posible_paths(
            self, start: Zone, end: Zone
            ) -> list[tuple[int, list[Zone]]] | None:
        """Compute shortest path distances using Dijkstra's algorithm.

        Args:
            start (Zone): start zone obj in map
            end (Zone): end zone obj in map

        Returns:
            list[Zone] | None: list of possible path
        """

        counter = itertools.count()
        paths_results: list[tuple[int, list[Zone]]] = []
        pqueue: list[tuple[int, int, list[Zone]]] = [
            (0, next(counter), [start])
        ]
        path_found = False
        l_drone = len(self.graph.drones)
        while pqueue and l_drone != 0:
            cur_cost, _, cur_path = heapq.heappop(pqueue)

            if cur_path[-1] == end:
                if not self._valid_path_add(paths_results, cur_cost, cur_path):
                    break
                path_found = True
                l_drone -= 1
                continue

            neighbors = self._get_neighbors_and_sort(cur_path[-1])
            for neighbor in neighbors:
                if neighbor.is_blocked():
                    continue
                if neighbor not in cur_path:
                    new_cost = cur_cost + neighbor.get_movement_cost()
                    heapq.heappush(
                        pqueue,
                        (new_cost, next(counter), cur_path + [neighbor])
                    )
        return paths_results if path_found else None
