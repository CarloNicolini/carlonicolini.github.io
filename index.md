---
layout: default
title: "Carlo Nicolini – AI Research Scientist"
description: "Senior AI Scientist at Ipazia. Research in modern artificial intelligence, machine learning, mechanistic interpretability, computational neuroscience, complex systems and statistical physics. Maintainer of skfolio. PhD in statistical physics and neuroscience."
sitemap:
  priority: 1.0
  changefreq: weekly
---

<div class="row">
  <div class="col-xs-9">
    <h2>About Me</h2>
    <p>
      Hi, I’m Carlo Nicolini—a physicist turned computational scientist, now Senior AI Research Scientist at <a href="https://ipazia.com">Ipazia SpA</a> in Milan. I build multi-agent AI systems, explore deep learning, and maintain <a href="https://www.skfolio.org">skfolio</a> for portfolio optimization.
    </p>
    <p>
      My research bridges statistical physics, complex networks, and artificial intelligence. Lately, I’m focused on making transformers more interpretable and applying machine learning to finance and language. I publish at conferences like ICAIF and COLM, and you can find my work on <a href="https://scholar.google.com/citations?user=jnpIfCwAAAAJ&hl=it">Google Scholar</a>.
    </p>
    <ul>
      <li>Senior AI Scientist, Ipazia SpA (2022–present)</li>
      <li>Maintainer of skfolio (portfolio optimization in Python)</li>
      <li>Research: complex systems, AI, statistical physics, NLP, interpretability</li>
    </ul>
  </div>
  <div class="col-xs-3">
    <img src="static/img/nicolini4.jpg" style="float: right; width: 100%" alt="Carlo Nicolini portrait">
  </div>
</div>

<br>


<h2>
My latest blog posts
</h2>
<p>
</p>
<ul class="post-list">
{% for post in site.categories.tech limit:5%}
<li>
<a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
</li>
{% endfor %}
</ul>


<h2>My PhD studies</h2>
<div class="row">
<div class="col-xs-12">
In my PhD I tackled the problem of modular structure identification in brain functional networks, from the point of view of complex networks. 
Complex networks theory offers a framework for the analysis of brain functional connectivity as measured by magnetic resonance imaging. Within this approach the brain is represented as a graph comprising nodes connected by links, with nodes corresponding to brain regions and the links to measures of inter-regional interaction. A number of graph theoretical methods have been proposed to analyze the modular structure of these networks. The most widely used metric is Newman's Modularity, which identifies modules within which links are more abundant than expected on the basis of a random network. However, Modularity is limited in its ability to detect relatively small communities, a problem known as resolution limit.
<br>
To read more, <a href="https://github.com/CarloNicolini/PHDThesis/blob/6ed9e25256b28ee7a71e2a0213067b416c566a9f/thesis_nicolini_submitted.pdf"> here is my PhD thesis.</a>
</div>
</div>
<hr/>

<div class="row">
<div class="col-xs-12">
<h2>Contact me</h2>
</div>
<div class="col-xs-12">
Find my contact on LinkedIn, then write me!
</div>
</div>
