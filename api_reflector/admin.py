"""
Declares the flask-admin instance and sets up the model views.
"""
from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from slugify import slugify

from api_reflector import auth, db, models


def admin_view(model: db.Model):
    """
    Registers a model with the admin.
    """

    def decorator(cls):
        admin.add_view(cls(model, db.session))
        return cls

    return decorator


class RestrictedAdminView(AdminIndexView):
    """
    Overrides default Flask-Admin admin view to implement OSS authentication before accessing.
    """

    def is_visible(self):
        return False

    def is_accessible(self):
        return auth.is_authorized()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("azure.login"))


admin = Admin(name="API Reflector", template_mode="bootstrap3", index_view=RestrictedAdminView())


class RestrictedView(ModelView):
    """
    Overrides ModelView to implement OSS authentication before accessing.
    """

    def is_accessible(self):
        return auth.is_authorized()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("azure.login"))


@admin_view(models.Tag)
class TagView(RestrictedView):
    """
    Admin modelview for the Tag model.
    """

    form_excluded_columns = ("responses",)

    def validate_form(self, form):
        if hasattr(form, "name") and form.name.data:
            form.name.data = slugify(form.name.data)
        return super().validate_form(form)


@admin_view(models.Endpoint)
class EndpointView(RestrictedView):
    """
    Admin modelview for the Endpoint model.
    """

    form_excluded_columns = ("responses",)
    form_widget_args = {"responses": {"disabled": True}}


@admin_view(models.Response)
class ResponseView(RestrictedView):
    """
    Admin modelview for the Response model.
    """

    column_exclude_list = ("content_type",)
    inline_models = (models.Rule, models.Action)


admin.add_link(MenuLink(name="Home", url="/"))
