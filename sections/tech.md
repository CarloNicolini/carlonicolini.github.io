---
layout: page
title: Technical stuff
permalink: /sections/tech
inheader: true
---

This part of my personal blog collects many notes that I've been collecting over the times.
Most of them are about unix/linux system administration, some of them are about Matlab, others about how to code efficiently with some programming languages like C/C++.

I'm also a fan of Latex and I enjoy producing beautifully typeset documents, here are some examples of latex typesetting, too. 

<ul class="post-list">
    {% for post in site.categories.tech %}
        <li>
            <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
            <h2>
                <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
            </h2>
            {{ post.excerpt }}
        </li>
    {% endfor %}
</ul>
