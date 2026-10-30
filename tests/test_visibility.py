# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Visibility tests."""

from types import SimpleNamespace

import pytest
from flask import Flask, g

from invenio_override import InvenioOverride
from invenio_override.visibility import is_visible, public_entries, visible_entries


@pytest.fixture()
def app():
    """Flask application without i18n, the visibility checks dont need it."""
    app = Flask("testapp")
    InvenioOverride(app)
    return app


def _identity(*roles):
    return SimpleNamespace(
        provides=[SimpleNamespace(method="role", value=role) for role in roles]
    )


def test_is_visible_without_restrictions(app):
    """An entry without roles and rule is visible to everyone."""
    with app.test_request_context():
        assert is_visible({"text": "Link", "url": "/link"})


def test_is_visible_by_role(app):
    """An entry with roles needs one of them."""
    entry = {"text": "Link", "url": "/link", "roles": ["archive-manager"]}
    with app.test_request_context():
        g.identity = _identity("archive-manager")
        assert is_visible(entry)
    with app.test_request_context():
        g.identity = _identity("other-role")
        assert not is_visible(entry)


def test_is_visible_by_rule(app):
    """An entry with a rule follows the rule."""
    app.config["OVERRIDE_VISIBILITY_RULES"] = {
        "on": lambda: True,
        "off": lambda: False,
    }
    with app.test_request_context():
        assert is_visible({"url": "/a", "visible": "on"})
        assert not is_visible({"url": "/a", "visible": "off"})


def test_is_visible_unknown_rule_fails_closed(app):
    """An unknown rule name keeps the entry hidden."""
    with app.test_request_context():
        assert not is_visible({"url": "/a", "visible": "unknown"})


def test_visible_entries_filters(app):
    """Only the visible entries remain."""
    app.config["OVERRIDE_VISIBILITY_RULES"] = {"off": lambda: False}
    entries = [
        {"text": "Everyone", "url": "/a"},
        {"text": "Hidden", "url": "/b", "visible": "off"},
    ]
    with app.test_request_context():
        assert [e["text"] for e in visible_entries(entries)] == ["Everyone"]


def test_public_entries_strips_visibility_keys(app):
    """The client never sees roles or rule names."""
    entries = [{"text": "Link", "url": "/a", "roles": ["x"], "visible": "r"}]
    app.config["OVERRIDE_VISIBILITY_RULES"] = {"r": lambda: True}
    with app.test_request_context():
        g.identity = _identity("x")
        assert public_entries(entries) == [{"text": "Link", "url": "/a"}]
