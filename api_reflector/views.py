"""
Defines the project's API endpoints.
"""

from functools import wraps
from typing import Any, Mapping

from flask import Blueprint, redirect, request, url_for
from flask_admin.base import render_template
from jinja2 import Template
from werkzeug.routing import Map, Rule

from api_reflector import actions, models, rules_engine
from api_reflector.auth import is_authorized
from api_reflector.reporting import get_logger

api = Blueprint("api", __name__)
log = get_logger("api")


def ensure_leading_slash(path: str) -> str:
    """
    Ensures that the given path has a leading slash.
    This is needed as mock paths are stored in the database with a leading slash, but flask passes the path parameter
    without one.
    """
    if path[0] != "/":
        return "/" + path
    return path


def match_endpoint(path: str) -> tuple[models.Endpoint, Mapping[str, Any]]:
    """
    Uses werkzeug routing to match the given path to an endpoint.
    Returns the matched endpoint as well as a mapping of URL parameters passed to the endpoint.
    If no endpoint was matched, raises a NotFound exception.
    """

    log.debug(f"Matching path `{path}`")

    endpoints: list[models.Endpoint] = models.Endpoint.query.filter(
        models.Endpoint.method == request.method.upper()
    ).all()

    urls = Map([Rule(endpoint.path, endpoint=endpoint, methods=[request.method]) for endpoint in endpoints]).bind(
        "localhost"
    )

    # we're disabling mypy here because you're supposed to get strings back from `match`, not full endpoint objects.
    return urls.match(path, method=request.method)  # type: ignore


def execute_response_actions(response: models.Response) -> None:
    """
    Executes all response actions for the given response.
    """
    log.debug(f"Executing actions for response: {response}")
    for action in response.actions:
        log.debug(f"Executing action: {action}")
        actions.action_executors[action.action](*action.arguments)


def requires_auth(view_function):
    """
    Flask view function decorator that ensures that the user is authenticated.
    The user is redirected to the Azure login flow if they are not already authenticated.
    """

    @wraps(view_function)
    def decorator(*args, **kwargs):
        if not is_authorized():
            return redirect(url_for("azure.login"))
        return view_function(*args, **kwargs)

    return decorator


@api.route("/healthz")
def healthz() -> tuple[Any, int]:
    """
    Returns a 200 OK response.
    """
    return "OK", 200


@api.route("/")
@requires_auth
def home() -> tuple[Any, int]:
    """
    Renders the home page.
    """
    endpoints = models.Endpoint.query.all()
    tags = models.Tag.query.all()
    return render_template("home.html", endpoints=endpoints, tags=tags), 200


@api.route("/mock/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def mock(path: str) -> tuple[Any, int]:
    """
    Mock endpoint. Tries to map the given path to a configured mock.
    """

    path = ensure_leading_slash(path)
    endpoint, params = match_endpoint(path)  # pylint: disable=unpacking-non-sequence

    log.info(f"Matched `{path}` to endpoint: {endpoint}")

    active_responses = [response for response in endpoint.responses if response.is_active]

    if not active_responses:
        return "No Mock Responses configured or active for this endpoint", 501

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
        for response in active_responses
    ]

    if request.is_json:
        json = request.json  # type: Any
    else:
        json = {}

    templateable_request = rules_engine.TemplatableRequest(params=params, json=json)
    response = rules_engine.find_best_response(templateable_request, response_rules)

    execute_response_actions(response)

    content = Template(response.content).render(
        {
            "request": templateable_request,
        }
    )

    return content, response.status_code
