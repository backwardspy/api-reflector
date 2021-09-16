"""
Declares the flask-admin instance and sets up the model views.
"""
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_dance.contrib.azure import azure
from flask import redirect, url_for
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError

from settings import settings

from api_reflector import models, db


class RestrictedAdminView(AdminIndexView):
    """
    Overrides default Flask-Admin admin view to implement OSS authentication before accessing.
    """

    def is_accessible(self):
        if not settings.azure_auth_enabled:
            return True

        if azure.authorized:
            try:
                resp = azure.get("/v1.0/me")
                resp.raise_for_status()
                return True
            except TokenExpiredError:
                return redirect(url_for("azure.login"))
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("azure.login"))


admin = Admin(name="API Reflector", template_mode="bootstrap3", index_view=RestrictedAdminView())


class RestrictedView(ModelView):
    """
    Overrides ModelView to implement OSS authentication before accessing.
    """

    def is_accessible(self):
        if not settings.azure_auth_enabled:
            return True

        if azure.authorized:
            try:
                resp = azure.get("/v1.0/me")
                resp.raise_for_status()
                return True
            except TokenExpiredError:
                return redirect(url_for("azure.login"))
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("azure.login"))


admin.add_views(
    RestrictedView(models.Endpoint, db.session),
    RestrictedView(models.Response, db.session),
    RestrictedView(models.Rule, db.session),
    RestrictedView(models.Action, db.session),
)
