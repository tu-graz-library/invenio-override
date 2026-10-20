# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2026 Graz University of Technology.
#
# invenio-override is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module for sharedRDM theme."""

import secrets
import traceback
from functools import wraps
from typing import Dict, Optional
from urllib.parse import urlencode

from flask import (
    Blueprint,
    current_app,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from invenio_communities.proxies import current_communities
from invenio_i18n import lazy_gettext as _
from invenio_i18n.proxies import current_i18n
from invenio_rdm_records.proxies import current_rdm_records
from invenio_rdm_records.resources.serializers import UIJSONSerializer
from invenio_records_global_search.resources.serializers import (
    GlobalSearchJSONSerializer,
)
from invenio_users_resources.proxies import current_user_resources
from invenio_vocabularies.proxies import current_service as vocabulary_service
from opensearch_dsl.utils import AttrDict

from .search import FrontpageRecordsSearch

blueprint = Blueprint(
    "invenio-override",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@blueprint.route("/me/overview")
@login_required
def overview():
    """Render the user overview dashboard."""
    url = current_user_resources.users_service.links_item_tpl.expand(
        g.identity, current_user
    )["avatar"]
    is_authenticated = current_identity_is_authenticated()

    return render_template(
        "invenio_override/overview.html",
        is_authenticated=is_authenticated,
        user_avatar=url,
    )


def records_serializer(records=None) -> list:
    """
    Serialize a list of records.

    :param records: List of records to serialize.
    :returns: Serialized records as a list of dictionaries.
    """
    serializer = GlobalSearchJSONSerializer()
    return [serializer.dump_obj(r.to_dict()) for r in records]


def index():
    """
    Render the frontpage.

    Fetches the most recent records and renders the frontpage template.
    """
    records = FrontpageRecordsSearch()[:3].sort("-created").execute()

    return render_template(
        "invenio_override/frontpage.html", records=records_serializer(records)
    )


def default_error_handler(e: Exception) -> tuple:
    """Handle unhandled errors.

    Generates a unique error ID, logs the full traceback with it, and renders
    the error page. The error ID makes it easy to correlate a user-reported
    error with the corresponding log entry.

    :param e: Exception raised.
    :returns: Rendered error page with HTTP 500 status.
    """
    error_id = secrets.token_hex(4)
    tb = "".join(traceback.format_exception(e))
    current_app.logger.error(
        "(caught by invenio-override default_error_handler):\n"
        "Error ID: #%s\nException class: %s\nException: %s\n%s",
        error_id,
        type(e),
        e,
        tb,
    )
    return (
        render_template(current_app.config["THEME_500_TEMPLATE"], error_id=error_id),
        500,
    )


@blueprint.app_template_filter("make_dict_like")
def make_dict_like(value: str, key: str) -> Dict[str, str]:
    """
    Convert a value to a dict-like structure.

    :param value: The value to include in the dictionary.
    :param key: The key associated with the value.
    :returns: A dictionary with the given key-value pair.
    """
    return {key: value}


@blueprint.app_template_filter("cast_to_dict")
def cast_to_dict(attr_dict: AttrDict) -> dict:
    """
    Convert an AttrDict to a regular dictionary.

    :param attr_dict: The AttrDict to convert.
    :returns: The converted dictionary.
    """
    return AttrDict.to_dict(attr_dict)


def comingsoon() -> str:
    """
    Render the coming soon page.

    :returns: Rendered HTML for the coming soon page.
    """
    return render_template("invenio_override/comingsoon.html")


def make_redirect(target: str, endpoint: str = "redirect"):
    """Return a view function that redirects to target."""

    def view():
        return redirect(target)

    view.__name__ = endpoint
    return view


def locked(e) -> str:
    """
    Render the locked error page.

    :param e: Exception raised for a locked resource.
    :returns: Rendered HTML for the locked error page.
    """
    return render_template("invenio_override/423.html")


@blueprint.route("/help")
def help_page():
    """Render the help page."""
    return render_template("invenio_override/help.html")


@blueprint.route("/communities")
def communities_frontpage():
    """Render the communities overview page."""
    can_create = current_communities.service.check_permission(g.identity, "create")
    return render_template(
        "invenio_override/communities_frontpage.html",
        permissions=dict(can_create=can_create),
    )


@blueprint.route("/records/search")
def records_search():
    """
    Render the search page UI.

    Adds a new endpoint at repository.tugraz.at/records/search,
    serving as the dedicated search page for RDM records.
    """
    return render_template("invenio_override/search.html")


# Advanced search form. Builds a query from the fields below and redirects to
# the search results.

DEFAULT_ADVANCED_SEARCH_FIELDS = [
    {
        "name": "title",
        "label": _("Title"),
        "kind": "text",
        "query": "metadata.title",
        "placeholder": _("e.g. deep learning"),
    },
    {
        "name": "author",
        "label": _("Author / Creator"),
        "kind": "text",
        "query": "metadata.creators.person_or_org.name",
        "placeholder": _("e.g. Smith"),
    },
    {
        "name": "abstract",
        "label": _("Abstract / Description"),
        "kind": "text",
        "query": "metadata.description",
    },
    {
        "name": "keywords",
        "label": _("Keywords / Subject"),
        "kind": "text",
        "query": "metadata.subjects.subject",
        "placeholder": _("e.g. machine learning"),
    },
    {
        "name": "date",
        "label": _("Publication date"),
        "kind": "daterange",
        "query": "metadata.publication_date",
    },
    {
        "name": "resource_type",
        "label": _("Resource type"),
        "kind": "select",
        "query": "metadata.resource_type.id",
        "vocabulary": "resourcetypes",
    },
    {
        "name": "license",
        "label": _("License"),
        "kind": "select",
        "query": "metadata.rights.id",
        "vocabulary": "licenses",
    },
    {
        "name": "funder",
        "label": _("Funder"),
        "kind": "text",
        "query": "metadata.funding.funder.name",
        "placeholder": _("e.g. European Commission"),
    },
]


def _advanced_search_fields() -> list:
    """Return the configured advanced-search field definitions."""
    return (
        current_app.config.get("OVERRIDE_ADVANCED_SEARCH_FIELDS")
        or DEFAULT_ADVANCED_SEARCH_FIELDS
    )


def _quote(value: str) -> str:
    """Quote a user value as a Lucene phrase, escaping backslash and quote."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def build_query(args, fields) -> str:
    """Build an InvenioRDM query string from the submitted fields."""
    clauses = []

    for field in fields:
        kind = field["kind"]

        if kind in ("text", "select"):
            value = (args.get(field["name"]) or "").strip()
            if value:
                token = value if kind == "select" else _quote(value)
                clauses.append(f"{field['query']}:{token}")

        elif kind == "daterange":
            date_from = (args.get(field["name"] + "_from") or "").strip()
            date_to = (args.get(field["name"] + "_to") or "").strip()
            if date_from or date_to:
                clauses.append(
                    f"{field['query']}:" f"[{date_from or '*'} TO {date_to or '*'}]"
                )

    return " AND ".join(clauses)


def _vocabulary_options(vocabulary_type: str) -> list:
    """Load a vocabulary as (id, label) pairs for a dropdown."""
    try:
        result = vocabulary_service.read_all(
            g.identity,
            fields=["id", "title"],
            type=vocabulary_type,
            max_records=500,
        )
        language = current_i18n.language
        items = []
        for hit in result.to_dict()["hits"]["hits"]:
            title = hit.get("title") or {}
            label = (
                title.get(language)
                or title.get("en")
                or next(iter(title.values()), hit["id"])
            )
            items.append((hit["id"], label))
        return sorted(items, key=lambda item: item[1].lower())
    except Exception:
        # the field falls back to no options
        current_app.logger.exception("Loading vocabulary %s failed", vocabulary_type)
        return []


@blueprint.route("/search/advanced")
def advanced_search():
    """Render the advanced-search form, or build the query and go to results."""
    fields = _advanced_search_fields()

    if request.args.get("submitted"):
        query = build_query(request.args, fields)
        target = current_app.config.get(
            "OVERRIDE_ADVANCED_SEARCH_TARGET", "/records/search"
        )
        if query:
            target = target + "?" + urlencode({"q": query})
        return redirect(target)

    options = {
        field["name"]: _vocabulary_options(field["vocabulary"])
        for field in fields
        if field["kind"] == "select"
    }

    return render_template(
        "invenio_override/advanced_search.html",
        fields=fields,
        options=options,
    )


def current_identity_is_authenticated() -> bool:
    """Check whether the current identity is authenticated via remote auth."""
    rdm_service = current_rdm_records.records_service
    return rdm_service.check_permission(
        g.identity, current_app.config["OVERRIDE_AUTHENTICATED_ROLE"]
    )


def require_authenticated(view_func):
    """Decorator to guard views against unauthenticated users."""

    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_identity_is_authenticated():
            return redirect(url_for("invenio-override.overview"))
        return view_func(*args, **kwargs)

    return decorated_view
