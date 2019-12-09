---
layout: post
published: false
date: 2019-12-09
title: Euler characteristic of complex networks
---


We are all used (or at least, some of us) with the concept of Euler characteristic.
Almost 200 years ago, Leohnard Euler, found that polyhedra have an interesting property.

If you count the number of vertices, denoted by $v$, the number of faces, denoted by $f$ and the number of edges, denoted by $e$, you always have this nice relation

\begin{equation}
v-e+f=2
\end{equation}

Hence, polyhedra have Euler charactestic of 2.
You can generalize this concept to complex networks, too, and the result is pretty amazing.
To do this, however, you need to play a bit with topology. Here I will try to remain as close to the ground as possible.

A graph $G=(V,E)$ is specified by a set of $n$ vertices $V$, and a set of $m$ edges, $E$.
Implicitly, a graph $G$ is also definining sets of higher order structures.

Indeed, a vertex can be seen as a $0$ complete graph, an edge can be seen as a $1$-complete graph, and so on.
We denote with $\mathcal{G}_k$ the set of complete $k+1$ subgraphs of $G$. Clearly $G_0=V$, the vertex set $K_1$, then $G_1=E$, the edge set made of complete subgraphs $K_2$, $G_2=T$, made of complete subgraphs $K_3$ set and so on.

Now one can see that a polyhedron can be seen as a graph.
Indeed its faces play the role of $K_3$ complete subgraphs. Hence if there are no tetrahedra $K_4$ in $G$, the standard Euler formula holds for the aforementioned graph.

However, when the graph has $K_4,K_5,\ldots$ subgraphs, the above formula is a bit different.
Here the introductive work of Oliver Knill is of help.
It is possible to define the Euler-charactestic of a finite simple graph $\chi(G)$ as

\begin{equation}
\chi(G) = \sum_{k=0}^\infty (-1)^k v_k
\end{equation}

where $v_k$ is the cardinality of the set $\mathcal{G}_k$ or in simple words the number of $k+1$ complete subgraphs inside the graph $G$.
Mathematicians like to call the number of vertices $n$ in $G$ with the word *order*, and the number of links $m$ with the word *size*.

We can identify the set $\mathcal{G}$ as the union of all the sets $\mathcal{G}_{k}$:

\begin{equation}
\mathcal{G} = \bigcup \limits_{k=0}^\infty \mathcal{G}_k
\end{equation}

### Dimension of graphs
One also can define the *dimension* of a graph, inductively by

\begin{equation}
\textrm{dim}(G) 1 + \frac{1}{n}\sum \limits_{v\in V}\textrm{dim}(S(v)), \qquad \textrm{dim}(\emptyset) = -1
\end{equation}
where $S(v)$ is the subgraph made by the neighbors of node $v$.

Cyclic graphs, trees or the dodecahedron are examples of graphs of dimension $1$, a triangle $K_3$, an octahedron or icosahedron has dimension $2$.
A tetrahedron has dimension $3$.
A complete graph $K_{k+1}$ on $k + 1$ vertices has dimension $k$.
Dimension is defined for any graph but can become a fraction.

For a truncated cube G for example, each unit sphere $S(v)$ is a graph of $3$ vertices and one edge, a graph of dimension $\textrm{dim}(S(v)) = 2/3$ so that $\textrm{dim}(G) = 5/3$.
The Euler characteristic of this graph is 

$$\chi(G) = v − e + f = 24 − 36 + 8 = −4.$$

### Forms on graphs
A $k$-form is a function on $G_k$ which is antisymmetric in its $(k + 1)$ arguments.
The set $\Omega^k$ of all $k$-forms is a vector space of dimension $v_k$.

Remembering the definition of $\mathcal{G}$ as the union set of all $k+1$ complete subgraphs, then we can form the vector space $\Omega$ as the direct sum of the $\mathcal{G}_k$ spaces.
Specifically we work in the space:

\begin{equation}
\Omega = \bigoplus _{k=0}^\infty \Omega^k
\end{equation}

from which we can build all the possible notions of scalar. The cardinality of $\mathcal{G}$, denoted by $v$ is the dimension of the vector space $\Omega$.

### Graphs and curvature
A $0$-form is a function on $V = \mathcal{G}_0$ and also called a **scalar function**.
We can introduce the gradient of the 0-form, as $df(a,b) = f(b)-f(a)$.
If an orientation is not defined, we can still look at a **directional derivative**

\begin{equation}
D_e (a,b) = f(b)-f(a)
\end{equation}
if $\{a,b\} \in E$. In the same spirit we can define the **exit-set** of a node $v$ as $S^{-}(v)$ as the set of neighbors $w$ of $v$ such that $f(w)-f(v)<0$.
Let $V_K(v)$ the number of $k+1$ dimensional subgraphs of $S_k(v)$. For example $V_0(v)$ is the node degree $\textrm{deg}(v)$, or the *order* of $S(v)$.
The **index** of a node $i_f(v) = 1 - \chi(S^{-}(v))$.

This makes it possible to define the **curvature** $K(v)$ of a node as:

\begin{equation}
K(v) = \sum \limits_{k=0}^{\infty} (-1)^k \frac{V_{k-1}(v)}{k+1}
\end{equation}


#### Dirac operator on graphs
We define the **Dirac operator** of a graph $\mathcal{D}$, represented by the Dirac matrix $\mathcal{D} : \Omega \to \Omega$ that is zero everywhere, expect for $D_{ij}=\pm 1$ if the object $i \subset j$ or $j\subset i$. In other words, the first upper-left block of $n \times n$ denotes the links, so saying $i\subset j$ indicates that the 0-form (vertex) $i$ and $j$ are in the same $1$-form.