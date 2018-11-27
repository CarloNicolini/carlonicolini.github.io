---
layout: post
title: Plotting custom brain parcellation beautifully in Python with nilearn
categories: science
published: false
use_math: true
date: 2018-11-27
---

In this post I would like to introduce to the nilearn user a modified set of functions based on the `nilearn.surface` module, that help in making beautiful surface colored pictures of brain, like the one in this figure.

<a name="Figure1">
<img src="/static/postfigures/nilearn-brain-parcellation-multiview.jpg" style="float: center; width: 100%"><br>
</a>

Why this post?
==============

I have found that Python still lacks a decent way to integrate beatiful visualization of brain templates with the results of network community detection. This is what is typically needed in the pipeline of analysis of connectomic data, as well as in the graph-theoretical treatment of brain data.
Most important, working with `seaborn` and a number of other libraries based on `matplotlib`, I needed to be able to put my results into `matplotlib` axes, as subplots. There are a number of libraries out there which can plot parcellized areas over a brain surface, but I did not have the degree of control over the colormaps, the brain surface and a number of other minor quirks.
For this reason I preferred to make my own functions for this task. I like home-made implementation of the stuff that I base my research on.

To be clear, I had  a `pandas dataframe`, where a column contain a `numpy array` with the node label assignments, and based on some other columns I wanted 

Why this visualization is useful?
=================================

We often work with community detection methods applied to brain connectivity.
In the paradigm of the study of functional connectivity with complex network based methods, we implement the following recipe:

1. Get a Nifti template, that assigns each voxel an integer number. Examples of these templates are the AAL120, or the Harvard-Oxford template, or the Destrieux atlas. A number of templates is available 