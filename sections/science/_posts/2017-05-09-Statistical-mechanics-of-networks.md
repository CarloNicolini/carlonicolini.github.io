---
layout: post
title: Statistical mechanics of networks - Park and Newman model of hidden variables
categories: science
published: false
date: 2017-05-09
---

### Introduction 

In these notes I will try to sum up the important points in the paper:
The statistical mechanics of networks, by Park and Newman, PRE, 2004

This work is based on exponential random graph model. They show that the ERG model can be obtained from first principles by means of maximum entropy methods.
Our goal will be to choose a probability distribution such that networks that are a better fit to observed characteristics are accorded higher probability in the model.

Suppose we have a collection of graph observables $$\{x_i\}$$, with $$i = 1 \ldots r$$, that we have measured in empirical observation of some real-world network or networks of interest to us.

We will, for the sake of generality, assume that we have an estimate $$\langle x_i \rangle$$ of the expectation value of each observable.

In practice it is often the case that we have only one measurement of an observable.

For instance, we have only one Internet, and hence only one measurement of the clustering coefficient of the Internet.

In that case, however, our best estimate of the expectation value of the clustering coefficient is simply equal to the one measurement that we have.

Let $$G \in \mathcal{G}$$ be a graph in our set of graphs and let $$P(G)$$ be the probability of that graph within our ensemble.

We would like to choose $$P(G)$$ so that the expectation value of each of our graph observables $$\{x_i\}$$ within that distribution is equal to its observed value, but this is a vastly underdetermined problem in most cases;
the number of degrees of freedom in the definition of the probability distribution is huge compared to the number of constraints imposed by our observations.

Problems of this type however are commonplace in statistical physics and we know well how to deal with them.
The best choice of probability distribution, in a sense that we will make precise in a moment, is the one that maximizes the Gibbs entropy $$S$$:

$$S(G) = - \sum \limits_{G \in \mathcal{G}} P(G)\log\left( P(G) \right )$$

 subject to some contraints, one is the normalization condition:

$$ \sum \limits_{G \in \mathcal{G}} P(G) = 1$$

and the second is that the observables must match their expected values:

$$\sum \limits_{G \in \mathcal{G}} P(G) x_i(G) = \langle x_i \rangle$$

Thanks to the Lagrangian multipliers $$\alpha$$ and $$\theta_i$$, one arrives to the Gibbs distribution:

$$P(G) = \frac{e^{-\beta H(G)}}{\sum \limits_{G \in \mathcal{G}} e^{-\beta H(G)} } \quad , Z = \sum \limits_{G \in \mathcal{G}} e^{-\beta H(G)}$$

where the graph Hamiltonian in this case is found to be $$H(G) = \sum_i \theta_i x_i(G)$$ and the denominator is called partition-function and indicated with the symbol $$Z$$. The partition function is a crucial quantity, upon which to obtain most of the thermodynamic quantities of interest.

The partition function $$Z$$, often very hard to compute, can be obtained analytically for simple models.
The exponential random graph is the distribution over a specified set of graphs that maximizes the entropy subject to the known constraints. It is also the exact analogue for graphs of the Boltzmann distribution of a physical system over its microstates at finite temperature.

The exponential random graph, like all such maximum entropy ensembles, gives the best prediction of an unknown quantity $$x$$, given a set of known quantities.

In this precise sense, the exponential random graph is the best ensemble model we can construct for a network given a particular set of observations.

### Exponential random graph as ER generalization

If we just know the average number of edges that a network should have (not a specific number) $$\langle m \rangle$$, the Hamiltonian takes the form $$H(G) = \theta m(G)$$, where the parameter $$\theta$$ acts as a mean-field or as an inverse temperature. 

It is possible to evaluate this in an ensemble of simple undirected graphs.
If the adjacency matrix $$A_{ij}$$ is one when one link is present and zero otherwise, then the number of edges in the graph $$m = \sum \limits_{i < j } A_{ij} $$ and the partition function $$ Z $$ can be written as:

\begin{align}
Z = \sum_G \exp{-H(G)} =& \sum \limits_{\{A_{ij}\}} \exp \left( {- \theta \sum \limits_{i < j} A_{ij}} \right ) \\ =& \prod \limits_{i< j} \sum \limits_{ A_{ij} =0 }^1 \exp \left({ \theta A_{ij} }\right) = \prod \limits_{i< j} \left( 1 + \exp({-\theta}) \right) = (1+ \exp(-\theta))^{\binom{n}{2}}
\end{align}


Starting from the partition function, one can define the free energy $$F = -\log(Z)$$
<!-- 
### Maximum entropy model for multilayer networks

Copying from the previous example it is simple to show that in a multilayer network with $$\mathcal{A}$$ layers, where each layer is indexed by $$\alpha \in \mathbb{N}$$, like for example $$A_{ij}^{(\alpha)}$$, one can define instead of one constraint, a number of $$\alpha$$ constraints, one for each layer.

The Hamiltonian containing the constraints becomes:

$$H(G) = \sum \limits_{\alpha}^{\mathcal{A}} \theta^{(\alpha)} m^{(\alpha)} = \sum \limits_{\alpha}^{\mathcal{A}} \theta^{(\alpha)} \sum \limits_{i < j} A^{(\alpha)}_{ij}$$

therefore the partition function becomes:

$$Z =  \prod \limits_{\alpha}\left( 1 + e^{-\theta^{(\alpha)}} \right)^{\binom{n^{(\alpha)}}{2}}$$
 -->
