---
layout: post
title: The Enhanced weighted random graph model (EWRG)
categories: science
published: true
date: 2017-05-12
---

<blockquote>
An exponential random graph model with fixed topology and multilinks.
</blockquote>

The ensemble of maximally random weighted graphs with the constant average number of edges and total weight.

Introduction
============

In this article I will try to apply the statistical mechanics formalism
to a not completely known model of random graphs, the **Enhanced
Weighted Random Graph** model (EWRG). In this model one tries to find
the probability distribution of a graph ensemble, constraining on the
observed total weight and number of edges. In other words, the
constraint on the number of edges tries to keep the topology fixed,
while the constraint on the total weight selects with higher probability
graphs having the same total weight as the observed one. The application
of both constraints results in a graph probability based on a mixed
statistics for the probability of observing an edge between two nodes.

Here I will show how the EWRG model can be obtained starting from no
other than first principles, thanks to the method, originally introduced
by Jaynes.

The goal of this derivation is to choose a probability distribution such
that networks that are a better fit to observed characteristics, are
accorded higher probability in this model.

The maximum entropy method
--------------------------

Let $G \in \mathcal{G}_{EWRG}$ be a graph in the set of graphs of the
EWRG and let $P(G)$ be the probability of that graph within this
ensemble. We would like to choose $P(G)$ so that the expectation value
of each of the expected number of edges $\langle L \rangle$ and the
expected total weight $\langle W \rangle$ within that distribution is
equal to its observed value. In other words that: $$\begin{aligned}
\label{eq:constraints_ewrg}
\langle W \rangle = W^{\star} \nonumber \\
\langle L \rangle = L^{\star}\end{aligned}$$

This is a vastly under-determined problem in most cases, since the
number of degrees of freedom in the definition of the probability
distribution is very large compared to the number of constraints imposed
by our observations. Problems of this type however are commonplace in
statistical physics. The best choice of probability distribution is the
one that maximizes the Gibbs entropy $S(G)$:

$$S(G) = - \sum \limits_{G \in \mathcal{G}} P(G)\log\left( P(G) \right ),$$

which must be subject to the above described constraints and to an
obvious but necessary normalization condition:
$$\sum \limits_{G \in \mathcal{G}} P(G) = 1$$

Here we have to introduce three Lagrangian multipliers
$\alpha,\beta_m,\beta_w$ and solve a new minimization problem where the
Lagrangian function has now the form: $$\begin{aligned}
L(G) = - \sum \limits_{G \in \mathcal{G}} P(G)\log\left( P(G) \right ) +  \alpha \left(1-\sum \limits_{G \in \mathcal{G}} P(G) \right) +& \beta_m \left( \langle L \rangle - \sum \limits_{G \in \mathcal{G}} m(G) P(G) \right)  +\nonumber \\ &\beta_w \left( \langle W \rangle - \sum \limits_{G \in \mathcal{G}} w(G) P(G) \right) \end{aligned}$$
or equivalently and more explicitly:
$$L(w_{ij}) = - \sum \limits_{\{ w_{ij} \}} P(w_{ij})\log\left( P(w_{ij}) \right) + \alpha \left(1 - \sum \limits_{\{ w_{ij} \}} P(w_{ij}) \right) + \sum \limits_{\{ w_{ij} \}} \left[ \beta_m \Theta(w_{ij}) + \beta_w w_{ij} \right]$$
where $\Theta(x)$ is the Heaviside function, that has value $1$ for any
$x>0$ and $0$ otherwise. This is needed to include the topology of the
network and not only the information on the weights. The Lagrangian has
to be extremized for all graphs $G$, which consists to set the
derivatives with respect to all the multipliers equal to zero and
solving the system of equations, obtaining
$\log P(G) + 1 + \alpha + \beta_m m(G) + \beta_w w(G) = 0$. This allows
to get the Hamiltonian of the problem, that reads:
$$\label{Eq:ewrg_hamiltonian}
H(G) := \sum_{i<j}  \beta_m \Theta(w_{ij}) + \beta_w w_{ij}$$ Summing
over all possible realizations of a graph in the EWRG ensemble, helps us
to compute the partition function $Z$, which in this case is simple to
write down explicitly: $$\begin{aligned}
\label{eq:partition_function1}
Z(G) = &\sum \limits_{G \in \mathcal{G}} e^{-H(G)}  = \sum \limits_{G \in \mathcal{G}} e^{- \sum \limits_{i<j} \beta_m \Theta(w_{ij}) + \beta_w w_{ij} }\nonumber \\ = & \sum \limits_{G \in \mathcal{G}} \prod_{i<j} e^{-\beta_m \Theta({w_{ij})} - \beta_w w_{ij}} = \prod \limits_{i<j} \sum \limits_{\{ w_{ij}=0 \}}^{\infty} e^{-\beta_m \Theta({w_{ij}}) - \beta_w w_{ij}} \nonumber \\
= & \prod \limits_{i<j} \left( 1 + \sum \limits_{\{ w_{ij}=1 \}}^{\infty} e^{-\beta_m \Theta({w_{ij}}) - \beta_w w_{ij}} \right) \end{aligned}$$
We now introduce a smart variables substitution to help us with the
calculations. We denote $p_m:=e^{-\beta_m}$ and $p_w:=e^{-\beta_w}$.
With this change of variables we can rearrange the partition function
$Z$ as:
$$Z(G) =  \left( 1 + \frac{e^{-\beta_m}}{e^{\beta_w}-1} \right)^{\binom{n}{2}} = \left( \frac{ 1 - p_w + p_m p_w}{1-p_w} \right)^{\binom{n}{2}}$$
which will become useful later on. The probability of a graph $G$ with
weighted adjacency matrix $\mathbf{W}=\{ w_{ij}\}$ in the Enhanced
Weighted Random graph model is then:

