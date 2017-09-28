---
layout: post
title: Log-likelihood derivatives of matrix functions
categories: science
published: false
use_math: true
date: 2017-09-23
---

<blockquote>
	"How to compute the derivatives of log-likelihood involving matrix exponentials?"
</blockquote>

In convex optimization one is often faced with the problem of computing derivatives with respect to some model parameters of complex log-likelihood functions that involve the definition of matrix functions. A typical example is how to compute the gradient with respect to some set of parameters $$\boldsymbol \theta \in \mathbb{R}^n$$ of a function of this kind:

$$
\begin{equation}\label{eq:derivloglike}
\frac{\partial}{\partial \boldsymbol{\theta}} \left( \log \det e^{\rho \log \sigma(\boldsymbol{\theta})} \right )
\end{equation}
$$

where $$\rho, \sigma \in \mathbb{S}_{++}^n$$ are positive definite $$n \times n$$ matrices. In this case $$\rho$$ is the Von Neumann quantum density matrix (it can be seen as a correlation matrix) of an observed quantum system and $$\sigma(\boldsymbol \theta)$$ is instead the Von Neumann quantum density of the model, for this reason it depends on the parameters vector $$\boldsymbol \theta$$. To do this computation we apply the chain rule of derivatives on a general matrix function $$V(\boldsymbol \theta)$$. As shown in [Hubbard & Hubbard 1999](http://www.matrixeditions.com/UnifiedApproach4th.html) one obtains the expression \ref{loglikelihoodderiv}:

$$
\begin{equation}
\label{loglikelihoodderiv}
\frac{\partial}{\partial {\theta}_k} \log \det V(\boldsymbol{\theta}) = \tr \left( V^{-1} \frac{\partial}{\partial {\theta}_k}V^T(\boldsymbol{\theta}) \right)
\end{equation}
$$

We define $$V(\boldsymbol \theta):= e^{\rho \log \sigma(\boldsymbol \theta)}$$ so we have to compute \ref{eq:derivloglike} as:

$$
\frac{\partial}{\partial \boldsymbol{\theta}} \left( \log \det e^{\rho \log \sigma(\boldsymbol{\theta})} \right ) = \tr \left( \left(e^{\rho \log \sigma(\boldsymbol{\theta})}\right)^{-1} \frac{\partial}{\partial {\theta}_k}\left( e^{\rho \log \sigma(\boldsymbol{\theta})} \right)^T \right) 
$$

We note that our matrix $$e^{\rho \log \sigma(\boldsymbol{\theta})}$$ is symmetric, then in this case $$V=V^T$$. With some manipulations we get for the derivatives of $$V(\boldsymbol \theta)$$ the following expression:

$$
\begin{align}
\frac{\partial}{\partial {\theta}_k} V(\boldsymbol{\theta}) =  \frac{\partial}{\partial {\theta}_k} e^{\rho \log \sigma(\boldsymbol{\theta})} &= 
e^{\rho \log \sigma(\boldsymbol{\theta})} \frac{\partial}{\partial {\theta}_k}\rho \log \sigma(\boldsymbol{\theta}) \\ &= 
e^{\rho \log \sigma(\boldsymbol{\theta})} \rho \frac{\partial}{\partial {\theta}_k}\log \sigma(\boldsymbol{\theta}) \\ &= 
e^{\rho \log \sigma(\boldsymbol{\theta})} \rho \sigma^{-1}(\boldsymbol{\theta}) \frac{\partial}{\partial {\theta}_k} \sigma(\boldsymbol{\theta})
\end{align}
$$


Now we know that $$\sigma(\boldsymbol \theta)$$ is the quantum density matrix that is written like:

$$
\sigma(\boldsymbol \theta) = \frac{e^{-\beta L(\boldsymbol \theta)}}{\tr{\left( e^{-\beta L(\boldsymbol \theta)}\right)}}
$$

and we have to take the derivative with respect to $$\theta_k$$. We obtain the following expression for the derivative of the quantum density matrix with respect to the model parameters:

$$
\begin{align}\label{dsigmadthetak}
\frac{\partial}{\partial {\theta}_k} \sigma(\boldsymbol{\theta}) = \frac{ \frac{\partial}{\partial {\theta}_k} \left\lbrack e^{-\beta L(\boldsymbol \theta)} \right \rbrack \tr \left \lbrack e^{-\beta L(\boldsymbol \theta)}\right \rbrack - \frac{\partial}{\partial {\theta}_k} \left\lbrack \tr \left\lbrack e^{-\beta L(\boldsymbol \theta)} \right\rbrack \right\rbrack e^{-\beta L(\boldsymbol \theta)}
}{ \left( \tr\left( e^{-\beta L(\boldsymbol \theta)} \right) \right)^2 }
\end{align}
$$

Now calculate each thing separately:

$$
\begin{equation}\label{dexpdthetak}
\frac{\partial}{\partial {\theta}_k} \left\lbrack e^{-\beta L(\boldsymbol \theta)} \right \rbrack = -\beta \left( \frac{\partial L(\boldsymbol \theta)}{\partial {\theta}_k} \right) e^{-\beta L(\boldsymbol \theta)}
\end{equation}
$$

$$
\begin{equation}\label{dtrexpdthetak}
\frac{\partial}{\partial {\theta}_k} \left\lbrack \tr \left \lbrack e^{-\beta L(\boldsymbol \theta)} \right\rbrack \right \rbrack = \tr \left\lbrack -\beta \left( \frac{\partial L(\boldsymbol \theta)}{\partial {\theta}_k} \right) e^{-\beta L(\boldsymbol \theta)} \right \rbrack
\end{equation}
$$

Plugging \ref{dtrexpdthetak} and \ref{dexpdthetak} into \ref{dsigmadthetak} we obtain the rather long expression for the derivative of the quantum density matrix of the model:

$$
\begin{align}\label{dsigmadthetakfinal}
\frac{\partial}{\partial {\theta}_k} \sigma(\boldsymbol{\theta}) & =
\frac{ -\beta \left( \frac{\partial L(\boldsymbol \theta)}{\partial {\theta}_k} \right) e^{-\beta L(\boldsymbol \theta)} \tr \lbrack e^{-\beta L(\boldsymbol \theta)} \rbrack}{\left( \tr\left  \lbrack e^{-\beta L(\boldsymbol \theta)} \right \rbrack \right)^2} + \ldots \\ & - \frac{ \tr \left\lbrack -\beta \left( \frac{\partial L(\boldsymbol \theta)}{\partial {\theta}_k} \right) e^{-\beta L(\boldsymbol \theta)} \right \rbrack e^{-\beta L(\boldsymbol \theta)}}{\left( \tr\left  \lbrack e^{-\beta L(\boldsymbol \theta)} \right \rbrack  \right)^2}
\end{align}
$$

We can now note that it is possible to recollect back $$\sigma(\boldsymbol \theta)$$ in the last expression \ref{dsigmadthetakfinal}. With this in mind we can write \ref{dsigmadthetakfinal} as:

$$
\begin{align}
\frac{\partial}{\partial {\theta}_k} \sigma(\boldsymbol{\theta}) & = -\beta \left( \frac{\partial L(\boldsymbol \theta)}{\partial {\theta}_k} \right)\sigma(\boldsymbol \theta) 
+ \beta \frac{\tr \left\lbrack \left( \frac{\partial L(\boldsymbol \theta)}{\partial {\theta}_k} \right) e^{-\beta L(\boldsymbol \theta)} \right \rbrack}{\tr\left  \lbrack e^{-\beta L(\boldsymbol \theta)} \right \rbrack} \sigma(\boldsymbol \theta)
\end{align} 
$$

Now we must glue together all the elements to get back to our original problem \ref{loglikelihoodderiv}.
We replace $$V(\boldsymbol \theta)$$ with $$e^{\rho \log \sigma(\boldsymbol \theta)}$$ and apply the necessary substitutions to get:

<!-- $$
\begin{equation}
\tr \left \lbrack  e^{-\rho \log \sigma(\boldsymbol\theta)} e^{\rho \log \sigma(\boldsymbol \theta)} \rho \sigma^{-1}(\boldsymbol \theta) \frac{ -\beta \left( \frac{\partial L(\boldsymbol \theta)}{\partial {\theta}_k} \right) e^{-\beta L(\boldsymbol \theta)} \tr \lbrack e^{-\beta L(\boldsymbol \theta)} \rbrack - \tr \left\lbrack -\beta \left( \frac{\partial L(\boldsymbol \theta)}{\partial {\theta}_k} \right) e^{-\beta L(\boldsymbol \theta)} \right \rbrack e^{-\beta L(\boldsymbol \theta)}}{\left( \tr\left  \lbrack e^{-\beta L(\boldsymbol \theta)} \right \rbrack \right)^2} \right \rbrack
\end{equation}
$$
 -->

$$
\begin{equation}\label{}
\frac{\partial}{\partial \theta_k}  \left( \log \det e^{\rho \log \sigma(\boldsymbol{\theta})} \right ) = \tr \left \lbrack - \beta \rho \sigma^{-1}(\boldsymbol \theta) \left( \frac{\partial L(\boldsymbol \theta)}{\partial \theta_k} \right) \sigma(\boldsymbol \theta) + \beta \rho \tr \left\lbrack \left(\frac{\partial L(\boldsymbol \theta)}{\partial \theta_k}  \right) \sigma(\boldsymbol \theta)\right\rbrack \right \rbrack
\end{equation}
$$

Here we can get rid of the $$\beta$$. Maximum likelihood solutions must zero the gradients (called Fisher scores). For this reason  

$$
\begin{equation}\label{gradients_loglike}
\frac{\partial}{\partial \theta_k}  \left( \log \det e^{\rho \log \sigma(\boldsymbol{\theta})} \right ) = - \beta
\tr \left \lbrack  \rho \sigma^{-1}(\boldsymbol \theta) \left( \frac{\partial L(\boldsymbol \theta)}{\partial \theta_k} \right) \sigma(\boldsymbol \theta) \right \rbrack + \beta \tr \left\lbrack \left(\frac{\partial L(\boldsymbol \theta)}{\partial \theta_k}  \right) \sigma(\boldsymbol \theta)\right\rbrack 
\end{equation}
$$

because $$\tr[\rho]=1$$ and $$\tr[\sigma]=1$$ by definition. When $$\rho \equiv \sigma$$ then the gradients are identically zero, as expected for points of maximum likelihood (minimum divergence).

It is possible to analytically compute the gradients for generative models for which we know the expected value of the realization of an edge, in other words for models where the graph laplacian can be described at edge with an analytical expression for $$E[L_{ij}]$$.
In the case of random modular graph 

The inverse of quantum density is computed as:

$$
\sigma^{-1}(\boldsymbol \theta)  = \left( \frac{e^{-\beta L(\boldsymbol \theta)}}{\tr \left \lbrack{e^{-\beta L(\boldsymbol \theta)}} \right \rbrack} \right)^{-1} = e^{\beta L(\boldsymbol \theta)} \tr \left \lbrack{e^{-\beta L(\boldsymbol \theta)}} \right \rbrack
$$

# Derivatives of the Jensen-Shannon divergence

We need to take the derivative with respect to the parameters of

$$
\frac{\partial }{\partial \boldsymbol \theta} D_{JS}(\rho \| \sigma(\boldsymbol \theta)) = \frac{\partial }{\partial \boldsymbol \theta}\left \lbrack \frac{1}{2} D_{KL}(\rho \| \mu(\boldsymbol \theta)) + \frac{1}{2} D_{KL}(\sigma(\boldsymbol \theta) \| \mu(\boldsymbol \theta)) \right \rbrack
$$

where $$\mu(\boldsymbol \theta) = (\rho + \sigma(\boldsymbol \theta))/2$$.
This is equivalent to:

$$
\frac{\partial }{\partial \boldsymbol \theta}\left \lbrack \frac{1}{2} D_{KL}(\rho \| \mu(\boldsymbol \theta)) + \frac{1}{2} D_{KL}(\sigma(\boldsymbol \theta) \| \mu(\boldsymbol \theta)) \right \rbrack = \frac{1}{2} \left (\frac{\partial }{\partial \boldsymbol \theta}\left \lbrack \tr\left \lbrack \rho \log (\rho) \right \rbrack - \tr \left \lbrack \rho \log \mu(\boldsymbol \theta) \right \rbrack \right \rbrack 
+
\frac{\partial }{\partial \boldsymbol \theta}\left \lbrack \tr\left \lbrack \sigma(\boldsymbol \theta) \log (\sigma (\boldsymbol \theta) \right \rbrack - \tr \left \lbrack \rho \log \mu(\boldsymbol \theta) \right \rbrack \right \rbrack

\right)
$$