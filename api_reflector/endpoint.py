"""
Contains types and methods related to mock API endpoints.
"""

from enum import Enum


class Method(Enum):
    """
    The HTTP methods supported for mock endpoints.
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

    def __str__(self) -> str:
        return self.value


def ensure_leading_slash(path: str) -> str:
    """
    Ensures that the given path has a leading slash.
    This is needed as mock paths are stored in the database with a leading slash, but flask passes the path parameter
    without one.
    """
    if path[0] != "/":
        return "/" + path
    return path
