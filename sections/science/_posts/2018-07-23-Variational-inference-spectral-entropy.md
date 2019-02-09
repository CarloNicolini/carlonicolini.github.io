---
layout: post
title: Variational inference and model fitting of complex networks 
categories: science
published: false
use_math: true
date: 2018-06-25
---

# Spectral maximum likelihood framework

Graphs with $n$ nodes and $m$ edges.
We want to model some observed network with Laplacian $\mathbf{L}^*$ and density matrix $\boldsymbol \rho$ using a model where entries are considered random variables parametrized by parameters $\boldsymbol \theta \in \mathbb{R}^l$.

We seek to minimize the following quantity over the space of network ensemble parameters:


\begin{equation}
\mathbb{E}\lbrack S(\boldsymbol \rho \| \boldsymbol \sigma(\boldsymbol \theta))\rbrack  = \mathbb{E}{ \mathrm{Tr} \lbrack \boldsymbol \rho \log  \boldsymbol \rho} - \mathbb{E}{\boldsymbol \rho \log \boldsymbol \sigma(\boldsymbol \theta)} \rbrack
\end{equation}

where the expectation $\mathbb{E}\left \lbrack \cdot \right \rbrack$ is to be made over the set of all networks produced by a generative model at parameters $\boldsymbol \theta$.

As in the Maximum Likelihood formalism, in our framework we can identify the relative entropy as composed of a term depending on the observation alone and a term depending on the log-likelihood of the model given the data.
Hence, \Cref{eq:expected_rel_entropy} can be decomposed in the contribution of a term not depending on the model parameters $\boldsymbol \theta$ plus a term depending on them:

