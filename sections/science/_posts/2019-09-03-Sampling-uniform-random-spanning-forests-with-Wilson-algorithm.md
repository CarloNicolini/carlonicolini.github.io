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

David Wilson invented an exact algorithm to generate a spanning tree of $G$ which follows the uniform distribution on the set of spanning trees of $G$.
Starting from vertex 1, the algorithm consists in setting $A_1=\{1\}$, and to simulate a path of the simple random walk on $G$ started from vertex 2 until it reaches $A_1$.
Then $A_2$ is the union of $A_1$ and of the loop erased version of this path.
If $A_2=V$, the algorithm is stopped.
If not, then we redo the same starting this time the path from smallest vertex not in $A_2$,
 stopping the path when it reaches $A_2$, and so on.
The Wilson algorithm can be naturally related to the Green function of the random walk on $G$ with Dirichlet boundary conditions on a subset of $V$.



