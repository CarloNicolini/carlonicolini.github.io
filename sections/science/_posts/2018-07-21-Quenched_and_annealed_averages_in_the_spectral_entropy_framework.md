---
layout: post
title: Quenched and annealed averages in the spectral entropy framework
categories: science
published: false
date: 2018-07-21
use_math: true
---


Introduction
============

We are in the same settings of the previous paper. Graphs with $$n$$ nodes
and $$m$$ edges. We want to model some observed network with Laplacian$$
{\mathbf{L}}^\star$$ and density matrix $$ \rho$$ using a model
where entries are considered random variables parametrized by parameters$$
{ \theta}\in \mathbb{R}^l$$. We want to minimize the
following quantity: 

$$
{E\left\lbrack S( \rho\| { \sigma}({ \theta})) \right\rbrack} = \underbrace{{E\left\lbrack {Tr\left\lbrack  \rho\log   \rho\right\rbrack}\right\rbrack}}_{\textrm{data}} - \underbrace{{E\left\lbrack  \rho\log { \sigma}({ \theta})\right\rbrack}}_{\textrm{avg. model log-likelihood}}
$$

where the expectation

$$
{E\left\lbrack \cdot\right\rbrack}
$$

is to be made over the set of all networks produced by a generative model at
parameters $${ \theta}$$. As in the Maximum Likelihood
formalism, in our framework we can identify the relative entropy as
composed of a term depending on the observation alone and a term
depending on the log-likelihood of the model given the data. Hence, can
be decomposed in the contribution of a term not depending on the model
parameters $${ \theta}$$ plus a term depending on them:$$$


{E\left\lbrack S( \rho\| { \sigma}({ \theta})) \right\rbrack} = \underbrace{{Tr\left\lbrack  \rho\log   \rho\right\rbrack}}_{\textrm{entropy observation}} - \underbrace{{E\left\lbrack  \rho\log { \sigma}({ \theta})\right\rbrack}}_{\textrm{avg. model log-likelihood}}
$$

This general form is typical of a number of energy based-models in
machine learning @mehta2018. The role of the probability distribution of
the model is specified here by the density matrix derived from the
Laplacian of the network generative model$$
{ \sigma}_{{ \theta}}({\mathbf{L}})$$.
Minimization of relative entropy corresponds to maximization of the
log-likelihood, as the first term is not dependent on the model. Hence,
as in classical maximum likelihood methods, the parameters of the model
are inferred by maximizing the ensemble averaged log-likelihood. In
equilibrium conditions, the density matrix of the generative model is in
the form of a Gibbs distribution, hence computing its log-likelihood is
simple [^1]. With this in mind we obtain a nice expression for the
ensemble averaged log-likelihood: 
$$

{E\left\lbrack {Tr\left\lbrack  \rho\log { \sigma}({ \theta})\right\rbrack}\right\rbrack} = \underset{\textrm{average energy term}}{-\beta {Tr\left\lbrack  \rho{E\left\lbrack {\mathbf{L}}({ \theta})\right\rbrack}\right\rbrack}} - \underset{\sim \textrm{free energy term}}{{E\left\lbrack \log Z({ \theta})\right\rbrack}}
$$

where in the last term we used the fact that $$\rho$$ has unit trace.
Another way to look at this is to use the properties of matrix trace,
getting an expression Hence, going back to the first expression for the
relative entropy, and thanks to the linearity of averaging$$
{E\left\lbrack \cdot\right\rbrack}$$ and trace$$
{Tr\left\lbrack \cdot\right\rbrack}$$ operators, we can
express it as: 
$$

{E\left\lbrack  S( \rho\| { \sigma}({ \theta})) \right\rbrack} = {Tr\left\lbrack  \rho\log  \rho\right\rbrack} + \underbrace{\beta {Tr\left\lbrack  \rho{E\left\lbrack  {\mathbf{L}}({ \theta}) \right\rbrack}\right\rbrack}}_{\textrm{avg. energy term}} + \underbrace{{E\left\lbrack \log Z({ \theta})\right\rbrack}}_{\textrm{free energy term}}
$$

