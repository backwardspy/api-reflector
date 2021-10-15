"""
Handles azure SSO authentication via flask-dance
"""
from functools import wraps

from cachetools import TTLCache, cached
from flask import redirect, url_for
from flask_dance.contrib.azure import azure
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError

from api_reflector.reporting import get_logger
from settings import settings

log = get_logger(__name__)


@cached(cache=TTLCache(maxsize=256, ttl=600))
def validate_token(_token: str) -> bool:
    """
    Tests if the current token is still valid.
    Cached to avoid spamming /v1.0/me too often.

    The `_token` param is only used to distinguish cache entries.
    """
    log.debug("Validating azure auth token.")
    try:
        resp = azure.get("/v1.0/me")
        resp.raise_for_status()
        return True
    except TokenExpiredError:
        return False


def is_authorized():
    """
    Returns true if the current user is authorized to access the system.
    """
    if not settings.azure_auth_enabled:
        # when auth is disabled, everyone is authorized.
        return True

    # otherwise we must have a token and that token must not have expired.
    return azure.authorized and validate_token(azure.access_token)


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
