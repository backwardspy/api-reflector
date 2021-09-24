"""
Creates the flask-sqlalchemy instance and aliases its Model and session properties.
"""

from flask_sqlalchemy import SQLAlchemy
from alembic.config import Config
from alembic import command

sqla = SQLAlchemy()
Model = sqla.Model
session = sqla.session


def run_migrations() -> None:
    cfg = Config("alembic.ini")
    command.upgrade(cfg, "head")
