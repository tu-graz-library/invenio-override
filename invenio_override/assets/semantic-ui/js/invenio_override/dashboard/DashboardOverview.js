/*
 * SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import { i18next } from "@translations/invenio_override/i18next";
import { Icon } from "semantic-ui-react";
import React from "react";

const NAV_BOXES = [
  {
    key: "uploads",
    title: () => i18next.t("Research Results"),
    description: () => i18next.t("Your deposited research results"),
    icon: "file alternate outline",
    url: "/me/uploads",
  },
  {
    key: "publications",
    title: () => i18next.t("Publications"),
    description: () => i18next.t("Browse and search publications"),
    icon: "book",
    url: "/publications/search",
    marc21Only: true,
  },
  {
    key: "educational-resources",
    title: () => i18next.t("Educational Resources"),
    description: () => i18next.t("Your openly licensed educational materials"),
    icon: "graduation cap",
    url: "/oer/uploads",
    lomOnly: true,
  },
  {
    key: "requests",
    title: () => i18next.t("Requests"),
    description: () =>
      i18next.t("Check for incoming notifications and assignments"),
    icon: "tasks",
    url: "/me/requests",
  },
  {
    key: "curations",
    title: () => i18next.t("Curation Requests"),
    description: () => i18next.t("Review and manage curation submissions"),
    icon: "clipboard check",
    url: "/curations/overview",
    curatorOnly: true,
  },
  {
    key: "upload-dataset",
    title: () => i18next.t("Upload Research Result"),
    description: () =>
      i18next.t("Deposit research data, software, preprints and more"),
    icon: "database",
    url: "/uploads/new",
    highlight: true,
  },
  {
    key: "upload-publication",
    title: () => i18next.t("Upload Publication"),
    description: () => i18next.t("Deposit a publication"),
    icon: "book",
    url: "/publications/uploads/new",
    marc21UploadOnly: true,
    highlight: true,
  },
  {
    key: "upload-educational-resource",
    title: () => i18next.t("Upload Educational Resource"),
    description: () => i18next.t("Deposit an educational resource"),
    icon: "graduation cap",
    url: "/oer/uploads/new",
    lomUploadOnly: true,
    highlight: true,
  },
];

export function DashboardOverview({
  showLom,
  showCurations,
  showPublications,
  canUploadPublications,
  canUploadOer,
}) {
  const boxes = NAV_BOXES.filter(
    (box) =>
      (!box.lomOnly || showLom) &&
      (!box.curatorOnly || showCurations) &&
      (!box.marc21Only || showPublications) &&
      (!box.marc21UploadOnly || canUploadPublications) &&
      (!box.lomUploadOnly || canUploadOer),
  );

  return (
    <div className="dashboard-nav-grid">
      {boxes.map((box) => (
        <a
          key={box.key}
          href={box.url}
          className={`dashboard-nav-box${box.highlight ? " dashboard-nav-box-highlight" : ""}`}
        >
          <div className="dashboard-nav-box-circle">
            <Icon name={box.icon} />
          </div>
          <span className="dashboard-nav-box-title">{box.title()}</span>
          <span className="dashboard-nav-box-desc">{box.description()}</span>
        </a>
      ))}
    </div>
  );
}
