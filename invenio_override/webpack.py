# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2026 Graz University of Technology.
#
# invenio-override  is free software.

"""JS/CSS Webpack bundles for theme."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "invenio-override-theme": "./less/invenio_override/theme.less",
                "invenio-override-js": "./js/invenio_override/theme.js",
                "invenio-override-dashboard": "./js/invenio_override/dashboard/index.js",
                "invenio-override-communities": "./js/invenio_override/communities/index.js",
            },
            dependencies={
                "jquery": "^3.2.1",
                # Peer dependencies required by react-searchkit 3.x
                "@visx/scale": "^3.12.0",
                "@visx/shape": "^3.12.0",
                "@visx/responsive": "^3.12.0",
            },
        )
    },
)
