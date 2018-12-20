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

\begin{equation}
H(G) = \sum \limits_{i<j} (\alpha_i + \alpha_j) \Theta(w_{ij}-t) + (\beta_i+\beta_j) (w_{ij} -t)
\end{equation}

where $t>0$ is a threshold, a model hyper-parameter here, which is also called the absolute threshold in most software packages. Its role is delete any binary link with weight less than $t$.
Importantly, this model allows weights less than $t$ indeed, as the threshold parameter only acts on the link existence, not on its weight. In this sense, a decoupling of edge weights from edge existence is required.
With the previous Hamiltonian we can start from the calculation of the partition function, that becomes:

\begin{align}
Z(\mathcal{G}) = \sum_{G \in \mathcal{G}} e^{-H(G)} &= \prod_{i<j} \int_{0}^{\infty} e^{-(\alpha_i + \alpha_j) \Theta(w'-t) - (\beta_i+\beta_j) w'}  \mathrm{d}w' \\\\ &= \prod_{i<j} t + \frac{e^{-(\alpha_i+\alpha_j) - (\beta_i + \beta_j) t }}{(\beta_i + \beta_j)}
\end{align}

This partition function is very peculiar, as it depends linearly on the threshold value $t$. We now try to compute the free energy that results:
\begin{equation}
F = -\log Z = - \sum \limits_{i<j} \log \left( t + \frac{e^{-(\alpha_i+\alpha_j) - (\beta_i + \beta_j) t }}{(\beta_i + \beta_j)}  \right)
\end{equation}

and the expectation of the values are:

\begin{equation}
\langle k_i \rangle = \frac{\partial F}{\partial \alpha_i} = \sum_{j\neq i} \frac{e^{- (\alpha_i + \alpha_j) - t \left(\beta_i + \beta_j\right)}}{t \left(\beta_i + \beta_j\right) + e^{- (\alpha_i + \alpha_j) - t \left(\beta_i + \beta_j\right)}}
\end{equation}

\begin{equation}
\langle s_i \rangle = \frac{\partial F}{\partial \beta_i} = \sum_{j\neq i} \frac{\left(t \left(\beta_i + \beta_j\right) + 1\right) e^{- (\alpha_i + \alpha_j) - t \left(\beta_i + \beta_j\right)}}{\left(\beta_i + \beta_j\right) \left(t \left(\beta_i + \beta_j\right) + e^{- (\alpha_i + \alpha_j) - t \left(\beta_i + \beta_j\right)}\right)}
\end{equation}

we now make the substitution $x_i=e^{-\alpha_i}$ and $y_i=e^{-beta_i}$ so we get:

\begin{equation}
\langle k_i \rangle = \frac{\partial F}{\partial \alpha_i} = \sum_{j\neq i} \frac{x_i x_j (y_i y_j)^t }{\log (y_i y_j)^t + x_i x_j (y_i y_j)^t}
\end{equation}

\begin{equation}
\langle s_i \rangle = \frac{\partial F}{\partial \beta_i} = \sum_{j\neq i} \frac{\left( 1 + (y_i y_j)^t \right) x_i x_j (y_i y_j)^t}{\log (y_i y_j) \left\lbrack \log (y_iy_j)^t + x_i x_j (y_i y_j)^t \right \rbrack}
\end{equation}