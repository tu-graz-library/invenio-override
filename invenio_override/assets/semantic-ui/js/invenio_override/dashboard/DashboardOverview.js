/*
 * SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
 * SPDX-FileCopyrightText: 2026 University of Graz.
 * SPDX-License-Identifier: MIT
 */

import { Icon } from "semantic-ui-react";
import React from "react";

// entries: OVERRIDE_DASHBOARD_ENTRIES, filtered by visibility and
// translated on the server.
export function DashboardOverview({ entries = [] }) {
  return (
    <div className="dashboard-nav-grid">
      {entries.map((entry) => (
        <a
          key={entry.key}
          href={entry.url}
          className={`dashboard-nav-box${entry.highlight ? " dashboard-nav-box-highlight" : ""}`}
        >
          <div className="dashboard-nav-box-circle">
            <Icon name={entry.icon} />
          </div>
          <span className="dashboard-nav-box-title">{entry.title}</span>
          <span className="dashboard-nav-box-desc">{entry.description}</span>
        </a>
      ))}
    </div>
  );
}
