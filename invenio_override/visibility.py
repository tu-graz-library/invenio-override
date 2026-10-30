# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Visibility of config driven entries, like header links and dashboard boxes.

An entry can restrict who sees it with two optional keys:

* ``roles``: the visitor has to hold one of the listed roles,
* ``visible``: the name of a rule in ``OVERRIDE_VISIBILITY_RULES``, a
  no-argument callable returning bool. Unknown rule names fail closed,
  the entry stays hidden.

All checks run server side, hidden entries never reach the client.
"""

from flask import current_app, g


def current_roles() -> set:
    """Role names held by the current identity."""
    return {need.value for need in g.identity.provides if need.method == "role"}


def is_visible(entry: dict) -> bool:
    """Check whether the current visitor may see the entry."""
    roles = entry.get("roles")
    if roles and not current_roles().intersection(roles):
        return False
    rule = entry.get("visible")
    if rule is None:
        return True
    check = current_app.config.get("OVERRIDE_VISIBILITY_RULES", {}).get(rule)
    if check is None:
        return False
    return bool(check())


def visible_entries(entries: list) -> list:
    """Filter the entries down to what the current visitor may see."""
    return [entry for entry in entries if is_visible(entry)]


def public_entries(entries: list) -> list:
    """Visible entries without the visibility keys, safe for the client."""
    return [
        {key: value for key, value in entry.items() if key not in ("roles", "visible")}
        for entry in visible_entries(entries)
    ]
