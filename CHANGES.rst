..
    Copyright (C) 2020-2026 Graz University of Technology.

    invenio-override is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

Changes
=======

Version v1.2.2 (released 2026-09-23)

- fix(frontpage): wrap header on narrow screens

Version v1.2.1 (released 2026-09-22)

- fix(translation): Community de Community

Version v1.2.0 (released 2026-09-22)

- feat(header): render notices
- fix(frontpage): move js block after extends
- fix(header): keep pinned header above deposit box
- fix(i18n): make config-driven labels extractable

Version v1.1.1 (released 2026-09-08)

- fix(i18n): replace fuzzy German guesses and resync translation catalog

Version v1.1.0 (released 2026-09-03)

- feat(header): keep top navbar visible on scroll
- feat(navbar): update header dropdown menus, add manual link to help menu
- ui(navbar): switch help/administration order
- feat(navbar): add publications to dropdown and dashboard overview, link them to the uploads dashboard
- feat(help): add help page with contact modal, search guide and file formats box
- feat(help): link via doc redirect routes
- feat(login): redesign login page and disable registration
- feat(login): add eduGAIN and SAML login options, add back to main page link
- feat(frontpage): add new communities tab, enlarge community cards
- feat(banner): show admin-managed banner on top
- feat(community): use clean banner on detail pages
- refactor(uploads): derive upload links from permissions
- feat(datamodels): override marc21 and lom uploads dashboards, match layout to OER
- feat(override): make upload roles configurable, gate OER upload by certification
- feat: configurable contact form bundle
- feat: add MARC21_SEARCH_NAV_TEMPLATE config hook
- ui: styled search results container, themed home icon, configurable logo size, green positive action buttons
- fix(theme): prevent page load flash
- fix: frontpage responsive layout, login page spacing and icons, styled flash messages
- fix(search): nav label pre-fill, recent uploads schema label, publication-date facet inset
- fix(deposit): sync deposit with upstream, marc21 deposit styling
- fix: theme issues from the test deployment
- fix(banner): keep test banner full width
- i18n: add German translations for new strings and pages
- docs: update documentation
- chore(styling): update variables.less
- chore: pin djlint to 1.36.4, add it as test dependency, reformat templates

Version v1.0.0 (released 2026-05-19)

- feat: complete UI redesign — new frontpage, header, navbar, dashboard
- feat: mobile responsive layout
- feat: search type switcher with query persistence across resource types
- feat: permission-based dashboard navigation circles
- feat: design tokens (LESS variables) for consistent theming
- feat: OER uploads page matching Research Results layout
- feat: generic error page templates (404, 500, 423)
- feat: deposit page descriptions via context processor
- feat: SAML login option
- feat: admin theme improvements
- fix: duplicate result count on search pages
- fix: remove double banner
- chore: upgrade to invenio-app-rdm v14
- chore: cleanup and documentation update

Version v0.0.7 (released 2025-02-11)

- refactor: overview responsiveness on the front page
- fix: footer_mug search guide
- fix: issues header when no lang
- ui: tailor navbar/frontpage to Research Results
- add restriction to admins
- Set ENV in overview section

Version v0.0.6 (released 2025-05-20)

- i18n: fix typo on fuzzy
- ci: update publish dependencies

Version v0.0.5 (released 2025-05-20)

- ui: improvements and bug fixes
- global: invenio-app-rdm v13
- global: split and move invenio-global-search dependencies to extras

Version v0.0.4 (released 2024-11-25)

- global: MUG requirements integrated

Version v0.0.3 (released 2024-02-02)

- global: configs naming

Version v0.0.2 (released 2024-02-02)

- global: remove scss

Version v0.0.1 (released 2024-02-01)

- global: init repository
