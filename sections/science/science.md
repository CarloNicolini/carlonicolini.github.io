---
layout: page
title: Blog
permalink: /sections/science
inheader: true
---

<ul class="post-list">
    {% for post in site.sections.science.posts %}
        <li>
            <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
            <h2>
                <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
            </h2>
            {{ post.excerpt }}
        </li>
    {% endfor %}
</ul>
