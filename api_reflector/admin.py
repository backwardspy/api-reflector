"""
Declares the flask-admin instance and sets up the model views.
"""

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from api_reflector import models, db

admin = Admin(name="API Reflector", template_mode="bootstrap3")

admin.add_views(
    ModelView(models.Endpoint, db.session),
    ModelView(models.Response, db.session),
    ModelView(models.Rule, db.session),
    ModelView(models.Action, db.session),
)
