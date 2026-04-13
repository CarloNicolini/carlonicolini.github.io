---
layout: post
title: Variational inference and model fitting of complex networks 
description: 'Variational inference and model fitting of complex networks.'
published: false
use_math: true
date: 2018-06-25
categories:
  - science
  - complex-networks
---

## Spectral maximum likelihood framework

Graphs with $n$ nodes and $m$ edges.
We want to model some observed network with Laplacian $\mathbf{L}^\star$ and density matrix $\boldsymbol{\rho}$ using a model where entries are considered random variables parametrized by parameters $\boldsymbol{\theta} \in \mathbb{R}^l$.

We seek to minimize the following quantity over the space of network ensemble parameters:

<div markdown="0">

\begin{equation}
\label{eq:expected_rel_entropy}
\mathbb{E}\left[ S(\boldsymbol{\rho} \| \boldsymbol{\sigma}(\boldsymbol{\theta})) \right]
= \mathbb{E}\left[ \mathrm{Tr}\left[ \boldsymbol{\rho} \log \boldsymbol{\rho} \right]
- \mathrm{Tr}\left[ \boldsymbol{\rho} \log \boldsymbol{\sigma}(\boldsymbol{\theta}) \right] \right]
\end{equation}

</div>

where the expectation $\mathbb{E}\left[ \cdot \right]$ is to be made over the set of all networks produced by a generative model at parameters $\boldsymbol{\theta}$.

As in the maximum likelihood formalism, in our framework we can identify the relative entropy as composed of a term depending on the observation alone and a term depending on the log-likelihood of the model given the data.
Hence, Eq.~$\eqref{eq:expected_rel_entropy}$ can be decomposed into the contribution of a term not depending on the model parameters $\boldsymbol{\theta}$ plus a term depending on them:

<div markdown="0">

\begin{equation}
\label{eq:decomposition}
\mathbb{E}\left[ S(\boldsymbol{\rho} \| \boldsymbol{\sigma}(\boldsymbol{\theta})) \right]
= \underbrace{\mathrm{Tr}\left[ \boldsymbol{\rho} \log \boldsymbol{\rho} \right]}_{\textrm{entropy observation}}
- \underbrace{\mathbb{E}\left[ \mathrm{Tr}\left[ \boldsymbol{\rho} \log \boldsymbol{\sigma}(\boldsymbol{\theta}) \right] \right]}_{\textrm{avg.\ model log-likelihood}}
\end{equation}

</div>

This general form is typical of a number of energy-based models in machine learning {% cite mehta2018 %}.
The role of the probability distribution of the model is specified here by the density matrix derived from the Laplacian of the network generative model $\boldsymbol{\sigma}_{\boldsymbol{\theta}}(\mathbf{L})$.
Minimization of relative entropy corresponds to maximization of the log-likelihood, as the first term is not dependent on the model. Hence, as in classical maximum likelihood methods, the parameters of the model are inferred by maximizing the ensemble averaged log-likelihood.
In equilibrium conditions, the density matrix of the generative model is in the form of a Gibbs distribution, hence computing its log-likelihood is simple (here the matrix logarithm is well defined because the argument is strictly positive definite, with strictly positive eigenvalues). With this in mind we obtain a nice expression for the ensemble averaged log-likelihood:

<div markdown="0">

\begin{equation}
\label{eq:gibbs_loglike}
\mathbb{E}\left[ \mathrm{Tr}\left[ \boldsymbol{\rho} \log \boldsymbol{\sigma}(\boldsymbol{\theta}) \right] \right]
= \underset{\textrm{average energy term}}{-\beta\, \mathrm{Tr}\left[ \boldsymbol{\rho}\, \mathbb{E}\left[ \mathbf{L}(\boldsymbol{\theta}) \right] \right]}
- \underset{\sim \textrm{free energy term}}{\mathbb{E}\left[ \log Z(\boldsymbol{\theta}) \right]}
\end{equation}

</div>

