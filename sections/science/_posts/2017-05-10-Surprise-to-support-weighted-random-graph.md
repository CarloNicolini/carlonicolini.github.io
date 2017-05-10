---
layout: post
title: Plugging the weighted random graph into Surprise
categories: science
published: false
date: 2017-05-10
---

Surprise is based on the calculation of the number of simple graphs with $$n$$ nodes and $$m$$ edges exactly.
This null model is called $$G_{nm}$$ model and is the microcanonical version of the Erdos-Renyi model also called $$G_{np}$$.

To compute the number of graphs in the Weighted Random Graph ensemble, where each link can carry a weight greater than 1, one needs to find out how many topological configurations are there and their multiplicity.
In other words, the number of topological configurations is the same as in the $$G_{nm}$$ model, but each configuration has a number of possible ways to distribute the multi-edges upon the already existing edges.

This means that one has to compute the product between the number of topological configurations of the $$G_{nm}$$ which is $$\binom{\binom{n}{2}}{m}$$ and the multiplicity of each configuration.
It turns out that the each configuration can exist in $$\binom{w-1}{m-1}$$ different sub-configurations of links, as this is the number of possible distinct partitions of an integer (in this case $$w$$) into $$m$$ parts. The demonstration is given with the help of the "Stars and bars" method by W.Feller, shortly explained here (https://en.wikipedia.org/wiki/Stars_and_bars_%28combinatorics%29)[https://en.wikipedia.org/wiki/Stars_and_bars_%28combinatorics%29].
