---
layout: page
title: Science and math
description: "Science and math posts: ML, networks, statistical physics, tutorials."
permalink: /sections/science
inheader: true
---


In this collection of articles I'm trying to answer some of the questions that arise in doing science, math and programming.

Posts are grouped by theme: **complex networks** (models, spectra, community structure), **language physics** (PLP, inference-time steering, energy-based views of LLMs), and **statistical learning** (classical ML, probability, linear algebra, short tutorials).

## Language physics

<ul class="post-list">
    {% assign posts = site.categories.language-physics | sort: 'date' | reverse %}
    {% for post in posts %}
        {% if post.categories contains 'science' %}
        <li>
            <h2>
                <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
            </h2>
            <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
            <p>{{ post.excerpt | strip_html | truncatewords: 25 }}</p>
        </li>
        {% endif %}
    {% endfor %}
</ul>

## Complex networks

<ul class="post-list">
    {% assign posts = site.categories.complex-networks | sort: 'date' | reverse %}
    {% for post in posts %}
        {% if post.categories contains 'science' %}
        <li>
            <h2>
                <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
            </h2>
            <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
            <p>{{ post.excerpt | strip_html | truncatewords: 25 }}</p>
        </li>
        {% endif %}
    {% endfor %}
</ul>

## Statistical learning

<ul class="post-list">
    {% assign posts = site.categories.statistical-learning | sort: 'date' | reverse %}
    {% for post in posts %}
        {% if post.categories contains 'science' %}
        <li>
            <h2>
                <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
            </h2>
            <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
            <p>{{ post.excerpt | strip_html | truncatewords: 25 }}</p>
        </li>
        {% endif %}
    {% endfor %}
</ul>
