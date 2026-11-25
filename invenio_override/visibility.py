# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-FileCopyrightText: 2026 University of Graz.
# SPDX-License-Identifier: MIT

"""Visibility of config driven entries, like header links and dashboard entries.

An entry can restrict who sees it with two optional fields:

* ``roles``: the visitor has to hold one of the listed roles,
* ``visible``: the name of a rule in ``OVERRIDE_VISIBILITY_RULES``, a
  no-argument callable returning bool. Unknown rule names fail closed,
  the entry stays hidden.

All checks run server side, hidden entries never reach the client. The
rules below are the defaults of ``OVERRIDE_VISIBILITY_RULES``.
"""

from types import SimpleNamespace

from flask import current_app, g
from flask_menu import current_menu

try:
    from invenio_records_marc21.proxies import current_records_marc21
except ImportError:
    current_records_marc21 = SimpleNamespace(
        records_service=SimpleNamespace(check_permission=lambda *args, **kwargs: False)
    )

try:
    from invenio_records_lom.proxies import current_records_lom
except ImportError:
    current_records_lom = SimpleNamespace(
        records_service=SimpleNamespace(check_permission=lambda *args, **kwargs: False)
    )


def current_roles() -> set:
    """Role names held by the current identity."""
    return {need.value for need in g.identity.provides if need.method == "role"}


def is_allowed(roles, rule: str | None) -> bool:
    """Check whether the current visitor holds one of the roles and passes the rule."""
    if roles and not current_roles().intersection(roles):
        return False
    if rule is None:
        return True
    check = current_app.config.get("OVERRIDE_VISIBILITY_RULES", {}).get(rule)
    if check is None:
        return False
    return bool(check())


def is_visible(entry: dict) -> bool:
    """Check whether the current visitor may see the dict entry."""
    return is_allowed(entry.get("roles"), entry.get("visible"))


def visible_entries(entries: list[dict]) -> list[dict]:
    """Filter the dict entries down to what the current visitor may see."""
    return [entry for entry in entries if is_visible(entry)]


def public_entries(entries: list[dict]) -> list[dict]:
    """Visible dict entries without the visibility keys, safe for the client."""
    return [
        {key: value for key, value in entry.items() if key not in ("roles", "visible")}
        for entry in visible_entries(entries)
    ]


def show_publications() -> bool:
    """Visibility rule: the instance shows publications."""
    return bool(current_app.config.get("OVERRIDE_SHOW_PUBLICATIONS_SEARCH"))


def can_upload_publications() -> bool:
    """Visibility rule: the visitor may deposit publications."""
    # OVERRIDE_SHOW_* gates the feature; the data-model permission
    # decides who may upload.
    return show_publications() and bool(
        current_records_marc21.records_service.check_permission(g.identity, "create")
    )


def can_upload_oer() -> bool:
    """Visibility rule: the visitor may deposit educational resources."""
    return bool(
        current_app.config.get("OVERRIDE_SHOW_EDUCATIONAL_RESOURCES")
        and current_records_lom.records_service.check_permission(
            g.identity, "handle_oer"
        )
    )


def is_curator() -> bool:
    """Visibility rule: the curation overview is in the visitor's menu."""
    return bool(current_menu.submenu("dashboard").submenu("curation-overview").visible)
