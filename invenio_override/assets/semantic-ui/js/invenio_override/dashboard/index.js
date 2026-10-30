/*
 * SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import { DashboardOverview } from "./DashboardOverview";
import React from "react";
import ReactDOM from "react-dom";

const container = document.getElementById("dashboard-overview");
if (container) {
  const showLom = container.dataset.showLom === "true";
  const showCurations = container.dataset.showCurations === "true";
  const showPublications = container.dataset.showPublications === "true";
  const canUploadPublications =
    container.dataset.canUploadPublications === "true";
  const canUploadOer = container.dataset.canUploadOer === "true";
  ReactDOM.render(
    <DashboardOverview
      showLom={showLom}
      showCurations={showCurations}
      showPublications={showPublications}
      canUploadPublications={canUploadPublications}
      canUploadOer={canUploadOer}
    />,
    container,
  );
}
