# SPDX-FileCopyrightText: 2026 University of Graz.
# SPDX-License-Identifier: MIT

"""The entry type of OVERRIDE_DASHBOARD_ENTRIES."""

from dataclasses import dataclass

from .visibility import is_allowed


@dataclass(frozen=True)
class DashboardEntry:
    """One entry: an item in the Dashboard menu and a tile on the overview.

    ``roles`` and ``visible`` restrict who sees the entry, see
    ``invenio_override.visibility``. Both are checked server side and never
    reach the client.
    """

    key: str
    title: str
    url: str
    description: str = ""
    icon: str = "plus"
    highlight: bool = False
    divider_before: bool = False
    roles: tuple[str, ...] = ()
    visible: str | None = None

    def is_visible(self) -> bool:
        """Check whether the current visitor may see the entry."""
        return is_allowed(self.roles, self.visible)

    def to_client(self) -> dict:
        """Fields for the templates and the overview page, translated."""
        return {
            "key": self.key,
            "title": str(self.title),
            "url": self.url,
            "description": str(self.description),
            "icon": self.icon,
            "highlight": self.highlight,
            "divider_before": self.divider_before,
        }
