"""
Handles azure SSO authentication via flask-dance
"""
from cachetools import TTLCache, cached
from flask_dance.contrib.azure import azure
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError

from settings import settings


@cached(cache=TTLCache(maxsize=1, ttl=60))
def validate_token() -> bool:
    """
    Tests if the current token is still valid.
    Cached to avoid spamming /v1.0/me too often.
    """
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
    return azure.authorized and validate_token()
