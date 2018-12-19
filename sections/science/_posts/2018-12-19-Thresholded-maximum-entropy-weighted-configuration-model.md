---
layout: post
title: Thresholded maximum entropy weighted configuration model
categories: science
published: false
use_math: true
date: 2018-11-28
---

Adding the threshold parameter in the strength weights
------------------------------------------------------

\begin{equation}
H(G) = \sum \limits_{i<j} (\alpha_i + \alpha_j) \Theta(w_{ij}-t) + (\beta_i+\beta_j) (w_{ij} -t)
\end{equation}

where $t>0$ is a threshold, a model hyper-parameter here, which is also called the absolute threshold in most software packages. Its role is delete any binary link with weight less than $t$.
Importantly, this model allows weights less than $t$ indeed, as the threshold parameter only acts on the link existence, not on its weight. In this sense, a decoupling of edge weights from edge existence is required.
With the previous Hamiltonian we can start from the calculation of the partition function, that becomes:

\begin{align}
Z(\mathcal{G}) = \sum_{G \in \mathcal{G}} e^{-H(G)} &= \prod_{i<j} \int_{0}^{\infty} e^{-(\alpha_i + \alpha_j) \Theta(w'-t) - (\beta_i+\beta_j) w'}  \mathrm{d}w' \\\\ &= \prod_{i<j} \frac{1 - e^{-t(\beta_i+\beta_j)} + e^{-(\alpha_i + \alpha_j) - (\beta_i+\beta_j)t }}{(\beta_i+\beta_j)}
\end{align}