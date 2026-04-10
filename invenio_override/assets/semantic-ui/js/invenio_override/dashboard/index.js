// Copyright (C) 2020-2026 Graz University of Technology.
//
// invenio-override is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { DashboardOverview } from "./DashboardOverview";
import React from "react";
import ReactDOM from "react-dom";

const container = document.getElementById("dashboard-overview");
if (container) {
  const showCurations = container.dataset.showCurations === "true";
  const showPublications = container.dataset.showPublications === "true";
  ReactDOM.render(<DashboardOverview showCurations={showCurations} showPublications={showPublications} />, container);
}
