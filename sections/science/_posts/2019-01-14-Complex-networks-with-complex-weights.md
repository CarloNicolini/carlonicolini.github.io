---
layout: post
title: Complex networks with complex weights
description: 'Complex networks with complex weights.'
published: false
use_math: true
date: 2019-01-14
categories:
  - science
  - complex-networks
---
Graphs with complex adjacency matrix elements
---------------------------------------------

Here we try to sketch a funny idea. What if we allow complex numbers populate the adjacency matrix of a graph?
What is the meaning of this? To solve this question here we try to formulate the complex counter-part of the simplest random graph, the Erdos-Renyi model, using the formalism of maximum entropy.

Let us consider the following optimization problem. As always we have our network probability $$P(G)$$ of a graph within the ensemble of graphs $$\mathcal{G}$$
 and we want to maximize its entropy:

$$
S(\mathcal{G}) = -\sum \limits_{G \in \mathcal{G}} P(G) \ln P(G)
$$

Here we make another step, different from the typical procedure of maximum entropy, writing $$P(G)$$ with the formalism of quantum mechanics, as the square of a wave function $$\psi(G) \in \mathbb{C}^{n\times n}$$, in other words:

$$
P(G) = | \psi(G) | ^2
$$

Our normalization condition is like in quantum mechanics, leading to:

$$
\lvert \psi(G) \rvert^2 = 1
$$

The total constraint is like for the ER graph, on the total number of links, so we build a Lagrangian $$\mathcal{L}(G)$$ that reads:

$$
\mathcal{L}(G) = - \sum \limits_{G \in \mathcal{G}}P(G) \ln P(G) 
$$


TO CONTINUE...