$$P(\mathbf{W}) = \frac{e^{-H(G)}}{Z(G)} = \prod \limits_{i<j} \frac{p_m^{\Theta(w_{ij})} p_w^{w_{ij}}}{Z(G)}$$

As a first application of these calculations we can obtain the values of
the observables by means of the derivatives of the free energy. The free
energy is simply defined as minus the logarithm of the partition
function $F=-\log(Z)$:
$$F = -\log(Z) = -\binom{n}{2}\log \left( 1 + \frac{e^{-\beta_m}}{e^{\beta_w} - 1} \right) \\ =
\binom{n}{2} \log \left( \frac{1-e^{-\beta_w}}{1-e^{-\beta_w} + e^{-\beta_w-\beta_m}}\right)$$
which again does not depend on node-wise quantities, but is instead a
quantity related to the graph itself. With the substitution as before
($p_m, p_w$) we get:
$$F = \binom{n}{2} \log \left( \frac{1-p_w}{1-p_w + p_m p_w} \right)$$

The expected number of edges in the EWRG model is obtained as:
$$\begin{aligned}
\langle L \rangle &= \frac{\partial F}{\partial \beta_m} = \frac{\partial F}{\partial p_m} \frac{\partial p_m}{\partial \beta_m} = \binom{n}{2} \frac{p_m p_w}{1-p_w+p_m p_w} \\
\langle W \rangle &= \frac{\partial F}{\partial \beta_w} = \frac{\partial F}{\partial p_w} \frac{\partial p_w}{\partial \beta_w} = \binom{n}{2} \frac{p_m p_w}{(1-p_w) (1 -p_w + p_m p_w)}\end{aligned}$$
From these two equations is evident that the average number of links and
average total weight in the EWRG ensemble are related, indeed we see
that: $$(1-p_w) \langle W \rangle = \langle L \rangle.$$ In the case
$p_w=0$, we recover the correspondence between expected total weight and
expected number of edges. To determine the specific parameters $p_m$ and
$p_w$, we need to solve the system of the two constraints that we have
set in : $$\begin{aligned}
\label{eq:constraints_system}
\langle L \rangle = \binom{n}{2} &\dfrac{p_m p_w}{1-p_w+p_m p_w} = L^\star \\ 
\langle W \rangle = \binom{n}{2} &\dfrac{p_m p_w}{(1-p_w)(1-p_w + p_m p_w)} = W^\star\end{aligned}$$
The solution of the system in gives the values of $p_m$ and $p_w$:
$$\begin{aligned}
p_m &= \frac{(L^{\star})^2}{(\binom{n}{2} - L^\star)( W^\star - L^\star)} \\
p_w &= \frac{W^\star-L^\star}{W^\star}\end{aligned}$$ The form of $p_m$
tells us that this is the ratio between the square of actual number of
edges $(L^\star)^2$ and the product of the non-edges
$\binom{n}{2}-L^\star$ times the discrepancy between the total weight
and the actual edges $(W^\star-L^\star)$. Differently from the simpler
WRG model, where $p_m$ was obtained as $2W^\star/(n(n-1)+2W^\star)$,
here we have to account both for topology and weights into the edge
picking probability.

Graph probability in the EWRG model
===================================

