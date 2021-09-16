"""
Provides the top level flask application configuration.
"""

from flask import Flask
from flask_dance.contrib.azure import make_azure_blueprint

from api_reflector import db
from api_reflector.views import api
from api_reflector.admin import admin
from settings import settings


def create_app() -> Flask:
    """
    Creates a flask application and registers the api blueprint.
    """
    app = Flask(__name__)
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
            redirect_url="/admin/",
        )
        app.register_blueprint(azure_blueprint)

    db.sqla.init_app(app)
    admin.init_app(app)

    app.register_blueprint(api)

    return app
