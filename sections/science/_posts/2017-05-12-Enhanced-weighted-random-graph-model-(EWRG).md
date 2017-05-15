---
layout: post
title: Enhanced weighted random graph model (EWRG)
categories: science
published: false
date: 2017-05-12
---

In this article I will try to apply the statistical mechanics formalism as in Park and Newman, to a not completely known model of random graphs, i.e. the Weighted Random Graph model with constraints on the observed total weight and number of edges, that I will call the Enhanced Weighted Random Graph Model, or EWRG. This kind of constraints will result in a mixed statistics for the probability of observing an edge between two nodes.
This article is based on the theory of exponential random graph models.

Here I will show that the EWRG model can be obtained from first principles by means of maximum entropy methods.
My goal will be to choose a probability distribution such that networks that are a better fit to observed characteristics, are accorded higher probability in this model.

Let $G \in \mathcal{G}$ be a graph in the set of graphs of the EWRG and let $P(G)$ be the probability of that graph within this ensemble.

We would like to choose $P(G)$ so that the expectation value of each of the expected number of edges $\langle m \rangle$ and the expected total weight $\langle w \rangle$ within that distribution is equal to its observed value. In other words that 

$$\begin{align}
\langle w \rangle = w^{\star} \nonumber \\\\ 
\langle m \rangle = m^{\star} \nonumber
\end{align}
$$

This is a vastly underdetermined problem in most cases, since the number of degrees of freedom in the definition of the probability distribution is huge compared to the number of constraints imposed by our observations.

Problems of this type however are commonplace in statistical physics and we know well how to deal with them.
The best choice of probability distribution is the one that maximizes the Gibbs entropy $S(G)$:

$$\begin{equation}
S(G) = - \sum \limits_{G \in \mathcal{G}} P(G)\log\left( P(G) \right )
\end{equation}
$$

which must be subject to the above described contraints and to an obvious but necessary normalization condition:

$$\begin{equation}
\sum \limits_{G \in \mathcal{G}} P(G) = 1
\end{equation}
$$

One has to introduce three Lagrangian multipliers $\alpha,\beta_m,\beta_w$ and solve the minimization problem where the Lagrangian has the form:

$$\begin{align}
L(G) = - \sum \limits_{G \in \mathcal{G}} P(G)\log\left( P(G) \right ) + & \alpha \left(1-\sum \limits_{G \in \mathcal{G}} P(G) \right) + \\\\
& + \beta_m \left( \langle m \rangle - \sum \limits_{G \in \mathcal{G}} m(G) P(G) \right)  \\\\
& + \beta_w \left( \langle w \rangle - \sum \limits_{G \in \mathcal{G}} w(G) P(G) \right) 
\end{align}
$$

or equivalently and more explicitly:

$$\begin{align}
L(w_{ij}) = - \sum \limits_{\\{ w_{ij} \\}} P(w_{ij})\log\left( P(w_{ij}) \right) + & \alpha \left(1 - \sum \limits_{\\{ w_{ij} \\}} P(w_{ij}) \right) + \\\\ & \sum \limits_{\\{ w_{ij} \\}} \left[ \beta_m \Theta(w_{ij}) + \beta_w w_{ij} \right]
\end{align}
$$
where $\Theta(x)$ is the Heaviside function, that measures the presence or absence of an edge.

The Lagrangian has to be extremized for all graphs $G$, which consists to set the derivatives with respect to all the multipliers equal to zero and solving the system of equations, obtaining

$$\begin{equation}
\log P(G) + 1 + \alpha + \beta_m m(G) + \beta_w w(G) = 0
\end{equation}
$$

This allows to get the Hamiltonian of the problem, that reads:

$$H(G) := H(w_{ij}) = \sum_{i<j} \left [ \beta_m \Theta(w_{ij}) + \beta_w w_{ij} \right]$$

Summing over all possible realizations of a graph in the EWRG ensemble, helps us to compute the partition function $Z$, which in this case is simple to write down explicitly:

$$\begin{align}
Z(G) = &\sum \limits_{G \in \mathcal{G}} e^{-H(G)}  = \sum \limits_{G \in \mathcal{G}} e^{- \sum \limits_{i<j} \beta_m \Theta(w_{ij}) + \beta_w w_{ij} }\nonumber \\\\ = & \sum \limits_{G \in \mathcal{G}} \prod_{i<j} e^{-\beta_m \Theta({w_{ij})} - \beta_w w_{ij}} = \prod \limits_{i<j} \sum \limits_{\{ w_{ij}=0 \}}^{\infty} e^{-\beta_m \Theta({w_{ij}}) - \beta_w w_{ij}} \nonumber \\\\
= & \prod \limits_{i<j} \left( 1 + \sum \limits_{\{ w_{ij}=1 \}}^{\infty} e^{-\beta_m \Theta({w_{ij}}) - \beta_w w_{ij}} \right) \nonumber \\\\
= & \left( 1 + \frac{e^{-\beta_m}}{e^{\beta_w}-1} \right)^{\binom{n}{2}}  \nonumber \\\\
\end{align} 
$$

Within the EWRG model, therefore the probability to observe a graph with a weighted adjacency matrix $\mathbf{W}=w_{ij}$ is described by:

