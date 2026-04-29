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
            print(f'    - {conn.zone_a} ↔ {conn.zone_b}')
    print()


def main() -> None:
    """ Entry point our app """

    logging.info('Logging Started\n')
    if len(sys.argv) < 2:
        logging.warning('Usage: python -m flyin.main <map_file>')
        sys.exit(1)

    try:
        pars = Parser(sys.argv[1], map_graph=Graph())
        pars.parsing()
        print_zones_and_connections(pars.graph.zones, pars.graph.connection)
        # import json  ##* delet us
        # with open('mp.json', 'w', encoding='utf-8') as f:   ##*
        #     a = {k: v.__repr__() for k, v in pars.graph.zones.items()}
            
        #     b = {f'{i.zone_a}-{i.zone_b}': i.__repr__() for i in pars.graph.connection}
        #     a.update(b)
        #     json.dump(a, f, indent=4)  ##*
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
