// Copyright (C) 2020-2026 Graz University of Technology.
// invenio-override is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { Grid, Segment } from "semantic-ui-react";
import { ResultsList, Sort } from "react-searchkit";

import { InvenioSearchPagination } from "@js/invenio_search_ui/components";
import PropTypes from "prop-types";
import React from "react";
import { i18next } from "@translations/invenio_override/i18next";

export const CommunitiesResults = ({
  sortOptions,
  paginationOptions,
  currentResultsState,
}) => {
  const { total } = currentResultsState.data;

  const handleResultsRendered = () => {
    window.invenio?.onSearchResultsRendered();
  };

  return total ? (
    <Grid>
      <Grid.Row>
        <Grid.Column width={16}>
          <Segment>
            <Grid>
              <Grid.Row
                verticalAlign="middle"
                className="small pt-5 pb-5 highlight-background"
              >
                <Grid.Column width={4}>
                  {i18next.t("{{total}} result(s) found", { total })}
                </Grid.Column>
                <Grid.Column width={12} textAlign="right">
                  {sortOptions && (
                    <Sort
                      values={sortOptions}
                      label={(cmp) => <>{cmp}</>}
                    />
                  )}
                </Grid.Column>
              </Grid.Row>
              <Grid.Row>
                <Grid.Column>
                  <ResultsList onResultsRendered={handleResultsRendered} />
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </Segment>
        </Grid.Column>
      </Grid.Row>
      <InvenioSearchPagination paginationOptions={paginationOptions} />
    </Grid>
  ) : null;
};

CommunitiesResults.propTypes = {
  sortOptions: PropTypes.array,
  paginationOptions: PropTypes.object.isRequired,
  currentResultsState: PropTypes.object.isRequired,
};

CommunitiesResults.defaultProps = {
  sortOptions: null,
};
