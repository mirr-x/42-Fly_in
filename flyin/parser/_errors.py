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


class InsaneError(ParserError):
    """InsaneError inherit from ParserError: it will get triggerd if you
        changed somting in dubug mode
    """


class DuplacateZoneError(ParserError):
    """DuplacateZoneError inherit from ParserError: get triggerd when passing
        duplucate start or end
    """


class DuplacateConnectionError(ParserError):
    """DuplacateConnectionError inherit from ParserError: get triggerd when
        passing duplucate connections
    """


class ElementNotFoundError(ParserError):
    """DuplacateConnectionError inherit from ParserError: get triggerd when
        passing duplucate connections
    """
