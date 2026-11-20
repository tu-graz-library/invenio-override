# SPDX-FileCopyrightText: 2026 University of Graz.
# SPDX-License-Identifier: MIT

"""Entries of the Dashboard menu and of the dashboard overview page."""

from dataclasses import dataclass

from invenio_i18n import lazy_gettext as _


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


DEFAULT_DASHBOARD_ENTRIES = [
    DashboardEntry(
        key="uploads",
        title=_("Research Results"),
        description=_("Your deposited research results"),
        icon="file alternate outline",
        url="/me/uploads",
    ),
    DashboardEntry(
        key="publications",
        title=_("Publications"),
        description=_("Your deposited publications"),
        icon="book",
        url="/publications/uploads",
        visible="show_publications",
    ),
    DashboardEntry(
        key="educational-resources",
        title=_("Educational Resources"),
        description=_("Your openly licensed educational materials"),
        icon="graduation cap",
        url="/oer/uploads",
        visible="can_upload_oer",
    ),
    DashboardEntry(
        key="requests",
        title=_("Requests"),
        description=_("Check for incoming notifications and assignments"),
        icon="tasks",
        url="/me/requests",
    ),
    DashboardEntry(
        key="curations",
        title=_("Curation Requests"),
        description=_("Review and manage curation submissions"),
        icon="clipboard check",
        url="/curations/overview",
        visible="is_curator",
    ),
    DashboardEntry(
        key="upload-dataset",
        title=_("Upload Research Result"),
        description=_("Deposit research data, software, preprints and more"),
        icon="database",
        url="/uploads/new",
        highlight=True,
        divider_before=True,
    ),
    DashboardEntry(
        key="upload-publication",
        title=_("Upload Publication"),
        description=_("Deposit a publication"),
        icon="book",
        url="/publications/uploads/new",
        highlight=True,
        visible="can_upload_publications",
    ),
    DashboardEntry(
        key="upload-educational-resource",
        title=_("Upload Educational Resource"),
        description=_("Deposit an educational resource"),
        icon="graduation cap",
        url="/oer/uploads/new",
        highlight=True,
        visible="can_upload_oer",
    ),
]
"""The entries invenio-override has always shown, in this order."""
