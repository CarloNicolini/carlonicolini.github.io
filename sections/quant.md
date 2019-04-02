---
layout: page
title: Math problems
permalink: /sections/quant
inheader: true
---

In this collection of articles I'm trying to solve some math exercises.

<ul class="post-list">
    {% for post in site.categories.quant %}
        <li>
            <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
            <h2>
                <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
            </h2>
            <!-- {{ post.excerpt }} -->
        </li>
    {% endfor %}
</ul>