where in the last term we used the fact that $\rho$ has unit trace.
Another way to look at this is to use the properties of matrix trace, getting an expression.
Hence, going back to the first expression for the relative entropy, and thanks to the linearity of averaging $\mathbb{E}\left[ \cdot \right]$ and trace $\mathrm{Tr}\left[ \cdot \right]$ operators, we can express it as:

<div markdown="0">

\begin{equation}
\label{eq:expected_relative_entropy_contrastive}
\mathbb{E}\left[ S(\boldsymbol{\rho} \| \boldsymbol{\sigma}(\boldsymbol{\theta})) \right]
= \mathrm{Tr}\left[ \boldsymbol{\rho}\log \boldsymbol{\rho} \right]
+ \underbrace{\beta\, \mathrm{Tr}\left[ \boldsymbol{\rho}\, \mathbb{E}\left[ \mathbf{L}(\boldsymbol{\theta}) \right] \right]}_{\textrm{avg.\ energy term}}
+ \underbrace{\mathbb{E}\left[ \log Z(\boldsymbol{\theta}) \right]}_{\textrm{free energy term}}
\end{equation}

</div>

The formulation of the problem in Eq.~$\eqref{eq:expected_relative_entropy_contrastive}$ highlights its *contrastive* nature.
The cost function to maximize is mainly composed of two terms, one corresponds to the energy of the model given the observation, or the *average energy* and a free energy term, obtained by *marginalization* over all possible configurations of the model given its parameters.

The average energy $\mathrm{Tr}\left[ \boldsymbol{\rho}\, \mathbb{E}\left[ \mathbf{L}(\boldsymbol{\theta}) \right] \right]$ is simpler to compute than the ensemble free energy (negative phase).
Indeed, exact calculations of the negative phase can be extremely challenging, the reason being that it is often impossible to accurately evaluate the partition function for the most interesting models.

The *loss*-function in Eq.~$\eqref{eq:expected_relative_entropy_contrastive}$ can also be seen as the sum of two terms, the first being the expectation over the data done through the trace operator of the model ensemble average, and the second term being the ensemble average of the log-partition function.

In the statistical physics jargon, the second term is also called the *quenched average*, an average of the log partition function over all the realization of the Hamiltonian represented by $\mathbf{L}(\boldsymbol{\theta})$ {% cite crisanti1992 %}.
The exact calculation of the quenched log-partition boils down to computing an average over the ensemble of all graphs constrained on the specific set of parameters:

<div markdown="0">

\begin{equation}
\label{eq:quenched_logZ}
\mathbb{E}\left[ \log Z(\boldsymbol{\theta}) \right]
= \sum_{g \in \mathcal{G}(\boldsymbol{\theta})} \Pr(g)\, \log \mathrm{Tr}\left[ e^{-\beta \mathbf{L}(g)} \right]
\end{equation}

</div>

where every graph $g$ is sampled from the set of graphs $\mathcal{G}$ with parameters $\boldsymbol{\theta}$ and within that ensemble has probability $\Pr(g)$.
The ensemble $\mathcal{G}(\boldsymbol{\theta})$ can be expressed as:

<div markdown="0">

\begin{equation}
\mathcal{G}(\boldsymbol{\theta}) = \left\lbrace A_{ij} \in \lbrace 0,1\rbrace \mid \langle \boldsymbol{\theta} \rangle = \boldsymbol{\theta}^\star \right\rbrace
\end{equation}

</div>

i.e.\ the set of all possible networks with adjacency matrix $A_{ij}$ such that the constraints represented by the empirical quantities $\theta^\star$ are on average equal to their required value $\langle \boldsymbol{\theta} \rangle$.
It corresponds to averaging over all matrices from the ensemble of independent identically distributed variables.
For example, if we set some value of $p^\star$ and model with the Erdos-Renyi random graph, we have an Hamiltonian that consists of off diagonal independent random variables sampled from a Bernoulli distribution with average $p^\star$ and diagonal terms modeled as binomial random variables (sum of Bernoulli r.v.) with average $np$.

