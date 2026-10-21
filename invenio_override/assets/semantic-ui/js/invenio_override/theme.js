import "semantic-ui-css";

import $ from "jquery";
import { CommunitiesResults } from "./CommunitiesResults";
import { CommunityCards } from "./communities/CommunityCards";
import { MultipleOptionsSearchBar } from "@js/invenio_search_ui/components";
import React from "react";
import ReactDOM from "react-dom";
import { UploadsResults } from "./UploadsResults";
import { i18next } from "@translations/invenio_override/i18next";
import { initSearchSwitcher } from "./searchSwitcher";
import { overrideStore } from "react-overridable";

overrideStore.add(
  "InvenioAppRdm.DashboardUploads.SearchApp.results",
  UploadsResults,
);
overrideStore.add("SearchApp.results", UploadsResults);
overrideStore.add("InvenioAppRdm.Search.SearchApp.results", UploadsResults);
overrideStore.add(
  "GlobalSearchRecords.Search.SearchApp.results",
  UploadsResults,
);
overrideStore.add(
  "InvenioAppRdm.DashboardCommunities.SearchApp.results",
  CommunitiesResults,
);
overrideStore.add("SearchApp.resultOptions", () => null);
overrideStore.add("InvenioAppRdm.Search.SearchApp.resultOptions", () => null);
overrideStore.add(
  "GlobalSearchRecords.Search.SearchApp.resultOptions",
  () => null,
);

/* FOUC guard reveal: fouc_guard.html hides the body, this shows it once
   the page has loaded. Lives in the bundle instead of an inline script so
   it also runs with a CSP without 'unsafe-inline' in script-src. */
function revealPage() {
  document.body.classList.add("ready");
}
if (document.readyState === "complete") {
  revealPage();
} else {
  window.addEventListener("load", revealPage);
}

/* sticky notification setup for test instance */
$(".ui.sticky.instance-banner").sticky({
  context: "body",
});

/* keep the top navigation bar visible while scrolling */
document.addEventListener("DOMContentLoaded", function () {
  const topbar = document.querySelector(".header-topbar");
  if (!topbar) {
    return;
  }
  const spacer = document.createElement("div");
  let stuck = false;
  window.addEventListener(
    "scroll",
    function () {
      if (!stuck && topbar.getBoundingClientRect().top <= 0) {
        spacer.style.height = `${topbar.offsetHeight}px`;
        topbar.before(spacer);
        topbar.classList.add("header-topbar--stuck");
        stuck = true;
      } else if (stuck && spacer.getBoundingClientRect().top > 0) {
        topbar.classList.remove("header-topbar--stuck");
        spacer.remove();
        stuck = false;
      }
    },
    { passive: true },
  );
});

const DEFAULT_LOGO = "/static/images/square-placeholder.png";

document.addEventListener("DOMContentLoaded", function () {
  /* Frontpage search bar */
  const frontpageSearchbar = document.getElementById("frontpage-search-bar");
  if (frontpageSearchbar) {
    let searchBarOptions;
    try {
      searchBarOptions = JSON.parse(frontpageSearchbar.dataset.options);
    } catch (e) {
      console.warn("frontpage-search-bar: invalid data-options JSON", e);
    }
    if (!searchBarOptions) {
      return;
    }
    ReactDOM.render(
      <div className="ui fluid input frontpage-search-container">
        <MultipleOptionsSearchBar
          options={searchBarOptions}
          placeholder={
            frontpageSearchbar.dataset.placeholder ||
            i18next.t(
              "Use this dropdown to search across different resource types",
            )
          }
        />
      </div>,
      frontpageSearchbar,
    );
  }

  /* Communities page — replace with nav boxes */
  const communitiesFrontpage = document.querySelector(".communities-frontpage");
  if (communitiesFrontpage) {
    communitiesFrontpage.innerHTML = "";
    communitiesFrontpage.classList.add("override-ready");
    ReactDOM.render(
      <div className="dashboard-nav-grid">
        <a href="/me/communities" className="dashboard-nav-box">
          <div className="dashboard-nav-box-circle">
            <i className="users icon" />
          </div>
          <span className="dashboard-nav-box-title">
            {i18next.t("My Communities")}
          </span>
          <span className="dashboard-nav-box-desc">
            {i18next.t("Communities you own or are a member of")}
          </span>
        </a>
        <a href="/communities-search" className="dashboard-nav-box">
          <div className="dashboard-nav-box-circle">
            <i className="globe icon" />
          </div>
          <span className="dashboard-nav-box-title">
            {i18next.t("All Communities")}
          </span>
          <span className="dashboard-nav-box-desc">
            {i18next.t("Browse and discover all communities")}
          </span>
        </a>
        <a
          href="/communities/new"
          className="dashboard-nav-box dashboard-nav-box-highlight"
        >
          <div className="dashboard-nav-box-circle">
            <i className="plus icon" />
          </div>
          <span className="dashboard-nav-box-title">
            {i18next.t("New Community")}
          </span>
          <span className="dashboard-nav-box-desc">
            {i18next.t("Create a new community")}
          </span>
        </a>
      </div>,
      communitiesFrontpage,
    );
  }
});

