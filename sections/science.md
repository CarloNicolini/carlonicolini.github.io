---
layout: page
title: Science and math
description: "Science and math posts: ML, networks, statistical physics, tutorials."
permalink: /sections/science
inheader: true
---

In this collection of articles I'm trying to answer some of the questions that arise in doing science, math and programming.

Posts are grouped by theme. Open a theme for a compact list (date + title), or use [search]({{ '/search/' | relative_url }}) to find a topic across the whole site.

<nav class="theme-hub" aria-label="Science themes">
  <a class="theme-hub__card" href="{{ '/sections/science/language-physics/' | relative_url }}">
    <h2 class="theme-hub__title">Language physics</h2>
    <p class="theme-hub__blurb">PLP, inference-time steering, energy-based views of LLMs.</p>
  </a>
  <a class="theme-hub__card" href="{{ '/sections/science/complex-networks/' | relative_url }}">
    <h2 class="theme-hub__title">Complex networks</h2>
    <p class="theme-hub__blurb">Models, spectra, community structure.</p>
  </a>
  <a class="theme-hub__card" href="{{ '/sections/science/statistical-learning/' | relative_url }}">
    <h2 class="theme-hub__title">Statistical learning</h2>
    <p class="theme-hub__blurb">Classical ML, probability, linear algebra, short tutorials.</p>
  </a>
</nav>

<ul class="post-list post-list--compact">
{% assign recent_science = site.categories.science | sort: 'date' | reverse %}
{% for post in recent_science limit: 8 %}
  <li>
    <time class="post-list--compact__date" datetime="{{ post.date | date: '%Y-%m-%d' }}">{{ post.date | date: "%Y-%m-%d" }}</time>
    <a class="post-list--compact__link" href="{{ post.url | relative_url }}">{{ post.title }}</a>
  </li>
{% endfor %}
</ul>

<p class="section-description hub-next"><a href="{{ '/sections/science/all/' | relative_url }}">Browse all science notes (compact list)</a> · <a href="{{ '/search/' | relative_url }}">Search the site</a></p>
