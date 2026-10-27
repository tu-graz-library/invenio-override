# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2026 Graz University of Technology.
#
# invenio-override is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Advanced search query builder tests."""

from invenio_override.views import build_query

FIELDS = [
    {"name": "title", "kind": "text", "query": "metadata.title"},
    {"name": "license", "kind": "select", "query": "metadata.rights.id"},
    {"name": "date", "kind": "daterange", "query": "metadata.publication_date"},
]


def test_build_query_empty():
    """No filled fields gives an empty query."""
    assert build_query({}, FIELDS) == ""
    assert build_query({"title": "  "}, FIELDS) == ""


def test_build_query_text_is_quoted():
    """Text values are quoted as a phrase."""
    query = build_query({"title": "deep learning"}, FIELDS)
    assert query == 'metadata.title:"deep learning"'


def test_build_query_escapes_quotes():
    """Quotes and backslashes in the value are escaped."""
    query = build_query({"title": 'say "hi" \\now'}, FIELDS)
    assert query == 'metadata.title:"say \\"hi\\" \\\\now"'


def test_build_query_select_is_raw():
    """Select values are vocabulary ids and stay unquoted."""
    query = build_query({"license": "cc-by-4.0"}, FIELDS)
    assert query == "metadata.rights.id:cc-by-4.0"


def test_build_query_daterange():
    """Date ranges use open bounds for missing ends."""
    assert (
        build_query({"date_from": "2020", "date_to": "2021"}, FIELDS)
        == "metadata.publication_date:[2020 TO 2021]"
    )
    assert (
        build_query({"date_from": "2020"}, FIELDS)
        == "metadata.publication_date:[2020 TO *]"
    )
    assert (
        build_query({"date_to": "2021"}, FIELDS)
        == "metadata.publication_date:[* TO 2021]"
    )


def test_build_query_joins_with_and():
    """Multiple filled fields are AND joined."""
    query = build_query({"title": "x", "license": "mit"}, FIELDS)
    assert query == 'metadata.title:"x" AND metadata.rights.id:mit'
