<!--
SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
SPDX-License-Identifier: MIT
-->

# invenio-override

[![CI](https://github.com/tu-graz-library/invenio-override/workflows/CI/badge.svg)](https://github.com/tu-graz-library/invenio-override/actions)
[![PyPI downloads](https://img.shields.io/pypi/dm/invenio-override.svg)](https://pypi.python.org/pypi/invenio-override)
[![Release](https://img.shields.io/github/tag/tu-graz-library/invenio-override.svg)](https://github.com/tu-graz-library/invenio-override/releases)
[![License](https://img.shields.io/github/license/tu-graz-library/invenio-override.svg)](https://github.com/tu-graz-library/invenio-override/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An InvenioRDM package based on [InvenioRDM](https://inveniosoftware.org/products/rdm/), built and maintained by [Graz University of Technology](https://www.tugraz.at).

`invenio-override` is installed as a package in your InvenioRDM instance. Each institution provides their own theme on top of it. Same package, different institutions.

**Features:**

- Custom header template
- Custom footer template
- Custom login/signup templates
- Custom frontpage template
- Custom contact template
- Overridden theme

---

## Configuration

All available `OVERRIDE_*` configuration variables with descriptions and default values are documented in [`invenio.cfg.example`](invenio.cfg.example). Copy the relevant sections into your instance's `invenio.cfg` and adjust the values for your institution.

---

## Supports

**Default**
- [invenio-rdm-records](https://github.com/inveniosoftware/invenio-rdm-records)
- [invenio-global-search](https://github.com/tu-graz-library/invenio-global-search)
- [invenio-curations](https://github.com/tu-graz-library/invenio-curations)

**Optional extras**
- [invenio-records-lom](https://github.com/tu-graz-library/invenio-records-lom) (OER)
- [invenio-records-marc21](https://github.com/tu-graz-library/invenio-records-marc21) (Publications)
- [invenio-edugain](https://github.com/tu-graz-library/invenio-edugain)
  - Make sure to have `EDUGAIN_LOGIN_ENABLED = True` to see the edugain login option

To install invenio-override with an extra: `uv pip install invenio-override[edugain]`
