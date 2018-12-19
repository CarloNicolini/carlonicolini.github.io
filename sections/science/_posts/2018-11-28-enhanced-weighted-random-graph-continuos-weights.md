---
layout: post
title: The Enhanced Weighted Random Graph Model with continuous weights
categories: science
published: false
use_math: true
date: 2018-11-28
---


Introduction
------------

In a [previous post](/sections/science/2017/05/12/Enhanced-weighted-random-graph-model-(EWRG).html), I introduced the statistical mechanics of complex networks, discussing a simple model for weighted random graphs with discrete weights $w_{ij} \in [1,2,3,\ldots ]$.
As a result we found that the maximum entropy distribution for networks with discrete weights is the geometric distribution.

However, we often deal with real world networks were weights take real-valued, positive values $w_{ij} \in R^+$.
In the following I will discuss how to simply embody the continuous nature of weights into more complex models.
What we will (re)discover, is that the maximum entropy distribution of positive real random variables is **exponential distribution**, the continuous counterpart of the geometric distribution.
However, we will also observe how more complex models based on continuous weights, yield probability distribution that are highly non-trivial.
To do this I will follow the basic derivation to show that the final probability of picking a weight $w$ in the case of continuous weights is $p(x)=\lambda e^{-\lambda x}$ with $\lambda>0$.

Moreover in the rest of this post we will extend the continuous model to constraint on node degree and strength, and as a final case, we introduce an interesting null model for thresholded real-valued networks.

We models that we discuss in this post are all variations of the weighted random graph model in the continuous domain.
We name them after the following convention.

