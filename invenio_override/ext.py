# SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
# SPDX-FileCopyrightText: 2026 University of Graz.
# SPDX-License-Identifier: MIT

"""invenio module for configurable theme."""

from flask import has_request_context, request
from flask_login import login_required
from invenio_i18n import lazy_gettext as _

from . import config
from .views import (
    blueprint,
    default_error_handler,
    index,
    locked,
    make_redirect,
    require_authenticated,
)
from .visibility import public_entries


class InvenioOverride(object):
    """invenio-override extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.add_url_rule
        app.add_url_rule("/", "index", index)
        self.init_config(app)
        app.register_error_handler(423, locked)
        app.register_error_handler(Exception, default_error_handler)
        app.config["THEME_LOGO"] = app.config.get("OVERRIDE_LOGO")
        app.extensions["invenio-override"] = self
        routes = app.config.get("OVERRIDE_ROUTES")
        blueprint.add_url_rule(routes["index"], view_func=index)

        for path, target in app.config.get("OVERRIDE_DOC_REDIRECTS", {}).items():
            endpoint = "doc_redirect_" + path.strip("/").replace("-", "_")
            blueprint.add_url_rule(
                path, endpoint=endpoint, view_func=make_redirect(target, endpoint)
            )

        @app.context_processor
        def inject_visibility():
            # The rules need a visitor; templates rendered outside a request
            # (mails) get no dashboard entries.
            entries = (
                app.config.get("OVERRIDE_DASHBOARD_ENTRIES", [])
                if has_request_context()
                else []
            )
            return {
                "override_header_links": public_entries(
                    app.config.get("OVERRIDE_HEADER_LINKS", [])
                ),
                "override_dashboard_entries": [
                    entry.to_client() for entry in entries if entry.is_visible()
                ],
            }

        @app.context_processor
        def inject_deposit_page_description():
            descriptions = {
                "invenio_communities.communities_search": _(
                    "Browse and discover all communities"
                ),
                "invenio_app_rdm.help_search": _(
                    "This guide explains how to write advanced search queries "
                    "using easy to understand examples."
                ),
                "invenio_app_rdm.help_statistics": _(
                    "Answers to frequently asked questions about how usage "
                    "statistics are collected, anonymized and displayed."
                ),
                "invenio_records_marc21.deposit_create": _("Deposit a publication"),
                "invenio_records_marc21.deposit_edit": _("Deposit a publication"),
                "invenio_catalogue_marc21.deposit_create": _(
                    "Deposit a catalogue record"
                ),
                "invenio_catalogue_marc21.deposit_edit": _(
                    "Deposit a catalogue record"
                ),
                "invenio_records_lom.uploads": _(
                    "Manage and publish your openly licensed educational materials"
                ),
                "invenio_records_lom.deposit_create": _(
                    "Deposit an educational resource"
                ),
                "invenio_records_lom.deposit_edit": _(
                    "Deposit an educational resource"
                ),
            }
            desc = descriptions.get(request.endpoint)
            return {"page_description": desc} if desc else {}

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("INVENIO_OVERRIDE_") or k.startswith("OVERRIDE_"):
                app.config.setdefault(k, getattr(config, k))


def finalize_app(app):
    """Finalize app."""
    modify_user_dashboard(app)
    guard_view_functions(app)


def modify_user_dashboard(app):
    """Modify user dashboard.

    To modify the dashboard menu, access the user_dashboard_menu
    through root_menu.submenu("dashboard").
    """
    root_menu = app.extensions["menu"].root_node
    user_dashboard_menu = root_menu.submenu("dashboard")

    if "overview" not in user_dashboard_menu.children:
        user_dashboard_menu.submenu("overview").register(
            "invenio-override.overview",
            text=_("Overview"),
            order=0,
        )

    root_menu.submenu("actions.deposit").register(
        "invenio-override.overview",
        _("My dashboard"),
        order=1,
    )


def guard_view_functions(app):
    """Guard view functions against unauthenticated access."""
    endpoints_to_guard = [
        "invenio_app_rdm_users.communities",
        "invenio_app_rdm_users.requests",
        "invenio_app_rdm_users.uploads",
    ]

    for endpoint in endpoints_to_guard:
        view_func = app.view_functions.get(endpoint)
        if not view_func:
            continue

        view_func = login_required(require_authenticated(view_func))

        app.view_functions[endpoint] = view_func