In the large $n$ limit the ensemble $\mathcal{G}$ is larger and the sampling variance is reduced. Hence the probability space represented by $\Pr(\mathcal{G})$ will be peaked around the average, such that $\langle{\boldsymbol{\theta}}\rangle = \boldsymbol{\theta}^\star$.


## Replica trick, quenched and annealed free energies

Model inference methods rely on the ability to correctly compute both the positive and negative phases of the gradients.
In the previous section we introduced the quenched log partition function, and noted that in most model an exact calculation is infeasible.
However, there are some cases in which some good estimates can be done thanks to methods of random matrix theory.
Indeed, the calculation of average traces of random matrix ensembles is strictly related to the ability to compute integrals over the spectral densities of random matrix ensembles.

Here we attempt a calculation of the quenched log-partition function in the limit $n\to \infty$ using the so-called *replica trick*.
This method is based on the following identity:

<div markdown="0">

\begin{equation}
\log Z = \lim_{k\to 0}\frac{Z^k-1}{k}.
\end{equation}

</div>

where $k$ is a real number.
The idea here is that while averaging the logarithm of $Z$ is usually a difficult task, taking the average of $Z^k$ might be feasible for any integer value of $k$.
Performing a (risky) analytic continuation to $k=0$, one might compute the averaged free energy over the quenched disorder as

<div markdown="0">

\begin{align}
\mathbb{E}\left[ \log Z(\boldsymbol{\theta}) \right]
&= \lim_{k\to 0} k^{-1} \left(\mathbb{E}\left[ Z^k \right] - 1\right)
= \lim_{k\to 0} k^{-1} \log \mathbb{E}\left[ Z^k \right]
\end{align}

</div>

With this consideration, one is able to find an upper-bound to the quenched free energy $F^q = -\beta^{-1}\, \mathbb{E}\left[ \log Z \right]$ by the much easier *annealed* free energy $F^a = -\beta^{-1} \log \mathbb{E}\left[ Z \right]$.
It must be noted that the annealed free energy is not the correct quantity to be used for the correct calculations. However it is a good lower bound of the quenched free energy, $F^a \leq F^q$ or in our case:

<div markdown="0">

\begin{equation}
\mathbb{E}\left[ \log Z \right] \geq \log \mathbb{E}\left[ Z \right].
\end{equation}

</div>

Hence, we transformed the difficult problem of computing the average log-partition function into the calculation of the logarithm of the average partition function.
This corresponds to computing averages over the disorder implicit to the random nature of the network itself.

## Annealed computations

The reason why we use the annealed version of the calculation is because it is easier.
For the annealed log-partition function we need to compute:

<div markdown="0">

\begin{equation}
\label{eq:annealed_log_partition}
\log \mathbb{E}\left[ \sum_{i=1}^n e^{-\beta \lambda_{i}} \right]
= \log \sum_{g \in \mathcal{G}(\boldsymbol{\theta})} \Pr(g)\, \mathrm{Tr}\left[ e^{-\beta \mathbf{L}(g)} \right]
\end{equation}

</div>

where $\mathbf{L}(g)$ denotes the Laplacian of graph $g$ sampled from the ensemble $\mathcal{G}(\boldsymbol{\theta})$.
We introduce the average spectral density of the random matrix ensemble of the Laplacian of the model and denote it with $\varrho$ (details in the appendix below).
For this reason we can write the expected partition function $\mathbb{E}\left[ \mathrm{Tr}\left[ e^{-\beta \mathbf{L}} \right] \right]$ as an integral over the spectral density $\varrho$ on the positive real axis, because all eigenvalues of the Laplacian are nonnegative:

<div markdown="0">

\begin{equation}
\label{eq:trace_spectral}
\mathbb{E}\left[ \mathrm{Tr}\left[ e^{-\beta \mathbf{L}} \right] \right]
= n \int_{0}^{+\infty} e^{-\beta \lambda}\, \varrho(\lambda)\, d\lambda
\end{equation}

