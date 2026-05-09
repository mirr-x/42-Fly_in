"""Pathfinding module for computing shortest paths in a zone graph."""

from typing import Optional

from flyin.models.zone import Zone
from flyin.graph.graph import Graph
from flyin.parser import _errors
import collections


class FindPath:
    """Find the the shortest path using BFS algo"""

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def find_shortest_path(self, start: Zone, end: Zone) -> list[Zone]:
        """Return the shortest path from start to end.

        Args:
            start: Starting zone.
            end: Destination zone.

        Returns:
            A list of zones representing the shortest path.
        """
        if start == end:
            return [start]
        parent_map = self._bfs(start, end)
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
        return path

    def _bfs(self, start: Zone, end: Zone) -> Optional[dict[Zone, Zone]]:
        queue = collections.deque()
        visited = set()
        parent_map = {}
        path_found = False

        queue.append(start)
        visited.add(start)
        while queue:
            current = queue.popleft()
            neighbors = self.graph.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parent_map[neighbor] = current
                    if neighbor == end:
                        path_found = True
                        break
            if path_found:
                break
        return parent_map if path_found else None