Within the EWRG model, the probability to get a link with weight
$w \in [0,w^\textrm{max}]$ between node $i$ and $j$ is irrespective by
which pairs of nodes are considered and is given by:
$$\label{Eq:qijewrg}
q_{ij}(w) = \dfrac{e^{-\beta_m \Theta(w) - \beta_w w}}{\sum_{w=0}^{w^\textrm{max}} e^{-\beta_m \Theta(w) - \beta_w w}} = 
\frac{p_m^{\Theta(w)}p_w^w}{\sum_{w'=0}^{w^{\textrm{max}}} p_m^{\Theta(w')} p_w^{w'}}$$
which, for simplicity, in the limit $w^\textrm{max} \rightarrow +\infty$
becomes: $$\label{Eq:qijewrg2}
q(w) := \lim_{w^\textrm{max} \rightarrow +\infty} q_{ij}(w) = \frac{p_m^{\Theta(w)}p_w^w}{\sum_{w'=0}^{w^{\textrm{max}}} p_m^{\Theta(w')} p_w^{w'}} = \frac{p_m^{\Theta(w)}p_w^w(1-p_w)}{1 -p_w + p_m p_w}$$
Hence, the probability to observe a graph with a certain weighted
adjacency matrix $\mathbf{W}^\star = \{ w_{ij}^\star\}$ is described by
the product of the probabilities over all undirected pairs of nodes,
taking into account also the edge weight: $$\label{eq:ewrg_probability}
P(\mathbf{W}^\star) = \prod \limits_{i<j} q(w_{ij}).$$ From we see that
the probability to sample and edge with a given weight $w$ is described
as the ratio of two terms. In the numerator we find the geometric
distribution of edge weights, which can be interpreted as the
probability described by a series of $w$-successes, after the first
failure happens, multiplied by a factor indicating the presence of the
edge. At the denominator of instead the term is more difficult to
interpret.

The constraint on both the topology and on the total weight, imposed by
the Lagrangian multipliers $\beta_m,\beta_w$, slightly modified the edge
picking probability of the simpler WRG probability which was only
proportional to a term $q(w) = p_w^w(1-p_w)$. The $q(w)$ described here
is a particular case of a more general model described in
[@Garlaschelli2009a], where the hidden variables are set as constants,
in particular the variables $x_i x_j=e^{-\beta_m}:=p_m$ and
$y_i y_j=e^{-\beta_w}:=p_w$. It is interesting to see that even if the
edge picking probabilities $p_{ij}$ and the weights probability $q_{ij}$
are independent, the observables carry a dependence on both of them
which can not be unentangled.

The $q(w)$ distribution of has the form of the generalized
**Bose-Fermi** mixed statistic. If we allow for only binary weights, in
other words $w^\textrm{max}=1$, we retrieve the Fermi-Dirac statistic.
When $w^\textrm{max} \rightarrow \infty$ instead the distribution tends
to the Bose-Einstein statistic. This distribution applies to any system
described by an Hamiltonian as in , where there constraints on both
topology and weights are imposed, and it represents the probability that
each node pair is populated by $w$ links. Even if multiple occupations
are allowed, like for bosons, the first occupation number is necessarily
binary like for fermions.

In order to get the probability that node $i$ and node $j$ are
topologically connected (to with any possible weight), we need to
calculate the complementary probability that an edge of weight $0$
exists:
$$\pi(w) := \lim \limits_{w^\textrm{max} \rightarrow \infty} p_{ij}(w) = \lim \limits_{w^\textrm{max} \rightarrow \infty} 1 - q_{ij}(0) = \frac{p_m p_w}{1-p_w+p_m p_w}$$

Expected values of the observables
----------------------------------

With the correct form of the null models for the topology $p_{ij}$ and
the weights $q_{ij}$ we can derive the expected values of the
observables, namely the degree, the weight of any edge and the strength
of the model (in the limit $w^\textrm{max} \rightarrow \infty$):
$$\begin{aligned}
\langle k_i \rangle &= \sum_{j=1,j\neq i}^n p_{ij} = (n-1)\left ( \frac{p_m p_w}{1-p_w+p_m p_w} \right) \\ 
\langle w_{ij} \rangle &= \sum \limits_{w>0} w q_{ij}(w) = \frac{p_m p_w}{(1-p_w) (1-p_w +p_m p_w)} \\
\langle s_i \rangle &= \sum \limits_{j} \langle W \rangle = (n-1)\frac{p_m p_w}{(1-p_w) (1-p_w +p_m p_w)}\end{aligned}$$
These estimates are very useful when evaluating the probability of a
graph given the EWRG ensemble. It is possible to estimate the variance
of the expected variables. The variance of the expected weight is:
$$\textrm{Var}(w) = \langle w_{ij}^2 \rangle - \langle w_{ij} \rangle^2 = \frac{p_m p_w (1 + p_w^2(p_m -1) )}{(1-p_w)^2 (1 - p_w + p_m p_w)^2}$$

Apparent community structure in the EWRG
========================================

It is possible to compare the

Including spatial informations in the EWRG model
================================================

If we change the Hamiltonian we can embed other informations to generate
the ensemble of maximally exponential random graphs with fixed topology
and total strength. The Hamiltonian becomes:

$$H(G) := H(w_{ij}) = \sum_{i<j}  \beta_m \Theta(w_{ij}) + \beta_w w_{ij} + z_{ij} d_{ij}$$

where we have introduced a set of $n(n-1)/2$ additional Lagrangian
multipliers $z_{ij}$ that constraint the ensemble of maximally random
networks to the observed distance between nodes $d_{ij}$. The distance
$d_{ij}$ can be modeled in a number of ways, each of this way can be
tested, by looking at the likelihood of the model, to see whether this
fits our observations. In this way we can generate the most random null
model to compare with any empirical network, in a totally theoretically
sound manner, thanks to the MaxEnt method.

Embedding the clustering informations in the model
==================================================

How can we test the likelihood of a partition by exploiting the null
model generated by the MaxEnt method? How can we put in the Hamiltonian
the quantities related to the clustering?
