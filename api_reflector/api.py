"""
Provides the top level flask application configuration.
"""

import sentry_sdk
from flask import Flask
from flask_cors import CORS
from flask_dance.contrib.azure import make_azure_blueprint
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from werkzeug.middleware.proxy_fix import ProxyFix

from api_reflector import db
from api_reflector.admin import admin
from api_reflector.migrations import run_migrations
from api_reflector.reporting import get_logger
from api_reflector.views import api
from settings import settings

log = get_logger(__name__)


def create_app() -> Flask:
    """
    Creates a flask application and registers the api blueprint.
    """
    if settings.sentry_dsn:
        log.debug("Initialising Sentry SDK.")
        sentry_sdk.init(  # pylint: disable=abstract-class-instantiated
            dsn=settings.sentry_dsn,
            integrations=[FlaskIntegration(), SqlalchemyIntegration()],
        )

    log.debug("Initializing app.")

    app = Flask(__name__)
    CORS(app)
    app.wsgi_app = ProxyFix(  # type: ignore
        app.wsgi_app,
        x_proto=int(settings.use_x_forwarded_proto),
        x_host=int(settings.use_x_forwarded_host),
    )

    app.config.update(
        SECRET_KEY=settings.secret_key,
        SQLALCHEMY_DATABASE_URI=settings.postgres_dsn,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        FLASK_ADMIN_SWATCH="darkly",
    )

    if settings.azure_auth_enabled:
        azure_blueprint = make_azure_blueprint(
            client_id=settings.azure_client_id,
            client_secret=settings.azure_client_secret,
            tenant=settings.azure_tenant,
            redirect_url="/",
        )
        app.register_blueprint(azure_blueprint)

    db.sqla.init_app(app)
    admin.init_app(app)

    app.register_blueprint(api)

    log.debug("Migrating database.")
    run_migrations.main()

    log.debug("App initialisation complete.")

    return app
