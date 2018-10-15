---
layout: page
title: Publications
permalink: /sections/publications
---

<div id="body">
	{% for pub in site.data.publications  %}
		<p>
			<h3>{{pub.title | markdownify }}</h3>
			<p>{{pub.authors }}</p>
			<p>{{pub.journal }}
			{% if pub.volume %}
				<strong>{{pub.volume}}</strong>,
			{% endif %}
			{% if pub.pages %}
				{{pub.pages}},
			{% endif %}
			({{pub.year }})
			</p>
			<p></p>
			
					<p><strong>Abstract</strong></p>
					<small>
					{{pub.abstract | markdownify }}
					</small>
			
			<p></p>
			<div class="row">
				<section class="col-xs-8">
					<img class="img-responsive" src="{{pub.image}}" alt="publication figure" style="width: 70%">
					<small>
					{% if pub.caption %}
						{{pub.caption}}
					{% endif %}
					</small>
				</section>
				<section class="col-xs-4">
						{% if pub.pmid %}
							<p>PubMed ID: <a href="http://www.ncbi.nlm.nih.gov/pubmed/{{pub.pmid}}" alt="pubmed link: {{pub.pmid}}"> {{pub.pmid}}</a>
						</p>
					{% endif %}
					{% if pub.pdf %}
						<p> PDF Download:
							<a href="{{pub.pdf}}" alt="PDF"><span class="fa fa-download"></span></a>
						</p>
					{% else %}
						<p> Paper submitted and/or under revision</p>
						<p> Preprint download:
							<a href="{{pub.preprint}}" alt="PDF"><span class="fa fa-download"></span></a>
						</p>
					{% endif %}
					{% if pub.ris %}
						<p>
							Reference: <a href="{{pub.ris}}" alt="RIS"><span class="fa fa-download"></span></a>
						</p>
					{% endif %}
					{% if pub.code %}
						<p>Code and methods:
							<a href="{{pub.code}}" alt="Code"><span class="fa fa-download"></span></a>
						</p>
					{% endif %}
			</section>
		</div>
	</p>
<hr size="5">
{% endfor %}
</div>


<p></p>

Conferences and proceedings
---------------------------

-- **Carlo Nicolini**, Thermodynamic of network model fitting with spectral entropies. NETSCI2018, Paris, June 11-16th 2018.
	[pdf](/static/pdf/presentation_netsci2018.pdf)  

- **Carlo Nicolini**, Cècile Bordier, Angelo Bifone, "Community detection in weighted brain connectivity networks beyond the resolution limit", Conference of the Complex Systems Society, Amsterdam, (2016) [CCS2016](ccs2016.org).

    [pdf](/static/pdf/conference_amsterdam_v2.pdf)

- **Carlo Nicolini**, Adam Liska, Francesco Sforazzini, Alberto Galbusera, Angelo Bifone, Alessandro Gozzi. *Modular organization of mouse brain functional connectivity networks*. ISMRM Joint Annual Meeting, Milano (2014).

- **Carlo Nicolini**, Carlo Fantoni, Giovanni Mancuso, Robert Volcic, Fulvio Domini. *A framework for the study of vision in active observers*. IS&T SPIE Electronic Imaging, San Francisco (2014). 

[link](http://proceedings.spiedigitallibrary.org/proceeding.aspx?articleid=1838237)
[pdf](https://www.researchgate.net/publication/260505676_A_Framework_for_the_Study_of_Vision_in_Active_Observers)

- Walter Gerbino, Carlo Fantoni, **Carlo Nicolini**, Robert Volcic, Fulvio Domini. *Active Multisensory Perception Tool: BUS experience and action comfort*. Human Factors and Ergonomics Society Europe, Torino (2013).
	
- **Carlo Nicolini**, Stefano Teso, Bruno Lepri, Andrea Passerini. *From on-going to complete activity recognition exploiting related activities*. International Workshop on Human Behaviour Understanding, Istanbul (2010).


Summer schools
---------------

- *Complex networks and their applications*, May 15, 2016, Como Villa del Grumello.
- *NSAS Connectomics* summer school, May 20 2015 Villa Finaly, Florence