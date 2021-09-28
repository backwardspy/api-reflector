"""
Declares the flask-admin instance and sets up the model views.
"""
from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_dance.contrib.azure import azure
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from slugify import slugify

from api_reflector import db, models
from settings import settings


class RestrictedAdminView(AdminIndexView):
    """
    Overrides default Flask-Admin admin view to implement OSS authentication before accessing.
    """

    def is_visible(self):
        return False

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


class TagView(RestrictedView):
    """
    Admin modelview for the Tag model.
    """

    def validate_form(self, form):
        if form.name.data:
            form.name.data = slugify(form.name.data)
        return super().validate_form(form)


class EndpointView(RestrictedView):
    """
    Admin modelview for the Endpoint model.
    """

    form_excluded_columns = ("responses",)
    form_widget_args = {"responses": {"disabled": True}}
    inline_models = (models.Response,)


admin.add_link(MenuLink(name="Home", url="/"))

admin.add_views(
    TagView(models.Tag, db.session),
    EndpointView(models.Endpoint, db.session),
    RestrictedView(models.Response, db.session),
    RestrictedView(models.Rule, db.session),
    RestrictedView(models.Action, db.session),
)
