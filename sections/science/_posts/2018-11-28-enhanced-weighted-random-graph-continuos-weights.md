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
If I apply maximum entropy formalism to this, I should recover the exponential distribution for the edge weights, which is the continuous counterpart of the geometric distribution.

To do this I will follow the basic derivation to show that the final probability of picking a weight $w$ in the case of continuous weights is $p(x)=\lambda e^{-\lambda x}$ with $\lambda>0$.

Continuos Weighted Random graph model
-------------------------------------

In this case the derivation simple, and the ideas have already been laid by the work of [Agatha Fronckzak](https://journals.aps.org/pre/pdf/10.1103/PhysRevE.85.056113).
Let us compute the partition function $Z(G)$:

\begin{aligned}
Z(G) = &\sum \limits_{G \in \mathcal{G}} e^{-H(G)}  = \sum \limits_{G \in \mathcal{G}} e^{- \sum \limits_{i < j} \beta_w w_{ij} }\nonumber \\\\ = & \sum \limits_{G \in \mathcal{G}} \prod_{i < j} e^{ - \beta_w w_{ij}} = \prod \limits_{i < j} \int \limits_{\{ w_{ij}=0 \}}^{\infty} e^{- \beta_w w_{ij}} \nonumber \\\\
= & \prod \limits_{i < j} \left( \frac{1}{\beta_w} \right) \\\\ =& \left( \frac{1}{\beta_w}\right)^{\binom{n}{2}}
\end{aligned}

Looking at this last expression for the partition function, it allows us to rewrite the probability of a network as:

\begin{equation}
P(G) = \frac{e^{-H(G)}}{Z} = \prod_{i<j} e^{-\beta_w w_{ij}} \beta_w 
\end{equation}

Hence, the edge **weights are exponentially distributed random variables**.
With the substitution $p(w) = e^{-\beta_w w} \beta_w$ we can write the probability of a graph in the continuous weighted random graph model as:
\begin{equation}
P(G) = \prod_{i<j} p(w_{ij})
\end{equation}

The expected weight (for each edge) is the mean value of the exponential distribution:

\begin{equation}
\langle w_{ij} \rangle = \frac{1}{\beta_w}
\end{equation}

and can be used to compute the expected strength:

\begin{equation}
\langle s_i \rangle = \sum_{i\neq j} \langle w_{ij} \rangle = (n-1) \frac{1}{\beta_w}
\end{equation}

Let us try to compute the expected total weight.
We compute the free energy $F=-\log Z$:

\begin{equation}
F = -\log (Z) = \binom{n}{2} \log \beta_w
\end{equation}

<!-- Now we make the substitution $p_w = e^{-\beta_w}$ and compute the derivatives of the free energy w.r.t $p_w$:

\begin{aligned}
\langle W \rangle = \frac{\partial F}{\partial p_w} = \frac{\partial F}{\partial \beta_w} \frac{\partial \beta_w}{\partial p_w} = \binom{n}{2} \frac{p_w}{\log p_w}
\end{aligned}

We now know the total weight of the empirical graph $W^\star$ and need to find the equation to choose $\beta_w$, so we equate $W^\star = \langle W \rangle$. Hence we need to solve the following equation:

\begin{equation}
-\binom{n}{2} \frac{e^{-\beta_w}}{\beta_w} - W^\star =0
\end{equation}

or equivalently:

\begin{equation}
\binom{n}{2} \frac{p_w}{\log p_w} - W^\star =0
\end{equation}

The solution for $p_w$ involves the calculation of the Lambert W function:

\begin{equation}
p_w = -\frac{2 W^\star}{n(n-1)} \mathrm{LambertW}\left( - \frac{n(n-1)}{2 W^\star}\right)
\end{equation} -->


Solution for the enhanced version
---------------------------------

In the enhanced case the solution is a bit more complicated.
Let us compute the partition function:

\begin{aligned}
\label{eq:partition_function_continuous}
Z(\mathcal{G}) = &\int \limits_{G \in \mathcal{G}} e^{-H(G)}  = \int \limits_{G \in \mathcal{G}} e^{- \sum \limits_{i < j} \beta_m \Theta(w_{ij}) + \beta_w w_{ij} } = \int \limits_{G \in \mathcal{G}} \prod_{i<j} e^{-\beta_m \Theta(w_{ij}) + \beta_w w_{ij} } = \\\\ =& \prod_{i<j}
\int_{G \in \mathcal{G}} e^{-\beta_m \Theta(w_{ij}) - \beta_w w_{ij}} = \\\\ =& \prod_{i<j} \int_{0}^{\infty} e^{-\beta_m\Theta(w) -\beta_w w } dw = \\\\ =& \prod_{i<j} \frac{e^{-\beta_m}}{\beta_w}
\end{aligned}

The free energy is simply:

\begin{equation}
F = - \log (Z) = \binom{n}{2} (\beta_m - \log(\beta_w))
\end{equation}

The expected number of links is:

\begin{aligned}
\langle L \rangle &= \frac{\partial F}{\partial \beta_m} = \binom{n}{2} \\\\\\
\langle W \rangle &= \frac{\partial F}{\partial \beta_w} = \binom{n}{2} \frac{1}{\beta_w}
\end{aligned}

the quantity $\beta_w^{-1}$ can be thought as the expected weight of a link.

We can write the probability of a graph as:

\begin{equation}
P(G) = \frac{e^{-H(G)}}{Z} = \prod_{i<j} \frac{\beta_w e^{-\beta_m \Theta(w) - \beta_w w}}{e^{-\beta_m}} = \prod_{i<j} \frac{e^{-\beta_m a_{ij}}}{e^{-\beta_m}} \beta_w e^{-\beta_w w_{ij}}
\end{equation}

Hence the probability of a link of weight $w_{ij}$ is 

\begin{equation}
p_{ij}(w_{ij})=\beta_w e^{-\beta_w w_{ij}} \frac{e^{-\beta_m \Theta(w_{ij})}}{e^{-\beta_m}}
\end{equation}

Differently from the purely weighted model discussed above, here the probability 