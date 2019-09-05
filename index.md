---
layout: default
---

<!-- <img src="static/img/CNCS.png" style="right; width: 15%">
<img src="static/img/UNIVR.jpg" style="right; width: 15%"> -->

<div class="row">
	<div class="col-xs-9">
	<h2>Presentation</h2>
	</div>
</div>
<div class="row">
	<div class="col-xs-8">
		<p>Physicist by education, I enjoy studying complex networks with tools from physics (statistical mechanics) and machine learning.
		I am a scientific programmer with real-world expertise in C/C++, Matlab and Python and the ability to learn very fast any new programming framework for data analysis.
		I like to tackle new problems that require mathematical modeling and advanced computational methods.
		<br>
		</p>
	</div>
	<div class="col-xs-4">
		<img src="static/img/nicolini4.jpg" style="float: right bottom; width: 100%">
	</div>
	<br>
</div>

I've always been involved with scientific computation in general.
In this last years, as a postdoctoral researcher, I've focused my studies in the **complex interaction** between the **physics of machine learning**, the **complexity of large scale networked systems**, and **probability theory**.
All this theoretical stuff is always followed by numerical simulations, done with the latest Python libraries, and when necessary using C++ and their highly efficient compiled numerical libraries.

I am now working on computational models of brain fMRI activity exploiting the powerful theoretical machinery of complex networks.

This blog contains temporary results, vague ideas and notebooks that I collect during my daily work.
For this reason, **most of the content of this website is under construction**, and mathematical contents are not complete, so please do not take it for granted.

<hr/>

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

<!-- <p>
</p>
<hr/>
<p>
</p> -->
<!-- 
<div>
<h2>Research interests</h2>
<div class="row">
<div class="col-xs-12">
I am currently working on methodological aspects of complex network theory, as applied to brain functional connectivity.
Typically FC networks are obtained from Pearson correlation of BOLD time series.
The transformation from a correlation matrix to a graph is justified only based empirical arguments.
It turns out indeed that many network-theoretical quantities are crucially dependent on how this conceptual passage is performed, which is heavily affected by a multitude nuisance factors.
</div>
</div>
</div> -->

<p>
</p>
<hr/>
<p>
</p>

<div class="row">
<div class="col-xs-12">
<h2>Contact me</h2>
</div>
<div class="col-xs-12">
I'm currently working at the Center for Neuroscience and Cognitive Systems of Istituto Italiano di Tecnologia, hosted at University of Trento, in the city of Rovereto, Corso Bettini 31, Italy.
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
