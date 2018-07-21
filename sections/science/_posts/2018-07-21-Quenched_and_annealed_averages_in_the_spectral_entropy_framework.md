---
layout: post
title: Quenched and annealed averages in the spectral entropy framework
categories: science
published: false
date: 2018-07-21
use_math: true
---

Introduction
===========

We are in the same settings of the previous paper. Graphs with $n$ nodes and $m$ edges.
We want to model some observed network with Laplacian $\mathbf{L}^\star$ and density matrix $\boldsymbol \rho$ using a model where entries are considered random variables parametrized by parameters $\boldsymbol \theta \in \mathbb{R}^l$. 
We want to minimize the following quantity:

$$\label{eq:expected_rel_entropy}
\mathbb{E}{S(\boldsymbol \rho \| \boldsymbol \sigma(\boldsymbol \theta)) } = \underbrace{\mathbb{E}{\textrm{Tr}{\boldsymbol \rho \log  \boldsymbol \rho}}}_{\textrm{data}} - \underbrace{\mathbb{E}{\boldsymbol \rho \log \boldsymbol \sigma(\boldsymbol \theta)}}_{\textrm{avg. model log-likelihood}}
$$

where the expectation $\mathbb{E}{\cdot}$ is to be made over the set of all networks produced by a generative model at parameters $\boldsymbol \theta$.

As in the Maximum Likelihood formalism, in our framework we can identify the relative entropy as composed of a term depending on the observation alone and a term depending on the log-likelihood of the model given the data.
Hence, \Cref{eq:expected_rel_entropy} can be decomposed in the contribution of a term not depending on the model parameters $\boldsymbol \theta$ plus a term depending on them:

$$
\mathbb{E}{S(\boldsymbol \rho \| \boldsymbol \sigma(\boldsymbol \theta)) } = \underbrace{\textrm{Tr}{\boldsymbol \rho \log  \boldsymbol \rho}}_{\textrm{entropy observation}} - \underbrace{\mathbb{E}{\boldsymbol \rho \log \boldsymbol \sigma(\boldsymbol \theta)}}_{\textrm{avg. model log-likelihood}}
$$

This general form is typical of a number of energy based-models in machine learning~\cite{mehta2018}.
The role of the probability distribution of the model is specified here by the density matrix derived from the Laplacian of the network generative model $\boldsymbol \sigma_{\boldsymbol \theta}(\mathbf{L})$.

Minimization of relative entropy corresponds to maximization of the log-likelihood, as the first term is not dependent on the model. Hence, as in classical maximum likelihood methods, the parameters of the model are inferred by maximizing the ensemble averaged log-likelihood.

In equilibrium conditions, the density matrix of the generative model is in the form of a Gibbs distribution, hence computing its log-likelihood is simple~\footnote{Taking the matrix logarithm of matrices is usually not always possible. However in this case we can as the argument is a strictly positive definite matrix, with all positive nonzero eigenvalues}. With this in mind we obtain a nice expression for the ensemble averaged log-likelihood:

$$\label{eq:loglikelihood}
\mathbb{E}{\textrm{Tr}{\boldsymbol \rho \log \boldsymbol \sigma(\boldsymbol \theta)}} = \underset{\textrm{average energy term}}{-\beta \textrm{Tr}{\boldsymbol \rho \mathbb{E}{\mathbf{L}(\boldsymbol \theta)}}} - \underset{\sim \textrm{free energy term}}{\mathbb{E}{\log Z(\boldsymbol \theta)}} 
$$

where in the last term we used the fact that $\rho$ has unit trace.

Another way to look at this is to use the properties of matrix trace, getting an expression 
Hence, going back to the first expression for the relative entropy, and thanks to the linearity of averaging $\mathbb{E}{\cdot}$ and trace $\textrm{Tr}{\cdot}$ operators, we can express it as:

$$\label{eq:expected_relative_entropy_contrastive}
\mathbb{E}{ S(\boldsymbol \rho \| \boldsymbol \sigma(\boldsymbol \theta)) } = \textrm{Tr}{\boldsymbol \rho\log \boldsymbol \rho} + \underbrace{\beta \textrm{Tr}{\boldsymbol \rho \mathbb{E}{ \mathbf{L}(\boldsymbol \theta) }}}_{\textrm{avg. energy term}} + \underbrace{\mathbb{E}{\log Z(\boldsymbol \theta)}}_{\textrm{free energy term}} 
$$

The formulation of the problem in~\Cref{eq:expected_relative_entropy_contrastive} highlights its {contrastative} nature.
The cost function to maximize is mainly composed of two terms, one corresponds to the energy of the model given the observation, or the {average energy} and a free energy term, obtained by {marginalization} over all possible configurations of the model given its parameters.
%In the machine learning literature these two quantities are identified as {positive} and {negative} phases, respectively.

