"""
Defines the project's API endpoints.
"""

from flask import Blueprint, request

from api_reflector import models

api = Blueprint("api", __name__)


def ensure_leading_slash(path: str) -> str:
    """
    Ensures that the given path has a leading slash.
    This is needed as mock paths are stored in the database with a leading slash, but flask passes the path parameter
    without one.
    """
    if path[0] != "/":
        return "/" + path
    return path


@api.route("/mock/<path:path>")
def mock(path: str):
    """
    Mock endpoint. Tries to map the given path to a configured mock.
    """

    path = ensure_leading_slash(path)

    endpoint = models.Endpoint.query.filter(
        models.Endpoint.method == request.method.upper(), models.Endpoint.path == path.lower()
    ).one_or_none()

    if not endpoint:
        return "", 404

    response = endpoint.responses[0]

    return response.content, response.status_code
