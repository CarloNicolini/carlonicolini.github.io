---
layout: page
title: Technical stuff
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
        </li>
    {% endfor %}
</ul>
