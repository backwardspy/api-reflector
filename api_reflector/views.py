"""
Defines the project's API endpoints.
"""
from typing import Any, Mapping

import psycopg2
from flask import Blueprint, Response, request
from flask_admin.base import render_template
from jinja2.exceptions import TemplateError, TemplateSyntaxError, UndefinedError
from werkzeug.routing import Map, Rule

from api_reflector import db, models, rules_engine
from api_reflector.auth import requires_auth
from api_reflector.endpoint import ensure_leading_slash
from api_reflector.reporting import get_logger
from api_reflector.templating import default_context, template_env

api = Blueprint("api", __name__)
log = get_logger(__name__)


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

    rules = [Rule(endpoint.path, endpoint=endpoint, methods=[request.method]) for endpoint in endpoints]
    urls = Map(rules).bind("localhost")

    # we're disabling mypy here because you're supposed to get strings back from `match`, not full endpoint objects.
    return urls.match(path, method=request.method)  # type: ignore


def _process_error_response(ex: UndefinedError | TemplateSyntaxError | TemplateError) -> Response:
    """Returns the error response for Jinja exceptions"""

    if isinstance(ex, UndefinedError):
        msg = "Undefined field used in the response template"
    elif isinstance(ex, TemplateSyntaxError):
        msg = "Syntax error in response template"
    else:
        msg = "Failed to render fields in the response template"

    error_content = f"{msg}. Details: {ex}"

    return Response(error_content, status=500, mimetype="text/plain")


@api.route("/healthz")
@api.route("/livez")
def healthz() -> tuple[Any, int]:
    """
    Returns a 204 OK response.
    """
    return "", 204


@api.route("/readyz")
def readyz() -> tuple[Any, int]:
    """
    Returns a 204 OK response if services are accessible, 500 otherwise.
    """
    try:
        db.sqla.engine.execute("SELECT 1").fetchone()
    except psycopg2.Error as ex:
        return f"Database is not accessible.\nException:\n\n{ex}", 500
    return "", 204


@api.route("/")
@requires_auth
def home() -> tuple[Any, int]:
    """
    Renders the home page.
    """
    endpoints = models.Endpoint.query.order_by(models.Endpoint.name).all()
    tags = models.Tag.query.order_by(models.Tag.name).all()
    return render_template("home.html", endpoints=endpoints, tags=tags), 200


@api.route("/mock/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def mock(path: str) -> Response:
    """
    Mock endpoint. Tries to map the given path to a configured mock.
    """

    path = ensure_leading_slash(path)
    endpoint, params = match_endpoint(path)  # pylint: disable=unpacking-non-sequence

    log.info(f"Matched `{path}` to endpoint: {endpoint}")

    active_responses = [response for response in endpoint.responses if response.is_active]

    if not active_responses:
        return Response("No Mock Responses configured or active for this endpoint", status=501)

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
        req_json = request.json  # type: Any
    else:
        req_json = {}

    templateable_request = rules_engine.TemplatableRequest(
        params=params, json=req_json, query=request.args, headers=request.headers
    )

    try:
        response = rules_engine.find_best_response(templateable_request, response_rules)
        content = template_env.from_string(response.content).render(
            {
                "request": templateable_request,
                **default_context,
            }
        )
        response.execute_actions(req_json, content)

    except UndefinedError as ex:
        return _process_error_response(ex)
    except TemplateSyntaxError as ex:
        return _process_error_response(ex)
    except TemplateError as ex:
        return _process_error_response(ex)
    else:
        return Response(content, status=response.status_code, mimetype=response.content_type)
