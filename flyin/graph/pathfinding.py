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
        parent_map_reversed = dict(reversed(parent_map.items()))
        cur = goal
        for child, parent in parent_map_reversed.items():
            if child == cur:
                path.append(cur)
                cur = parent
        if cur == start:
            path.append(cur)
        path.reverse()
        return path

    def _bfs(self, start: Zone, end: Zone) -> Optional[dict[Zone, Zone]]:
        queue = collections.deque()
        visited = set()
        parent_map = {}
        path_found = False

        queue.append(start)
        visited.add(queue[0])
        while queue:
            parent = queue[0]
            queue.popleft()
            neighbors = self.graph.get_neighbors(parent)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parent_map[neighbor] = parent
                    if neighbor == end:
                        path_found = True
        if path_found:
            print("PATH FOUND!")
            print(parent_map)
        return parent_map if path_found else None

# TODO: check witch GPT if this code is valid and all is good and its good with changes happend in subject ?? to move to phase 3
