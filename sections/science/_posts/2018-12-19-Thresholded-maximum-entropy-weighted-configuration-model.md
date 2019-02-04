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
\langle w_{ij} \rangle =  \frac{\partial F}{\partial \beta_{ij}} = \frac{\beta_{ij}t + 1}{\beta_{ij}(\beta_{ij} t e^{\alpha_ij + \beta_{ij}t}+1)} = \frac{t\log(y_{ij})-1}{\log( y_{ij})} \left(\frac{x_{ij} y_{ij}^t}{x_{ij}y_{ij}^t - t \log y_{ij}} \right) = \frac{t\log(y_{ij})-1}{\log( y_{ij})} \langle a_{ij} \rangle
\end{align}

The likelihood is obtained by the log of the probability:

\begin{align}
\log P(G) =& \sum_{i<j} \log(-\log(y_iy_j)) + \Theta(w_{ij}-t)\log(x_i x_j) + \\\\ & w_{ij}\Theta(w_{ij}-t)\log(y_i y_j) - \log\left( x_i
 x_j (y_i y_j)^t - t \log(y_i y_j) \right)
\end{align}


Generic solution
----------------

We are able to give the general form of the problem.
Given the Hamiltonian $H(G)$:

\begin{equation}
H(G) = \sum \limits_{i<j} (\alpha_{ij}) \Theta(w_{ij}-t) + (\beta_{ij}) w_{ij} \Theta(w_{ij}-t)
\end{equation}

we call $\Theta(w_{ij}-t):=A_{ij}$ and $w_{ij} \Theta(w_{ij}-t):= A_{ij} w_{ij}$. We make the substitions $e^{-\alpha_{ij}}=x_{ij}$ and $e^{-\beta_{ij}}=y_{ij}$ so we have

\begin{equation}
H(G) = - \sum \limits_{i<j} \log(x_{ij})^{A_{ij}} \log(y_{ij})^{A_{ij}W_{ij}}
\end{equation}

The partition function is

\begin{equation}
Z(\mathcal{G}) = \prod_{i<j} t + \frac{e^{-\alpha_{ij} e^{-\beta_{ij}}} }{\beta_{ij}} = \prod_{i<j} t - \frac{x_{ij} y_{ij}^t}{\log(y_{ij})}
\end{equation}

hence the graph probability becomes:

\begin{equation}
P(G) = \frac{e^{-H(G)}}{Z} = \log (y_{ij}) \frac{x_{ij}^{A_{ij}} y_{ij}^{w_{ij}A_{ij}} }{t \log (y_{ij}) - x_{ij}y_{ij}^t}
\end{equation}

hence the log-likelihood becomes

\begin{equation}
\log P(G) = \sum_{i<j} \left(w_{ij} \left(\log{\left (y_{i} y_j \right )} \right) + \log{\left (x_{i} x_j \right )} \right) a_{ij} + \log{\left (- \frac{\log{\left (y_{i} y_j \right )} } {- t \left(\log{\left (y_{i} y_j \right )}\right) + x_{i} x_{j} \left(y_{i} y_{j}\right)^{t}} \right )}
\end{equation}

# Convince your self

{% highlight python %}
import sympy as sp
#from sympy.abc import k,s,t,x,y,alpha,beta,w
sp.init_printing()

aij=sp.Symbol('a_{ij}', positive=True,real=True)
wij=sp.Symbol('w_{ij}', positive=True,real=True)
t = sp.Symbol('t', positive=True,real=True)
alphai = sp.Symbol('\\alpha_i',positive=True,real=True)
alphaj = sp.Symbol('\\alpha_j',positive=True,real=True)
betai = sp.Symbol('\\beta_i',positive=True,real=True)
betaj = sp.Symbol('\\beta_j',positive=True,real=True)

xi = sp.Symbol('x_i',positive=True,real=True)
xj = sp.Symbol('x_j',positive=True,real=True)
yi = sp.Symbol('y_i',positive=True,real=True)
yj = sp.Symbol('y_j',positive=True,real=True)

