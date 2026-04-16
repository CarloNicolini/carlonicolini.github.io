---
layout: page
title: Search
description: "Search across science and tech posts by title, excerpt, or category."
permalink: /search/
inheader: true
---

<p class="section-description">Type a word or phrase. Matching is simple substring search over title, excerpt, categories, and tags (all posts, client-side).</p>

<div class="site-search">
  <label class="site-search__label" for="site-search-input">Search</label>
  <input type="search" id="site-search-input" class="site-search__input" autocomplete="off" placeholder="e.g. variational, spark, portfolio…" />
  <p class="site-search__meta" id="site-search-count" aria-live="polite"></p>
  <ul class="site-search__results post-list post-list--compact" id="site-search-results" hidden></ul>
</div>

{% include site-search.html %}