1. In the [Continuous Weighted Random Graph Model (cWRG)](#CWRG) we only constraint on the total network weight $W^\star$.
2. In the [Continuous Weighted Random Configuration Model (cUWCM)](#cUWCM) we constraint on the strength sequence $s_i^\star$.
3. In the [Continuos Enhanced Weighted Configuration Model (cEWCM)](#cEWCM) we constraint on the degree sequence $k_i^\star$ and on the strength sequence $s_i^\star$.
4. The thresholded version of the last model cEWM with threshold (#cEWCMt) where we constraint on the degree sequence $k_i^\star$ and on the strength sequence $s_i^\star$, and include an additional global threshold parameter. This last model is the most general in this class.

The resulting models are referred herein as, **cWRG**, **cEWRG** and **cEWRGt**.

<a name="cWRG"></a>

Continuous Weighted Random graph model (cWRG)
---------------------------------------------

In this case the derivation simple, and the ideas have already been laid by the work of [Agatha Fronckzak](https://journals.aps.org/pre/pdf/10.1103/PhysRevE.85.056113) \[[1](#Fronczak2012)\]. We consider a graph with total weight $W^\star$. The Hamiltonian of the problem is:

\begin{equation}
H(G) = \sum \limits_{i<j} \beta_w w_{ij} = \beta_w W^{\star}
\end{equation}

We can compute the partition function $Z(G)$ by means of an integral over the positive domain, resulting in:

\begin{align}
Z(G) = &\sum \limits_{G \in \mathcal{G}} e^{-H(G)}  = \sum \limits_{G \in \mathcal{G}} e^{- \sum \limits_{i < j} \beta_w w_{ij} }\nonumber \\\\ = & \sum \limits_{G \in \mathcal{G}} \prod_{i < j} e^{ - \beta_w w_{ij}} = \prod \limits_{i < j} \int \limits_{\{ w_{ij}=0 \} }^{\infty} e^{- \beta_w w_{ij}} \nonumber \\\\
= \prod \limits_{i < j} \left( \frac{1}{\beta_w} \right)  = \left( \frac{1}{\beta_w}\right)^{\binom{n}{2}}
\end{align}

The last expression for the partition function, makes possible to rewrite the probability of a network as:
\begin{equation}
P(G) = \frac{e^{-H(G)}}{Z} = \prod_{i<j} e^{-\beta_w w_{ij}} \beta_w 
\end{equation}

In other words, the edge weights are iid **exponential random variables**, and the probability of the graph is the product of the probability of each edge under the exponential distribution (not to be confused with *exponential family*). We indicate the **pdf** of the edges as $q(w)= \beta_w e^{-\beta_w w}$.
With this substitution, we can write the probability of a graph in the continuous weighted random graph model as:

\begin{equation}
P(G) = \prod_{i<j} q(w_{ij})
\end{equation}

Under the exponential distribution, the expectation is described by the inverse rate parameter (here $\beta_w$). Hence, we expect each edge to have average weight $1/\beta_w$, independent of the specific edge.
This can be verified by computing the expectation of the total weight in this model, by means of the statistical mechanics framework that we introduced.
We start from the free energy $F=-\log Z$:

\begin{equation}
F = -\log (Z) = \binom{n}{2} \log \beta_w.
\end{equation}

Taking the derivatives with respect to $\beta_w$, we have the expected total weight of the graph:

\begin{equation}
\langle W \rangle = \sum_{G \in \mathcal{G}} W(G)e^{-\beta_w W(G)}  = \frac{\partial F}{\partial \beta_w} = \binom{n}{2} \frac{1}{\beta_w}.
\end{equation}

Hence it becomes clear that each edge is expected to contribute equally to the total expected weight:

\begin{equation}
\langle w_{ij} \rangle = \frac{1}{\beta_w}
\end{equation}

The same applies for the expected node strength, which is uniform for each node, being the Hamiltonian of the problem uniform over all nodes:

<a name="7"> </a>
\begin{equation}
\langle s_i \rangle = \sum \limits_{i\neq j} \langle w_{ij} \rangle = (n-1) \frac{1}{\beta_w}
\end{equation}

This a *dense* model, so we expect the degree of the nodes to be maximum $k_i=(n-1)$, hence the graph has $\binom{n}{2}$ undirected links.

How about a measure of *network density* in the cWRG? 
We [knew that](https://arxiv.org/pdf/0902.0897.pdf) \[[2](#Garlaschelli2009)\] in the **discrete case**  the maximum likelihood estimate of weighted network density was obtained as:

\begin{equation}
p^\star_{\textrm{WRG}} = \frac{2W^\star}{n(n-1) + 2W^\star}.
\end{equation} 

However in the continuous case, things are a little bit different. 
To find the parameter $\beta_w$ we have to solve Equation [(7)](#7) in the variable $\beta_w$. Hence we get, rather simply:

\begin{equation}
\beta_w = \frac{n(n-1)}{2 W^\star}
\end{equation}

and we identify $\beta_w$ as the inverse density of the network.
We note that in this continuous model the network density at maximum likelihood is different from the discrete case.



<a name="cUWCM"></a>

Continuous Weighted Configuration Model (cUWCM)
-----------------------------------------------

This model has Hamiltonian $H(G)$:

\begin{equation}
H(G) = \sum \limits_{i<j} (\theta_i + \theta_j) w_{ij} = \sum_i \theta_i s_i
\end{equation}
where $s_i$ is the $i$-th node strength.

The partition function can be computed with the same technique described before. We integrate over the positive real domain, to include all weights in the partition function:

\begin{align}
Z(G)= \int_{G \in \mathcal{G}} e^{-H(G)} = \int_{G \in \mathcal{G}} \prod_{i<j} e^{-(\theta_i + \theta_j) w_{ij}} = \prod_{i<j} \int_{0}^{\infty} e^{-(\theta_i+\theta_j)w_{ij}} \\\\ = \prod_{i<j} \frac{1}{(\theta_i + \theta_j)} e^{-(\theta_i+\theta_j)}
\end{align}

Taking the logarithm of the inverse of the partition function, as always, we get the free energy that reads:

\begin{align}
F=-\log Z &= -\sum \limits_{i<j} \log\left(\frac{1}{(\theta_i+\theta_j)} e^{-(\theta_i + \theta_j)w_{ij}} \right) = \\\\ &=\sum \limits_{i<j}\log (\theta_i + \theta_j) + (\theta_i+\theta_j)w_{ij}
\end{align}

So under the *cEWRG*, the graph probability $P(G)$ becomes a product of exponential random variables, where the rate parameters are given by the sum of the Lagrange multipliers associated with the node strengths $\theta_i+\theta_j$:

\begin{align}
P(G) \equiv P(W) = \frac{e^{-H(G)}}{Z(G)} = \prod_{i<j} \frac{(\theta_i+\theta_j) e^{-(\theta_i+\theta_j)w_{ij}}}{e^{-(\theta_i+\theta_j)}} \\\\ = \prod_{i<j} (\theta_i+\theta_j) e^{- w_{ij} (\theta_{i} + \theta_{j}) + (\theta_{i} + \theta_{j})}
\end{align}

As always, taking the partial derivatives of the free energy with respect to the Lagrange multipliers, we can get the expected value of its associated constraint, in this case the expected node strength:

\begin{equation}
\frac{\partial F}{\partial \theta_i} = \prod_{i<j} \frac{1}{(\theta_i + \theta_j)}
\end{equation}

In general we want to find the $\theta_i$ parameters by numerical optimization. There are two ways to tackle this problem. The maximum likelihood principle requires to look for the partial derivatives of $\log P(\theta)$ with respect to $\theta$ to vanish. The log-likelihood of the model is taken by the log of the probability of the model, hence:

\begin{equation}
\log P(W) = \sum \limits_{i<j} \log(\theta_i+\theta_j) + w_{ij}(\theta_i+\theta_j) + (\theta_i + \theta_j)
\end{equation}

The partial derivatives of the log-likelihood set to zero yields the following system of equations:

\begin{align}
\frac{\partial \log P}{\partial \theta_i} = 0 = \\\\
\sum \limits_{i<j} \frac{1}{(\theta_i+\theta_j)} + w_{ij} - 1 = 0 \\\\
\end{align}

Alternatively we can look for the solution of a system of $n$ non linear equations where the expected and empirical nodal strengths are compared in order to recover the parameters $\theta_i$

\begin{align}
s_i^\star = \langle s \rangle
\end{align}


<a name="cEWCM"> </a>

Continuous Enhanced Weighted Configuration Model (cEWCM)
--------------------------------------------------------

The partition function of the model that constraints on both the degree and strength sequence becomes:

\begin{align}
Z(\mathcal{G}) = &\int \limits_{G \in \mathcal{G}} e^{-H(G)}  = \int \limits_{G \in \mathcal{G}} e^{- \sum \limits_{i < j} \(\alpha_i + \alpha_j) \Theta(w_{ij}) + \(\beta_i + \beta_j) w_{ij} } = \int \limits_{w_{ij}} \prod_{i<j} e^{-\(\alpha_i + \alpha_j) \Theta(w_{ij}) - \(\beta_i + \beta_j) w_{ij} } \\\\ =& \prod_{i<j}
\int_{w_{ij}} e^{-\(\alpha_i + \alpha_j) \Theta(w_{ij}) - \(\beta_i + \beta_j) w_{ij}} = \prod_{i<j} \int_{0}^{\infty} e^{-\(\alpha_i + \alpha_j)\Theta(w') -\(\beta_i + \beta_j) w } \mathrm{d}w' \\\\ =& \prod_{i<j} \frac{e^{-\(\alpha_i + \alpha_j)}}{\(\beta_i + \beta_j)}
\end{align}

The free energy $F=-\log Z$ can be calculated as:

\begin{align}
F=-\log Z &= -\sum \limits_{i<j} \log\left(\frac{e^{-(\alpha_i+\alpha_j)}}{(\beta_i+\beta_j)} e^{-(\beta_i + \beta_j)w_{ij} - (\alpha_i+\alpha_j)a_{ij}} \right) \\\\ &=\sum \limits_{i<j}\log (\beta_i + \beta_j) + (\beta_i+\beta_j)w_{ij} + (\alpha_i+\alpha_j)a_{ij} + (\alpha_i+\alpha_j)
\end{align}

Hence the link existence probability becomes:

\begin{equation}
\langle k_i \rangle = \frac{\partial F}{\partial \alpha_i} = \sum \limits_{i\neq j} a_{ij} + 1
\end{equation}

\begin{equation}
\langle s_i \rangle = \frac{\partial F}{\partial \beta_i} = \sum \limits_{i \neq  j} \frac{w_{ij} \left(\beta_i + \beta_j\right) + 1}{\beta_i + \beta_j}
\end{equation}


<a name="cEWCMt"> </a>

Introducing the threshold parameter (cEWCMt)
--------------------------------------------

We introduce a threshold parameter $t$ in the Hamiltonian for the degree dependent Lagrangian multiplier, so to constrain the degree sequence:

\begin{equation}
H(G) = \sum \limits_{i<j} (\alpha_i + \alpha_j) \Theta(w_{ij}-t) + (\beta_i+\beta_j) w_{ij}
\end{equation}

where $t>0$ is a threshold, a model hyper-parameter here, which is also called the absolute threshold in most software packages. Its role is delete any binary link with weight less than $t$.
Importantly, this model allows weights less than $t$ indeed, as the threshold parameter only acts on the link existence, not on its weight. In this sense, a decoupling of edge weights from edge existence is required.
With the previous Hamiltonian we can start from the calculation of the partition function, that becomes:

\begin{align}
Z(\mathcal{G}) = \sum_{G \in \mathcal{G}} e^{-H(G)} &= \prod_{i<j} \int_{0}^{\infty} e^{-(\alpha_i + \alpha_j) \Theta(w'-t) - (\beta_i+\beta_j) w'}  \mathrm{d}w' \\\\ &= \prod_{i<j} \frac{1 - e^{-t(\beta_i+\beta_j)} + e^{-(\alpha_i + \alpha_j) - (\beta_i+\beta_j)t }}{(\beta_i+\beta_j)}
\end{align}

the free energy becomes:

\begin{align}
F = -\log Z &= - \sum \limits_{i<j}\left \lbrack \log \left( 1 - e^{-t(\beta_i+\beta_j)} + e^{-(\alpha_i + \alpha_j) - (\beta_i+\beta_j)t } \right) - \log (\beta_i + \beta_j) \right \rbrack \\\\ 
\end{align}
with the substitution $x_i=e^{-\alpha_i}$ and $y_i=e^{-\beta_i}$ we have:

\begin{align}
F = - \sum \limits_{i<j}\left \lbrack \log \left( 1 - (y_i y_j)^t + x_i x_j (y_i y_j)^t \right)  - \log\left( -\log y_i -\log y_j \right) \right \rbrack 
\end{align}

We can compute the expectation of the presence of a link (probability) and its weight by taking the derivatives w.r.t $\alpha_i$ and $\beta_i$. By the chain rule of derivatives, we have:

\begin{align}
p_{ij} = \langle a_{ij} \rangle = \frac{\partial F}{\partial \alpha_i} = \frac{\partial F}{\partial x_i}\frac{\partial x_i}{\partial \alpha_i} = \frac{x_i x_j (y_i y_j)^t}{1 + x_i  x_j (y_i y_j)^t-(y_i y_j)^t}
\end{align}

and for the expected weight:

\begin{align}
\langle w_{ij} \rangle = \frac{\partial F}{\partial \beta_i} = \frac{\partial F}{\partial x_i}\frac{\partial x_i}{\partial \beta_i} =  \frac{t (x_i  x_j-1) (y_i y_j)^t}{1 + x_i  x_j (y_i
    y_j)^t-(y_i y_j)^t}-\frac{1}{\log (y_i)+\log (y_j)}
\end{align}

Let us study these formulas in the limit $t \to 0$.

\begin{align}
\lim \limits_{t \to 0} \langle w_{ij} \rangle = - \frac{1}{\log (y_i y_j)} = \beta_i + \beta_j
\end{align}
and we recover the expectation in the exponential distribution, as expected. 
For the probability of link existence, we have instead :

\begin{align}
\lim \limits_{t \to 0} \langle p_{ij} \rangle = \frac{x_i x_j}{x_i x_j -1 + 1} = 1
\end{align}

so the total number of links is $\langle L \rangle = \prod_{i<j} 1 = \binom{n}{2}$ and the total weight is $\langle W \rangle = \prod_{i<j} \beta_i + \beta_j$.

Great, it looks correct when considered in the limit case. So the parameter $t$ which is the thresholding value controls the sparsity of the model, and in the case it is not exactly 0, the random graph model seems very interesting.

The expected degree is computed from the link probability as:

\begin{equation}
\langle k_i \rangle = \sum_{ j \neq i}
\end{equation}

### Ratio $\langle w_{ij} \rangle/p_{ij}$
Let us study the ratio between expected weight and expected link probability:

\begin{equation}
\frac{\langle w_{ij} \rangle}{p_{ij}} = \frac{(y_i y_j)^{-t} \left((x_i  x_j-1) (y_i y_j)^t (t \log (y_i y_j)-1)-1\right)}{x_i  x_j \log (y_i y_j)}
\end{equation}

or in Python code:

{% highlight python %}
def ratio_wij_pij(xij, yij, t):
    from numpy import log
    num = -1 + (-1 + xij) * ((yij)**t) * (-1 + t * log(yij))
    den = xij*((yij)**t) * log(yij)
    return num / den
{% endhighlight %}

As we can see it is not possible to simplify $x_i x_j$ as in the discrete case.

### Likelihood optimization

We now need to design the equations for fitting this powerful null model to real-world networks.
To do this we need to maximize the likelihood of this model that can be obtained as the logarithm of the graph probability, or to solve a system of $2N$ non-linear equations, where we equate each individual degree and strength to the empirical one.

\begin{equation}
k_i^\star = \langle k_i \rangle = \sum \limits_{i \neq j} p_{ij}
\end{equation}

\begin{equation}
s_i^\star = \langle s_i \rangle = \sum \limits_{i \neq j} \langle w_{ij} \rangle 
\end{equation}

This can be solved by any nonlinear system equation solver, given enough accuracy is passed. In this code snippet we use the `scipy.optimize.root` solver, with the Levenberg-Marquardt method `method='lm'`, and a very small error tolerance on gradients, values and gradients (we use `options={'xtol':1E-16,'gtol':1E-16,'ftol':1E-16})`). Convergence is slow but the result is good agreement with toy datasets.

## Higher order properties

We may ask, given this null model, what is the expected number of connected components given the threshold $t \in \mathbb{R}$ or how the degrees and the strengths are correlated.
To my knowledge this things have never been studied for a continuous model and we may find interesting new answers.

The correlation function $\langle k_i k_j \rangle$ can be obtained as 

\begin{equation}
\langle k_i k_j \rangle = \frac{\partial^2 F}{\partial x_i \partial x_j} =  \frac{x_i  x_j (y_i y_j)^t}{(x_i  x_j-1) (y_i
    y_j)^t+1}
\end{equation}

and for the strengths $\langle s_i s_j \rangle$ we have

\begin{equation}
\langle s_i s_j \rangle = \frac{\partial^2 F}{\partial y_i \partial y_j} =  -\frac{t}{(x_i  x_j-1) (y_i y_j)^t+1}+t-\frac{1}{\log(y_i y_j)}
\end{equation}


However as a first application of this null model, we try to solve for the threshold that maintains a specific number of links $L^{\star} = \sum_{i<j} p_{ij}$ and a specific total weight $W^{\star} = \sum_{i<j} \langle w_{ij} \rangle$.
This can be very useful to be able to compare two networks specifing the same number of links and total weight. Indeed, this has never been studied before. Hence, the question: does a threshold that maintains both the conditions exists?

We need to solve the two simultaneous conditions:

\begin{align}
x \\\\
y
\end{align}



Numerical approach to the problem
---------------------------------

Here we detail a numerical approach to this problem. The problem has to be solved in the variables $x_i,y_i$, hence a system of $2N$ non-linear equations has to be solved.
This is in general a difficult problem, and suffers of a lot of local optima.

We first define a benchmark network that tries to replicate a typical matrix encountered in brain functional connectivity. It is based on a extension of the factor model used in finance

{% highlight python %}
import matplotlib.pyplot as plt
import numpy as np

def factor_model(ci,T,eta,mu, correlation=False):
    N = len(ci) # number of nodes, length of membership vector,
    # Initialize the observations vector a TxN matrix of NaNs,
    Y = np.ones([T,N])*np.nan
    
    # Fill the identical observations in the maximally correlated subsets,
    for c in np.unique(ci):
        i = np.where(ci==c)[0]
        Y[:,i] = np.kron(np.ones((1,(ci==c).sum())),np.random.randn(T,1))

    # Add local noise beta on each time-series,
    Y += eta*np.random.randn(T,N)
    # Add global signal mu that correlates globally each time series,
    Y += mu*np.kron(np.ones((1,N)),np.random.randn(T,1))

    from scipy.stats import zscore
    Y = zscore(Y)
    if correlation:
        C = np.corrcoef(Y.T)
        np.fill_diagonal(C,0)
    else:
        C = np.cov(Y.T)
    return C
{% endhighlight %}

As an example, tihs is a possible outcome of the factor model defined here, where the parameters `eta` and `mu` control the local and global noise respectively, while the nodal membership is specified as input.

{% highlight python %}
t = 0.0 # threshold
T = 200 # number of time points to sample
eta = 3.0 # localnoise
mu = 1.2 # globalnoise
C = np.arctanh(factor_model([1]*50 + [2]*25 + [3]*25 + [4]*50, T, eta, mu, True))
At = bct.threshold_absolute(C,t)
n=len(At)
k = (At>0).sum(axis=0)
s = At.sum(axis=0)
plt.imshow(At)
plt.colorbar()
{% endhighlight %}

We then move to the definition of the equations to be solved, both in $x_i$ and $y_i$.

{% highlight python %}
from scipy.optimize import root
import bct

eps = np.finfo(float).eps
def pij_wij(x,y,t):
    xij = np.outer(x,x) # outer product produces the matrix x_i x_j
    yij = np.outer(y,y) # outer product produces the matrix y_i y_j
    pij = xij*((yij)**t)/(1.0+xij*(yij**t) - (yij**t))
    wij = (t*(xij-1.0)*(yij**t))/((1.0 + xij*(yij**t) - (yij**t) )) - 1.0/(np.log(np.abs(yij+eps)))
    return pij,wij

def eq(z, t, ki, si):
    nz = len(z)
    n = nz//2
    pij,wij = pij_wij(z[0:n],z[n:],t) # x is first half, y is second half
    #print(pij.shape,wij.shape,ki.shape,si.shape)
    #pij -= pij.di
    np.fill_diagonal(pij,0)
    np.fill_diagonal(wij,0)
    delta_pij = np.sum(pij,axis=0) - ki
    delta_wij = np.sum(wij,axis=0) - si
    return np.concatenate([delta_pij, delta_wij])
{% endhighlight %}

Now the choice of the solver is of high importance. We need to solve a bounded problem, as we know that both $x_i>0$ and $y_i>0$, since their nature is of exponentials.
Initialization is also a very important factor to keep into account. A large number of local optima are hidden in the optimization landscape, and we must avoid them.
As we know that $x_i$ and $y_i$ are in some way correlated to the degrees and the strengths of the empirical network, we initialize the solution $z_0 = \[x_1,x_2,\ldots,x_n, y_1,y_2,\ldots y_n \] \in \mathbb{R}^{2n}$ to be exactly the concatenation of degrees and strengths:

\begin{equation}
z_0 = \[ k_1, k_2, \ldots, k_n, s_1,s_2, \ldots s_n \]
\end{equation}

This intuition makes the optimization much much faster. Here we use a combination of the `scipy.optimize.root` function, together with a refinement offered by the `scipy.optimize.least_squares`.

{% highlight python %}
from scipy.optimize import root
sollm = root(lambda v: eq(v,t,k,s),
             x0=np.concatenate([k,s])*1E-4,
             method='lm', # use levenberg-marquardt method
             options={'xtol':1E-30,'gtol':1E-30,'ftol':1E-30},
             tol=1E-6)

from scipy.optimize import least_squares
sollm = least_squares(lambda v: eq(v,t,k,s),
                      x0=sollm['x'],
                      bounds= (0,np.inf),
                      method='trf',
                      ftol=1E-8,
                      xtol=1E-8,
                      verbose=1)

print('Final cost', sollm['cost'])
sollm = sollm['x']
n2 = int(len(sollm)//2)
x,y = sollm[0:n2],sollm[n2:]
{% endhighlight %}

Then we plot the results. A solution always exists, it is important though to check that the optimization algorithms terminated successfully.

{% highlight python %}
A=At
pij,wij = pij_wij(x,y,t) # compute the output from the optimization result
plt.figure(figsize=(12,8))
plt.subplot(2,3,1)
im = plt.imshow(pij)
plt.colorbar(im,fraction=0.046, pad=0.04)
plt.grid(False)
plt.title('$p_{ij}$')

plt.subplot(2,3,2)
im = plt.imshow(wij)
plt.colorbar(im,fraction=0.046, pad=0.04)
plt.grid(False)
plt.title('$<w_{ij}>$')

plt.subplot(2,3,3)
im = plt.imshow(A)
plt.colorbar(im,fraction=0.046, pad=0.04)
plt.grid(False)
plt.title('A')

plt.subplot(2,3,4)
plt.plot((A>0).sum(axis=0),pij.sum(axis=0), 'b.')
plt.plot(np.linspace(0,pij.sum(axis=0).max()),np.linspace(0,pij.sum(axis=0).max()),'r-')
plt.grid(True)
plt.axis('equal')
plt.title('$k_i - <k_i>$')
plt.ylabel('model')
plt.xlabel('empirical')
plt.xlim([0,min((A>0).sum(axis=0).max(),pij.sum(axis=0).max())])
plt.ylim([0,min((A>0).sum(axis=0).max(),pij.sum(axis=0).max())])

plt.subplot(2,3,5)
plt.plot(A.sum(axis=0),wij.sum(axis=0), 'b.')
plt.plot(np.linspace(0,wij.sum(axis=0).max()),np.linspace(0,wij.sum(axis=0).max()),'r-')
plt.title('$ s_i - <s_i>$')
plt.axis('equal')
plt.xlim([0,wij.sum(axis=0).max()])
plt.ylim([0,wij.sum(axis=0).max()])
plt.grid(True)
plt.ylabel('model')
plt.xlabel('empirical')

plt.tight_layout()
{% endhighlight %}


References
----------

- <a name="Garlaschelli2009"></a> The weighted random graph model. Garlaschelli D. https://arxiv.org/pdf/0902.0897.pdf
- <a name="Fronczak2012"></a> Statistical mechanics of the international trade network, Fronczak A., Fronczak P. [https://link.aps.org/doi/10.1103/PhysRevE.85.056113](https://link.aps.org/doi/10.1103/PhysRevE.85.056113)


