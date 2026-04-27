"""Internal error definitions for the parser."""


class ParserError(Exception):
    """Custom parser error to inherit from Exception"""


class InvalidFormatError(ParserError):
    """InvalidFormatError inherit from ParserError: for invalid format"""


class InvalidValueError(ParserError):
    """InvalidValueError inherit from ParserError: for invalid value"""


class InvalidCordsError(ParserError):
    """InvalidCordsError inherit from ParserError: for invalid cords"""


class ParserFileNotFoundError(ParserError):
    """ParserFileNotFoundError inherit from ParserError: if file not found"""
