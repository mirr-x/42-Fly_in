"""This module is used t Excute and run the Fly-in project

    Usage:
        python -m flyin.main <map_file>

    Argument:
            <map_file>: path of the map dron

"""

import sys
import logging
from flyin.parser import _errors
from flyin.parser.parser import Parser
from flyin.graph.graph import Graph
from flyin.models.zone import Zone
from flyin.models.connection import Connection
from flyin.pathfinding.dijkstra import Dijkstra


def print_zones_and_connections(
    zones: dict[str, Zone],
    connections: list[Connection]
) -> None:
    """Display the Zones and Conctions

    Args:
        zones (dict[str, Zone]): zones objects in map
        connections (list[Connection]): connections objects in map
    """

    if zones:
        print('Zones loaded:')
        for zone in zones.values():
            print(f'    - {zone.name}')
    if connections:
        print('\nConnections:')
        for conn in connections:
            print(f'    - {conn.zone_a.name} ↔ {conn.zone_b.name}')
    print()


def main() -> None:
    """ Entry point our app """

    logging.info('Logging Started\n')
    if len(sys.argv) < 2:
        logging.warning('Usage: python -m flyin.main <map_file>')
        sys.exit(1)

    try:
        parsed = Parser(sys.argv[1], map_graph=Graph())
        parsed.parsing()
        print_zones_and_connections(
            parsed.graph.zones,
            parsed.graph.connections
        )
        # finding path phase
        find_path = Dijkstra(parsed.graph)
        shortest_path = find_path.find_shortest_path(
            parsed.start_zone,
            parsed.end_zone
        )
        print(shortest_path)
    except _errors.InvalidPathError as exc:
        logging.warning('Path Error: %s', exc)
    except _errors.InsaneError as exc:
        logging.critical('Graph Error: %s', exc)
    except _errors.ParserError as exc:
        logging.error('Map file error: %s (cause: %s)', exc, exc.__cause__)
    logging.info('Parsing successful')


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    try:
        main()
    except KeyboardInterrupt:
        logging.exception('Execution interrupted by user')
        sys.exit(130)
    # except Exception as unexpected_error:  # [broad-exception-caught]
    #     logging.exception('Unexpected error: %s', unexpected_error)
