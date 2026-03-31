---
layout: home
title: "AI Research Scientist"
description: "Senior AI Research Scientist at Ipazia working on reliable AI systems, mechanistic interpretability, probabilistic inference, and machine learning for finance. Maintainer of skfolio. PhD in statistical physics and neuroscience."
sitemap:
  priority: 1.0
  changefreq: weekly
---

## About Me

I am Carlo Nicolini, a senior AI research scientist working at the intersection of artificial intelligence, statistical physics, computational neuroscience, and information theory.
My work is centered on problems that require both theoretical clarity and reliable execution: building models, abstractions, and scientific software that help researchers and engineers reason about complex systems with more rigor.

My early research focused on brain functional connectivity and the modular organization of neural networks, with a strong emphasis on community detection, resolution limits, and entropy-based measures of structure.
That line of work led me to develop methods and software for analyzing complex networks through the lens of statistical mechanics and information theory, including [networkqit](https://github.com/carlonicolini/networkqit), [xyz](https://github.com/carlonicolini/xyz), and others.

As a side interest, I always found the connection between the mathematical methods used in fMRI analysis and finance very striking.
This led me down the rabbit hole of quantitative finance, where I developed [scikit-portfolio](https://github.com/carlonicolini/scikit-portfolio) first, then I became involved as a maintainer of [skfolio](https://skfolio.org), a large collaborative project to improve the scientific foundations of portfolio allocation with modern optimization methods. A recurring theme in my work is taking a fragmented technical space, identifying the right abstractions, and turning them into tools, APIs, and explanations that make an entire line of work more usable.

More recently, my attention has shifted toward modern artificial intelligence.
I am particularly interested in LLM systems, [vector symbolic architectures](https://openreview.net/forum?id=MSm0VFL9pq), mechanistic interpretability, AI reliability, probabilistic language programming, and the design of scaffolds that make inference-time behavior more auditable, controllable, and semantically grounded.

In my [recent writing](/sections/science/), I explore how branching, verification, and decomposition shape the reliability of AI systems, how inference-time scaffolds can be understood as structured probabilistic procedures, and how better interfaces between theory and engineering can make advanced systems more legible and robust.

My research portfolio also extends to machine learning applications in finance and optimization, including portfolio construction, online convex optimization, and AI-assisted research workflows. Across these projects, I tend to work at the boundary between research, engineering, and real-world constraints: framing the problem clearly, choosing the right level of abstraction, and turning ideas into systems that are mathematically grounded, computationally efficient, and genuinely useful in practice.

## My contributions

I work across research, engineering, and open-source software, with publications spanning modern AI, machine learning for finance, and complex systems.
My work appears at venues such as **COLM**, **ICAIF**, **TMLR**, **EPJ Data Science**, **Physical Review E**, and **NeuroImage**, and is collected on [Google Scholar](https://scholar.google.com/citations?user=jnpIfCwAAAAJ&hl=it).

- Senior AI Research Scientist, Ipazia SpA (2022–present)
- Maintainer of [skfolio](https://www.skfolio.org) (portfolio optimization in Python)
- Research: reliable AI systems, interpretability, compound AI, NLP, optimization, complex systems
- Focus: connecting deep theory, reusable software, and collaborative research execution

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

## Latest blog posts

I maintain a research blog where I develop ideas in public, document ongoing work, and refine the conceptual foundations behind the systems and tools I build.

<ul class="post-list">
  {% for post in site.categories.science limit:5 %}
  <li>
    <h2>
      <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
    </h2>
    <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
  </li>
  {% endfor %}
</ul>

## Contact

If you are working on reliable AI systems, mechanistic interpretability, inference-time methods, or machine learning for finance, feel free to write me at [c.nicolini@ipazia.com](mailto:c.nicolini@ipazia.com).
I am also available on LinkedIn for professional contact.

Connect on [LinkedIn](https://www.linkedin.com/in/carlo-nicolini).