\begin{equation}
\mathbb{E}\left \lbrack S(\boldsymbol \rho \| \boldsymbol \sigma(\boldsymbol \theta)) } = \underbrace{\mathrm{Tr}\left \lbrack \boldsymbol \rho \log  \boldsymbol \rho}}_{\textrm{entropy observation}} - \underbrace{\bE{\boldsymbol \rho \log \boldsymbol \sigma(\boldsymbol \theta)}}_{\textrm{avg. model log-likelihood \right \rbrack \right \rbrack
\end{equation}

This general form is typical of a number of energy based-models in machine learning~\cite{mehta2018}.
The role of the probability distribution of the model is specified here by the density matrix derived from the Laplacian of the network generative model $\boldsymbol \sigma_{\boldsymbol \theta}(\mathbf{L})$.
Minimization of relative entropy corresponds to maximization of the log-likelihood, as the first term is not dependent on the model. Hence, as in classical maximum likelihood methods, the parameters of the model are inferred by maximizing the ensemble averaged log-likelihood.
In equilibrium conditions, the density matrix of the generative model is in the form of a Gibbs distribution, hence computing its log-likelihood is simple~\footnote{Taking the matrix logarithm of matrices is usually not always possible. However in this case we can as the argument is a strictly positive definite matrix, with all positive nonzero eigenvalues}. With this in mind we obtain a nice expression for the ensemble averaged log-likelihood:
\begin{equation}
\mathbb{E}\left \lbrack \mathrm{Tr}\left \lbrack \boldsymbol \rho \log \boldsymbol \sigma(\boldsymbol \theta)}} = \underset{\textrm{average energy term}}{-\beta \Tr{\boldsymbol \rho \bE{\mathbf{L}(\boldsymbol \theta)}}} - \underset{\sim \textrm{free energy term}}{\bE{\log Z(\boldsymbol \theta) \right \rbrack \right \rbrack 
\end{equation}
where in the last term we used the fact that $\rho$ has unit trace.
Another way to look at this is to use the properties of matrix trace, getting an expression 
Hence, going back to the first expression for the relative entropy, and thanks to the linearity of averaging $\mathbb{E}\left \lbrack \cdot}$ and trace $\Tr{\cdot \right \rbrack$ operators, we can express it as:
\begin{equation}
\mathbb{E}\left \lbrack  S(\boldsymbol \rho \| \boldsymbol \sigma(\boldsymbol \theta)) } = \mathrm{Tr}\left \lbrack \boldsymbol \rho\log \boldsymbol \rho} + \underbrace{\beta \Tr{\boldsymbol \rho \bE{ \mathbf{L}(\boldsymbol \theta) }}}_{\textrm{avg. energy term}} + \underbrace{\bE{\log Z(\boldsymbol \theta)}}_{\textrm{free energy term \right \rbrack \right \rbrack 
\end{equation}
The formulation of the problem in~\Cref{eq:expected_relative_entropy_contrastive} highlights its \emph{contrastative} nature.
The cost function to maximize is mainly composed of two terms, one corresponds to the energy of the model given the observation, or the \emph{average energy} and a free energy term, obtained by \emph{marginalization} over all possible configurations of the model given its parameters.
%In the machine learning literature these two quantities are identified as \emph{positive} and \emph{negative} phases, respectively.

The average energy $\mathrm{Tr}\left \lbrack \boldsymbol \rho \mathbb{E}\left \lbrack \mathbf{L}(\boldsymbol \theta) \right \rbrack \right \rbrack$ is simpler to compute than the ensemble free energy (negative phase).
Indeed, exact calculations of the negative phase can be extremely challenging, the reason being that it is often impossible to accurately evaluate the partition function for the most interesting models.

The \emph{loss}-function in~\Cref{eq:expected_relative_entropy_contrastive} can also be seen as the sum of two terms, the first being the expectation over the data done through the trace operator of the model ensemble average, and the second term being the ensemble average of the log-partition function.  

In the statistical physics jargon, the second term is also called the \emph{quenched average}, an average of the log partition function over all the realization of the Hamiltonian represented by $\mathbf{L}(\boldsymbol \theta)$~\cite{crisanti1992}.
The exact calculation of the quenched log-partition boils down to computing an average over the ensemble of all graphs constrained on the specific set of parameters:
\begin{equation}
\mathbb{E}\left \lbrack \log Z(\boldsymbol \theta)} = \sum \limits_{ g \in \mathcal{G}(\boldsymbol \theta) } \Pr(g)\log \mathrm{Tr}\left \lbrack e^{-\beta \mathbf{L}(g)}} %= \sum \limits_{ g \in \mathcal{G}(\boldsymbol \theta) } \Pr(g) \sum \limits_{i=1}^n e^{-\beta \lambda_i(\mathbf{L}^{g \right \rbrack) \right \rbrack
\end{equation}
where every graph $g$ is sampled from the set of graphs $\mathcal{G}$ with parameters $\boldsymbol \theta$ and within that ensemble has probability $\Pr(g)$.
The ensemble $\mathcal{G}(\boldsymbol \theta)$ can be expressed as:
\begin{equation}
\mathcal{G}(\boldsymbol \theta) = \{ A_{ij}=\{0,1\} | \langle \boldsymbol \theta \rangle = \boldsymbol \theta^* \}
\end{equation}
i.e. the set of all possible networks with adjacency matrix $A_{ij}$ such that the constraints represented by the empirical quantities $\theta^*$ are on average equal to their required value $\langle \boldsymbol \theta \rangle$.
It corresponds to averaging over all matrices from the ensemble of independent identically distributed variables.
For example, if we set some value of $p^*$ and model with the Erdos-Renyi random graph, we have an Hamiltonian that consists of off diagonal independent random variables sampled from a Bernoulli distribution with average $p^*$ and diagonal terms modeled as binomial random variables (sum of Bernoulli r.v.) with average $np$.

In the large $n$ limit the ensemble $\mathcal{G}$ is larger and the sampling variance is reduced. Hence the probability space represented by $\Pr(\mathcal{G})$ will be peaked around the average, such that $\langle{\boldsymbol \theta}\rangle = \boldsymbol \theta^*$.


## Replica trick, quenched and annealed free energies
Model inference methods rely on the ability to correctly compute both the positive and negative phases of the gradients.
In the previous section we introduced the quenched log partition function, and noted that in most model an exact calculation is infeasible.
However, there are some cases in which some good estimates can be done thanks to methods of random matrix theory.
Indeed, the calculation of average traces of random matrix ensembles is strictly related to the ability to compute integrals over the spectral densities of random matrix ensembles.

Here we attempt a calculation of the quenched log-partition function in the limit $n\to \infty$ using the so-called \emph{replica-trick}.
This method is based on the following identity:
\begin{equation}
\log Z = \lim \limits_{k\to 0}\frac{Z^k-1}{k}.
\end{equation}
where $k$ is a real number.
The idea here is that while averaging the logarithm of $Z$ is usually a difficult task, taking the average of $Z^k$ might be feasible for any integer value of $k$.
Performing a (risky) analytic continuation to $k=0$, one might compute the averaged free energy over the quenched disorder as 
\begin{align}
\mathbb{E}\left \lbrack \log Z(\boldsymbol \theta)} =& \lim \limits_{k\to 0}k^{-1} \left(\bE{Z^k}-1\right ) = \lim \limits_{k\to 0} k^{-1}\log \bE{Z^k} \nonumber \\= &\lim \limits_{k\to 0} \log \bE{Z^k \right \rbrack
\end{align}
With this consideration, one is able to find an upper-bound to the quenched free energy $F^q = -\beta^{-1} \mathbb{E}\left \lbrack \log Z}$ by the much easier \emph{annealed} free energy $F^a = -\beta^{-1}\log \bE{Z \right \rbrack$.
It must be noted that the annealed free energy is not the correct quantity to be used for the correct calculations. However it is a good lower bound of the quenched free energy, $F^a \leq F^q$ or in our case:
\begin{equation}
\mathbb{E}\left \lbrack \log Z} \geq \log \bE{Z \right \rbrack.
\end{equation}
Hence, we transformed the difficult problem of computing the average log-partition function into the calculation of the logarithm of the average partition function.
This corresponds to computing averages over the disorder implicit to the random nature of the network itself.

## Annealed computations
The reason why we use the annealed version of the calculation is because it is easier. 
For the annealed log-partition function we need to compute:
\begin{equation}
\log \mathbb{E}\left \lbrack  \sum_{i=1}^n e^{-\beta \lambda_i} } = \log \sum \limits_{g \in \mathcal{G}(\boldsymbol \theta)}\Pr(g) \mathrm{Tr}\left \lbrack e^{-\beta \mathbf{L} \right \rbrack \right \rbrack
\end{equation}
where $\mathbf{L}(g)$ denotes the Laplacian of graph $g$ sampled from the ensemble $\mathcal{G}(\boldsymbol \theta)$.
We introduce the average spectral density of the random matrix ensemble of the Laplacian of the model and denote it with $\varrho$ (details in the appendix~\ref{app:ensemble_average_spectral_density}).
For this reason we can write the expected partition function $\mathrm{Tr}\left \lbrack e^{-\beta \mathbf{L}} \right \rbrack$ as an integral over the spectral density $\varrho$ in the positive real axis, because all eigenvalues are positive:
\begin{equation}
\mathrm{Tr}\left \lbrack e^{-\beta L}} = n \int \limits_{0}^{+\infty} e^{-\beta \lambda} \varrho(e^{-\beta \lambda \right \rbrack) d\lambda
\end{equation}
where $\varrho$ is the average spectral density. We need to compute the derivatives with respect to the model parameters of this quantity, so we get 
\begin{equation}
\frac{\partial}{\partial \boldsymbol \theta}\mathrm{Tr}\left \lbrack e^{-\beta L}} = n \frac{\partial}{\partial \boldsymbol \theta} \int \limits_{0}^{+\infty} e^{-\beta \lambda} \varrho(e^{-\beta \lambda \right \rbrack) d\lambda
\end{equation}
By the derivative chain rule, we get:
\begin{align}
\frac{\partial}{\partial \boldsymbol \theta} \int \limits_{0}^{+\infty} e^{-\beta \lambda} \varrho(e^{-\beta \lambda}) d\lambda =& \frac{1}{Z(\lambda)} \int \limits_{0}^{+\infty} \frac{\partial}{\partial \boldsymbol \theta}\left[\varrho\left(e^{-\beta \lambda}\right)\right] e^{-\beta \lambda}\nonumber \\& - \beta \int \limits_{0}^{+\infty} \frac{\partial \lambda}{\partial \boldsymbol \theta} e^{-\beta \lambda} \varrho\left(e^{-\beta \lambda}\right)
\end{align}
where $Z(\lambda)=\int \limits_{0}^{+\infty} e^{-\beta \lambda} \varrho(e^{-\beta \lambda})$ is the ensemble averaged partition function $\mathbb{E}\left \lbrack \mathrm{Tr}\left \lbrack e^{-\beta \mathbf{L}} \right \rbrack \right \rbrack$.

#{Model optimization as variational inference}
To perform model inference on the data, we need to rely on the calculation of the gradients of the ensemble average relative entropy with respect to the model parameters.
Being the entropy of the observed network independent on the model parameters, the gradients of Equation 1 can be written as the sum of two terms:
\begin{equation}
\nabla_{\boldsymbol \theta}\mathbb{E}\left \lbrack  S(\boldsymbol \rho \| \boldsymbol \sigma(\boldsymbol \theta)) } = \beta \mathrm{Tr}\left \lbrack \boldsymbol \rho \nabla_{\boldsymbol \theta} \bE{\mathbf{L}(\boldsymbol \theta)}} + \nabla_{\boldsymbol \theta \right \rbrack\bE{\log Z(\boldsymbol \theta) \right \rbrack
\end{equation}
Similarly to the case of learning undirected graphical models in machine learning, the expression for the gradients of the expected relative entropy with respect to model parameters can be considered as a difference of moments - one calculated directly from the observation and one calculated from our model using the current model parameters~\cite{hinton1984}.
The observation dependent (the positive phase) and the model-dependent term (the negative phase) of the gradient have an intuitive explanation for likelihood-based training procedures.
The gradient acts on the model to lower the energy of configurations that are near observed network (positive phase, or average energy) while raising the energy of configurations that are far from observed data points (negative phase, free energy term represented by the quenched log-partition).

In the case where the quenched log-partition cannot be computed exactly one needs to rely on numerical procedures for the estimation of the gradients.
One way to do this is to draw samples from the graph ensemble $\mathcal{G}(\boldsymbol \theta)$ specified by the generative model:
\begin{equation}
\mathbb{E}\left \lbrack \log Z(\boldsymbol \theta)} = \sum \limits_{ g \in \mathcal{G}(\boldsymbol \theta)  \right \rbrack \Pr(g) \log Z_g(\boldsymbol \theta)
\end{equation}
The exact computation of the gradient requires to enumerate over all possible configurations of graphs constrained on the variables $\boldsymbol \theta$, which can be extremely large.
However it turns out that one can devise an optimization procedure based on incomplete sampling of the ensemble.
Following the very same ideas of \emph{energy-based models} from machine learning, each step of the optimization process involves a parameter update of the form:
\begin{align}
\boldsymbol \theta^{(i+1)} = \boldsymbol \theta^{(i)} - \eta  &\beta \mathrm{Tr}\left \lbrack \boldsymbol \rho \nabla_{\boldsymbol \theta} \mathbb{E}\left \lbrack \mathbf{L}(\boldsymbol \theta) \right \rbrack \right \rbrack +
\\&  \eta \sum_{g' \in \mathcal{G'} \subset \mathcal{G}(\boldsymbol \theta)} \nabla_{\boldsymbol \theta}\Pr(g') \log \left ( Z'(\boldsymbol \theta) \right ) 
\end{align}
where $\eta$ is the so-called \emph{learning-rate} in machine learning, $\Pr(g')$ is the probability of the graph $g'$ in the subset $\mathcal{G}'(\boldsymbol \theta)$ of graphs sampled from $\mathcal{G}(\boldsymbol \theta)$ and $Z'(\boldsymbol \theta)=\mathrm{Tr}\left \lbrack \exp({-\beta \mathbf{L}')}}$ is the corresponding partition function, where $\mathbf{L \right \rbrack'$ denotes the laplacian of the graph $g'$.

##{Practical model optimization}
Luckily this kind of computations can be tackled by means of \emph{automatic differentiation}, a technique based on the chain-rule of calculus that is of huge help in the computation of complicate derivatives of arbitrarily complicated compositions of differentiable functions.
The most recent software packages for large-scale machine learning implement automatic differentiation transparently to the user, only requiring one to define the \emph{computational graph}, i.e. the abstract graph representing the dependence between variables in the calculation of the target function to optimize. For our interest, luckily the Google's \emph{Tensorflow} package~\cite{tensorflow2015} supports automatic differentiation in the hermitian eigenvalues routine.




##{Heims perturbation theory}
%We want to compute how an increase in the probability of connection in the Erdos-Renyi model, affects the quenched free energy.
We want to study with a first order perturbation method the effects of a perturbation of the Hamiltonian $\mathbf{L}(\boldsymbol \theta)$ on the partition function.
Given the discreteness of graph theory, the smallest change we can do to a graph is adding or removing a link.
To do this we can apply the Heims perturbation theory at the first order~(\cite{jaynes2003} chapter 30), to the expected partition function:
\begin{align}
\delta \mathbb{E}\left \lbrack Z} =& \lim \limits_{\epsilon \to 0} \bE{ \mathrm{Tr}\left \lbrack e^{-(\beta \mathbf{L} + \epsilon \mathbf{L}')}}  } \nonumber \\=& \lim \limits_{\epsilon \to 0}\bE{ \Tr{e^{-\beta \mathbf{L}}\left( 1 + \epsilon \int_0^1 e^{\beta \mathbf{L}}\mathbf{L}' e^{-\beta \mathbf{L}} \right)}  \right \rbrack \nonumber \\&+ O((\epsilon \mathbf{L \right \rbrack')^2)
\end{align}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\appendix
#{Calculation of ensemble average spectral density}
The spectral density $\varrho$ of a Laplacian matrix $\mathbf{L}$ can be defined via the delta function as~\cite{nadakuditi2012,nadakuditi2013}:
\begin{equation}
\varrho(z) = \frac{1}{n}\sum_{i=1}^n \delta(z-\lambda_i)
\end{equation}
where $\lambda_i$ are the eigenvalues of the matrix.
Thanks to the so-called Plemelij-Sokhotski formula, it is possible to write the delta function as the limit in the complex plane approaching the real line of the imaginary part of the following quantity:
\begin{equation}
\delta(x) = -\frac{1}{\pi} \lim \limits_{\eta \to 0^+} \Im {\frac{1}{x + \ramuno \eta } },
\end{equation}
hence for the spectral density we recover the following expression:
\begin{equation}
\varrho(x) = -\frac{1}{n \pi} \lim \limits_{\eta \to 0^+} \Im {\sum \limits_{i=1}^n \frac{1}{x + \ramuno \eta - \lambda_i} }.
\end{equation}
Now we identify the complex variable $z=x+\ramuno \eta$ and thanks to a change of basis and the properties of matrix functions, we evaluate the sum in the argument of the imaginary part as:
\begin{equation}
\sum \limits_{i=1}^n \frac{1}{x + \ramuno \eta -\lambda_i } = \mathrm{Tr}\left \lbrack (z \bI - \mathbf{L})^{-1} \right \rbrack.
\end{equation}
The function $R(z)=(z\bI -\mathbf{L})^{-1}$ is called the \emph{resolvent matrix} of $\mathbf{L}$.
By averaging over the resolvent we can get an expression for the expected spectral density over the ensemble of random matrices denoted by $\mathbf{L}(\boldsymbol \theta)$:
\begin{equation}
\mathbb{E}\left \lbrack \varrho(z)} = -\frac{1}{n \pi} \lim \limits_{\eta \to 0^+} \Im{ \mathrm{Tr}\left \lbrack  \bE{ (z I - \mathbf{L} )^{-1} }  \right \rbrack \right \rbrack
\end{equation}
where the expectation is taken over the ensemble of networks $\mathbf{L}$ with parameters $\boldsymbol \theta$. The quantity $\mathrm{Tr}\left \lbrack (z I - \mathbf{L} )^{-1} \right \rbrack/n$  is called the Stieltjes transform.
The resolvent is the generating function of the moments $\mu_k=\mathbb{E}\left \lbrack \mathrm{Tr}\left \lbrack \mathbf{L}^k \right \rbrack \right \rbrack$ of the spectral density:
\begin{align}
\mathbb{E}\left \lbrack  (z I - \mathbf{L} )^{-1} }  =& \int dx' \frac{\varrho(x')}{z-x'}  = \frac{1}{z}\sum_{k=0}^{\infty} dx' \varrho(x') \left( \frac{x'}{z}^k \right) \\&= \sum_{k=0}^{\infty} \frac{\mu_k}{z^{k+1} \right \rbrack
\end{align}
where, by normalization of the density $\mu_0=1$. In general we can compute the average traces of a random matrix $\mathbf{X}$ by means of integrals over their spectral density:
\begin{equation}\mathbb{E}\left \lbrack \mathrm{Tr}\left \lbrack \mathbf{X}^k} \right \rbrack= n \int d\lambda \lambda^k \varrho(\lambda | \mathbf{X \right \rbrack).
\end{equation}
In the rest of this document, to simplify notation we identify the average spectral density $\mathbb{E}\left \lbrack \varrho \right \rbrack$ simply as $\varrho$.
This also apply in the case of matrix functions, thanks to the series expansion. Keep this in mind for the purpose of our investigation:
\begin{equation}
\mathbb{E}\left \lbrack \mathrm{Tr}\left \lbrack e^{-\beta \mathbf{L}}}} = n \int \limits_{-\infty}^{\infty} e^{-\beta \lambda \right \rbrack \varrho(e^{-\beta \lambda \right \rbrack) d\lambda
\end{equation}

Coming back to the issue of computing the quenched average of the log partition function, then we have identified some powerful tools for its quantification. If we approximate the quenched average $\mathbb{E}\left \lbrack \log Z}$ with the annealed average $\log \bE{Z}$ we then can integrate using \Cref{eq:trace_integral} over the spectral density of the random networks. In other words, we could obtain a nice approximation to the quenched average by looking at the average spectral density.