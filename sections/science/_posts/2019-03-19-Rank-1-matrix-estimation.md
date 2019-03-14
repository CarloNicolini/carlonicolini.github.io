---
layout: post
title: Rank 1 matrix estimation
categories: science
date: 2019-03-19
published: false
use_math: true
---

Reccomender systems are a class of algorithms to deal with missing information.
Given that we have some available information about the relations of a set of objects, and these informations are specified by real numbers, how can we estimate the relations between another subset of objects that we did not observe?

Let us take for example a sparse set of observations $\{ R_{ij} \}$ between object $i$ and object $j$.
Obviously this could be cast in a dense square matrix, if the set of object that $i$ and $j$ belongs are the same.
Hence we can write a matrix $\mathbf{R} = \{ R_{ij} \}$ as follows

If we hypothesize, though, that the relations between the observed objects $i$ and $j$ can be written as the ratios of an unknown *load* variable $u_i$ and $u_j$, then we can estimate the *load* vector $\mathbf{u}=\{u_1, \ldots, u_n \}$ by means of nonlinear optimization.

\begin{equation}
\underset{\mathbf{u}}{\textrm{argmin}} \left( R_{ij} - \frac{u_i}{u_j} \right)^2
\end{equation}
