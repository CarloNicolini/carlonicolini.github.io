---
layout: post
title: Decision tree tutorial
date: 2020-10-19
published: false
categories: science
---


# Classification and regression trees (CART)
Also called decision trees, are a recursive partitioning of the feature space, defining a local model in each region of the space.

For the parallel axis split, namely a recursive subdivision based on some threshold values on each feature combination, the piecewise surface defining the region is:

\begin{equation}
f(\mathbf{x}) = \mathbb{E}[y \vert \mathbf{x}] = \sum \limits_{m=1}^M w_m \mathbb{I}(\mathbf{x} \in R_m) = \sum \limits_{m=1}^M w_m \phi(\mathbf{x}; \mathbf{v}_m)
\end{equation}

where $R_m$ is the $m$-th region, $w_m$ is the mean response in this region and $\mathbf{v}_m$ encodes the choice of variable to split on with the threshold value, on the path from the root to the $m$-th leaf.

A leaf is called 'pure' if it has only examples of a specific class and no examples of other classes.

Generally speaking, finding the optimal partitioning of the data is NP-complete, so it is common to use a greedy procedure to compute a locally optimal maximum likelihood estimation.

### Cost function
The split function chooses the best feature and the best value for that feature as follows

\begin{equation}
(j^\star, t^\star) =\underset{j \in \{1,\ldots,D\}}{\mathrm{argmin}} \min \, \rm{cost}\left( \lbrack \mathbf{x}_i,y_i x_{ij} \leq t \rbrack \right) + \rm{cost}\left( \{ \mathbf{x}_i,y _i \vert x_{ij}> t\} \right)
\end{equation}

where the cost function cost depends if we have a classification or regression problem.
In the case of regression we use the least-squares cost:

\begin{equation}
\textrm{cost}({\mathcal{D}}) = \sum_{i \in \mathcal{D}} (y_i - \bar{y}_i)^2
\end{equation}
where $\bar{y}$ is the mean of the response variable in the specified set of data. 

In the classification setting we have different possible choices for the cost function. Having fitted a multinomial bernoulli model to the data in the leaf satisfying the test $X_j <t$ with the conditional probabilities

\begin{equation}
\hat{\pi}_c = \frac{1}{|\mathcal{D}|} = \sum \limits_{i \in \mathcal{D}} \mathbb{I}(y_i = c)
\end{equation}

- Misclassification rate
