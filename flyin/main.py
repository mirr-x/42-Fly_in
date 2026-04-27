"""This module is used t Excute and run the Fly-in project

    Usage:
        python -m flyin.main <map_file>

    Argument:
            <map_file>: path of the map dron

"""

import sys
from flyin.parser.parser import Parser
from flyin.parser import (
    InvalidFormatError,
    InvalidValueError,
    InvalidCordsError,
    ParserFileNotFoundError,
    ParserError
)



def main() -> None:
    """ Entry point our app """

    print(sys.argv[3])  # delete me
    try:
        parsing = Parser(sys.argv[3])
    except 



if __name__ == "__main__":

    try:
        main()
    except Exception as e:
        print('Unhandled exception in main %s', e)
        sys.exit(1)
