# SPDX-FileCopyrightText: 2026 University of Graz.
# SPDX-License-Identifier: MIT

"""Dashboard entries."""

from types import SimpleNamespace

import pytest
from flask import Flask, g
from flask_babel import Babel

from invenio_override import InvenioOverride, ext
from invenio_override.dashboard import DEFAULT_DASHBOARD_ENTRIES, DashboardEntry


@pytest.fixture()
def app(monkeypatch):
    """Flask application with the extension, without menu and marc21."""
    monkeypatch.setattr(ext, "current_identity_can_view", lambda: False)
    app = Flask("testapp")
    Babel(app)
    InvenioOverride(app)
    # The bare app has no menu: nobody is a curator.
    app.config["OVERRIDE_VISIBILITY_RULES"]["is_curator"] = lambda: False
    return app


def _identity(*roles):
    return SimpleNamespace(
        provides=[SimpleNamespace(method="role", value=role) for role in roles]
    )


def _entries(app):
    (inject,) = [
        processor
        for processor in app.template_context_processors[None]
        if processor.__name__ == "inject_visibility"
    ]
    return inject()["override_dashboard_entries"]


def test_default_entries(app):
    """Without config the dashboard shows the entries it always had."""
    assert app.config["OVERRIDE_DASHBOARD_ENTRIES"] == DEFAULT_DASHBOARD_ENTRIES
    with app.test_request_context():
        g.identity = _identity()
        keys = [entry["key"] for entry in _entries(app)]
    # publications, educational resources and curations are switched off
    # in the bare app
    assert keys == ["uploads", "requests", "upload-dataset"]


def test_builtin_rules_follow_the_config(app):
    """show_publications follows OVERRIDE_SHOW_PUBLICATIONS_SEARCH."""
    app.config["OVERRIDE_SHOW_PUBLICATIONS_SEARCH"] = True
    with app.test_request_context():
        g.identity = _identity()
        keys = [entry["key"] for entry in _entries(app)]
    assert "publications" in keys


def test_instance_rule_replaces_builtin_rule():
    """A rule of the same name in the instance config wins."""
    app = Flask("testapp")
    app.config["OVERRIDE_VISIBILITY_RULES"] = {"is_curator": lambda: True}
    InvenioOverride(app)
    assert app.config["OVERRIDE_VISIBILITY_RULES"]["is_curator"]() is True
    assert "can_upload_oer" in app.config["OVERRIDE_VISIBILITY_RULES"]


def test_entries_follow_roles_and_rules(app):
    """Own entries are filtered like the header links, in their order."""
    app.config["OVERRIDE_VISIBILITY_RULES"]["off"] = lambda: False
    app.config["OVERRIDE_DASHBOARD_ENTRIES"] = [
        DashboardEntry(key="all", title="All", url="/a"),
        DashboardEntry(key="staff", title="Staff", url="/b", roles=("staff",)),
        DashboardEntry(key="hidden", title="Hidden", url="/c", visible="off"),
    ]
    with app.test_request_context():
        g.identity = _identity("staff")
        entries = _entries(app)
    assert [entry["key"] for entry in entries] == ["all", "staff"]
    assert "roles" not in entries[1]
    assert "visible" not in entries[1]
    with app.test_request_context():
        g.identity = _identity("other-role")
        assert [entry["key"] for entry in _entries(app)] == ["all"]


def test_no_entries_outside_a_request():
    """Templates rendered without a visitor (mails) get no entries."""
    # Not the app fixture: pytest-flask pushes a request context for it.
    bare = Flask("bare")
    Babel(bare)
    InvenioOverride(bare)
    with bare.app_context():
        assert _entries(bare) == []


def test_to_client():
    """The client gets display fields only, with plain strings."""
    entry = DashboardEntry(
        key="k", title="T", url="/u", roles=("r",), visible="v", highlight=True
    )
    assert entry.to_client() == {
        "key": "k",
        "title": "T",
        "url": "/u",
        "description": "",
        "icon": "plus",
        "highlight": True,
        "divider_before": False,
    }
