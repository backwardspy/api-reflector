"""
Defines the project's API endpoints.
"""

from typing import Any

from flask import Blueprint, request

from api_reflector import models, rules_engine

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


@api.route("/mock/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def mock(path: str):
    """
    Mock endpoint. Tries to map the given path to a configured mock.
    """

    path = ensure_leading_slash(path)

    endpoint: models.Endpoint = models.Endpoint.query.filter(
        models.Endpoint.method == request.method.upper(), models.Endpoint.path == path.lower()
    ).one_or_none()

    if not endpoint:
        # check if we have one for another method or not
        method_not_allowed = (
            models.Endpoint.query.with_entities(models.Endpoint.id).filter(models.Endpoint.path == path).one_or_none()
        )
        if method_not_allowed:
            return "endpoint exists under another method", 405
        return "no such endpoint has been configured", 404

    if request.is_json:
        json = request.json  # type: Any
    else:
        json = {}

    response_rules = [
        (
            response,
            [
                rules_engine.ScoringRule(
                    operator=rule.operator,
                    arguments=rule.arguments,
                )
                for rule in response.rules
            ],
        )
        for response in endpoint.responses
    ]

    response = rules_engine.find_best_response(rules_engine.TemplatableRequest(json=json), response_rules)

    return response.content, response.status_code
