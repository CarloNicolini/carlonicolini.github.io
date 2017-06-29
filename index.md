---
layout: default
---

<!-- <img src="static/img/CNCS.png" style="right; width: 10%">
<img src="static/img/UNIVR.jpg" style="right; width: 10%"> -->

<div class="row">
	<div class="col-xs-9">
	<h2>Presentation</h2>
	</div>
</div>
<div class="row">
	<div class="col-xs-9">
		<p>I am a network neuroscientist, with an increasing competence in complex networks theory networks. I recently took the challenge of using complex networks science to better understand the most complex organ in nature: the brain.
		</p>
	</div>
	<div class="col-xs-3">
		<img src="static/img/nicolini3.jpg" style="float: right bottom; width: 75%">
	</div>
</div>

<br>

<div class="row">
<div class="col-xs-12">
In my career I've always been involved with computation in many of its applications.
I've started with Monte Carlo methods in radiation treatment planning, then moved to machine learning. In the last years I shifted my attention to computational models of brain fMRI activity exploiting the powerful theoretical machinery of complex networks.
This blog collects results, ideas and notebooks of my work. Not all the content of this website is completely finished, so take it as it is.
</div>
</div>

<h2>My PhD studies</h2>
<div class="row">
<div class="col-xs-12">
In my PhD I tackled the problem of modular structure identification in brain functional networks, from the point of view of complex networks. 
Complex networks theory offers a framework for the analysis of brain functional connectivity as measured by magnetic resonance imaging. Within this approach the brain is represented as a graph comprising nodes connected by links, with nodes corresponding to brain regions and the links to measures of inter-regional interaction. A number of graph theoretical methods have been proposed to analyze the modular structure of these networks. The most widely used metric is Newman's Modularity, which identifies modules within which links are more abundant than expected on the basis of a random network. However, Modularity is limited in its ability to detect relatively small communities, a problem known as resolution limit. To read more, <a href="https://www.dropbox.com/s/8o2hlws6bv21ogq/thesis_nicolini_submitted.pdf?dl=0">download my PhD thesis.</a>
</div>
</div>

<h2>My research interests, right now</h2>
<div class="row">
<div class="col-xs-12">
I am currently working on methodological aspects of complex network theory, as applied to brain functional connectivity.
Typically FC networks are obtained from Pearson correlation of BOLD time series.
The transformation from a correlation matrix to a graph is  justified only based empirical arguments.
It turns out indeed that many network-theoretical quantities are crucially dependent on how this conceptual passage is performed, which is heavily affected by a multitude nuisance factors. 

To alleviate the researchers from an hard-to-justify choice, I am working on a maximum entropy filtering method to filter spurious correlations at spectral level.
This work is in collaboration with Diego Garlaschelli and Assaf Almog, at Leiden University.

</div>
</div>

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
I'm currently working at the Lorentz Center for Theoretical Physics, Leiden University, The Netherlands.

Drop me an email at: <a href="nicolini@lorentz.leidenuniv.nl">nicolini@lorentz.leidenuniv.nl</a>
<!-- I'm currently working at the Center for Neuroscience and Cognitive Systems of Istituto Italiano di Tecnologia, hosted at University of Trento, in the city of Rovereto, Corso Bettini 31, Italy -->.
</div>


</div>
<br>
<address>
  <strong>Carlo Nicolini</strong><br>
  Center for Neuroscience and Cognitive Systems<br>
  Corso Bettini 31<br>
  38086 Rovereto<br>
  Italy<br>
</address>



<!-- 
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script><div style="overflow:hidden;height:100px;width:$device;"><div id="gmap_canvas" style="height:100px;width:$device;"><style>#gmap_canvas img{max-width:none!important;background:none!important}</style><a class="google-map-code" href="http://www.map-embed.com" id="get-map-data">embed google map</a></div><script type="text/javascript"> function init_map(){var myOptions = {zoom:14,center:new google.maps.LatLng(45.8923739,11.043936400000007),mapTypeId: google.maps.MapTypeId.ROADMAP};map = new google.maps.Map(document.getElementById("gmap_canvas"), myOptions);marker = new google.maps.Marker({map: map,position: new google.maps.LatLng(45.8923739, 11.043936400000007)});infowindow = new google.maps.InfoWindow({content:"<b>Center for Neuroscience and Cognitive Systems</b><br/>Corso Bettini 31 <br/>38066 Rovereto" });google.maps.event.addListener(marker, "click", function(){infowindow.open(map,marker);});infowindow.open(map,marker);}google.maps.event.addDomListener(window, 'load', init_map);</script> -->

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
