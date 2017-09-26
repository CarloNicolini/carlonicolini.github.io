---
layout: post
title: Matrix derivatives
categories: science
published: false
use_math: true
date: 2017-09-23
---

## Computing the derivatives of a log-likelihood function involving matrix exponentials

Let's try to compute the derivatives with respect to $$\boldsymbol{\theta}$$ of this complex matrix function

$$
\begin{equation}
\frac{\partial}{\partial \boldsymbol{\theta}} \left( \log \det e^{\rho \log \sigma(\boldsymbol{\theta})} \right )
\end{equation}
$$

Here $$\boldsymbol \theta$$ is a vector of $$K$$ (real) parameters. To compute this derivative we apply the chain rule obtaining for a general matrix function $$V(\boldsymbol \theta)$$ the following expression (\ref{loglikelihoodderiv}):

$$
\begin{equation}
\label{loglikelihoodderiv}
\frac{\partial}{\partial {\theta}_k} \log \det V(\boldsymbol{\theta}) = \tr \left( V^{-1} \frac{\partial}{\partial {\theta}_k}V^T(\boldsymbol{\theta}) \right)
\end{equation}
$$

where in our case:

$$
V(\boldsymbol{\theta}) =  e^{\rho \log \sigma(\boldsymbol{\theta})}
$$

so we have to compute this:

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
\frac{\partial}{\partial {\theta}_k} \sigma(\boldsymbol{\theta}) & = -\beta \left( \frac{\partial L(\boldsymbol \theta)}{\partial {\theta}_k} \right) e^{-\beta L(\boldsymbol \theta)}\sigma(\boldsymbol \theta) 
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