H = ((alphai+alphaj)*sp.Heaviside(wij-t) + (betai+betaj)*wij*sp.Heaviside(wij-t))
Z = sp.simplify(sp.integrate(sp.exp(-H.rewrite(sp.Piecewise)), (wij,0,sp.oo)))
Z = sp.simplify(Z.replace(betai,-sp.log(yi)).replace(betaj,-sp.log(yj)).replace(alphai,-sp.log(xi)).replace(alphaj,-sp.log(xj)))
{% endhighlight %}

The resulting partition function is exactly as before specified:
\begin{equation}
Z(\mathcal{G}) = \frac{- x_{i} x_{j} \left(y_{i} y_{j}\right)^{t} + \log{\left (\left(y_{i} y_{j}\right)^{t} \right )}}{\log{\left (y_{i} y_{j} \right )}}
\end{equation}

The graph probability becomes:
{% highlight python %}
P = sp.simplify(sp.exp(-H.replace(betai,-sp.log(yi)).replace(betaj,-sp.log(yj)).replace(alphai,-sp.log(xi)).replace(alphaj,-sp.log(xj)))/Z)
sp.expand_log(P)
{% endhighlight %}
with the result:
\begin{equation}
P(G) = - \frac{\left(x_{i} x_{j} \left(y_{i} y_{j}\right)^{w_{ij}}\right)^{\theta\left(- t + w_{ij}\right)} \left(\log{\left (y_{i} \right )} + \log{\left (y_{j} \right )}\right)}{- t \left(\log{\left (y_{i} \right )} + \log{\left (y_{j} \right )}\right) + x_{i} x_{j} \left(y_{i} y_{j}\right)^{t}}
\end{equation}

and its logarithm, i.e. the likelihood becomes:
{% highlight python %}
sp.expand_log(sp.log(P))
{% endhighlight %}
with the following result
\begin{equation}
\log  P(G \vert x_i, y_i) = - \frac{\left(x_{i} x_{j} \left(y_{i} y_{j}\right)^{w_{ij}}\right)^{\theta\left(- t + w_{ij}\right)} \left(\log{\left (y_{i} \right )} + \log{\left (y_{j} \right )}\right)}{- t \left(\log{\left (y_{i} \right )} + \log{\left (y_{j} \right )}\right) + x_{i} x_{j} \left(y_{i} y_{j}\right)^{t}} 
\end{equation}

where $\Theta(w_{ij}-t)$ is clearly the binarized adjacency matrix.

The link existence probability $\langle a_{ij}\rangle$ is obtained as $\partial F/\partial \alpha_i$, where $F=-\log(Z)$, hence:

{% highlight python %}
F = -sp.log(sp.expand_log(Z))
dalphai=-sp.log(xi)
dbetai=-sp.log(yi)
sp.simplify(sp.diff(F,xi)*sp.diff(sp.exp(-alphai),alphai)).replace(sp.exp(-alphai),xi)
{% endhighlight %}

and the result is:
\begin{equation}
\langle a_{ij} \rangle  =  \frac{x_{i} x_{j} \left(y_{i} y_{j}\right)^{t}}{x_{i} x_{j} \left(y_{i} y_{j}\right)^{t} - \log{\left (\left(y_{i} y_{j}\right)^{t} \right )}}
\end{equation}

the expected link weight is instead 

\begin{equation}
\langle w_{ij} \rangle = \frac{\log{\left (y_{i}^{t} y_{j}^{t} \right )} - 1}{\log{\left (y_{i} y_{j} \right )}} \frac{x_{i} x_{j} \left(y_{i} y_{j}\right)^{t}}{x_{i} x_{j} \left(y_{i} y_{j}\right)^{t} - \log{\left (\left(y_{i} y_{j}\right)^{t} \right )}}
\end{equation}