</div>

where $\varrho$ is the average spectral density. We need to compute the derivatives with respect to the model parameters of this quantity, so we get

<div markdown="0">

\begin{equation}
\frac{\partial}{\partial \boldsymbol{\theta}}\,
\mathbb{E}\left[ \mathrm{Tr}\left[ e^{-\beta \mathbf{L}} \right] \right]
= n \frac{\partial}{\partial \boldsymbol{\theta}} \int_{0}^{+\infty} e^{-\beta \lambda}\, \varrho(\lambda)\, d\lambda .
\end{equation}

</div>

Treating $\varrho(\lambda;\boldsymbol{\theta})$ as depending smoothly on the ensemble parameters, a straightforward application of the chain rule gives:

<div markdown="0">

\begin{equation}
\frac{\partial}{\partial \boldsymbol{\theta}} \int_{0}^{+\infty} e^{-\beta \lambda}\, \varrho(\lambda)\, d\lambda
= \int_{0}^{+\infty} e^{-\beta \lambda}\, \frac{\partial \varrho(\lambda;\boldsymbol{\theta})}{\partial \boldsymbol{\theta}}\, d\lambda
\end{equation}

</div>

which should be compared with more elaborate spectral-shift formulas when individual eigenvalues move with $\boldsymbol{\theta}$.

## Model optimization as variational inference

To perform model inference on the data, we need to rely on the calculation of the gradients of the ensemble average relative entropy with respect to the model parameters.
Being the entropy of the observed network independent on the model parameters, the gradients of Eq.~$\eqref{eq:expected_rel_entropy}$ can be written as the sum of two terms:

<div markdown="0">

\begin{equation}
\label{eq:gradient_relent}
\nabla_{\boldsymbol{\theta}}\, \mathbb{E}\left[ S(\boldsymbol{\rho} \| \boldsymbol{\sigma}(\boldsymbol{\theta})) \right] = \beta\, \mathrm{Tr}\left[ \boldsymbol{\rho}\, \nabla_{\boldsymbol{\theta}}\, \mathbb{E}\left[ \mathbf{L}(\boldsymbol{\theta}) \right] \right] + \nabla_{\boldsymbol{\theta}}\, \mathbb{E}\left[ \log Z(\boldsymbol{\theta}) \right]
\end{equation}

</div>

Similarly to the case of learning undirected graphical models in machine learning, the expression for the gradients of the expected relative entropy with respect to model parameters can be considered as a difference of moments---one calculated directly from the observation and one calculated from our model using the current model parameters {% cite hinton1984 %}.
The observation dependent (the positive phase) and the model-dependent term (the negative phase) of the gradient have an intuitive explanation for likelihood-based training procedures.
The gradient acts on the model to lower the energy of configurations that are near observed network (positive phase, or average energy) while raising the energy of configurations that are far from observed data points (negative phase, free energy term represented by the quenched log-partition).

In the case where the quenched log-partition cannot be computed exactly one needs to rely on numerical procedures for the estimation of the gradients.
One way to do this is to draw samples from the graph ensemble $\mathcal{G}(\boldsymbol{\theta})$ specified by the generative model:

<div markdown="0">

\begin{equation}
\mathbb{E}\left[ \log Z(\boldsymbol{\theta}) \right]
= \sum_{g \in \mathcal{G}(\boldsymbol{\theta})} \Pr(g)\, \log Z_g(\boldsymbol{\theta})
\end{equation}

</div>

The exact computation of the gradient requires to enumerate over all possible configurations of graphs constrained on the variables $\boldsymbol{\theta}$, which can be extremely large.
However it turns out that one can devise an optimization procedure based on incomplete sampling of the ensemble.
Following the very same ideas of *energy-based models* from machine learning, each step of the optimization process involves a parameter update of the form:

<div markdown="0">

