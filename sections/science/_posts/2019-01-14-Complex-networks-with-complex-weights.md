---
layout: post
title: Complex networks with complex weights
categories: science
published: false
use_math: true
date: 2019-01-14
---

Graphs with complex adjacency matrix elements
---------------------------------------------

Here we try to sketch a funny idea. What if we allow complex numbers populate the adjacency matrix of a graph?
What is the meaning of this? To solve this question here we try to formulate the complex counter-part of the simplest random graph, the Erdos-Renyi model, using the formalism of maximum entropy.

Let us consider the following optimization problem. As always we have our network probability $P(G)$ of a graph within the ensemble of graphs $\mathcal{G}$
 and we want to maximize its entropy:

\begin{align}
S(\mathcal{G}) = -\sum \limits_{G \in \mathcal{G}} P(G) \ln P(G)
\end{align}

Here we make another step, different from the typical procedure of maximum entropy, writing $P(G)$ with the formalism of quantum mechanics, as the square of a wave function $\psi(G) \in \mathbb{C}^{n\times n}$, in other words:

\begin{equation}
P(G) = | \psi(G) | ^2
\end{equation}

Our normalization condition is like in quantum mechanics, leading to:

\begin{equation}
\lvert \psi(G) \rvert^2 = 1
\end{equation}

The total constraint is like for the ER graph, on the total number of links, so we build a Lagrangian $\mathcal{L}(G)$ that reads:

\begin{equation}
\mathcal{L}(G) = - \sum \limits_{G \in \mathcal{G}}P(G) \ln P(G) 
\end{equation}


TO CONTINUE...
