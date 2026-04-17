// Copyright (C) 2020-2026 Graz University of Technology.
// invenio-override is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { Image, http } from "react-invenio-forms";
import { i18next } from "@translations/invenio_override/i18next";
import React, { Component } from "react";

class CommunityCard extends Component {
  render() {
    const { community, defaultLogo } = this.props;
    const title = community.metadata?.title || i18next.t("Untitled");
    const description = community.metadata?.description || "";
    const href = `/communities/${community.slug}`;

    return (
      <a href={href} className="override-community-card">
        <div className="override-community-card-logo">
          <Image
            src={community.links?.logo}
            fallbackSrc={defaultLogo}
            loadFallbackFirst
            alt={title}
          />
        </div>
        <div className="override-community-card-body">
          <span className="override-community-card-title">{title}</span>
          {description && (
            <span className="override-community-card-desc">{description}</span>
          )}
        </div>
      </a>
    );
  }
}

export class CommunityCards extends Component {
  constructor(props) {
    super(props);
    this.state = { hits: [], isLoading: true };
  }

  componentDidMount() {
    const { fetchUrl } = this.props;
    http
      .get(fetchUrl, { headers: { Accept: "application/json" } })
      .then((r) => {
        const data = r.data;
        const hits = data?.hits?.hits || data?.hits || [];
        this.setState({ hits, isLoading: false });
      })
      .catch(() => this.setState({ isLoading: false }));
  }

  render() {
    const { hits, isLoading } = this.state;
    const { defaultLogo, emptyMessage } = this.props;

    if (isLoading) return null;

    if (!hits.length) {
      return (
        <p className="override-community-empty">{emptyMessage}</p>
      );
    }

    return (
      <div className="override-community-grid">
        {hits.map((community) => (
          <CommunityCard
            key={community.id}
            community={community}
            defaultLogo={defaultLogo}
          />
        ))}
      </div>
    );
  }
}
