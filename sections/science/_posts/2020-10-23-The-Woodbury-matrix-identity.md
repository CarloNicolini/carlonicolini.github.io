---
layout: post
title: The Woodbury matrix identity
date: 2020-10-23
categories: science
published: true
---


The Woodbury matrix identity is a useful identity in linear algebra.
It says that you can invert the sum of a matrix plus a $k$-rank correction by doing a rank $k$-correction to the inverse of the original matrix.
It is also called *matrix inversion lemma* or *Sherman-Morrison-Woodbury formula*.

More explicitly the identity states:

\begin{equation}
\left( \mathbf{A} + \mathbf{U}\mathbf{C}\mathbf{V}} \right)^{-1} = \mathbf{A}^{-1} - \mathbf{A}^{-1} \mathbf{U}\left( \mathbf{C}^{-1} + \mathbf{V} \mathbf{A}^{-1} \mathbf{U} \right)^{-1} V \mathbf{A}^{-1}
\end{equation}

where $\mathbf{A},\mathbf{U},\mathbf{C},\mathbf{V}$ are all matrices with the correct shapes, specifically, $\mathbf{A}$ is a square $n\times n$, $\mathbf{U}$ is $n \times k$, $\mathbf{C}$ is $k\times k$ and $\mathbf{V}$ is $k \times n$.

A more general form of the Woodbury matrix identity can be found using blockwise matrix inversion.

