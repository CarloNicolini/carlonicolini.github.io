---
layout: post
title: A Graduate Course in Econometrics
categories: science
published: false
use_math: true
date: 2017-09-27
---


# \lbrackIntroduction to matrix econometrics\rbrack()

One can write 

$$
y_i = \beta_0 + \beta_1 x_{1i} + \ldots \beta_p x_{pi} + \epsilon_i
$$

this can be written in matrix terms as 

$$
\begin{equation}
\mathbf{Y} = \boldsymbol \mathbf{X}\beta  + \boldsymbol \epsilon
\end{equation}
$$

where $$\mathbf{Y}$$ is a $$n \times 1$$ column  vector, $$\mathbf{X}$$ is a $$n \times p$$ matrix and $$\boldsymbol \beta$$ is another $$n \times 1$$ column vector.

At the end one gets for the least square estimators the following famous expression:

$$
\begin{equation}
\hat{\boldsymbol \beta} = \left( \mathbf{X}^T \mathbf{X} \right)^{-1} \mathbf{X}^T \mathbf{Y}
\end{equation}
$$

# Variance of random vector times a matrix

$$
\textrm{Var}\lbrack\mathbf{A} \mathbf{x}\rbrack = \mathbf{A} \textrm{Var}\lbrack\mathbf{x}\rbrack \mathbf{A}^T 
$$

So for this reason the variance of the estimator is

$$
\textrm{Var}\lbrack\boldsymbol \hat{\beta}\rbrack =\textrm{Var}\lbrack\left( \mathbf{X}^T \mathbf{X} \right)^{-1} \mathbf{X}^T \mathbf{Y}\rbrack 
$$

and for the properties of the variance of the product of a matrix with a vector and also considered that $$\mathbf{Y}=\mathbf{X}\boldsymbol \beta + \mathbf{u}$$ we have:

$$
\textrm{Var}\lbrack\boldsymbol \hat{\beta}\rbrack =\textrm{Var}\lbrack \left( \mathbf{X}^T \mathbf{X} \right)^{-1} \mathbf{X}^T \mathbf{Y}\rbrack = \left( \mathbf{X}^T \mathbf{X} \right)^{-1} \mathbf{X}^T \textrm{Var}\lbrack \mathbf{Y} \rbrack \mathbf{X} \left( \mathbf{X}^T \mathbf{X} \right)^{-1}
$$


$$
\textrm{Var}\lbrack\boldsymbol \hat{\beta}\rbrack = \left( \mathbf{X}^T \mathbf{X} \right)^{-1} \mathbf{X}^T \sigma^2 \mathbf{X} \left( \mathbf{X}^T \mathbf{X} \right)^{-1}
$$

because the variance of $$\mathbf{Y}$$ is homoskedastic then it's a diagonal matrix $$\sigma^2 \mathbf{I}$$.
