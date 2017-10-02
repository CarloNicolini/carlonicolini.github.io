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

# Gradients of the log-likelihood

We can write the log-likelihood as:

$$
\begin{equation}\label{eq:loglikelihood}
\log \mathcal{L}(\rho,\sigma(\boldsymbol \theta)) = \tr \lbrack \rho \log \sigma(\boldsymbol \theta)\rbrack
\end{equation}
$$

In order to maximize \ref{eq:loglikelihood} we minimize the $$-\log \mathcal{L}$$. Here we compute the gradients with respect to the parameters $$\boldsymbol \theta$$, where

$$
\begin{equation}\label{eq:logsigma}
\log \sigma(\boldsymbol \theta)= \log \left( e^{-\beta L} \right) - \log\left( \tr \lbrack e^{-\beta L}\rbrack \right) \mathbf{I}
\end{equation}
$$

where $$\mathbf{I}$$ is the $$n\times n$$ identity matrix.
It is possible to simplify the first term in \ref{eq:logsigma} as $$-\beta L$$ because we assume for positive definite matrices we can say $$\log \exp -\beta L = -\beta L$$ (To be checked).
We proceed plug \ref{eq:logsigma} in \ref{eq:loglikelihood} and write:

$$
\begin{equation}\label{eq:loglikelihood2}
-\log \mathcal{L}(\rho,\sigma(\boldsymbol \theta)) = -\tr \left \lbrack \rho \left(-\beta L - \log\left( \tr \lbrack e^{-\beta L}\rbrack \right) \mathbf{I}\right) \right \rbrack
\end{equation}
$$

Now we take the derivates with respect to the model parameters $$\boldsymbol \theta$$ embedded in $$\sigma(\boldsymbol \theta)$$ as follows:

$$
\begin{align*}
- \frac{\log \mathcal{L}}{\partial \boldsymbol \theta} =& -\frac{ \partial \tr \lbrack \rho \log\sigma(\boldsymbol \theta) \rbrack}{\partial \boldsymbol \theta} = - \tr \left \lbrack \rho \frac{\partial}{\partial \boldsymbol \theta}\left(-\beta L - \log\left( \tr \lbrack e^{-\beta L}\rbrack \right) \mathbf{I}\right) \right\rbrack \\ =& - \tr \left \lbrack \rho \left(-\beta \frac{\partial L}{\partial \boldsymbol \theta} - \frac{\mathbf{I}}{\tr\lbrack e^{-\beta L} \rbrack} \frac{\partial }{\partial \boldsymbol \theta}\left( \tr \lbrack e^{-\beta L}\rbrack \right) \right) \right\rbrack  \\ = & 
\beta \tr \left \lbrack \rho \frac{\partial L}{\partial \boldsymbol \theta} \right \rbrack + \frac{1}{\tr \lbrack e^{-\beta L}\rbrack} \frac{\partial}{\partial \boldsymbol \theta}\tr \left\lbrack e^{-\beta L} \right\rbrack
\end{align*} 
$$

We need to compute the last term $$\frac{\partial}{\partial \boldsymbol \theta}\tr \left\lbrack e^{-\beta L} \right\rbrack $$. In general the following holds:

$$
\begin{align*}
\frac{d}{d t}\tr \left\lbrack e^{X(t)} \right\rbrack &= \tr \left\lbrack \frac{d}{d t} e^{X(t)} \right\rbrack  \\&= \tr \int_0^1 e^{\alpha X(t)}\frac{d X}{d t} e^{(1-\alpha) X(t)} d\alpha  \\&= \int_0^1 \tr \left\lbrack e^{\alpha X(t)}\frac{d X}{d t} e^{(1-\alpha) X(t)}  \right\rbrack d\alpha \\&= \int_0^1 \tr \left\lbrack e^{(1-\alpha) X(t)} e^{\alpha X(t)}\frac{d X}{d t} \right\rbrack d\alpha \\&= \int_0^1 \tr \left\lbrack e^{X(t)} \frac{d X}{d t} \right\rbrack d\alpha \\&= \tr \left\lbrack e^{X(t)} \frac{d X}{d t} \right\rbrack
\end{align*}
$$

If we apply to our case we have:

$$
\begin{equation}
\frac{\partial}{\partial \boldsymbol \theta}\tr \left \lbrack e^{-\beta L} \right\rbrack = \tr \left\lbrack e^{-\beta L} \frac{\partial (-\beta L)}{\partial \boldsymbol \theta} \right\rbrack = -\beta \tr \left\lbrack e^{-\beta L} \frac{\partial L}{\partial \boldsymbol \theta} \right\rbrack
\end{equation}
$$

Therefore we have:

$$
\begin{align*}
- \frac{\partial \log \mathcal{L}}{\partial \boldsymbol \theta} &= \beta \tr \left \lbrack \rho \frac{\partial L}{\partial \boldsymbol \theta} \right \rbrack - \beta \frac{1}{\tr \lbrack e^{-\beta L}\rbrack} \tr \left\lbrack e^{-\beta L} \frac{\partial L}{\partial \boldsymbol \theta}  \right\rbrack = \\&= \beta \tr \left \lbrack \rho \frac{\partial L}{\partial \boldsymbol \theta} \right \rbrack - \beta \tr \left\lbrack \sigma(\boldsymbol \theta) \frac{\partial L}{\partial \boldsymbol \theta}  \right\rbrack \\&= \beta \tr \left \lbrack \left( \rho-\sigma(\boldsymbol \theta) \right) \frac{\partial L}{\partial \boldsymbol \theta} \right \rbrack 
\end{align*}
$$

## Second derivatives

# Derivatives of the Jensen-Shannon divergence

We need to take the derivative with respect to the parameters of

$$
\frac{\partial }{\partial \boldsymbol \theta} D_{JS}(\rho \| \sigma(\boldsymbol \theta)) = \frac{\partial }{\partial \boldsymbol \theta}\left \lbrack \frac{1}{2} D_{KL}(\rho \| \mu(\boldsymbol \theta)) + \frac{1}{2} D_{KL}(\sigma(\boldsymbol \theta) \| \mu(\boldsymbol \theta)) \right \rbrack
$$

where $$\mu(\boldsymbol \theta) = (\rho + \sigma(\boldsymbol \theta))/2$$.
This is equivalent to:

$$\begin{align*}
\frac{\partial }{\partial \boldsymbol \theta}\left \lbrack \frac{1}{2} D_{KL}(\rho \| \mu(\boldsymbol \theta)) + \frac{1}{2} D_{KL}(\sigma(\boldsymbol \theta) \| \mu(\boldsymbol \theta)) \right \rbrack = \\ \frac{1}{2} \left (\frac{\partial }{\partial \boldsymbol \theta}\left \lbrack \tr\left \lbrack \rho \log (\rho) \right \rbrack - \tr \left \lbrack \rho \log \mu(\boldsymbol \theta) \right \rbrack \right \rbrack 
+
\frac{\partial }{\partial \boldsymbol \theta}\left \lbrack \tr\left \lbrack \sigma(\boldsymbol \theta) \log (\sigma (\boldsymbol \theta) \right \rbrack - \tr \left \lbrack \rho \log \mu(\boldsymbol \theta) \right \rbrack \right \rbrack \right) 
\end{align*}
$$