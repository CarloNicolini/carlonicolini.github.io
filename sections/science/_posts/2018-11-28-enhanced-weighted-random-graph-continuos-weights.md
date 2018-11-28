---
layout: post
title: The Enhanced weighted random graph model with continuous weights
categories: science
published: false
date: 2018-11-28
---

In a previous post, I treated the case of networks with positive discrete weights $w_{ij} \in [1,2,3,\ldots ]$.
Our results was that the weights in the maximum entropy formalism are modeled by the geometric distribution.

However, some real world networks are assigned real-valued weights $w_{ij} \in R^+$.
If I apply maximum entropy formalism to this, I should recover the **exponential distribution** for the edge weights, which is the continuous counterpart of the geometric distribution.

To do this I will follow the basic derivation to show that the final probability of picking a weight $w$ in the case of continuous weights is $p(a)=w e^{-a w}$ with $a>0$.

The derivation is similar to the one given in the previous section, but one has to keep in mind that I no longer sum over all discrete weights, but rather I integrate.

Summing over all possible realizations of a graph in the continuous EWRG ensemble, helps us to compute the partition function $Z$, which in this case is simple to
write down explicitly:

\begin{aligned}
\label{eq:partition_function_continuous}
Z(G) = &\sum \limits_{G \in \mathcal{G}} e^{-H(G)}  = \sum \limits_{G \in \mathcal{G}} e^{- \sum \limits_{i < j} \beta_m \Theta(w_{ij}) + \beta_w w_{ij} }\nonumber \\\\ = & \sum \limits_{G \in \mathcal{G}} \prod_{i < j} e^{-\beta_m \Theta({w_{ij})} - \beta_w w_{ij}} = \prod \limits_{i < j} \int \limits_{\{ w_{ij}=0 \}}^{\infty} e^{-\beta_m \Theta({w_{ij}}) - \beta_w w_{ij}} \nonumber \\\\
= & \prod \limits_{i < j} \left( 1 + \sum \limits_{\{ w_{ij}=1 \}}^{\infty} e^{-\beta_m \Theta({w_{ij}}) - \beta_w w_{ij}} \right)
\end{aligned}

Let us start from the Lagrangian of the constrained optimization problem, but with integrals replacing sums, as the ensemble $\mathcal{G}$ must be continuously integrated:

\begin{aligned}
L(G) = - \int \limits_{G \in \mathcal{G}} P(G)\log\left( P(G) \right ) +  \alpha \left(1-\int \limits_{G \in \mathcal{G}} P(G) \right) +& \beta_m \left( \langle L \rangle - \int \limits_{G \in \mathcal{G}} m(G) P(G) \right)  +\nonumber \\\\ &\beta_w \left( \langle W \rangle - \int \limits_{G \in \mathcal{G}} w(G) P(G) \right)
\end{aligned}

The stationary point of this Lagrangian is taking the functional derivatives w.r.t the probability $P(G)$ and  set them to zero, finding a system of equations, with result:

\begin{equation}
\log P(G) + 1 + \alpha + \beta_m m(G) + \beta_w w(G) = 0
\end{equation}

Now I must remember that the weights are continuos, hence sums $\{ w_{ij} \}$ must be replaced by integrals. In other words I must write $m(G) = \sum_{i < j} \Theta(w_{ij})$ and $w(G) = \sum_{ i < j }$
