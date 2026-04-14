// Copyright (C) 2020-2026 Graz University of Technology.
//
// invenio-override is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/invenio_override/i18next";
import { Icon } from "semantic-ui-react";
import React from "react";

const NAV_BOXES = [
  {
    key: "uploads",
    title: () => i18next.t("My Uploads"),
    description: () => i18next.t("Your deposited records"),
    icon: "file alternate outline",
    url: "/me/uploads",
  },
  {
    key: "requests",
    title: () => i18next.t("My Requests"),
    description: () => i18next.t("Open and closed requests"),
    icon: "tasks",
    url: "/me/requests",
  },
  {
    key: "curations",
    title: () => i18next.t("Curation Requests"),
    description: () => i18next.t("Review and manage submissions"),
    icon: "clipboard check",
    url: "/curations/overview",
    curatorOnly: true,
  },
  {
    key: "upload-dataset",
    title: () => i18next.t("Upload Dataset"),
    description: () => i18next.t("Deposit research data"),
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
    marc21Only: true,
    highlight: true,
  },
];

export function DashboardOverview({ showCurations, showPublications }) {
  const boxes = NAV_BOXES.filter(box =>
    (!box.curatorOnly || showCurations) &&
    (!box.marc21Only || showPublications)
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
