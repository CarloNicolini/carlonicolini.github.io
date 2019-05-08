---
layout: post
title: Low rank estimation of sparse observed ratios
categories: science
date: 2019-03-13
published: false
use_math: true
---

Reccomender systems are a class of algorithms to deal with missing information.
Given that we have some available rate about the relations of a set of objects, and these informations are specified by real numbers, how can we estimate the relations between another subset of objects that we did not observe?

Let us take for example a sparse set of observations $\mathbf{R} = \{ R_{ij} \}$ between a set of objects, from the same set $V$. We denote these objects as $i$ and object $j$.
Unfortunately, we only have a partial information about the relations of these objects, and this information may be contaminated by noise.
We only know the pairs specified by the subset $E$ of the complete set $\{ (i,j) | (i,j) \in V^2 \}$.

This sparse graph can be cast in a dense square matrix, if the set of object that $i$ and $j$ belongs are the same, but a matrix with a lot of missing entries, so not exactly a matrix, but something like this:

\begin{align}
\begin{pmatrix}
1 & \color{red}{?} & 2 & \color{red}{?} & \color{red}{?}\\\
\color{red}{?} & \color{red}{?} & \color{red}{?} & \color{red}{?} & 4\\\
2 & \color{red}{?} & 4 & 5 & \color{red}{?}\\\
\color{red}{?} & \color{red}{?} & 3 & \color{red}{?} & \color{red}{?}\\\
\color{red}{?} & 1 & \color{red}{?} & 3 & \color{red}{?}\\\
\end{pmatrix}
\end{align}

Now we make an important hypothesis.
The nature of the non-missing numbers in our sparse observation is one of ratio of positive real numbers. They can be, for example, currency exchange rates.

Hence, the relations between the observed objects $i$ and $j$ can be written as the ratios of an unknown *load* variable $u_i$ and $u_j$. 
On the diagonal, the matrix $R$ has ones, as the ratio of any number with itself is one.
An example of such matrix, is the following:
\begin{align}
\mathbf{R}= \begin{pmatrix}
1 & \color{red}{?} & 2 & \color{red}{?} & \color{red}{?}\\\
\color{red}{?} & 1 & \color{red}{?} & \color{red}{?} & 4\\\
1/2 & \color{red}{?} & 1 & 1/5 & \color{red}{?}\\\
\color{red}{?} & \color{red}{?} & 5 & 1 & 1/3\\\
\color{red}{?} & 1/4 & \color{red}{?} & 3 & 1\\\
\end{pmatrix}
\end{align}
If this is the case, our sparse observation matrix has a very specific structure that we can exploit.
We know, in the currency rates case, that the symmetric elements must be related by an inverse relation.
In other words, switching the row and column indices, makes the rate become its inverse:
\begin{equation}
R_{ij} = R_{ji}^{-1}
\end{equation}
For example, in the case above described, starting 
How can we estimate the remaining missing numbers in the matrix $R$?

Moreover, if we only can describe this matrix as a ratio of the elements of a vector, how can we be sure that the ratios are fair?
The simplest option is to transform this problem into one of least-squares estimation.
We can estimate a **load** vector $\mathbf{u}=\{u_1, \ldots, u_n \}$ by means of nonlinear optimization of the squares residual, as specified in the following equation:

\begin{equation}
\underset{\mathbf{u}\in \mathbf{R^+}}{\textrm{argmin}} \sum_{(i,j) \in E }\left( R_{ij} - \frac{u_i}{u_j} \right)^2
\end{equation}

However, in the case that the ratios take very big or very small values, this problem may become numerically badly behaved.
The terms in the residual of squares with the largest ratios are those that dominate and local optimization may become stuck at some local-optima.

A trick to tackle this problem, is to transform ratios into subtractions, via logarithmic transformation.
If indeed, we take the logarithm of the non-missing entries in $R_{ij}$, then the range of the values gets stretched and numerically this can be solved more easily. The log-transformed matrix becomes a skew-symmetric matrix $\mathbf{L}$ with zero diagonal elements.
The corresponding problem of optimization becomes:

