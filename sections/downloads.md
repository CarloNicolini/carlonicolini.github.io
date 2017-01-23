---
layout: page
title: Download area
permalink: /sections/downloads
---

# Code for community detection on networks
Here is a short list for the code used in my research paper.

- [FAGSO](https://github.com/carlonicolini/fagso) Fast Agglomerative Surprise optimization in Matlab, Python and as a C++ library.

	<img src="/static/fagso_trim.png" alt="Community Detection" style="width: 150px;"/>

	FAGSO is an agglomerative Surprise Optimization algorithm written in C++ with bindings as MEX MATLAB and Octave file as well as Python library. It comes as the first proof of concept implementation of the idea, and accompanies the paper Modular structure of brain functional connectivity: breaking the resolution limit by Surprise.


- [PACO](https://github.com/carlonicolini/paco) PArtitioning Cost Optimization in Matlab, Python and as C++ library.
	
	<img src="/static/paco.png" alt="Community Detection" style="width: 150px;"/>

	PACO is the second iteration of the FAGSO algorithm, written from scratch with better data structures implementation as well as the full support of the igraph library. PACO implements agglomerative optimization methods as well as simulated annealing, and its written in a modular fashion so optimization of cost funcitons of various type can be carried on in a series of subsequent steps.

- [CommunityAlg](https://github.com/carlonicolini/communityalg) Algorithms and methods for community detection in Matlab.
	
	<img src="/static/community_detection.jpg" alt="Community Detection" style="width: 150px;"/>

	CommunityAlg is a set of Matlab functions for the analysis of complex networks and it extends largely the Brain connectivity Toolbox (BCT) by Sporns and Rubinov. CommunityAlg at the moment is a moving target and the implementations of the methods may change in the future as well as their signatures. Nonetheless many of the CommunityAlg functions are pretty well documented and some new ideas are tested in the form of simple quality functions.

- [InfomapMEX](https://github.com/carlonicolini/infomapmex) Infomap method adapted to a Matlab Mex file.

	<img src="https://brainetlab.github.io/static/img/software/infomapmx.png" alt="InfomapMEX" style="width: 150px;"/>

	A Matlab wrapper around the latest available implementation of Rosvall and Bergstroms Infomap code available on <a href="http://github.com/mapequation/infomap">github</a>. Infomap optimizes the map equation, which exploits the information-theoretic duality between the problem of compressing data, and the problem of detecting and extracting significant patterns or structures within those data. Specifically, the map equation is a flow-based method and operates on dynamics on the network.

- [Multilouvain](https://github.com/carlonicolini/multilouvain) Louvain method adapted to a Matlab Mex file.

  <img src="https://brainetlab.github.io/static/img/software/multilouvain.png" alt="Multilouvain" style="width: 150px"/>

  Multilouvain comes a C++ library and a Matlab mex wrapper that is able to optimize different quality functions for community detection on graphs. Multilouvain features Asymptotical Surprise, Significance, Reichardt and Bornholdt, CPM and Newman modularity in a single unified framework. All the credits for the C++ code are to <a href="http://www.traag.net">Vincent Traag</a>. This wrapper modified some functions to make faster calls to methods and the code is not completely equal, though.

- [LFRWMX](https://github.com/carlonicolini/lfrwmx) Lancichinetti-Fortunato-Radicchi benchmark adapted to a MEX file.

  <img src="https://brainetlab.github.io/static/img/software/lfr.png" alt="Multilouvain" style="width: 150px"/>

  LFR is an implementations of the planted partition model where the degrees and the community size is modeled after powerlaws with specific exponents. This implementation is a Matlab wrapper around the LFR Weighted with non overlapping communities that is available on the website of Santo Fortunato.

# GraphInsight
- GraphInsight is a software that let you visualize complex networks interactively.

	<img src="/static/logoGI.png" alt="GraphInsight" style="width: 150px;"/>

	[GraphInsight](https://github.com/carlonicolini/graphinsight) is released in its final version in many flavours: OSX, Linux and Windows 7. Here is a complete list of the versions you can download depending on your operating system.

	**Linux** Tested on Ubuntu 10.04 or newer, Debian.
	- 15.3 MB [GraphInsight-Pro-1.3.3-Linux-i686.deb](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-i686.deb)
	- 3.41 MB [GraphInsight-Pro-1.3.3-Linux-i686.rpm](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-i686.rpm)
	- 15.4 MB [GraphInsight-Pro-1.3.3-Linux-i686.sh](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-i686.sh)
	- 15.3 MB [GraphInsight-Pro-1.3.3-Linux-i686.tar.gz](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-i686.tar.gz)
	- 19.9 MB [GraphInsight-Pro-1.3.3-Linux-x86_64.deb](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-x86_64.deb)
	- 3.51 MB [GraphInsight-Pro-1.3.3-Linux-x86_64.rpm](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-x86_64.rpm)
	- 19.9 MB [GraphInsight-Pro-1.3.3-Linux-x86_64.sh](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-x86_64.sh)
	- 19.9 MB [GraphInsight-Pro-1.3.3-Linux-x86_64.tar.gz](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-x86_64.tar.gz)

	**OSX** Tested on OSX 10.8 or newer
	- 28.8 MB [GraphInsight-Pro-1.3.3-MacOSX-i386.dmg](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-MacOSX-i386.dmg)

	**Windows** Tested on Windows 7 or newer
	- 6.36 MB [GraphInsight-Pro-1.3.3-Windows-x86.exe](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Windows-x86.exe)
	- 8.17 MB [GraphInsight-Pro-1.3.3-Windows-x86.zip](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Windows-x86.zip)
	- [Source code (zip)](https://github.com/CarloNicolini/GraphInsight/archive/1.3.3.zip)
	- [Source code (tar.gz)](https://github.com/CarloNicolini/GraphInsight/archive/1.3.3.tar.gz)




