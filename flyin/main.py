"""_summary_
    This module is used t Excute and run the Fly-in project

    Usage:
        python -m flyin.main <map_file>

    Argument:
            <map_file>: path of the map dron

"""
import sys
import logging

from flyin.parser.parser import Parser


def main() -> None:
    """ Entry point our app """
    logging.info('Logging Started')

    print(sys.argv[3])  # delete me
    parsing = Parser(sys.argv[3])



if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    try:
        main()
    except Exception as e:
        logging.exception('Unhandled exception in main %s', e)
        sys.exit(1)
