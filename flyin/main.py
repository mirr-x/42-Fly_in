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


def main() -> None:
    """ Entry point our app """

    logging.info('Logging Started\n')
    if len(sys.argv) < 2:
        logging.warning('Usage: python -m flyin.main <map_file>')
        sys.exit(1)

    try:
        pars = Parser(sys.argv[1], map_graph=Graph())
        pars.parsing()
        # import json  ##* delet us
        # with open('mp.json', 'w', encoding='utf-8') as f:   ##*
        #     a = list(map(lambda z: z.__repr__(), pars.graph.zones.values()))
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
