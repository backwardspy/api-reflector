"""
Declares the flask-admin instance and sets up the model views.
"""

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_dance.contrib.azure import azure
from flask import Blueprint, request, redirect, url_for
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError

from api_reflector import models, db


class RestrictedAdminView(AdminIndexView):
    def is_accessible(self):
        if azure.authorized:
            try:
                resp = azure.get("/v1.0/me")
                assert resp.ok
                return True
            except TokenExpiredError as e:
                return redirect(url_for("azure.login"))

    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("azure.login"))


admin = Admin(name="API Reflector", template_mode="bootstrap3", index_view=RestrictedAdminView())


class RestrictedView(ModelView):
    def is_accessible(self):
        if azure.authorized:
            resp = azure.get("/v1.0/me")
            assert resp.ok
            return True
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("azure.login"))


admin.add_views(
    RestrictedView(models.Endpoint, db.session),
    RestrictedView(models.Response, db.session),
    RestrictedView(models.Rule, db.session),
    RestrictedView(models.Action, db.session),
)
