---
layout: post
title: Quantum information theory and complex networks
categories: science
published: false
date: 2016-03-11
---

Recently, some of the concepts and the ideas presented [in this previous post](/sections/science/2016/08/26/Spectral_density_random_graph_models_planted_partition.html) have been discussed in a recent paper of [DeDomenico](#DeDomenico2016)
where the authors took a little different approach in the definition of spectral densities.
It resulted a new approach to *complex networks information theory* that casts a powerful analogy between complex networks and quantum theory, lying down the foundations of something that in the next years will very probably be part of the basic knowledge in network science.

Laplace, Boltzmann, Von Neumann, Shannon. These are big names in physics and still are big names in network science. In developing a information theory of networks, these are names that recurrently appear.
In these notes I'm going to explain why these names matter, introducing some of the ideas that they brought to modern complex network science, probably unconsciouly.

#### Laplace
There's a deep connection in mathematics between a graph and the algebraic properties of special matrices associated with that graph. 
Many agrees that the best description of a network is not its adjacency matrix, but another quantity that is called combinatorial graph laplacian.
We will see that eigenvalues are closely related to almost all major invariants of a graph, linking one extremal property to another. There is no question that eigenvalues play a central role in our fundamental understanding of graphs.

Given any graph $$G=(V,E)$$, with adjacency matrix $$\mathbf{A}$$ and a diagonal matrix $$\mathbf{D}$$ containing the degree of vertices on the diagonal, the (combinatorial) Laplacian of a graph is defined as:

$$
\mathbf{L} = \mathbf{D} - \mathbf{A}
$$


<img src="https://samidavies.files.wordpress.com/2016/09/laplacian-example.png?w=525" style='float:center; width: 75%'>

The graph Laplacian is of extreme importance in spectral graph theory as it is a semi-positive definite matrix that tells us many informations about the graph structure. In some sense it's related to the laplacian operator $$\Delta$$ in differential equations and in general to the theory of quadratic forms in linear algebra.
Graph Laplacian can be used to compute the number of connected components of a graph, the number of spanning trees, the sparsest cut: some of the properties of Laplacian are summarized here:

- $$L$$ is symmetric
- $$L$$ is positive semidefinite, that is $$x L x^T \geq 0$$ for any $$x\in \mathbb{R}^N$$, therefore $$\lambda_i(L) \geq 0$$.
- Rows and columns sum to zero, therefore $$\lambda_0=0$$.
- The number of zero eigenvalues is the number of connected components.
- The smallest non-zero eigenvalue is called *spectral gap*.
- The second smallest eigenvalue of $$L$$ is called *Fiedler eigenvalue*.
- Laplacian encodes random walker
- Laplacian eigenvalues from first to j-th are bounded in $$0 \leq \lambda_i(L) \leq 2 k_{\max}$$, and for the last $$\lambda_n(L) \geq k_{\max}$$.


For simple networks, Laplacian eigenvalues can be computed analytically and are simple in their formulation.

- Path graph with $$n$$ nodes $$P_n$$: $$\lambda_j(L)= 2 - 2\cos\left( \frac{\pi(j-1)}{n}\right)$$
- Cycle graph with $$n$$ nodes, $$C_n$$: $$\lambda_j(L) = 2-2\cos\left( \frac{2\pi j}{n} \right)$$
- Star graph $$S_n$$: $$\{ 0\, 1^{n-2}\, n\}$$ (the first is 0, all other eigenvalues are 1 until the last that is n).
- Complete graph $$K_n$$: $$\{ 0\,n^{n-1}\}$$ (the first is 0, the remaining others are $$n$$).

The eigenvalues of the Laplacian

    ESPANDERE LAPLACIANO

Some of the many properties of the Laplacian are:

    INSERIRE PROPRIETA' LAPLACIANO


Inspired by how entropy is calculated in quantum systems, one can define a connectivity based quantum density matrix to calculate the von Neumann Entropy of a network.

### Von Neumann entropy of a complex network

A density matrix is a matrix formalism introduced by Von Neumann that describes a quantum system in a mixed state, a statistical ensemble of several quantum states. This should be contrasted with a single state vector that describes a quantum system in a pure state.
The density matrix is the quantum-mechanical analogue to a phase-space probability measure (probability distribution of position and momentum) in classical statistical mechanics.

In quantum mechanics, the state of a quantum system is represented by a state vector $$\left\vert \phi \right\rangle$$ and is called a *pure* state.
However it is also possible for a system to be in a statistical ensemble of different state vectors, for example there may be a 50% probability that the state vector is $$\left\vert \phi_1 \right\rangle$$ and 50% chance that state vector is $$\left\vert \phi_2 \right\rangle$$.
This system would be in a mixed state.
The density matrix is especially useful for mixed states, because any state, pure or mixed, can be characterized by a single density matrix.

Quantum mechanics can be formulated in terms of a density matrix $$\boldsymbol \rho$$, a positive defined (in general Hermitian) matrix with unitary trace, used to represent both mixed and pure quantum states.
A system is in a pure state $$\left\vert \phi \right\rangle$$ if and only if the bound $$\textrm{Tr}(\rho^2)$$ is saturated. The spectral decomposition of a density matrix is:

$$
\rho = \sum_{i=1}^N \lambda_i \left| \phi_i \right\rangle \left\langle \phi_i \right|.
$$

In the realm of complex networks we instead define a density matrix $$\boldsymbol \rho$$ that takes the following form:

$$
\boldsymbol \rho = \frac{\exp({-\beta \mathbf{L}})}{Z} \qquad Z= \sum \limits_{i=1}^N \exp({-\beta \lambda_i(\mathbf{L})})
$$

where $$\beta \in \mathbb{R}$$ is a parameter and $$L$$ is the graph Laplacian. The parameter $$\beta$$ can be estimated via the Maximum Entropy method and turns out that the optimal beta for the subsequent relative entropy minimization is the solution of the equation:

$$
\sum \limits_{i=1}^N \exp{ -\beta \lambda_i(\mathbf{L})} \left( \lambda_i(\mathbf{L} - \frac{1}{N})right) = 0
$$

Interestingly $$\beta$$ can represent many physical variables.
For the statistical physicists $$\beta:=1/(k_T T)$$ is the inverse temperature of statistical mechanics and with this interpretation, $$\boldsymbol \rho$$ provides the Gibbs state of the system in equilibrium at finite temperature.

When $$\beta$$ encodes the time, $$\beta:=t$$, then the density matrix $$\boldsymbol \rho$$ represents the evolution matrix of a diffusive process with an Hamiltonian $$\mathbf{H}=\mathbf{L}$$ and its trace is $$N$$ times the average return probability, i.e. the probability that a random walker stars and ends at the same node at time $$t$$.

In the case instead $$\beta=-1$$, one recovers the definition of communicability matrix introduced by [Estrada](#Estrada).

The density matrix $$\boldsymbol \rho$$ turns out to be a good density matrix for describing the quantum state of a complex networks. It's hermitian (positive-semidefinite) and has unitary trace. Therefore, on the density matrix $$\boldsymbol \rho$$, specifically on its eigenvalues, is possible to compute the Von Neumann entropy (in bits) as:

$$
S(\rho) = - \textrm{Tr}(\rho \log_2 \rho) = -\sum \limits_{i=1}^N \lambda_i(\rho) \log_2 \left( \lambda_i(\rho) \right)
$$

With some manipulations is possible to show that this last formulation of Von Neumann entropy is based on the computation of the product between graph Laplacian and density matrix, precisely we obtain:

$$
S(G) = \log_2 Z + \beta \textrm{Tr}\left[ \right]
$$


- <a name ="DeDomenico2016"></a> De Domenico, M., Biamonte J., "Spectral entropies as information theoretic tools for complex network comparison".http://arxiv.org/pdf/1609.01214v1.pdf
- <a name="Estrada2012"></a>Estrada, E., Hatano, N., Benzi, M., 2012. The physics of communicability in complex networks. Phys. Rep. 514, 89–119. doi:10.1016/j.physrep.2012.01.006

### Von Neumann Entropy of random graph models
