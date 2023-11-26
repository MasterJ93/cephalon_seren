"""
A list of custom exceptions for this bot to use.
"""

class InvalidFileType(Exception):
    """
    A custom Exception where an unsupported image format is detected.
    """


class IDAlreadyExistsException(Exception):
    """
    A custom exception for handling cases where a clan ID already exists.
    """


class IDNotFoundException(Exception):
    """
    A custom exception for handling cases where a clan ID hasn't been found.
    """

class RequestFailedException(Exception):
    """
    A custom exception for handling cases where a web request has failed.
    """
