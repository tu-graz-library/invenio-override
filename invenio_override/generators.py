# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Permission generators that can be configured from the instance."""

from flask import current_app
from flask_principal import RoleNeed
from invenio_records_permissions.generators import Generator


class CommunityCreator(Generator):
    """Grant permissions to users with configured community-creator roles.

    Roles are configured via the `OVERRIDE_COMMUNITIES_CREATE_ROLES` config variable.
    """

    def needs(self, record=None, **kwargs):
        """Override needs."""
        roles = current_app.config.get("OVERRIDE_COMMUNITIES_CREATE_ROLES")
        return [RoleNeed(r) for r in roles]
