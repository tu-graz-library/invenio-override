<!--
  Copyright (C) 2020-2026 Graz University of Technology.

  invenio-override is free software; you can redistribute it and/or
  modify it under the terms of the MIT License; see LICENSE file for more
  details.
-->

# invenio-override

[![CI](https://github.com/sharedRDM/invenio-override/workflows/CI/badge.svg)](https://github.com/sharedRDM/invenio-override/actions)
[![PyPI downloads](https://img.shields.io/pypi/dm/invenio-override.svg)](https://pypi.python.org/pypi/invenio-override)
[![Release](https://img.shields.io/github/tag/sharedRDM/invenio-override.svg)](https://github.com/sharedRDM/invenio-override/releases)
[![License](https://img.shields.io/github/license/sharedRDM/invenio-override.svg)](https://github.com/sharedRDM/invenio-override/blob/master/LICENSE)
[![Docs](https://readthedocs.org/projects/invenio-override/badge/?version=latest)](https://invenio-override.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Override InvenioRDM theme.

**Features:**

- Custom header template
- Custom footer template
- Custom login/signup templates
- Custom frontpage template
- Custom contact template
- Overridden theme

## Configuration

All available `OVERRIDE_*` configuration variables with descriptions and
default values are documented in [`invenio.cfg.example`](invenio.cfg.example).
Copy the relevant sections into your instance's `invenio.cfg` and adjust
the values for your institution.

## Deployment

For cluster setup and operations see [themes/K3S-OPS.md](themes/K3S-OPS.md).

## Further documentation

<!-- TODO: expand this section after the PR is merged -->

https://invenio-override.readthedocs.io/
