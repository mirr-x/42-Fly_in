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

    def find_shortest_path(self, start: Zone, end: Zone) -> list[Zone]:
        """Return the shortest costing path from start to end.

        Args:
            start: Starting zone.
            end: Destination zone.

        Returns:
            A list of zones representing the shortest path.
        """
        if start == end:
            return [start]
        parent_map = self.dijkstra(start, end)
        if parent_map is None:
            raise _errors.InvalidPathError('Path couldnt be find !!!')
        return self._reconstruct_path(parent_map, start, end)

    def _reconstruct_path(
        self,
        parent_map: dict[Zone, Zone],
        start: Zone,
        goal: Zone,
    ) -> list[Zone]:
        path = []
        cur = goal
        while cur != start:
            path.append(cur)
            cur = parent_map[cur]
        path.append(start)
        path.reverse()
        self.graph.dijkstra_path = path
        return path

    def _get_neighbors_and_sort(self, zone: Zone) -> list[Zone]:
        zones = self.graph.get_neighbors(zone)
        return list(
            sorted(
                zones,
                key=lambda a: 0 if a.category is ZoneCategory.PRIORITY else 1
            )
        )

    def dijkstra(self, start: Zone, end: Zone) -> dict[Zone, Zone] | None:
        """Compute shortest path distances using Dijkstra's algorithm."""

        counter = itertools.count()
        pqueue = [(start.get_movement_cost(), next(counter), start)]
        distances = {zone: float('inf') for zone in self.graph.zones.values()}
        parent_map = {}
        path_found = False

        distances[start] = 0
        while pqueue:
            cur_cost, _, cur = heapq.heappop(pqueue)

            if cur_cost > distances[cur]:
                continue

            if cur == end:
                path_found = True
                break

            neighbors = self._get_neighbors_and_sort(cur)
            for neighbor in neighbors:
                if neighbor.is_blocked():
                    continue
                new_cost = cur_cost + neighbor.get_movement_cost()
                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    parent_map[neighbor] = cur
                    heapq.heappush(
                        pqueue,
                        (distances[neighbor], next(counter), neighbor)
                    )
        return parent_map if path_found else None
