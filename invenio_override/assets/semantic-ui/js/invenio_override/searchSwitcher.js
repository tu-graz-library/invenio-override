// Copyright (C) 2020-2026 Graz University of Technology.
// invenio-override is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import $ from "jquery";

const STORAGE_KEY = "search-switcher-q";

function saveQuery(query) {
  try {
    sessionStorage.setItem(STORAGE_KEY, query);
  } catch (_) {}
}

function getStoredQuery() {
  try {
    return sessionStorage.getItem(STORAGE_KEY) || "";
  } catch (_) {
    return "";
  }
}

function queryFromURL(urlStr) {
  try {
    const search = (urlStr || "").includes("?") ? urlStr.split("?")[1] : "";
    return new URLSearchParams(search).get("q") || "";
  } catch (_) {
    return "";
  }
}

export function initSearchSwitcher() {
  const form = document.getElementById("search-switcher-form");
  if (!form) {
    return;
  }

  const typeDropdown = document.getElementById("search-switcher-type");
  const searchInput = document.getElementById("search-switcher-input");
  const clearButton = document.getElementById("search-switcher-clear");
  const $typeDropdown = $(typeDropdown);

  function getValue() {
    return $typeDropdown.dropdown("get value") || "";
  }

  function syncAction() {
    form.action = getValue();
  }

  function syncClear() {
    clearButton.style.display = searchInput.value ? "flex" : "none";
  }

  function syncFromURL(urlStr) {
    const query = queryFromURL(urlStr);
    searchInput.value = query;
    saveQuery(query);
    syncClear();
  }

  if (!searchInput.value) {
    searchInput.value = getStoredQuery();
  }

  let initializing = true;
  $typeDropdown.dropdown({
    onChange: function (value) {
      if (initializing) {
        return;
      }
      form.action = value;
      saveQuery(searchInput.value);
      form.submit();
    },
  });

  const activeItem = typeDropdown.querySelector(".item.active");
  const firstItem = typeDropdown.querySelector(".item");
  const initValue = (activeItem || firstItem || {}).dataset.value;
  if (initValue) {
    $typeDropdown.dropdown("set selected", initValue);
  }
  initializing = false;

  const origPushState = window.history.pushState.bind(window.history);
  window.history.pushState = function (state, title, url) {
    origPushState(state, title, url);
    if (url) {
      syncFromURL(url);
    }
  };

  window.addEventListener("popstate", function () {
    syncFromURL(window.location.href);
  });

  form.addEventListener("submit", function () {
    saveQuery(searchInput.value);
    syncAction();
  });

  clearButton.addEventListener("click", function () {
    searchInput.value = "";
    saveQuery("");
    syncAction();
    form.submit();
  });

  searchInput.addEventListener("input", function () {
    saveQuery(searchInput.value);
    syncClear();
  });

  syncAction();
  syncClear();
}
