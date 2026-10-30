# SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import pytest
from flask import Flask
from invenio_i18n import InvenioI18N

from invenio_override import InvenioOverride


@pytest.fixture()
def app(request):
    """Basic Flask application."""
    app = Flask("testapp")
    app.config.update(
        I18N_LANGUAGES=[("en", "English"), ("de", "German")],
    )
    InvenioOverride(app)
    InvenioI18N(app)

    return app