The formulation of the problem in  highlights its *contrastative*
nature. The cost function to maximize is mainly composed of two terms,
one corresponds to the energy of the model given the observation, or the
*average energy* and a free energy term, obtained by *marginalization*
over all possible configurations of the model given its parameters. The
average energy$$
{Tr\left\lbrack  \rho{E\left\lbrack {\mathbf{L}}({ \theta})\right\rbrack}\right\rbrack}$$
is simpler to compute than the ensemble free energy (negative phase).ù
Indeed, exact calculations of the negative phase can be extremely
challenging, the reason being that one it is impossible to accurately
evaluate the partition function for most interesting models in complex
network theory. The *loss*-function in  can also be seen as the sum of
two terms, the first being the expectation over the data done through
the trace operator of the model ensemble average, and the second term
being the ensemble average of the log-partition function.

In the statistical physics jargon, the second term is also called the
*quenched average*, an average of the log partition function over all
the realization of the Hamiltonian represented by$$
{\mathbf{L}}({ \theta})$$ @crisanti1992. The exact
calculation of the quenched log-partition boils down to computing an
average over the ensemble of all graphs constrained on the specific set
of parameters: 
$$

{E\left\lbrack \log Z({ \theta})\right\rbrack} = \sum \limits_{ g \in \mathcal{G}({ \theta}) } \Pr(g)\log {Tr\left\lbrack e^{-\beta {\mathbf{L}}(g)}\right\rbrack} 
$$

where every graph $$g$$ is sampled from the set of graphs $$\mathcal{G}$$
with parameters $${ \theta}$$ and within that ensemble has
probability $$\Pr(g)$$.

The ensemble $$\mathcal{G}({ \theta})$$ where we are summing
over can also be expressed as:$$$


\mathcal{G}({ \theta}) = \{ A_{ij}=\{0,1\} | \langle { \theta}\rangle = { \theta}^\star \}
$$

i.e. the set of all possible links $$A_{ij}$$ such that the constraints
represented by the empirical quantities $$\theta^\star$$ are on average equal
to their required value $$\langle { \theta}\rangle$$. It
corresponds to averaging over all matrices from the ensemble of
independent identically distributed variables. For example, if we set
some value of $$p^\star$$ and model with the Erdos-Renyi random graph, we have
an Hamiltonian that consists of off diagonal independent terms coupled
with a constant term $$p^\star$$ and diagonal terms modeled as binomial random
variables with average $$np$$.

Moreover, in the large $$n$$ limit the ensemble $$\mathcal{G}$$ is larger
and the sampling variance is reduced. Hence the probability space
represented by $$\Pr(\mathcal{G})$$ will be peaked around the average,
such that$$
\langle{{ \theta}}\rangle = { \theta}^\star$$.

Approximating the quenched free energy
--------------------------------------

Model inference methods rely on the ability to correctly compute both
the positive and negative phases of the gradients. In the previous
section we introduced the quenched log partition function, and noted
that in most model an exact calculation is infeasible. However, there
are some cases in which some good estimates can be done thanks to
methods of random matrix theory. Indeed, the calculation of average
traces of random matrix ensembles is strictly related to the ability to
compute integrals over the spectral densities of random matrix
ensembles.

Here we attempt a calculation of the quenched log-partition function in
the limit $$n\to \infty$$ using the so-called *replica-trick*. This method
is based on the following identity:$$$


\log Z = \lim \limits_{k\to 0}\frac{Z^k-1}{k}.
$$


 where $$k$$ is taken to
be a real number. The idea here is that while averaging the logarithm of$$
Z$$ is usually a difficult task, taking the average of $$Z^k$$ might be
feasible for any integer value of $$k$$. Performing a (risky) analytic
continuation to $$k=0$$, one might compute the averaged free energy over
the quenched disorder as 
$$


\begin{aligned}
{E\left\lbrack \log Z({ \theta})\right\rbrack} =& \lim \limits_{k\to 0}k^{-1} \left({E\left\lbrack Z^k\right\rbrack}-1\right ) = \lim \limits_{k\to 0} k^{-1}\log {E\left\lbrack Z^k\right\rbrack} \nonumber \\= &\lim \limits_{k\to 0} \log {E\left\lbrack Z^k\right\rbrack}\end{aligned}
$$

With this consideration, one is able to find an upper-bound to the
quenched free energy$$
F^q = -\beta^{-1} {E\left\lbrack \log Z\right\rbrack}$$
by the much easier *annealed* free energy$$
F^a = -\beta^{-1}\log {E\left\lbrack Z\right\rbrack}$$.
It must be noted that the annealed free energy is not the correct
quantity to be used for the correct calculations. However it is a good
lower bound of the quenched free energy, $$F^a \leq F^q$$ or in our case:$$$


