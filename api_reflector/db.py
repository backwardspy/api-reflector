"""
Creates the flask-sqlalchemy instance and aliases its Model and session properties.
"""

from flask_sqlalchemy import SQLAlchemy

sqla = SQLAlchemy()
Model = sqla.Model
session = sqla.session
