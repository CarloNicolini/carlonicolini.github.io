---
layout: post
title: Matrix derivatives
categories: science
published: false
date: 2017-09-23
---

Let's try to compute the derivatives with respect to $$\boldsymbol{\theta}$$ of this complex matrix function

$$
\begin{equation}
\frac{\partial}{\partial \boldsymbol{\theta}} \left( \log \det e^{\rho \log \sigma(\boldsymbol{\theta})} \right )
\end{equation}
$$

To do this let's apply this rule:

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
\frac{\partial}{\partial {\theta}_k} V(\boldsymbol{\theta}) =  \frac{\partial}{\partial {\theta}_k} e^{\rho \log \sigma(\boldsymbol{\theta})}
$$

which results in:

$$
\begin{align}
\frac{\partial}{\partial {\theta}_k} e^{\rho \log \sigma(\boldsymbol{\theta})} \\ &= 
\frac{\partial}{\partial {\theta}_k} e^{\rho \log \sigma(\boldsymbol{\theta})} \\ &= 
e^{\rho \log \sigma(\boldsymbol{\theta})} \frac{\partial}{\partial {\theta}_k}\rho \log \sigma(\boldsymbol{\theta}) \\ &= 
e^{\rho \log \sigma(\boldsymbol{\theta})} \rho \frac{\partial}{\partial {\theta}_k}\log \sigma(\boldsymbol{\theta}) \\ &= 
e^{\rho \log \sigma(\boldsymbol{\theta})} \rho \sigma^{-1}(\boldsymbol{\theta}) \frac{\partial}{\partial {\theta}_k} \sigma(\boldsymbol{\theta})
\end{align}
$$

Now we know that $$\sigma(\theta)$$ is the quantum density that is written like:

$$
\sigma(\boldsymbol \theta) = \frac{e^{-\beta L(\boldsymbol \theta)}}{\tr{\left( e^{-\beta L(\boldsymbol \theta)}\right)}}
$$

and we have to take the derivative 

$$
\begin{align}\label{dsigmadthetak}\tag{1}
\frac{\partial}{\partial {\theta}_k} \sigma(\boldsymbol{\theta}) = \frac{ \frac{\partial}{\partial {\theta}_k} \left\lbrack e^{-\beta L(\boldsymbol \theta)} \right \rbrack \tr \left \lbrack e^{-\beta L(\boldsymbol \theta)}\right \rbrack - \frac{\partial}{\partial {\theta}_k} \left\lbrack \tr \left\lbrack e^{-\beta L(\boldsymbol \theta)} \right\rbrack \right\rbrack e^{-\beta L(\boldsymbol \theta)}
}{ \left( \tr\left( e^{-\beta L(\boldsymbol \theta)} \right) \right)^2 }
\end{align}
$$

Now calculate each thing separately:

$$
\begin{equation}\label{dexpdthetak}\tag{2}
\frac{\partial}{\partial {\theta}_k} \left\lbrack e^{-\beta L(\boldsymbol \theta)} \right \rbrack = -\beta \left( \frac{\partial}{\partial {\theta}_k}  \lbrack L(\boldsymbol \theta)\rbrack \right) e^{-\beta L(\boldsymbol \theta)}
\end{equation}
$$

$$
\begin{equation}\label{dtrexpdthetak}\tag{3}
\frac{\partial}{\partial {\theta}_k} \left\lbrack \tr \left \lbrack e^{-\beta L(\boldsymbol \theta)} \right\rbrack \right \rbrack = \tr \left\lbrack -\beta \left( \frac{\partial}{\partial {\theta}_k}  \lbrack L(\boldsymbol \theta)\rbrack \right) e^{-\beta L(\boldsymbol \theta)} \right \rbrack
\end{equation}
$$

Plugging \ref{dtrexpdthetak} and \ref{dexpdthetak} into \ref{dsigmadthetak} we obtain:

