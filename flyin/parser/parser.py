"""_summary_
    This Module is used to handle All parsing in Fly-in project
"""
import os
import sys

class Parser:
    """_summary_
        Parses raw map files into zone and connection objects

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
            raise ValueError(f"Error: number of drones should be included in line {line_n}")
        if v <= 0:
                raise ValueError(f"Error: drons cannot be 0 in line {line_n}")

    @staticmethod # Err method
    def _validate_spliting(s: str, line_n: int) -> list[str]:
        rus = s.split(":", 1)
        if len(rus) != 2:
            raise ValueError(f"Error: Missing colon seprator in line {line_n}")
        if not rus[0] or not rus[1]:
            raise ValueError(f"Error: missing format <key>: <val> in line {line_n}")
        return rus

    def parsing(self) -> None:
        try:
            with open(self.file_path, "r") as f:
                for line_n, line in enumerate(f):
                    striped = line.strip()
                    if not striped.startswith("#"):
                        key, val = self._validate_spliting(striped, line_n) # TODO: HANDLE FALIURE
                        if key == "nb_drones":
                            self._validate_drones(val, line_n) # TODO: HANDLE FALIURE
                            self.nb_drones = int(val)
                        elif key == "start_hub":
                            # TODO: now we jump to zone file cause we have detected an zone