$$\begin{align}
P(\mathbf{W}) = \dfrac{e^{-H(G)}}{Z} = \prod \limits_{i<j} \left[ \frac{e^{-\beta_m \Theta(w_{ij})-\beta_w w_{ij}}}{\left( 1 + \frac{e^{-\beta_m}}{e^{\beta_w}-1} \right)} \right].
\end{align}
$$

The probability to get a link with weight $w \in [0,\infty]$ between edge $i$ and $j$ is given by:

$$
\begin{equation}
q_{ij}(w) = \dfrac{e^{-\beta_m \Theta(w) - \beta_w w}}{\sum_{w=0}^{w^\star} e^{-\beta_m \Theta(w) - \beta_w w}} = \dfrac{e^{-\beta_m \Theta(w) - \beta_w w}}{1+e^{-\beta_m}\sum_{w^\prime=1}^{w^\star} e^{-\beta_w w^\prime}}
\end{equation}
$$

This is the form of the generalized **Bose-Fermi** statistic and $w^\star$ can be set to 1 for fermions and to $+\infty$ for bosons. This statistic interpolates between the Fermi-Dirac statistic (with $w^\star=1$ and $e^{-\beta_m}=1$) and Bose-Einstein (with $w^\star=+\infty$ and $e^{-\beta_w}=1$).
It applies to any system described by an Hamiltonian as described before and represents the probability that its states are populated $w$ times. Even if multiple occupations are allowed, like for bosons, the first occupation number is necessarily binary like for fermions.

Let's define the constants $p_m=e^{-\beta_m}$ and $p_w=e^{-\beta_w}$. In this terms then we can rewrite the probability to pick an edge between node $i$ and node $j$ with weight $w$ as:
$$\begin{equation}
q_{ij}(w) = \frac{p_m^{\Theta(w)} p_w^w}{1 + p_m \sum_{w^\prime=1}^{w^\star}p_w^{w^\prime}}
\end{equation}
$$

and the probability that node $i$ and node $j$ are connected as:
$$\begin{equation}
p_{ij}(w) = 1-q_{ij}(0)
\end{equation}
$$

## Expected values of the observables

It is possible to compute the expected degree in this model as:
$$\begin{align}
\langle k_i \rangle = \sum_{j=1}^n p_{ij} = n - n q_{ij}(0) = \frac{n p_m p_w \left(p_w^{w^s}-1\right)}{p_m p_w^{w^s+1}-\left(p_m-1\right) p_w-1}
\end{align}
$$

and the expected strength as:
$$\begin{align}
\langle s_i \rangle = \sum_{j=1}^N q_{ij}(w) = TODO
\end{align}
$$

### Using the free energy to get expected values

Another way to get the quantities of interest is to compute the free energy from the partition function $Z$. The free energy is simply defined as minus the logarithm of the partition function $F=-\log(Z)$:

$$
\begin{align}
F = -\log(Z) = -\binom{n}{2}\log \left( 1 + \frac{e^{-\beta_m}}{e^{\beta_w} - 1} \right) \\\\ =
\binom{n}{2} \log \left( \frac{1-e^{-\beta_w}}{1-e^{-\beta_w} + e^{-\beta_w-\beta_m}}\right)
\end{align}
$$

The derivatives of the free energy with respect to the Lagrangian multipliers corresponding to the quantities they constraint are giving us the expected observables.
To make it concrete, to get the expected number of edges $\langle m \rangle$, one has to take the derivative with respect to $\beta_m$ of the free energy $F$:

$$
\begin{align}
\langle m \rangle = \frac{\partial F}{\partial \beta_m} = \binom{n}{2} \frac{1}{e^{\beta _m} \left(e^{\beta _w}-1\right)+1}
\end{align}
$$
This same result can be obtained also by summing over all pairs of nodes the quantity $p_{ij}$ as follows:

$$
\begin{align}
\langle m \rangle = \sum_{i < j} p_{ij}
\end{align}
$$

but since $p_{ij} = 1-q_{ij}(0)$ and is an independent variable for each pair of nodes, we get that the average over the ensemble of the number of edges in the EWRG model is 

$$
\begin{align}
\langle m \rangle = \sum_{i < j} (1-q_{ij}(0)) = \binom{n}{2}\left(1-\frac{1}{1+p_m p_w^{w^\star+1}} \right ) = \\\\ 1-\frac{ p_m p_w \left(p_w^{w^\star}-1\right)}{p_w-1} \\\\
&= \binom{n}{2} \frac{1}{-e^{\beta _m}+e^{\beta _m+\beta _w}+1} &=\\\\ \binom{n}{2} \frac{p_m p_w}{1+p_m p_w - p_w} = \\\\ &=
\frac{1}{e^{\beta _m} \left(e^{\beta _w}-1\right)+1}
\end{align}
$$

To get the expected total weights $\langle w \rangle $ one has to take the derivative with respect to $\beta_w$ of the free energy, which results in:
$$
\begin{align}
\langle w \rangle = \frac{\partial F}{\partial \beta_w} &=  \binom{n}{2} \frac{e^{\beta _w}}{e^{\beta _m} \left(e^{\beta _w}-1\right){}^2+e^{\beta_w}-1} \\\\ &= 
\frac{1}{2 e^{\beta _m} \left(\cosh \left(\beta _w\right)-1\right)-e^{\beta
   _w}+1} \\\\ & = 
\binom{n}{2} \frac{p_m p_w}{(1-p_w)\left((p_m-1)p_w +1\right)}
\end{align}
$$
