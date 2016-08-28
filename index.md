---
layout: default
---

<h2> Facts in short</h2>
<img src="static/nicolini.jpg" style="float: right; width: 20%">
<p>Phyisicst.</p>
<p>Scientific Programmer.</p>
<p>Interest in complex systems and the their applications in neuroscience.</p>
<p>PhD Candidate, University of Verona, Italy.</p>
<p>Research technician, Istituto Italiano di Tecnologia, Rovereto, Italy.</p>
([map](https://www.google.com/maps/place/Roveret://www.google.com/maps/place/38068+Rovereto+TN,+It%C3%A1lie/@47.2603133,11.7074777,5z/data=!4m2!3m1!1s0x47820ec143127041:0x6a9664123aebfadf)).

<h3> Longer story </h3>

<p>In my career I've always been involved with the biological aspects and applications of computation. I've started with Monte Carlo methods in radiation treatment planning, then moved to machine learning and now I'm focusing my attentions on computational models of brain fMRI activity with the tools of statistical physics.
</p>
<p>For a list of publications and conferences, look the Publications section in the blog.</p>

<hr/>

<h2>Recent posts</h2>

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
