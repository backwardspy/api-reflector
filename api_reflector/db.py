"""
Creates the flask-sqlalchemy instance and aliases its Model and session properties.
"""

from flask_sqlalchemy import SQLAlchemy

from alembic import command
from alembic.config import Config

sqla = SQLAlchemy()
Model = sqla.Model
session = sqla.session


def run_migrations() -> None:
    """
    Invokes alembic to upgrade the database to the latest schema revision.
    """
    cfg = Config("alembic.ini")
    command.upgrade(cfg, "head")
