// Copyright (C) 2020-2026 Graz University of Technology.

import { CommunityCards } from "./CommunityCards";
import React from "react";
import ReactDOM from "react-dom";

const DEFAULT_LOGO = "/static/images/square-placeholder.png";

document.addEventListener("DOMContentLoaded", () => {

  const subheader = document.querySelector(".page-subheader");
  if (subheader) {
    subheader.querySelector("h1.ui.header")?.closest(".row")?.remove();
    subheader.querySelector("p")?.closest(".row")?.remove();
  }

  const userContainer = document.getElementById("user-communities");
  if (userContainer) {
    ReactDOM.render(
      <CommunityCards
        fetchUrl="/api/user/communities?size=10"
        defaultLogo={DEFAULT_LOGO}
        emptyMessage="You are not a member of any community yet."
      />,
      userContainer
    );
  }

  const newContainer = document.getElementById("new-communities");
  if (newContainer) {
    ReactDOM.render(
      <CommunityCards
        fetchUrl="/api/communities?sort=newest&size=10"
        defaultLogo={DEFAULT_LOGO}
        emptyMessage="No communities yet."
      />,
      newContainer
    );
  }
});

