---
layout: page
title: Technical stuff
description: "Tech notes: devops, Python, Spark, LLMs, short how-tos."
permalink: /sections/tech/
inheader: true
---

A collection of notes on system administration, efficient coding in C/C++ and Matlab, and examples of beautiful LaTeX typesetting.

<ul class="post-list post-list--compact">
{% assign recent = site.categories.tech | sort: 'date' | reverse %}
{% for post in recent limit: 8 %}
  <li>
    <time class="post-list--compact__date" datetime="{{ post.date | date: '%Y-%m-%d' }}">{{ post.date | date: "%Y-%m-%d" }}</time>
    <a class="post-list--compact__link" href="{{ post.url | relative_url }}">{{ post.title }}</a>
  </li>
{% endfor %}
</ul>

<p class="section-description hub-next"><a href="{{ '/sections/tech/all/' | relative_url }}">Browse all tech notes (compact list)</a> · <a href="{{ '/search/' | relative_url }}">Search the site</a></p>
