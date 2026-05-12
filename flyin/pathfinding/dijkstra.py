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
        _map = self.dijkstra(start, end)
        if _map is None:
            raise _errors.InvalidPathError('Path couldnt be find !!!')
        self.graph.dijkstra_path = _map
        return _map
        # return self._reconstruct_path(parent_map, start, end)

    # def _reconstruct_path(
    #     self,
    #     parent_map: dict[Zone, Zone],
    #     start: Zone,
    #     goal: Zone,
    # ) -> list[Zone]:
    #     path = []
    #     cur = goal
    #     while cur != start:
    #         path.append(cur)
    #         cur = parent_map[cur]
    #     path.append(start)
    #     path.reverse()
    #     self.graph.dijkstra_path = path
    #     return path

    def _get_neighbors_and_sort(self, zone: Zone) -> list[Zone]:
        zones = self.graph.get_neighbors(zone)
        return list(
            sorted(
                zones,
                key=lambda a: 0 if a.category is ZoneCategory.PRIORITY else 1
            )
        )

    # TODO: rewrite djikstra algo to get all posible paths
    def dijkstra(self, start: Zone, end: Zone) -> list[Zone] | None:
        """Compute shortest path distances using Dijkstra's algorithm."""

        counter = itertools.count()
        paths_ruselts: list[tuple[int, list[Zone]]] = []
        pqueue: list[tuple[int, int, list[Zone]]] = [
            (0, next(counter), [start])
        ]
        distances = {zone: float('inf') for zone in self.graph.zones.values()}
        path_found = False

        distances[start] = 0
        while pqueue:
            cur_cost, _, cur_path = heapq.heappop(pqueue)

            if cur_cost > distances[cur_path[-1]]:
                continue

            if cur_path[-1] == end:  # cur_path[-1]
                path_found = True
                paths_ruselts.append((cur_cost, cur_path))
                break

            neighbors = self._get_neighbors_and_sort(cur_path[-1])
            for neighbor in neighbors:
                if neighbor.is_blocked():
                    continue
                if neighbor not in cur_path:
                    new_cost = cur_cost + neighbor.get_movement_cost()
                    distances[neighbor] = new_cost
                    heapq.heappush(
                        pqueue,
                        (new_cost, next(counter), cur_path + [neighbor])
                    )
        return paths_ruselts[0][1] if path_found else None
