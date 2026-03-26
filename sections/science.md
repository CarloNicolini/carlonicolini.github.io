---
layout: page
title: Science and math
permalink: /sections/science
inheader: true
---


In this collection of articles I'm trying to answer some of the questions that arise in doing science, math and programming.

<ul class="post-list">
    {% for post in site.categories.science %}
        <li>
            <h2>
                <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
            </h2>
        </li>
    {% endfor %}
</ul>

