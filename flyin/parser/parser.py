"""This Module is used to handle All parsing in Fly-in project"""

import os
import sys

class Parser:
    """Parses raw map files into zone and connection objects

        Attrbutes:
            file_path: full path to the map file
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.nb_drones = 0

    @staticmethod # Err method
    def _validate_drones(val: str, line_n: int) -> None:
        try:
            v = int(val)
        except ValueError:
            raise ValueError(f'Error: number of drones should be included in line {line_n}')
        if v <= 0:
            raise ValueError(f'Error: drons cannot be <= 0 At line {line_n}')

    @staticmethod # Err method
    def _validate_missing_key_val(s: str, line_n: int) -> list[str]:
        parts = s.split(':', 1)
        if len(parts) != 2:
            raise ValueError(f'Error: Missing colon seprator in line {line_n}')
        parts[0] = parts[0].strip()
        parts[1] = parts[1].strip()
        if not parts[0] or not parts[1]:
            raise ValueError(f'Error: missing format <key>: <val> in line {line_n}')
        return parts

    @staticmethod # Err method
    def _validate_cords(x: str, y: str, line_n: int) -> None:
        try:
            v1 = int(x)
            v2 = int(y)
        except ValueError:
            raise ValueError(f'Error: Cords should be included in line {line_n}')
        if v1 <= 0 or v2:
            raise ValueError(f'Error: Cords cannot be <= 0 At line {line_n}')

    @staticmethod # Err method
    def _validate_hup_values(val: str, line_n: int) -> None:
        parts = val.split(' ', 3) # <name> <x> <y> [metadata]
        if not (3 <= len(parts) <= 4):
            raise ValueError(f'Error: hub invalid formal <name> <x> <y> optional[metadata] At line {line_n}')
        Parser._validate_cords(parts[1], parts[2], line_n) # TODO: Handle val ERR
        


    def parsing(self) -> None:
        try:
            with open(self.file_path, 'r') as f:
                for line_n, line in enumerate(f):
                    striped = line.strip()
                    if not striped.startswith('#'):
                        key, val = self._validate_missing_key_val(striped, line_n) # TODO: HANDLE FALIURE
                        if key == 'nb_drones':
                            self._validate_drones(val, line_n) # TODO: HANDLE FALIURE
                            self.nb_drones = int(val)
                        elif key == 'start_hub' or key == 'end_hub' or key == 'hub':
                            # TODO: now we jump to zone file cause we have detected an zone
                            # parts = val.split(' ', 3)
                            # TODO: validate Fisrt then creat Zone then CONTINUE