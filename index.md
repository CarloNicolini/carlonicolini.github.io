---
layout: default
---

<img src="static/img/nicolini4.jpg" style="float: right; width: 22%">
<!-- <img src="static/img/CNCS.png" style="right; width: 10%">
<img src="static/img/UNIVR.jpg" style="right; width: 10%"> -->


## Facts in short

- Physicist.
- Scientific Programmer.
- Network neuroscientist.

## Longer story

<p>In my career I've always been involved with computation in many of its applications. I've started with Monte Carlo methods in radiation treatment planning, then moved to machine learning. In the last years I shifted my attention to computational models of brain fMRI activity exploiting the powerful theoretical machinery of complex networks.
This blog collects results, ideas and notebooks of my work. Not all the content of this website is completely finished, so take it as it is.
</p>

## Contact me
I'm currently working at the **Center for Neuroscience and Cognitive Systems** of **Istituto Italiano di Tecnologia**, hosted at University of Trento, in the city of **Rovereto, Corso Bettini 31**, Italy.

<!-- 
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script><div style="overflow:hidden;height:100px;width:$device;"><div id="gmap_canvas" style="height:100px;width:$device;"><style>#gmap_canvas img{max-width:none!important;background:none!important}</style><a class="google-map-code" href="http://www.map-embed.com" id="get-map-data">embed google map</a></div><script type="text/javascript"> function init_map(){var myOptions = {zoom:14,center:new google.maps.LatLng(45.8923739,11.043936400000007),mapTypeId: google.maps.MapTypeId.ROADMAP};map = new google.maps.Map(document.getElementById("gmap_canvas"), myOptions);marker = new google.maps.Marker({map: map,position: new google.maps.LatLng(45.8923739, 11.043936400000007)});infowindow = new google.maps.InfoWindow({content:"<b>Center for Neuroscience and Cognitive Systems</b><br/>Corso Bettini 31 <br/>38066 Rovereto" });google.maps.event.addListener(marker, "click", function(){infowindow.open(map,marker);});infowindow.open(map,marker);}google.maps.event.addDomListener(window, 'load', init_map);</script> -->


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