\begin{equation}
\underset{\mathbf{v}\in \mathbf{R}^n}{\textrm{argmin}} \sum_{(i,j) \in E }\left( \log(R_{ij}) - (v \cdot \mathbf{1}^T - v^T \cdot \mathbf{1}) \right)^2
\end{equation}

where the quantity $\mathbf{V} = (v \cdot \mathbf{1}^T - v^T \cdot \mathbf{1})$ is a rank 2 matrix that has elements $V_{ij} = v_i - v_j$.
Also, the problem becomes much simpler, as the positivity constraint is lost, and we can look over the unbounded real domain.
Once solved, the estimated load vector $\mathbf{u}$ is obtained by taking the exponential of the elements of $\mathbf{v}$.

# Why this problem is interesting

Currency markets are often handled by exchanges. They may offer only some specific pairs to trade, as for example USD \$ to EUR, or USD to CAD.
However one would like to know, if given a set of specific exchange rates, others, missing exchange rates are fairly traded.
In the case they are not, an arbitrage possibility emerges, i.e. a way to buy and sell a series of assets, in order to profit from their inbalance in the market.
In a stationary market, all the prices are fair, meaning that it is not possible to perform risk-free arbitrage, as high frequency trading system are already doing it.

However, there are markets where non-stationarity conditions are prolonged in time, or the exchanges are fraudolent, and the rates are not fair.
In this case, the sum of squares of the errors can become non-zero, and the optimization procedure that I've described is of help in finding these situations.

# Code
{% highlight python %}
import autograd.numpy as np
from autograd import grad, hessian
from scipy.optimize import minimize
def rank1_log_completition(R, repetitions=100, lambd=0, **kwargs):
    """
    This function "fills" the matrix R with the estimated exchange rates, in a way
    that is similar to what reccomender systems do.
    It solves the following non-linear optimization problem

    argmin_x sum_{(i,j) in E} (log(R_e) - ( (x-x^T)_e ))^2
    
    where E is the set of nonzero elements of R, and log(R_e) is the logarithm of the rate of
    the coins i and j.
    
    This problem is log-transformed for better numerical stability.
    The quantity x-x.T is a rank 1 matrix where each entry is x(i)-x(j).
    The optimization variables are unbounded, and the problem is simpler.

    Input:
        R (np.array): a N x N numpy array, with the empirical rates of coins
                      where no rate is known, a 0 is set
        repetitions (int): number of repetitions of random restarts. The higher the better

    Returns:
        x (np.array): the N x 1 numpy array with estimated node centralities
        Rtilde (np.array): the N x N numpy array with the estimated rates, to be compared with the matrix R.
                           Each entry is the ratio x_i/x_j
        best_sol (scipy.OptimizeResult):  a dictionary with the results of the optimization

    """
    n = len(R) # number of nodes
    L = R.copy() # log transformed
    L[L<=0] = np.nan
    ij = np.nonzero(np.logical_not(np.isnan(L)))
    L = np.log(L[ij])

    if np.isnan(L.sum()) or np.isinf(L.sum()):
        raise RuntimeError('nan or inf in log transformed matrix')
    
    def error(x): 
        xn = np.reshape(x,[n,1]) # to exploit broadcasting
        e = np.mean( ( L - (xn-xn.T)[ij] )**2 )
        e += lambd * np.linalg.norm(xn)
        return e
    
    # these options yields good results
    # to control accuracy in the solution change ftol or eps
    opts = {'ftol':1E-18, 'maxiter':1E6,  'eps':1E-19, 'disp':False}
    
    # Repeat the iteration "repetitions" times until the solution with 
    # the least error is found
    lowest_err = np.inf
    best_sol = None
    for _ in range(repetitions):
        x0 = np.random.randn(n,1)

        sol = minimize(error,
                       jac = grad(error),
                       x0=x0, # no bounds 
                       method='SLSQP', # the fastest
                       tol=1E-15,
                       options=opts)

        if sol['fun'] < lowest_err:
            lowest_err = sol['fun']
            best_sol = sol

    x = best_sol['x']
    Rtilde = np.outer(np.exp(x),np.exp(-x))
    return x, Rtilde, best_sol
{% endhighlight %}