$$
\begin{align}\label{dsigmadthetakfinal}
\frac{\partial}{\partial {\theta}_k} \sigma(\boldsymbol{\theta}) = 
\frac{ -\beta \left( \frac{\partial}{\partial {\theta}_k}  \lbrack L(\boldsymbol \theta)\rbrack \right) e^{-\beta L(\boldsymbol \theta)} \tr \lbrack e^{-\beta L(\boldsymbol \theta)} \rbrack - \tr \left\lbrack -\beta \left( \frac{\partial}{\partial {\theta}_k}  \lbrack L(\boldsymbol \theta)\rbrack \right) e^{-\beta L(\boldsymbol \theta)} \right \rbrack e^{-\beta L(\boldsymbol \theta)}}{\left( \tr\left  \lbrack e^{-\beta L(\boldsymbol \theta)} \right \rbrack \right)^2}
\end{align}
$$

with

$$\Gamma(\boldsymbol \theta) := -\beta \left( \frac{\partial}{\partial {\theta}_k}  \lbrack L(\boldsymbol \theta)\rbrack \right) e^{-\beta L(\boldsymbol \theta)} $$

it becomes:

$$
\begin{align}\label{dsigmadthetakfinal2}
\frac{\partial}{\partial {\theta}_k} \sigma(\boldsymbol{\theta}) = 
\frac{ \Gamma(\boldsymbol \theta) \tr \lbrack e^{-\beta L(\boldsymbol \theta)} \rbrack - \tr \left\lbrack \Gamma(\boldsymbol \theta) \right \rbrack e^{-\beta L(\boldsymbol \theta)}}{\left( \tr\left  \lbrack e^{-\beta L(\boldsymbol \theta)} \right \rbrack \right)^2}
\end{align}
$$

we can now plug \ref{dsigmadthetakfinal2} into \ref{loglikelihoodderiv} to obtain

$$
\begin{equation}\label{}
\tr \left \lbrack  e^{-\rho \log \sigma(\boldsymbol\theta)} e^{\rho \log \sigma(\boldsymbol \theta)} \rho \sigma^{-1} \frac{ -\beta \left( \frac{\partial}{\partial {\theta}_k}  \lbrack L(\boldsymbol \theta)\rbrack \right) e^{-\beta L(\boldsymbol \theta)} \tr \lbrack e^{-\beta L(\boldsymbol \theta)} \rbrack - \tr \left\lbrack -\beta \left( \frac{\partial}{\partial {\theta}_k}  \lbrack L(\boldsymbol \theta)\rbrack \right) e^{-\beta L(\boldsymbol \theta)} \right \rbrack e^{-\beta L(\boldsymbol \theta)}}{\left( \tr\left  \lbrack e^{-\beta L(\boldsymbol \theta)} \right \rbrack \right)^2} \right \rbrack
\end{equation}
$$


$$
\begin{equation}\label{}
\tr \left \lbrack  I \rho \sigma^{-1} \frac{ -\beta \left( \frac{\partial}{\partial {\theta}_k}  \lbrack L(\boldsymbol \theta)\rbrack \right) e^{-\beta L(\boldsymbol \theta)} \tr \lbrack e^{-\beta L(\boldsymbol \theta)} \rbrack - \tr \left\lbrack -\beta \left( \frac{\partial}{\partial {\theta}_k}  \lbrack L(\boldsymbol \theta)\rbrack \right) e^{-\beta L(\boldsymbol \theta)} \right \rbrack e^{-\beta L(\boldsymbol \theta)}}{\left( \tr\left  \lbrack e^{-\beta L(\boldsymbol \theta)} \right \rbrack \right)^2} \right \rbrack
\end{equation}
$$


$$
\begin{equation}\label{}
- \beta \rho \sigma^{-1}(\boldsymbol \theta) \left( \frac{\partial}{\partial \theta_k}L(\boldsymbol \theta) \right) \sigma(\boldsymbol \theta) + \beta \rho \tr \left\lbrack \left(\frac{\partial}{\partial \theta_k}L(\boldsymbol \theta)  \right) \sigma(\boldsymbol \theta)\right\rbrack
\end{equation}
$$