{E\left\lbrack \log Z\right\rbrack} \geq \log {E\left\lbrack Z\right\rbrack}.
$$

Hence, we transformed the difficult problem of computing the average
log-partition function into the calculation of the logarithm of the
average partition function. This corresponds to computing averages over
the disorder implicit to the random nature of the network itself.

Annealed computations
---------------------

The reason why we use the annealed version of the calculation is because
it is easier. For the annealed log-partition function we need to
compute:$$$


\log {E\left\lbrack  \sum_{i=1}^n e^{-\beta \lambda_i} \right\rbrack} = \log \sum \limits_{g \in \mathcal{G}({ \theta})}\Pr(g) {Tr\left\lbrack e^{-\beta {\mathbf{L}}}\right\rbrack}
$$

where $${\mathbf{L}}(g)$$ denotes the Laplacian of graph $$g$$ sampled from
the ensemble $$\mathcal{G}({ \theta})$$. We introduce the
average spectral density of the random matrix ensemble of the Laplacian
of the model and denote it with $$\varrho$$ (details in the
appendix \[app:ensemble\_average\_spectral\_density\]). For this reason
we can write the expected partition function$$
{Tr\left\lbrack e^{-\beta {\mathbf{L}}}\right\rbrack}$$
as an integral over the spectral density $$\varrho$$ in the positive real
axis, because all eigenvalues are positive:$$$


{Tr\left\lbrack e^{-\beta L}\right\rbrack} = n \int \limits_{0}^{+\infty} e^{-\beta \lambda} \varrho(e^{-\beta \lambda}) d\lambda
$$

where $$\varrho$$ is the average spectral density. We need to compute the
derivatives with respect to the model parameters of this quantity, so we
get$$$


\frac{\partial}{\partial { \theta}}{Tr\left\lbrack e^{-\beta L}\right\rbrack} = n \frac{\partial}{\partial { \theta}} \int \limits_{0}^{+\infty} e^{-\beta \lambda} \varrho(e^{-\beta \lambda}) d\lambda
$$

By the derivative chain rule, we get: 
$$


\begin{aligned}
\frac{\partial}{\partial { \theta}} \int \limits_{0}^{+\infty} e^{-\beta \lambda} \varrho(e^{-\beta \lambda}) d\lambda =& \frac{1}{Z(\lambda)} \int \limits_{0}^{+\infty} \frac{\partial}{\partial { \theta}}\left[\varrho\left(e^{-\beta \lambda}\right)\right] e^{-\beta \lambda}\nonumber \\& - \beta \int \limits_{0}^{+\infty} \frac{\partial \lambda}{\partial { \theta}} e^{-\beta \lambda} \varrho\left(e^{-\beta \lambda}\right)\end{aligned}
$$

where$$
Z(\lambda)=\int \limits_{0}^{+\infty} e^{-\beta \lambda} \varrho(e^{-\beta \lambda})$$
is the ensemble averaged partition function$$
{E\left\lbrack {Tr\left\lbrack e^{-\beta {\mathbf{L}}}\right\rbrack}\right\rbrack}$$.

Model optimization as variational inference
===========================================

To perform model inference on the data, we need to rely on the
calculation of the gradients of the ensemble average relative entropy
with respect to the model parameters. Being the entropy of the observed
network independent on the model parameters, the gradients of  can be
written as the sum of two terms:$$$


\nabla_{{ \theta}}{E\left\lbrack  S( \rho\| { \sigma}({ \theta})) \right\rbrack} = \beta {Tr\left\lbrack  \rho\nabla_{{ \theta}} {E\left\lbrack {\mathbf{L}}({ \theta})\right\rbrack}\right\rbrack} + \nabla_{{ \theta}}{E\left\lbrack \log Z({ \theta})\right\rbrack}
$$

Similarly to the case of learning undirected graphical models in machine
learning, the expression for the gradients of the expected relative
entropy with respect to model parameters can be considered as a
difference of moments - one calculated directly from the observation and
one calculated from our model using the current model
parameters @hinton1984. The observation dependent (the positive phase)
and the model-dependent term (the negative phase) of the gradient have
an intuitive explanation for likelihood-based training procedures. The
gradient acts on the model to lower the energy of configurations that
are near observed network (positive phase, or average energy) while
raising the energy of configurations that are far from observed data
points (negative phase, free energy term represented by the quenched
log-partition).

