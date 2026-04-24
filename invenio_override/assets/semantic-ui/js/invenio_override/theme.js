import "semantic-ui-css";

import $ from "jquery";
import { CommunitiesResults } from "./CommunitiesResults";
import { CommunityCards } from "./communities/CommunityCards";
import { MultipleOptionsSearchBar } from "@js/invenio_search_ui/components";
import React from "react";
import ReactDOM from "react-dom";
import { UploadsResults } from "./UploadsResults";
import { i18next } from "@translations/invenio_override/i18next";
import { overrideStore } from "react-overridable";

overrideStore.add("InvenioAppRdm.DashboardUploads.SearchApp.results", UploadsResults);
overrideStore.add("InvenioAppRdm.DashboardCommunities.SearchApp.results", CommunitiesResults);

/* sticky notification setup for test instance */
$(".ui.sticky.test-instance").sticky({
  context: "body",
});

const DEFAULT_LOGO = "/static/images/square-placeholder.png";

document.addEventListener("DOMContentLoaded", function () {
  /* Frontpage search bar */
  const frontpageSearchbar = document.getElementById("frontpage-search-bar");
  if (frontpageSearchbar) {
    const searchBarOptions = JSON.parse(frontpageSearchbar.dataset.options);
    ReactDOM.render(
      <div className="ui fluid input frontpage-search-container">
        <MultipleOptionsSearchBar
          options={searchBarOptions}
          placeholder={i18next.t("Use this dropdown to search across different resource types")}
        />
      </div>,
      frontpageSearchbar
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
          <span className="dashboard-nav-box-title">{i18next.t("My Communities")}</span>
          <span className="dashboard-nav-box-desc">{i18next.t("Communities you own or are a member of")}</span>
        </a>
        <a href="/communities-search" className="dashboard-nav-box">
          <div className="dashboard-nav-box-circle">
            <i className="globe icon" />
          </div>
          <span className="dashboard-nav-box-title">{i18next.t("All Communities")}</span>
          <span className="dashboard-nav-box-desc">{i18next.t("Browse and discover all communities")}</span>
        </a>
        <a href="/communities/new" className="dashboard-nav-box dashboard-nav-box-highlight">
          <div className="dashboard-nav-box-circle">
            <i className="plus icon" />
          </div>
          <span className="dashboard-nav-box-title">{i18next.t("New Community")}</span>
          <span className="dashboard-nav-box-desc">{i18next.t("Create a new community")}</span>
        </a>
      </div>,
      communitiesFrontpage
    );
  }
});

/* load Zammad script on document ready
$(function () {
  importZammadScript();
});
*/

/* function to import Zammad script for feedback form
function importZammadScript() {
  let scriptNode = document.createElement("hidden");
  scriptNode.id = "zammad_form_script";
  scriptNode.src = "URL";
  document.head.appendChild(scriptNode);

  $.getScript("URL", () => {
    $("#feedback-form").ZammadForm({
      messageTitle: "Contact us",
      showTitle: true,
      messageSubmit: "Submit",
      messageThankYou: "Thank you for your message, (#%s). We will get back to you as quickly as possible!",
      modal: true,
    });
  });
}
*/

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
  if (document.body.dataset.facetCollapseReady) return;
  document.body.dataset.facetCollapseReady = "1";

  document.body.addEventListener("click", function (e) {
    const header = e.target.closest(
      "aside.column .ui.card.borderless.facet > .content > h2.header"
    );
    if (!header) return;
    if (e.target.closest("button")) return;

    const card = header.closest(".ui.card.borderless.facet");
    if (card.classList.contains("mt-0")) return;

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

document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.querySelector(".header-mobile-toggle");
  const nav = document.querySelector(".header-mobile-nav");
  if (!toggle || !nav) return;

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
    const arrow = dropdown.querySelector(":scope > .header-topbar-link .topbar-arrow");
    const menu = dropdown.querySelector(".header-topbar-dropdown-menu");
    if (!arrow || !menu) return;

    arrow.addEventListener("click", function (e) {
      if (window.innerWidth >= 768) return;
      e.preventDefault();
      e.stopPropagation();
      const isOpen = menu.style.display === "block";
      nav.querySelectorAll(".header-topbar-dropdown-menu").forEach(function (m) {
        m.style.display = "";
      });
      menu.style.display = isOpen ? "" : "block";
    });
  });
});

/* User profile dropdown */
$("#user-profile-dropdown.ui.dropdown").dropdown({
  showOnFocus: false,
  selectOnKeydown: false,
  action: (text, value, element) => {
    let path = element.attr("href");
    window.location.pathname = path;
  },
  onShow: () => {
    $("#user-profile-dropdown-btn").attr("aria-expanded", true);
  },
  onHide: () => {
    $("#user-profile-dropdown-btn").attr("aria-expanded", false);
  },
});
