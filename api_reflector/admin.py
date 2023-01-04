"""
Declares the flask-admin instance and sets up the model views.
"""
import json
from json import JSONDecodeError

from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from jinja2.runtime import Context
from slugify import slugify
from wtforms import validators

from api_reflector import auth, db, models


def is_valid_json(data: str) -> None:
    """
    Validator function for checking whether form field content is a valid JSON.
    """

    try:
        json.loads(data)
    except JSONDecodeError as exc:
        raise validators.ValidationError("Response content data must be a valid JSON object or empty.") from exc


form_validators = {
    "application/json": is_valid_json,
}


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
        if form.data.get("name"):
            form.name.data = slugify(form.data["name"])
        return super().validate_form(form)


@admin_view(models.Endpoint)
class EndpointView(RestrictedView):
    """
    Admin modelview for the Endpoint model.
    """

    form_excluded_columns = ("responses",)
    form_widget_args = {"responses": {"disabled": True}}
    column_searchable_list = (
        "name",
        "path",
    )

    def validate_form(self, form):
        if form.data.get("path") and not form.data["path"].startswith("/"):
            form.path.data = f"/{form.data['path']}"
        return super().validate_form(form)


@admin_view(models.Response)
class ResponseView(RestrictedView):
    """
    Admin modelview for the Response model.
    """

    column_exclude_list = ("content_type",)
    inline_models = (models.Rule, models.Action)
    form_widget_args = {"content": {"rows": 8, "style": "font-family: monospace;"}}
    column_searchable_list = ("name",)

    def on_model_change(self, form, model, is_created):
        if validator := form_validators.get(form.content_type.data):
            validator(form.content.data)
            super().on_model_change(form, model, is_created)

    def content_formatter(self, _ctx: Context, model: models.Model, _name: str):
        """
        Limits the content field to a maximum length in the list view.
        """
        max_length = 50
        if len(model.content) > max_length:
            return f"{model.content[:max_length - 3]}..."
        return model.content

    column_formatters = {
        "content": content_formatter,
    }


admin.add_link(MenuLink(name="Home", url="/"))