In the case where the quenched log-partition cannot be computed exactly
one needs to rely on numerical procedures for the estimation of the
gradients. One way to do this is to draw samples from the graph ensemble$$
\mathcal{G}({ \theta})$$ specified by the generative model:$$$


{E\left\lbrack \log Z({ \theta})\right\rbrack} = \sum \limits_{ g \in \mathcal{G}({ \theta}) } \Pr(g) \log Z_g({ \theta})
$$

The exact computation of the gradient requires to enumerate over all
possible configurations of graphs constrained on the variables$$
{ \theta}$$, which can be extremely large. However it turns
out that one can devise an optimization procedure based on incomplete
sampling of the ensemble. Following the very same ideas of *energy-based
models* from machine learning, each step of the optimization process
involves a parameter update of the form: 
$$


\begin{aligned}
{ \theta}^{(i+1)} = { \theta}^{(i)} - \eta  &\beta {Tr\left\lbrack  \rho\nabla_{{ \theta}} {E\left\lbrack {\mathbf{L}}({ \theta})\right\rbrack}\right\rbrack} +
\\&  \eta \sum_{g' \in \mathcal{G'} \subset \mathcal{G}({ \theta})} \nabla_{{ \theta}}\Pr(g') \log \left ( Z'({ \theta}) \right ) \end{aligned}
$$

where $$\eta$$ is the so-called *learning-rate* in machine learning,$$
\Pr(g')$$ is the probability of the graph $$g'$$ in the subset$$
\mathcal{G}'({ \theta})$$ of graphs sampled from$$
\mathcal{G}({ \theta})$$ and$$
Z'({ \theta})={Tr\left\lbrack \exp({-\beta {\mathbf{L}}')}\right\rbrack}$$
is the corresponding partition function, where $${\mathbf{L}}'$$ denotes
the laplacian of the graph $$g'$$.

Practical model optimization
----------------------------

Luckily this kind of computations can be tackled by means of *automatic
differentiation*, a technique based on the chain-rule of calculus that
is of huge help in the computation of complicate derivatives of
arbitrarily complicated compositions of differentiable functions. The
most recent software packages for large-scale machine learning implement
automatic differentiation transparently to the user, only requiring one
to define the *computational graph*, i.e. the abstract graph
representing the dependence between variables in the calculation of the
target function to optimize. For our interest, luckily the Google’s
*Tensorflow* package @tensorflow2015 supports automatic differentiation
in the hermitian eigenvalues routine.

Heims perturbation theory
-------------------------

We want to study with a first order perturbation method the effects of a
perturbation of the Hamiltonian $${\mathbf{L}}({ \theta})$$ on
the partition function. Given the discreteness of graph theory, the
smallest change we can do to a graph is adding or removing a link. To do
this we can apply the Heims perturbation theory at the first
order (@jaynes2003 chapter 30), to the expected partition function:$$$


