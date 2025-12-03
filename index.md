---
layout: default
---

<!-- <img src="static/img/CNCS.png" style="right; width: 15%">
<img src="static/img/UNIVR.jpg" style="right; width: 15%"> -->

<div class="row">
  <div class="col-xs-9">
    <h2>About Me</h2>
    <p>
      Hi, I’m Carlo Nicolini—a physicist turned computational scientist, now Senior AI Scientist at <a href="https://ipazia.com">Ipazia SpA</a> in Milan. I build multi-agent AI systems, explore deep learning, and maintain <a href="https://www.skfolio.org">skfolio</a> for portfolio optimization.
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
{% for post in site.categories.science limit:5%}
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
To read more, <a href="https://www.dropbox.com/s/8o2hlws6bv21ogq/thesis_nicolini_submitted.pdf?dl=0">download my PhD thesis.</a>
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

<!-- <br>
<address>
<strong>Carlo Nicolini</strong><br>
Center for Neuroscience and Cognitive Systems<br>
Corso Bettini 31<br>
38086 Rovereto<br>
Italy<br>
</address> -->

<!-- 
<h2>Recently posted</h2>

<ul class="post-list">
    {% for post in site.posts limit:3 %}
        <li>
            <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
            <h2>
                <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
            </h2>
            {{ post.excerpt }}
        </li>
    {% endfor %}
</ul>
-->
