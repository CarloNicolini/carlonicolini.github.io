---
layout: post
title: Thresholded maximum entropy weighted configuration model
categories: science
published: false
use_math: true
date: 2018-11-28
---

Adding the threshold parameter in the strength weights
------------------------------------------------------

<!-- The present program may be used to fit the lagragian multipliers that are needed to generate maximum entropy ensembles for a variety of constraints and types of weighted networks. This lagrangian multipliers allow to later generate networks belonging to ensembles of many different types of networks (weighted, multi-edge, accumulated weighted and accumulated binary networks) with a set of prescribed properties (such as degree sequence, strength sequence, total cost...). This procedure can be either used to generate networks to model several phenomena or to assess relevance of features detected in real data. It is very usefull for hypotehsis testing. (copied from Oleguer Sagarra github) -->

We start from the problem Hamiltonian $H(G)$:

\begin{equation}
H(G) = \sum \limits_{i<j} (\alpha_{ij}) \Theta(w_{ij}-t) + (\beta_{ij}) w_{ij} \Theta(w_{ij}-t)
\end{equation}

and compute the partition function, using separating the integral $\int_0^\infty$ in two parts, given our formulation that uses Heaviside step function. 
We use interchangeably $(\alpha_i+\alpha_j)=\alpha_{ij}$, when more clear.
We get for the partition function $Z(\mathcal{G})$ the following expression:

\begin{align}
Z(\mathcal{G}) = \sum_{G \in \mathcal{G}} e^{-H(G)} &= \prod_{i<j} \int_{0}^{\infty} e^{-(\alpha_i + \alpha_j) \Theta(w'-t) - (\beta_i+\beta_j) w' \Theta(w'-t)}  \mathrm{d}w' \\\\ &= \prod_{i<j} t + \frac{e^{-(\alpha_i+\alpha_j) - (\beta_i + \beta_j) t }}{(\beta_i + \beta_j)}
\end{align}

or equivalently with the substitution $x_i=e^{-\alpha_i}$ and $y_i=e^{-\beta_i}$:

\begin{align}
Z(\mathcal{G}) = \prod_{i<j} \frac{t \log (y_i y_j) - x_i x_j (y_i y_j)^t }{\log(y_i y_j)}
\end{align}

hence the graph probability is obtained as:
\begin{equation}
P(G) = \frac{e^{-H(G)}}{Z(G)} = \prod_{i<j} \log(y_iy_j) \frac{(x_i x_j)^{\Theta(w_{ij}-t)} (y_iy_j)^{w_{ij}\Theta(w_{ij}-t)}}{t \log(y_i y_j) - (x_i x_j) (y_i y_j)^t }
\end{equation}

The free energy $F=-\log Z$

\begin{align}
F=-\log Z = - \sum_{i<j} \log\left ( -t \log(y_i y_j) + (x_i x_j)(y_i y_j)^t \right) + \sum_{i<j} \log(-\log(y_i y_j))
\end{align}

the expected link probability is found by taking the derivatives with respect to $\alpha_{ij}$ of the free energy:

\begin{align}
\langle a_{ij} \rangle = \frac{\partial F}{\partial \alpha_{ij}} = \frac{1}{\beta_{ij} t e^{\alpha_ij + \beta_{ij}t}+1} = \frac{e^{-\alpha_{ij}-\beta_{ij}t}}{\beta_{ij}t+e^{-\alpha_{ij}-\beta_{ij}t}} = \frac{x_{ij} y_{ij}^t}{x_{ij}y_{ij}^t - t \log y_{ij}}
\end{align}

and the expected link weight $\langle w_{ij} \rangle$

\begin{align}
\langle w_{ij} \rangle =  \frac{\partial F}{\partial \beta_{ij}} = \frac{\beta_{ij}t + 1}{\beta_{ij}(\beta_{ij} t e^{\alpha_ij + \beta_{ij}t}+1)} = \frac{t\log(y_{ij})-1}{t \log( y_{ij})} \left(\frac{x_{ij} y_{ij}^t}{x_{ij}y_{ij}^t - t \log y_{ij}} \right)
\end{align}

The likelihood is obtained by the log of the probability:

\begin{align}
\log P(G) =& \sum_{i<j} \log(-\log(y_iy_j)) + \Theta(w_{ij}-t)\log(x_i x_j) + \\\\ & w_{ij}\Theta(w_{ij}-t)\log(y_i y_j) - \log\left( x_i x_j (y_i y_j)^t - t \log(y_i y_j) \right)
\end{align}

