---
layout: page
title: Business idea and how to realize them
permalink: /sections/biz
inheader: true
---

In this collection of notes I'm collecting some business ideas and some temptative to solve the challenges they present.

<ul class="post-list">
    {% for post in site.categories.biz %}
        <li>
            <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
            <h2>
                <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
            </h2>
            <!-- {{ post.excerpt }} -->
        </li>
    {% endfor %}
</ul>

