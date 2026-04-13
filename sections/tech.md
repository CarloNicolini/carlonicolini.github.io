---
layout: page
title: Technical stuff
description: "Tech notes: devops, Python, Spark, LLMs, short how-tos."
permalink: /sections/tech
inheader: true
---

A collection of notes on system administration, efficient coding in C/C++ and Matlab, and examples of beautiful LaTeX typesetting.

<ul class="post-list">
    {% for post in site.categories.tech %}
        <li>
            <h2>
                <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
            </h2>
            <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
            <p>{{ post.excerpt | strip_html | truncatewords: 25 }}</p>
        </li>
    {% endfor %}
</ul>
