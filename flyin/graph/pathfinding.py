"""Pathfinding module for computing shortest paths in a zone graph."""

from flyin.models.zone import Zone
from flyin.graph. graph import Graph


class PathFind:
    """Find the the shortest path using BFS algo"""

    def __init__(self, graph: Graph | None = None) -> None:
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

    def _bfs(self, start: Zone, end: Zone) -> list[Zone]:
        raise NotImplementedError