The average energy $\textrm{Tr}{\boldsymbol \rho \mathbb{E}{\mathbf{L}(\boldsymbol \theta)}}$ is simpler to compute than the ensemble free energy (negative phase).ù
Indeed, exact calculations of the negative phase can be extremely challenging, the reason being that one it is impossible to accurately evaluate the partition function for most interesting models in complex network theory.
The {loss}-function in~\Cref{eq:expected_relative_entropy_contrastive} can also be seen as the sum of two terms, the first being the expectation over the data done through the trace operator of the model ensemble average, and the second term being the ensemble average of the log-partition function.  

In the statistical physics jargon, the second term is also called the {quenched average}, an average of the log partition function over all the realization of the Hamiltonian represented by $\mathbf{L}(\boldsymbol \theta)$~\cite{crisanti1992}.

The exact calculation of the quenched log-partition boils down to computing an average over the ensemble of all graphs constrained on the specific set of parameters:

$$\label{eq:annealed_partition}
\mathbb{E}{\log Z(\boldsymbol \theta)} = \sum \limits_{ g \in \mathcal{G}(\boldsymbol \theta) } \Pr(g)\log \textrm{Tr}{e^{-\beta \mathbf{L}(g)}} %= \sum \limits_{ g \in \mathcal{G}(\boldsymbol \theta) } \Pr(g) \sum \limits_{i=1}^n e^{-\beta \lambda_i(\mathbf{L}^{g})}
$$

where every graph $g$ is sampled from the set of graphs $\mathcal{G}$ with parameters $\boldsymbol \theta$ and within that ensemble has probability $\Pr(g)$.

The ensemble $\mathcal{G}(\boldsymbol \theta)$ where we are summing over can also be expressed as:
$$
\mathcal{G}(\boldsymbol \theta) = \{ A_{ij}=\{0,1\} | \langle \boldsymbol \theta \rangle = \boldsymbol \theta^\star \}
$$

i.e. the set of all possible links $A_{ij}$ such that the constraints represented by the empirical quantities $\theta^\star$ are on average equal to their required value $\langle \boldsymbol \theta \rangle$.
It corresponds to averaging over all matrices from the ensemble of independent identically distributed variables.
For example, if we set some value of $p^\star$ and model with the Erdos-Renyi random graph, we have an Hamiltonian that consists of off diagonal independent terms coupled with a constant term $p^\star$ and diagonal terms modeled as binomial random variables with average $np$.

Moreover, in the large $n$ limit the ensemble $\mathcal{G}$ is larger and the sampling variance is reduced. Hence the probability space represented by $\Pr(\mathcal{G})$ will be peaked around the average, such that $\langle{\boldsymbol \theta}\rangle = \boldsymbol \theta^\star$.

## Approximating the quenched free energy
Model inference methods rely on the ability to correctly compute both the positive and negative phases of the gradients.
In the previous section we introduced the quenched log partition function, and noted that in most model an exact calculation is infeasible.
However, there are some cases in which some good estimates can be done thanks to methods of random matrix theory.

Indeed, the calculation of average traces of random matrix ensembles is strictly related to the ability to compute integrals over the spectral densities of random matrix ensembles.

Here we attempt a calculation of the quenched log-partition function in the limit $n\to \infty$ using the so-called {replica-trick}.
This method is based on the following identity:

$$
\log Z = \lim \limits_{k\to 0}\frac{Z^k-1}{k}.
$$

where $k$ is taken to be a real number.
The idea here is that while averaging the logarithm of $Z$ is usually a difficult task, taking the average of $Z^k$ might be feasible for any integer value of $k$.
Performing a (risky) analytic continuation to $k=0$, one might compute the averaged free energy over the quenched disorder as

$$
\mathbb{E}{\log Z(\boldsymbol \theta)} = \lim \limits_{k\to 0}k^{-1} \left(\mathbb{E}{Z^k}-1\right ) = \lim \limits_{k\to 0} k^{-1}\log \mathbb{E}{Z^k} = \lim \limits_{k\to 0} \log \mathbb{E}{Z^k}
$$

With this consideration, one is able to find an upper-bound to the quenched free energy $F^q = -\beta^{-1} \mathbb{E}{\log Z}$ by the much easier {annealed} free energy $F^a = -\beta^{-1}\log \mathbb{E}{Z}$.
It must be noted that the annealed free energy is not the correct quantity to be used for the correct calculations. However it is a good lower bound of the quenched free energy, $F^a \leq F^q$ or in our case:
$$
\mathbb{E}{\log Z} \geq \log \mathbb{E}{Z}.
$$

Hence, we transformed the difficult problem of computing the average log-partition function into the calculation of the logarithm of the average partition function.
This corresponds to computing averages over the disorder implicit to the random nature of the network itself.
