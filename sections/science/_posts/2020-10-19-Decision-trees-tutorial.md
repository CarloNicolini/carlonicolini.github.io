---
layout: post
title: Decision trees (CART) — a short tutorial
date: 2020-10-19
published: false
categories: science
---

Decision trees recursively split the feature space into axis-aligned regions and fit a simple predictor in each region. The same greedy template covers both **classification** and **regression**; in scikit-learn this family is implemented as `DecisionTreeClassifier` and `DecisionTreeRegressor` (CART-style, binary splits).

## Piecewise prediction on recursive partitions

For axis-parallel splits, the fitted function is a sum of **leaf indicators**. With regions $R_1,\ldots,R_M$ and leaf values $w_m$,

$$
f(\mathbf{x}) = \sum_{m=1}^M w_m \,\mathbb{I}(\mathbf{x} \in R_m).
$$

Each region $R_m$ corresponds to a leaf; the path from the root encodes which feature $j$ was split and at which threshold $t$. In regression, $w_m$ is typically the mean response in $R_m$. In classification, $w_m$ is often the majority class or the vector of empirical class probabilities at the leaf.

A leaf is **pure** (for classification) if all training points that reach it share the same label.

Finding a globally optimal partition is computationally hard in general, so practical algorithms use **greedy recursive splitting**: at each node, choose one split that most reduces a local impurity or loss, then recurse on the children.

## Choosing a split

Let $\mathcal{D}$ denote the indices of training points at the current node. For candidate feature $j$ and threshold $t$, define the left and right child subsets

$$
\mathcal{D}_L(j,t) = \{ i \in \mathcal{D} : x_{ij} \le t \}, \qquad
\mathcal{D}_R(j,t) = \{ i \in \mathcal{D} : x_{ij} > t \}.
$$

A greedy CART step solves

$$
(j^\star, t^\star) \in \arg\min_{j,t} \Big[ \mathrm{cost}\big(\mathcal{D}_L(j,t)\big) + \mathrm{cost}\big(\mathcal{D}_R(j,t)\big) \Big],
$$

where $\mathrm{cost}(\cdot)$ is an impurity for classification or a squared-error objective for regression. Searches over $t$ are usually restricted to midpoints between sorted distinct values of $x_{ij}$ on $\mathcal{D}$.

### Regression (least squares)

For a node with labels $\{y_i : i \in \mathcal{D}\}$ and mean $\bar{y}_{\mathcal{D}} = \frac{1}{|\mathcal{D}|}\sum_{i \in \mathcal{D}} y_i$, a common node cost is the within-node residual sum of squares:

$$
\mathrm{cost}(\mathcal{D}) = \sum_{i \in \mathcal{D}} (y_i - \bar{y}_{\mathcal{D}})^2.
$$

Minimizing the sum of left and right costs after a split is equivalent to maximizing the **reduction in variance** between parent and children.

### Classification (empirical frequencies and impurity)

Let $C$ be the number of classes. Empirical class probabilities at a node are

$$
\hat{\pi}_c = \frac{1}{|\mathcal{D}|} \sum_{i \in \mathcal{D}} \mathbb{I}(y_i = c), \qquad c = 1,\ldots,C.
$$

Common impurity functions $\mathrm{cost}(\mathcal{D}) = \mid \mathcal{D} \mid \cdot I(\hat{\boldsymbol{\pi}})$ (scaled by sample count so the split objective is additive) include:

- **Misclassification error** (not smooth; rarely used for split selection alone):
  $$
  I_{\mathrm{mis}}(\hat{\boldsymbol{\pi}}) = 1 - \max_c \hat{\pi}_c.
  $$

- **Gini index** (default in many implementations, e.g. scikit-learn’s `criterion="gini"`):
  $$
  I_{\mathrm{Gini}}(\hat{\boldsymbol{\pi}}) = \sum_{c=1}^{C} \hat{\pi}_c (1 - \hat{\pi}_c).
  $$

- **Entropy / deviance** (`criterion="entropy"`):
  $$
  I_{\mathrm{ent}}(\hat{\boldsymbol{\pi}}) = -\sum_{c=1}^{C} \hat{\pi}_c \log \hat{\pi}_c
  $$
  (with the convention $0\log 0 = 0$).

Gini and entropy are differentiable in the interior of the simplex and tend to favor purer children more aggressively than misclassification rate.

## When to stop (and what to do about depth)

Pure greedy growth until every leaf is pure **overfits** noisy data. Standard controls include:

- **Minimum samples per leaf** (`min_samples_leaf`) or **minimum samples to split** (`min_samples_split`).
- **Maximum depth** (`max_depth`) or **maximum number of leaves** (`max_leaf_nodes`).
- **Minimum impurity decrease** (`min_impurity_decrease`).

**Post-pruning** (e.g. cost-complexity pruning with a penalty $\alpha$ on tree size) fits a sequence of nested subtrees on a training set and selects $\alpha$ by cross-validation. scikit-learn exposes this via `cost_complexity_pruning_path` and the `ccp_alpha` parameter.

## Minimal scikit-learn usage

```python
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.model_selection import cross_val_score

clf = DecisionTreeClassifier(criterion="gini", max_depth=5, min_samples_leaf=10, random_state=0)
scores = cross_val_score(clf, X, y, cv=5)

reg = DecisionTreeRegressor(max_depth=4, min_samples_leaf=20, random_state=0)
reg.fit(X_train, y_train)
```

Trees are **unstable** (small data changes can change splits) and have **high variance**; **random forests** and **gradient boosting** aggregate many trees to improve generalization while keeping the axis-aligned decision surface idea.

## References

- Breigman, Friedman, Olshen, Stone — *Classification and Regression Trees* (1984).
- Hastie, Tibshirani, Friedman — *The Elements of Statistical Learning*, [Chapter 9 — Trees](https://web.stanford.edu/~hastie/ElemStatLearn/) (free PDF).
- scikit-learn user guide: [Decision trees](https://scikit-learn.org/stable/modules/tree.html).
