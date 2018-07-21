---
layout: post
title: Spectral density via the average resolvent
categories: science
published: true
date: 2018-06-25
---

The spectral density of a random matrix can be obtained numerically via histogramming or in a more analytically amenable form thanks to the resolvent and Stieltjes transform.

The spectral density $$\varrho$$ of a Laplacian matrix $$\mathbf{L}$$ can be defined via the delta function as:
\begin{equation}
\varrho(z) = \frac{1}{n}\sum_{i=1}^n \delta(z-\lambda_i)
\end{equation}
where $$\lambda_i$$ are the eigenvalues of the matrix.
Thanks to the so-called Plemelij-Sokhotski formula, it is possible to write the delta function as the limit in the complex plane approaching the real line of the imaginary part of the following quantity:
\begin{equation}
\delta(x) = -\frac{1}{\pi} \lim \limits_{\eta \to 0^+} \mathrm{Im} {\frac{1}{x + i \eta } },
\end{equation}
hence for the spectral density we recover the following intimidating expression:
\begin{equation}
\varrho(x) = -\frac{1}{n \pi} \lim \limits_{\eta \to 0^+} \mathrm{Im} {\sum \limits_{i=1}^n \frac{1}{x + i \eta - \lambda_i} }.
\end{equation}
Now we identify the complex variable $$z=x+i \eta$$ and thanks to a change of basis and the properties of matrix functions, we can evaluate the sum in the argument of the imaginary function as:
\begin{equation}
\sum \limits_{i=1}^n \frac{1}{x + i \eta -\lambda_i } = \mathrm{Tr}{(z \mathbf{I} - \mathbf{L})^{-1}}
\end{equation}
The function $$R(z)=(z\mathbf{I} -\mathbf{L})^{-1}$$ is called the \emph{resolvent matrix} of $$\mathbf{L}$$.
By averaging over the resolvent we can get an expression for the expected spectral density over the ensemble of random matrices denoted by $$\mathbf{L}(\boldsymbol{\theta})$$:
\begin{equation}
\mathbb{E}{\varrho(z)} = -\frac{1}{n \pi} \lim \limits_{\eta \to 0^+} \mathrm{Im}{ \mathrm{Tr}{ \mathbb{E}{ (z I - \mathbf{L} )^{-1} } }}
\end{equation}
where the expectation is taken over the ensemble of networks $$\mathbf{L}$$ with parameters $$\boldsymbol{\theta}$$. The quantity $$\mathrm{Tr}{(z I - \mathbf{L} )^{-1}}/n$$  is called the Stieltjes transform.
Importantly the resolvent is the generating function of the moments $$\mu_k=\mathbb{E}{\mathrm{Tr}{\mathbf{L}^k}}$$ of the spectral density:
\begin{equation}
\mathbb{E}{ (z I - \mathbf{L} )^{-1} }  = \int dx' \frac{\varrho(x')}{z-x'} = \frac{1}{z}\sum_{k=0}^{\infty} dx' \varrho(x') \left( \frac{x'}{z}^k \right) = \sum_{k=0}^{\infty} \frac{\mu_k}{z^{k+1}}
\end{equation}
where, by normalization of the density $$\mu_0=1$$. In general we can compute the average traces of a random matrix $$\mathbf{X}$$ by means of integrals over their spectral density:
\begin{equation}\mathbb{E}{\mathrm{Tr}{\mathbf{X}^k}}= n \int d\lambda \lambda^k \varrho(\lambda | \mathbf{X}).
\end{equation}
In the rest of this document, to simplify notation we identify the average spectral density $$\mathbb{E}{\varrho}$$ simply as $$\varrho$$.
This also apply in the case of matrix functions, thanks to the series expansion. Keep this in mind for the purpose of our investigation:
\begin{equation}\label{eq:trace_integral}
\mathbb{E}{\mathrm{Tr}{e^{-\beta \mathbf{L}}}} = n \int \limits_{-\infty}^{\infty} e^{-\beta \lambda} \varrho(e^{-\beta \lambda}) d\lambda
\end{equation}
	
This is a Python code to compute the spectral density of a random matrix ensemble via the average resolvent.

{% highlight python %}
import numpy as np
from scipy.linalg import eigvalsh
import matplotlib.pyplot as plt

def spectral_density_laplacian_er(n,p,x,reps,eps=1E-1):
    def resolvent_trace(x,lambdai):
        return np.sum([1.0/(xi+1j*eps-x) for xi in lambdai])
    def average_resolvent_trace(x):
        return np.mean([resolvent_trace(x, eigvalsh(LER(n,p)) ) for r in range(0,reps)])
    return [-1/(np.pi*n)*np.imag(average_resolvent_trace(z)) for z in x]
{% endhighlight %}

The $$\epsilon$$ parameter (`eps` in the code) is the one present in the limit.
While analytically a limit procedure should be computed, but to perform the thing numerically, it corresponds to the bin size of an histogram, so if it is not too big (in the order 0.1) the noise of the expectations is averaged out.
The spectral density is computed as:
\begin{equation}\label{eq:xxx}
\rho(x) = -\frac{1}{\pi n} \lim \limits_{\epsilon \to 0^+} \mathrm{Im} \left \langle \sum \limits_{i=1}^n \frac{1}{\lambda_i + j\epsilon - x} \right \rangle
\end{equation}

You can test it in this way:

{% highlight python %}
n=200
p=0.25
x=np.linspace(350,650,50)
reps=10
rho = spectral_density_laplacian_er(n,p,x,reps)
plt.plot(x,rho)
{% endhighlight %}

and compare with this result:

{%highlight python %}
plt.hist(np.array([eigvalsh(LER(n,p)) for r in range(0,10)]).flatten(),200,normed='freq')
plt.show()
{% endhighlight %}


