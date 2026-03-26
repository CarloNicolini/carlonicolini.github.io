---
layout: home
title: "AI Research Scientist"
description: "Senior AI Scientist at Ipazia. Research in modern artificial intelligence, machine learning, mechanistic interpretability, computational neuroscience, complex systems and statistical physics. Maintainer of skfolio. PhD in statistical physics and neuroscience."
sitemap:
  priority: 1.0
  changefreq: weekly
---

## About Me

I am Carlo Nicolini, an AI research scientist working at the intersection of artificial intelligence, statistical physics, computational neuroscience, and information theory.

My early research focused on brain functional connectivity and the modular organization of neural networks, with a strong emphasis on community detection, resolution limits, and entropy-based measures of structure.
That line of work led me to develop methods and software for analyzing complex networks through the lens of statistical mechanics and information theory, including [networkqit](https://github.com/carlonicolini/networkqit), [xyz](https://github.com/carlonicolini/xyz), and other tools for spectral entropy, mutual information, and directed information flow.
As a side interest, I always found the connection between the mathematical methods used in fMRI analysis and finance very striking.
This led me down the rabbit hole of quantitative finance, where I developed [scikit-portfolio](https://github.com/carlonicolini/scikit-portfolio) first, then I became involved as a maintainer of [skfolio](https://skfolio.org) a large collaborative project to improve the scientific aspects of financial portfolio allocation with the latest cutting edge mathematical methods.

More recently, my attention has shifted toward modern artificial intelligence.
I am particularly interested in LLM systems, [vector symbolic architectures](https://openreview.net/forum?id=MSm0VFL9pq), mechanistic interpretability, agent reliability, probabilistic language programming, and the design of scaffolds that make inference-time behavior more auditable and semantically grounded.
In my recent writing, I explore how branching, verification, and decomposition shape the reliability of AI systems, and how we can reason about them as probabilistic programs rather than opaque chains of prompts.

My research portfolio also extends to machine learning applications in finance and optimization, including portfolio construction, online convex optimization, and AI-assisted research workflows. Across all these projects, I am drawn to the same core question: how can we build models and systems that are mathematically grounded, computationally efficient, and genuinely useful in practice?

## My interests

Lately, I am interested in mechanistic interpretability of large language models, theoretical foundations of compound AI systems, and machine learning for language and finance.

I'm a contributor to many open-source ML tools and occasionally work in the statistical physics of complex systems. I've published at venues like **COLM** and **ICAIF**, and my work appears on [Google Scholar](https://scholar.google.com/citations?user=jnpIfCwAAAAJ&hl=it).

- Senior AI Research Scientist, Ipazia SpA (2022–present)
- Maintainer of [skfolio](https://www.skfolio.org) (portfolio optimization in Python)
- Research: interpretability, multi-agent systems, NLP, complex systems, statistical physics

<h2>Selected publications</h2>
<p>
  Recent work on LLM interpretability, NLP, and statistical physics. <a href="{{ site.baseurl }}/sections/publications">Full list →</a>
</p>
<ul class="post-list">
  {% for pub in site.data.publications %}
    {% if pub.title and forloop.index <= 4 %}
  <li>
    <a class="post-link" href="{% if pub.url %}{{ pub.url }}{% elsif pub.pdf %}{{ pub.pdf }}{% endif %}">{{ pub.title }}</a>
    <span class="post-meta"> — {{ pub.authors | default: pub.author }}{% if pub.journal %}, {{ pub.journal }}{% endif %}{% if pub.year %} ({{ pub.year }}){% endif %}</span>
  </li>
    {% endif %}
  {% endfor %}
</ul>

<h2>Software &amp; code</h2>
<p>
  Open-source projects I develop or maintain. <a href="{{ site.baseurl }}/sections/software">Full list →</a>
</p>
<ul class="post-list">
  {% assign count = 0 %}
  {% for code in site.data.software %}
    {% if code.name and count < 6 %}
  <li>
    <a class="post-link" href="{% if code.documentation %}{{ code.documentation }}{% elsif code.github %}{{ code.github }}{% endif %}">{{ code.name }}</a>
    — {{ code.description }}
    {% if code.github %} <a href="{{ code.github }}">GitHub</a>{% endif %}
  </li>
      {% assign count = count | plus: 1 %}
    {% endif %}
  {% endfor %}
</ul>

<h2>Latest blog posts</h2>
<ul class="post-list">
  {% for post in site.categories.tech limit:5 %}
  <li>
    <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
  </li>
  {% endfor %}
</ul>

<h2>Latest science posts</h2>
<ul class="post-list">
  {% for post in site.categories.science limit:5 %}
  <li>
    <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
  </li>
  {% endfor %}
</ul>

## PhD studies

In my PhD I tackled the problem of modular structure identification in brain functional networks, from the point of view of complex networks.
Complex networks theory offers a framework for the analysis of brain functional connectivity as measured by magnetic resonance imaging. Within this approach the brain is represented as a graph comprising nodes connected by links, with nodes corresponding to brain regions and the links to measures of inter-regional interaction. A number of graph theoretical methods have been proposed to analyze the modular structure of these networks. The most widely used metric is Newman's Modularity, which identifies modules within which links are more abundant than expected on the basis of a random network. However, Modularity is limited in its ability to detect relatively small communities, a problem known as resolution limit.

To read more, [here is my PhD thesis.](https://github.com/CarloNicolini/PHDThesis/blob/6ed9e25256b28ee7a71e2a0213067b416c566a9f/thesis_nicolini_submitted.pdf)

## Contact

Find my contact on [LinkedIn](https://www.linkedin.com/in/carlo-nicolini), then write me!
