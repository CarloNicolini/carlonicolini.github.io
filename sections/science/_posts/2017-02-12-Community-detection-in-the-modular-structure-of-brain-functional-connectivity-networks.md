---
layout: post
title: Community detection in the modular structure of brain functional connectivity networks
categories: science
published: false
date: 2017-02-12
--- 

<blockquote>
Complex networks theory offers a framework for the analysis of brain functional connectivity as measured by magnetic resonance imaging. 
</blockquote>

Complex networks theory offers a framework for the analysis of brain functional connectivity as measured by magnetic resonance imaging.
Within this approach the brain is represented as a graph comprising nodes connected by links, with nodes corresponding to brain regions and the links to measures of inter-regional interaction.

A number of graph theoretical methods have been proposed to analyze the modular structure of these networks.
The most widely used metric is Newman's Modularity, which identifies modules within which links are more abundant than expected on the basis of a random network.

However, Modularity is limited in its ability to detect relatively small communities, a problem known as resolution limit.
As a consequence, unambiguously identifiable modules, like complete sub-graphs, may be unduly merged into larger communities when they are too small compared to the size of the network.

This limit, first demonstrated for Newman's Modularity, is quite general and affects, to a different extent, all methods that seek to identify the community structure of a network through the optimization of a global quality function.
Hence, the resolution limit may represent a critical shortcoming for the study of brain networks, and is likely to have affected many of the studies reported in the literature.

This work pioneers the use of Surprise and Asymptotical Surprise, two quality functions rooted in probability theory that aim at overcoming the resolution limit for both binary and weighted networks.
Hereby, heuristics for their optimization are developed and tested, showing that the resulting optimal partitioning can highlight anatomically and functionally plausible modules from brain connectivity datasets, on binary and weighted networks.

This novel approach is applied to the partitionining of two different human brain networks that have been extensively characterized in the literature, to address the resolution-limit issue in the study of the brain modular structure.
Surprise maximization in human resting state networks revealed the presence of a rich structure of modules with heterogeneous size distribution undetectable by current methods.
Moreover, Surprise led to different, more accurate classification of the network's connector hubs, the elements that integrate the brain modules into a cohesive structure.

In synthetic networks, Asymptotical Surprise showed high sensitivity and specificity in the detection of ground-truth structures, particularly in the presence of noise and variability such as those observed in experimental functional MRI data.

Finally, the methodological advances hereby introduced are shown to be an helpful tool to better discern differences between the modular organization of functional connectivity of healthy subjects and schizophrenic patients.

Importantly, these differences may point to new clinical hypotheses on the aetiology of schizophrenia, and they would have gone unnoticed with resolution-limited methods.

This may call for a revisitation of some of the current models of the modular organization of the healthy and diseased brain.

In short, Surprise and Asymptotical represent a promising alternative to current methods, and demonstrate the presence of functional modules of very different sizes in resting state networks.

