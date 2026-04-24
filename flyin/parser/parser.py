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
    def __init__(self, file_path):
        self.file_path = file_path
        self.nb_drones = 0

    def parsing(self):
        try:
            with open(self.file_path, "r") as f:
                for i in f:
                    striped = i.strip() # TODO: U should ignore the commenter creat func to validate
                    if not striped.startswith("#"):
                        key, val = striped.split(":", 1) # TODO: HANDLE SPLIT FALIURE
                        if not (key or val):
                            raise ValueError("Error: missing format <key>: <val>")
                        if key == "nb_drones":
                            