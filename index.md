---
layout: default
---

<h2>About me</h2>
<img src="static/nicolini.jpg" style="float: right; width: 30%">
I'm Carlo Nicolini, a graduate student at the University of Verona and working in parallel at the Center for Neuroscience and Cognitive Systems (Istituto Italiano di Tecnologia) in Rovereto, Italy. 


<!-- ([map](https://www.google.com/maps/place/Roveret://www.google.com/maps/place/38068+Rovereto+TN,+It%C3%A1lie/@47.2603133,11.7074777,5z/data=!4m2!3m1!1s0x47820ec143127041:0x6a9664123aebfadf)). -->

<h2> Bio </h2>
I have multiple interests, all of them with a common baseline: computational approaches to neuroscience.
In my experience I've spanned multiple fields and applications 

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
