"""Pathfinding module for computing shortest paths in a zone graph."""

from flyin.models.zone import Zone
from flyin.graph. graph import Graph
import collections


class FindPath:
    """Find the the shortest path using BFS algo"""

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    # TODO: now i will desing my own find_path()
    def find_path(self, start: Zone, end: Zone) -> list[Zone]:
        """Return the shortest path from start to end.

        Args:
            start: Starting zone.
            end: Destination zone.

        Returns:
            A list of zones representing the shortest path.
        """
        raise NotImplementedError

    # def _reconstruct_path(parent_map, start, goal) ->

    def _bfs(self, start: Zone, end: Zone) -> dict[Zone, list[Zone]] | None:
        queue = collections.deque()
        visited = set()
        parent_map = collections.defaultdict(list)
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
                    parent_map[parent].append(neighbor)
                    if neighbor == end:
                        path_found = True
        if path_found:
            print("PATH FOUND!")
            print(dict(parent_map))
        else:
            print("PATH NOT VALID!!")
        return dict(parent_map) if path_found else None