\begin{align}
\boldsymbol{\theta}^{(i+1)} = \boldsymbol{\theta}^{(i)} - \eta\, &\beta\, \mathrm{Tr}\left[ \boldsymbol{\rho}\, \nabla_{\boldsymbol{\theta}}\, \mathbb{E}\left[ \mathbf{L}(\boldsymbol{\theta}) \right] \right] \\
&+ \eta \sum_{g^{\prime} \in \mathcal{G}^{\prime} \subset \mathcal{G}(\boldsymbol{\theta})} \nabla_{\boldsymbol{\theta}} \Pr(g^{\prime})\, \log Z^{\prime}(\boldsymbol{\theta})
\end{align}

</div>

where $\eta$ is the so-called *learning rate* in machine learning, $\Pr(g^{\prime})$ is the probability of the graph $g^{\prime}$ in the subset $\mathcal{G}^{\prime}(\boldsymbol{\theta})$ of graphs sampled from $\mathcal{G}(\boldsymbol{\theta})$ and $Z^{\prime}(\boldsymbol{\theta})=\mathrm{Tr}\left[ \exp({-\beta \mathbf{L}^{\prime}}) \right]$ is the corresponding partition function, where $\mathbf{L}^{\prime}$ denotes the Laplacian of the graph $g^{\prime}$.

## Practical model optimization

Luckily this kind of computations can be tackled by means of *automatic differentiation*, a technique based on the chain-rule of calculus that is of huge help in the computation of complicate derivatives of arbitrarily complicated compositions of differentiable functions.
The most recent software packages for large-scale machine learning implement automatic differentiation transparently to the user, only requiring one to define the *computational graph*, i.e.\ the abstract graph representing the dependence between variables in the calculation of the target function to optimize. For our interest, luckily the Google's *Tensorflow* package {% cite tensorflow2015 %} supports automatic differentiation in the Hermitian eigenvalues routine.

## Perturbation expansion for the partition function

We want to study with a first order perturbation method the effects of a perturbation of the Hamiltonian $\mathbf{L}(\boldsymbol{\theta})$ on the partition function.
Given the discreteness of graph theory, the smallest change we can do to a graph is adding or removing a link.
To do this we can apply a first-order expansion in the sense of {% cite jaynes2003 %} (chapter~30), to the expected partition function:

<div markdown="0">

\begin{align}
\delta\, \mathbb{E}\left[ Z \right]
&= \lim_{\epsilon \to 0} \mathbb{E}\left[ \mathrm{Tr}\left[ e^{-\beta \mathbf{L} + \epsilon \mathbf{L}^{\prime}} \right] \right] \\
&= \lim_{\epsilon \to 0} \mathbb{E}\left[ \mathrm{Tr}\left[ e^{-\beta \mathbf{L}}\left( \mathbf{I} + \epsilon \int_0^1 e^{s \beta \mathbf{L}}\mathbf{L}^{\prime} e^{-s \beta \mathbf{L}}\, ds \right) \right] \right] + O(\epsilon^2)
\end{align}

</div>

## Appendix: calculation of ensemble average spectral density

The spectral density $\varrho$ of a Laplacian matrix $\mathbf{L}$ can be defined via the delta function as {% cite nadakuditi2012 nadakuditi2013 %}:

<div markdown="0">

\begin{equation}
\varrho(z) = \frac{1}{n}\sum_{i=1}^n \delta(z-\lambda_{i})
\end{equation}

</div>

where $\lambda_{i}$ are the eigenvalues of the matrix.
Thanks to the so-called Plemelj--Sokhotski formula, it is possible to write the delta function as the limit in the complex plane approaching the real line of the imaginary part of the following quantity:

<div markdown="0">

\begin{equation}
\delta(x) = -\frac{1}{\pi} \lim_{\eta \to 0^+} \operatorname{Im}\frac{1}{x + \mathrm{i}\,\eta},
\end{equation}

</div>

