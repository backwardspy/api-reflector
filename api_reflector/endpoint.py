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
