---
layout: post
title: Gilbert model for loopy multigraphs
categories: science
date: 2016-10-18
---

<blockquote>
"How many rewirings are there in a graph with m edges and n nodes?"
</blockquote>

The number of **simple** graphs with $$n$$ nodes and exactly $$m$$ edges is

$$
| \Omega_{G_{np}}| = \binom{\binom{n}{2}}{m}
$$

The binomial coefficient count represent a combination without repetitions. A combination is a way of selecting items from a collection, such that (unlike permutations) the order of selection does not matter.

Because the binomial coefficient counts the total possible combinations without repetition of the number of pairs of nodes, this means that we pick simple graphs, i.e. the same pair is picked once.

If we instead want to allow for loopy multigraphs we must extend the possible number of pairs to $$n(n+1)/2$$ and count them with repetitions.
This is done by the number of combinations with repetitions

$$
\left( \binom{n}{k}  \right) = \binom{n+k-1}{k}
$$

that in the case of the $$G_{nm}$$ model turns out to be

$$
| \Omega_{G_{nm}'} |= \binom{n^2+m-1}{m}
$$

For example the triangle graph has $$m=3$$ edges and $$n=3$$ nodes, therefore there exist $$\binom{3}{3}$$ possible simple graphs with $$m=3,n=3$$ but $$\binom{3+3-1}{3}=\binom{5}{3}=10$$ possible loopy multigraphs with $$n=3,m=3$$.
