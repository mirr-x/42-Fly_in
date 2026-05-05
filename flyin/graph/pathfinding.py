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

    def _bfs(self, start: Zone, end: Zone) -> None:  # -> list[Zone]
        queue = collections.deque()
        visited = set()
        parent_map = {}

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
                    parent_map[parent] = neighbor
                    if neighbor == end:
                        print("PATH FOUND!")
                        print(parent_map)
                        exit(1)
    # TODO: Next you will dubug all this if all good an working on all maps and you will implemnt and skipp dead end and so an
    # so we can finish phase 3


# {
#     start: [waypoint1],
#     waypoint1: [start, waypoint2],
#     waypoint2: [waypoint1, goal],
#     goal: [waypoint2]
# }
#
# queue = {start}
# visited = {start}
# map = {}
#
# loop 1:
        # queue = {waypoint1}
        # visited = {start}
        # neighbors = [waypoint1]
        # map = {start -> waypoint1}
# loop 2:
        # queue = {waypoint2}
        # visited = {start, waypoint1}
        # neighbors = [start, waypoint2]
        # map = {start -> waypoint1,
        #        waypoint1 -> waypoint2}
# loop 3:
        # queue = {goal}
        # visited = {start, waypoint1, goal}
        # neighbors = [waypoint1, goal]
        # map = {start -> waypoint1,
        #        waypoint1 -> waypoint2
        #        waypoint2-> goal}
