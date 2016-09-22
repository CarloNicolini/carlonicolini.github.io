---
layout: page
title: Download area
permalink: /sections/downloads
---

# Code for community detection on networks
Here is a short list for the code used in my research paper.

- [FAGSO](https://github.com/carlonicolini/fagso)

	<img src="/static/fagso_trim.png" alt="Community Detection" style="width: 150px;"/>

	FAGSO is an agglomerative Surprise Optimization algorithm written in C++ with bindings as MEX MATLAB and Octave file as well as Python library. It comes as the first proof of concept implementation of the idea, and accompanies the paper Modular structure of brain functional connectivity: breaking the resolution limit by Surprise.


- [PACO](https://github.com/carlonicolini/paco)
	
	<img src="/static/paco.png" alt="Community Detection" style="width: 150px;"/>

	PACO is the second iteration of the FAGSO algorithm, written from scratch with better data structures implementation as well as the full support of the igraph library. PACO implements agglomerative optimization methods as well as simulated annealing, and its written in a modular fashion so optimization of cost funcitons of various type can be carried on in a series of subsequent steps.

- [CommunityAlg](https://github.com/carlonicolini/communityalg)
	
	<img src="/static/community_detection.jpg" alt="Community Detection" style="width: 150px;"/>

	CommunityAlg is a set of Matlab functions for the analysis of complex networks and it extends largely the Brain connectivity Toolbox (BCT) by Sporns and Rubinov. CommunityAlg at the moment is a moving target and the implementations of the methods may change in the future as well as their signatures.

# GraphInsight
GraphInsight is a software that let you visualize complex networks interactively.
<img src="/static/logoGI.png" alt="GraphInsight" style="width: 150px;"/>

[GraphInsight](https://github.com/carlonicolini/graphinsight)


