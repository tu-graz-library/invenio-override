# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Permission policies that can be configured from the instance."""

from invenio_administration.generators import Administration
from invenio_communities.permissions import CommunityPermissionPolicy
from invenio_records_permissions.generators import (
    AuthenticatedUser,
    IfConfig,
    SystemProcess,
)

from invenio_override.generators import CommunityCreator


class CustomCommunitiesPermissionPolicy(CommunityPermissionPolicy):
    """Custom permission policy for communities."""

    can_create = [
        IfConfig(
            "OVERRIDE_COMMUNITIES_RESTRICT_CREATION",
            then_=[CommunityCreator(), Administration(), SystemProcess()],
            else_=[AuthenticatedUser(), SystemProcess()],
        )
    ]

    can_include_directly = [Administration(), SystemProcess()]
