---
layout: post
categories: math
date: 2019-03-04
title: Matrix factorization things
---

Notes from [Coursera course](https://www.coursera.org/lecture/matrix-factorization/singular-value-decomposition-K5NBy)

# Singular value decomposition
A $m \times n$ matrix can be factorized into two rank-1 matrices $U$ and $V'$ and a diagonal matrix $S$.
Values in the diagonal $S$ by absolute value, represents how important the new dimensions are in expressing the original matrix $R$.
For example the reconstructed matrix $R_k =U_k S_k V_k'$ is the closest rank-k matrix.

\begin{equation}
R = P \Sigma Q^T
\end{equation}


where
- $R$ is a $m\times n$ matrix
- $P$ is a $m \times k$ user-feature affinity matrix, is formed by row vectors $p_u$
- $Q$ is a $n \times k$ item-feature relevance matrix, is formed by row vectors $q_i$
- $\Sigma$ is a $k \times k$ diagonal feature weight matrix

The matrices $P$ and $Q$ are orthogonal.
Hence SVD describes preferences in terms of latent features. The features are not necessarily interpretable, instead we select features that optimize the predictive power.
The features define a shared vector space for users and items (feature space), and it enables compact representation of each.

The vectors $r_u$ is in the user space, $r_i$ is in the item space (they are row and column vectors)