hence for the spectral density we recover the following expression:

<div markdown="0">

\begin{equation}
\varrho(x) = -\frac{1}{n \pi} \lim_{\eta \to 0^+} \operatorname{Im}\sum_{i=1}^n \frac{1}{x + \mathrm{i}\,\eta - \lambda_{i}}.
\end{equation}

</div>

Now we identify the complex variable $z=x+\mathrm{i}\,\eta$ and thanks to a change of basis and the properties of matrix functions, we evaluate the sum in the argument of the imaginary part as:

<div markdown="0">

\begin{equation}
\sum_{i=1}^n \frac{1}{x + \mathrm{i}\,\eta - \lambda_{i}} = \mathrm{Tr}\left[ (z \mathbf{I} - \mathbf{L})^{-1} \right].
\end{equation}

</div>

The function $R(z)=(z\mathbf{I} -\mathbf{L})^{-1}$ is called the *resolvent matrix* of $\mathbf{L}$.
By averaging over the resolvent we can get an expression for the expected spectral density over the ensemble of random matrices denoted by $\mathbf{L}(\boldsymbol{\theta})$:

<div markdown="0">

\begin{equation}
\mathbb{E}\left[ \varrho(z) \right] = -\frac{1}{n \pi} \lim_{\eta \to 0^+} \operatorname{Im}\,\mathrm{Tr}\,\mathbb{E}\left[ (z \mathbf{I} - \mathbf{L} )^{-1} \right]
\end{equation}

</div>

where the expectation is taken over the ensemble of networks $\mathbf{L}$ with parameters $\boldsymbol{\theta}$. The quantity $\mathrm{Tr}\left[ (z \mathbf{I} - \mathbf{L} )^{-1} \right]/n$ is called the Stieltjes transform.
The resolvent is the generating function of the moments $\mu_{k}=\mathbb{E}\left[ \mathrm{Tr}\left[ \mathbf{L}^{k} \right] \right]$ of the spectral density:

<div markdown="0">

\begin{align}
\mathbb{E}\left[ (z \mathbf{I} - \mathbf{L} )^{-1} \right]
&= \int \frac{\varrho(x')}{z-x'}\, dx'
= \frac{1}{z} \sum_{k=0}^{\infty} \int \varrho(x') \left( \frac{x'}{z} \right)^k dx' \\
&= \sum_{k=0}^{\infty} \frac{\mu_k}{z^{k+1}}
\end{align}

</div>

where, by normalization of the density $\mu_{0}=1$. In general we can compute the average traces of a random matrix $\mathbf{X}$ by means of integrals over their spectral density:

<div markdown="0">

\begin{equation}
\mathbb{E}\left[ \mathrm{Tr}\left[ \mathbf{X}^k \right] \right]
= n \int \lambda^k\, \varrho(\lambda \mid \mathbf{X})\, d\lambda .
\end{equation}

</div>

In the rest of this document, to simplify notation we identify the average spectral density $\mathbb{E}\left[ \varrho \right]$ simply as $\varrho$.
This also apply in the case of matrix functions, thanks to the series expansion. Keep this in mind for the purpose of our investigation:

<div markdown="0">

\begin{equation}
\label{eq:trace_integral}
\mathbb{E}\left[ \mathrm{Tr}\left[ e^{-\beta \mathbf{L}} \right] \right]
= n \int_{0}^{\infty} e^{-\beta \lambda}\, \varrho(\lambda)\, d\lambda
\end{equation}

</div>

Coming back to the issue of computing the quenched average of the log partition function, then we have identified some powerful tools for its quantification. If we approximate the quenched average $\mathbb{E}\left[ \log Z \right]$ with the annealed average $\log \mathbb{E}\left[ Z \right]$ we then can integrate using Eq.~$\eqref{eq:trace_integral}$ over the spectral density of the random networks. In other words, we could obtain a nice approximation to the quenched average by looking at the average spectral density.

## References

{% bibliography --cited %}
