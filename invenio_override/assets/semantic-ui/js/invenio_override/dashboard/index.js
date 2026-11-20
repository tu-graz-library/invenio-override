/*
 * SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
 * SPDX-FileCopyrightText: 2026 University of Graz.
 * SPDX-License-Identifier: MIT
 */

import { DashboardOverview } from "./DashboardOverview";
import React from "react";
import ReactDOM from "react-dom";

const container = document.getElementById("dashboard-overview");
if (container) {
  let entries = [];
  try {
    entries = JSON.parse(container.dataset.entries || "[]");
  } catch (e) {
    entries = [];
  }
  ReactDOM.render(<DashboardOverview entries={entries} />, container);
}