\begin{aligned}
\delta {E\left\lbrack Z\right\rbrack} =& \lim \limits_{\epsilon \to 0} {E\left\lbrack  {Tr\left\lbrack e^{-(\beta {\mathbf{L}}+ \epsilon {\mathbf{L}}')}\right\rbrack}  \right\rbrack} \nonumber \\=& \lim \limits_{\epsilon \to 0}{E\left\lbrack  {Tr\left\lbrack e^{-\beta {\mathbf{L}}}\left( 1 + \epsilon \int_0^1 e^{\beta {\mathbf{L}}}{\mathbf{L}}' e^{-\beta {\mathbf{L}}} \right)\right\rbrack} \right\rbrack} \nonumber \\&+ O((\epsilon {\mathbf{L}}')^2)\end{aligned}
$$


Calculation of ensemble average spectral density {#app:ensemble_average_spectral_density}
================================================

The spectral density $$\varrho$$ of a Laplacian matrix $${\mathbf{L}}$$ can
be defined via the delta function as @nadakuditi2012 [@nadakuditi2013]:$$$


\varrho(z) = \frac{1}{n}\sum_{i=1}^n \delta(z-\lambda_i)
$$


 where$$
\lambda_i$$ are the eigenvalues of the matrix. Thanks to the so-called
Plemelij-Sokhotski formula, it is possible to write the delta function
as the limit in the complex plane approaching the real line of the
imaginary part of the following quantity:$$$


\delta(x) = -\frac{1}{\pi} \lim \limits_{\eta \to 0^+} {\operatorname{Im}\left( \frac{1}{x + {i}\eta } \right)},
$$

hence for the spectral density we recover the following expression:$$$


\varrho(x) = -\frac{1}{n \pi} \lim \limits_{\eta \to 0^+} {\operatorname{Im}\left( \sum \limits_{i=1}^n \frac{1}{x + {i}\eta - \lambda_i} \right)}.
$$

Now we identify the complex variable $$z=x+{i}\eta$$ and thanks to a
change of basis and the properties of matrix functions, we evaluate the
sum in the argument of the imaginary part as:$$$


\sum \limits_{i=1}^n \frac{1}{x + {i}\eta -\lambda_i } = {Tr\left\lbrack (z {\mathbf{I}}- {\mathbf{L}})^{-1}\right\rbrack}.
$$

The function $$R(z)=(z{\mathbf{I}}-{\mathbf{L}})^{-1}$$ is called the
*resolvent matrix* of $${\mathbf{L}}$$. By averaging over the resolvent we
can get an expression for the expected spectral density over the
ensemble of random matrices denoted by$$
{\mathbf{L}}({ \theta})$$:$$$


{E\left\lbrack \varrho(z)\right\rbrack} = -\frac{1}{n \pi} \lim \limits_{\eta \to 0^+} {\operatorname{Im}\left(  {Tr\left\lbrack  {E\left\lbrack  (z I - {\mathbf{L}})^{-1} \right\rbrack} \right\rbrack}\right)}
$$

where the expectation is taken over the ensemble of networks$$
{\mathbf{L}}$$ with parameters $${ \theta}$$. The quantity$$
{Tr\left\lbrack (z I - {\mathbf{L}})^{-1}\right\rbrack}/n$$
is called the Stieltjes transform. The resolvent is the generating
function of the moments$$
\mu_k={E\left\lbrack {Tr\left\lbrack {\mathbf{L}}^k\right\rbrack}\right\rbrack}$$
of the spectral density: 
$$


\begin{aligned}
{E\left\lbrack  (z I - {\mathbf{L}})^{-1} \right\rbrack}  =& \int dx' \frac{\varrho(x')}{z-x'}  = \frac{1}{z}\sum_{k=0}^{\infty} dx' \varrho(x') \left( \frac{x'}{z}^k \right) \\&= \sum_{k=0}^{\infty} \frac{\mu_k}{z^{k+1}}\end{aligned}
$$

where, by normalization of the density $$\mu_0=1$$. In general we can
compute the average traces of a random matrix $$\mathbf{X}$$ by means of
integrals over their spectral density:$$$


{E\left\lbrack {Tr\left\lbrack \mathbf{X}^k\right\rbrack}\right\rbrack}= n \int d\lambda \lambda^k \varrho(\lambda | \mathbf{X}).
$$

In the rest of this document, to simplify notation we identify the
average spectral density$$
{E\left\lbrack \varrho\right\rbrack}$$ simply as$$
\varrho$$. This also apply in the case of matrix functions, thanks to
the series expansion. Keep this in mind for the purpose of our
investigation: 
$$

{E\left\lbrack {Tr\left\lbrack e^{-\beta {\mathbf{L}}}\right\rbrack}\right\rbrack} = n \int \limits_{-\infty}^{\infty} e^{-\beta \lambda} \varrho(e^{-\beta \lambda}) d\lambda
$$


Coming back to the issue of computing the quenched average of the log
partition function, then we have identified some powerful tools for its
quantification. If we approximate the quenched average$$
{E\left\lbrack \log Z\right\rbrack}$$ with the
annealed average$$
\log {E\left\lbrack Z\right\rbrack}$$ we then
can integrate using over the spectral density of the random networks. In
other words, we could obtain a nice approximation to the quenched
average by looking at the average spectral density.

[^1]: Taking the matrix logarithm of matrices is usually not always
    possible. However in this case we can as the argument is a strictly
    positive definite matrix, with all positive nonzero eigenvalues