/* function to toggle visibility of an element by ID
export function toggleVisibility(id) {
  const element = document.getElementById(id);
  const isHidden = element.style.display === "none";
  element.style.display = isHidden ? "block" : "none";
}
window.toggleVisibility = toggleVisibility;
*/

/* ======================================
   Search sidebar — collapsible facets
   GridResponsiveSidebarColumn renders <aside class="column"> (no .sidebar-container).
   React mounts async so we use MutationObserver.
====================================== */
function initFacetCollapse() {
  // Use document-level delegation so it works for both desktop aside and mobile sidebar
  if (document.body.dataset.facetCollapseReady) {
    return;
  }
  document.body.dataset.facetCollapseReady = "1";

  document.body.addEventListener("click", function (e) {
    const header = e.target.closest(
      "aside.column .ui.card.borderless.facet > .content > h2.header",
    );
    if (!header) {
      return;
    }
    if (e.target.closest("button")) {
      return;
    }

    const card = header.closest(".ui.card.borderless.facet");
    if (card.classList.contains("mt-0")) {
      return;
    }

    card.classList.toggle("facet-collapsed");
  });
}

function watchForSearchSidebar() {
  if (document.querySelector("aside.column .ui.card.borderless.facet")) {
    initFacetCollapse();
    return;
  }
  const observer = new MutationObserver(function () {
    if (document.querySelector("aside.column .ui.card.borderless.facet")) {
      observer.disconnect();
      initFacetCollapse();
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });
}

document.addEventListener("DOMContentLoaded", watchForSearchSidebar);
document.addEventListener("DOMContentLoaded", initSearchSwitcher);

document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.querySelector(".header-mobile-toggle");
  const nav = document.querySelector(".header-mobile-nav");
  if (!toggle || !nav) {
    return;
  }

  toggle.addEventListener("click", function (e) {
    e.stopPropagation();
    const open = nav.classList.toggle("is-open");
    toggle.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
  });

  document.addEventListener("click", function (e) {
    if (!toggle.contains(e.target) && !nav.contains(e.target)) {
      nav.classList.remove("is-open");
      toggle.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    }
  });

  /* Mobile: */
  nav.querySelectorAll(".header-topbar-dropdown").forEach(function (dropdown) {
    const arrow = dropdown.querySelector(
      ":scope > .header-topbar-link .topbar-arrow",
    );
    const menu = dropdown.querySelector(".header-topbar-dropdown-menu");
    if (!arrow || !menu) {
      return;
    }

    arrow.addEventListener("click", function (e) {
      if (window.innerWidth >= 768) {
        return;
      }
      e.preventDefault();
      e.stopPropagation();
      const isOpen = menu.style.display === "block";
      nav
        .querySelectorAll(".header-topbar-dropdown-menu")
        .forEach(function (m) {
          m.style.display = "";
        });
      menu.style.display = isOpen ? "" : "block";
    });
  });
});

/* Frontpage tabbed section: Recent uploads <-> New communities.*/
function initFrontpageTabs() {
  const root = document.querySelector(".frontpage-tabbed");
  if (!root) {
    return;
  }

  const activate = (name) => {
    root.querySelectorAll(".frontpage-tab").forEach((tab) => {
      tab.classList.toggle("active", tab.dataset.tab === name);
    });
    root.querySelectorAll(".frontpage-tab-panel").forEach((panel) => {
      panel.hidden = panel.dataset.panel !== name;
    });
    root.querySelectorAll(".more[data-more]").forEach((link) => {
      link.hidden = link.dataset.more !== name;
    });
  };

  root.querySelectorAll(".frontpage-tab").forEach((tab) => {
    tab.addEventListener("click", () => activate(tab.dataset.tab));
    tab.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        activate(tab.dataset.tab);
      }
    });
  });
}

document.addEventListener("DOMContentLoaded", initFrontpageTabs);
