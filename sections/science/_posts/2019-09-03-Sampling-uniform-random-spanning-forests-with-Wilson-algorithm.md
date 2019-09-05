---
layout: post
date: 2019-09-02
title: Sampling uniform spanning forests with Wilson algorithm in Python
published: false
---

In this post I would like to describe the fashinating bridge that connects random forests, graphs, probability theory and statistical mechanics.
We start from a binary undirected graph $G=(V,E)$, and would like to find a way to sample all the random forests, i.e. the union of spanning trees that cover the whole vertex set $V$.


# Wilson algorithm in Python
In this section I provide a simple yet efficient implementation of the Wilson algorithm to sample random spanning.
The algorithm follows this line.

1. Given an undirected graph $G=(V,E)$ with vertex set $V$ and edge set $E$, convert it to a directed graph, where all undirected links $(u,v)$ are replaced by two directed links $(u,v)$ and $(v,u)$.
2. Add a node called *root* to the graph $G$.
3. Connect all nodes with directed edges to the root node with weight $q$. Do not connect $r$ to all other nodes in the other direction.
4. Sample a random spanning tree starting from a random node (not $r$).
5. Eliminate the root node $r$ together with all its connections.

What remains is a random spanning forests, i.e. a random variable $\Phi_q$ sampled from the following probability distribution

\begin{equation}
\mathbb{P}(\Phi_q = \phi) = \frac{w(\phi) q^{|\mathcal{R}(q)|}}{Z(q)}
\end{equation}

where $\mathcal{R}(\phi)$ is the set of roots of the trees in the forest. The root vertices are such that, given any other vertex in the tree, following the directed edges in the tree you always reach the root.
The quantity $Z(q)$ is a *partition function* and sums the numerator over all possible random spanning forests (denoted by the set $\mathcal{F}$)

\begin{equation}
Z(q) = \sum \limits_{\phi \in \mathcal{F}} w(\phi)q^{|\mathcal{R}(q)|}
\end{equation}
