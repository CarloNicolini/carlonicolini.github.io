---
layout: default
---

<img src="static/img/nicolini.jpg" style="float: right; width: 22%">
<!-- <img src="static/img/CNCS.png" style="right; width: 10%">
<img src="static/img/UNIVR.jpg" style="right; width: 10%"> -->


## Facts in short

- Physicist by formation.
- Scientific Programmer for work.
- Network neuroscientist for study.
<!-- <p>Interest in complex systems and the their applications in neuroscience.</p> -->
- PhD Candidate, University of Verona, Italy.
- Research technician, Istituto Italiano di Tecnologia, Rovereto, Italy.

## Longer story

<p>In my career I've always been involved with computation in many of its applications. I've started with Monte Carlo methods in radiation treatment planning, then moved to machine learning. In the last years I shifted my attention to computational models of brain fMRI activity exploiting the powerful theoretical machinery of complex networks.
This blog collects results, ideas and notebooks of my work. Not all the content of this website is completely finished, so take it as it is.
</p>


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
