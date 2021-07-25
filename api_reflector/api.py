"""
Provides the top level flask application configuration.
"""

from flask import Flask

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

    db.sqla.init_app(app)
    admin.init_app(app)

    app.register_blueprint(api)

    return app
