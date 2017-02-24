---
layout: post
title: Eigenvalue spectra of modular matrix techniques and calculations
categories: science
published: false
date: 2017-02-12
--- 

<blockquote>
How to compute spectra of Laplacian of a block matrix
</blockquote>

Network with $$N$$ nodes, 2 blocks of size $$n_A$$ non connected by any link.
Remember that 
$$\det( \mathbf{M} - \lambda \mathbf{I})=0$$

is like 
$$ \det( \mathbf{A} - \lambda \mathbf{I}) \det(\mathbf{A} + \lambda \mathbf{I}) = 0$$
where $$\mathbf{A}$$ is the submatrix with $$n_a$$ nodes.


Consider a modular graph with two disconnected fully dense components:

$$\mathbf{A} = \left( \begin{bmatrix} K_n & 0 \\ 0 K_n \end{bmatrix}  \right )$$

with a total number of nodes $$N= n B$$ and $$B$$ is the number of blocks.

The eigenvalues of the Laplacian of this graph are:

$$ \lambda_i(\mathbf{L}) = \{ 0,\ldots,0, \frac{N}{B} \}$$

therefore the eigenvalues of the density matrix

$$\rho = \frac{e^{-\beta \frac{N}{B}}}{Tr(e^{-\beta \frac{N}{B}})}$$

are 

$$\lambda_i(\rho)=\frac{e^{-\beta \lambda_i(L)}}{\sum_i e^{-\beta \lambda_i(L)}}$$

the Von Neumann entropy $$H(\rho)$$ is the Shannon entropy of the eigenvalues of the density operator.

Notes from Wilde, Quantum Information Theory, Cambridge University Press.

- $$H(\rho) \geq 0$$ 
- $$H(\rho)$$ is zero whenever the density operator is a pure state. The minimum value equivalently occurs when the eigenvalues of a density operator are distributed with all the mass on one value and zero on the others, so that the density operator is rank one and corresponds to a pure state. Why should the entropy of a pure quantum state vanish? It seems that there is quantum uncertainty inherent in the state itself and that a measure of quantum uncertainty should capture this fact. This last observation only makes sense if we do not know anything about the state that is prepared. But if we know exactly how it was prepared, we can perform a special quantum measurement to verify that the quantum state was prepared, and we do not learn anything from this measurement because the outcome of it is always certain.
- $$H(\rho)$$ maximum is $$\log(N)$$ where $$N$$ is the size of the system (number of nodes in the graph).
- $$H(\rho)$$ is **concave** in the density operator, in other words entropy can never decrease under a mixing operation.
- $$H(\rho)$$ is **invariant** under unitary operators (rotations, whatever it means for a graph...)

It may seem that Von Neumann entropy is completely equal to the classical Shannon entropy. This is not true though. In fact the Shannon entropy of the joint distribution of two variables is never smaller than the Shannon entropy of the single variables.

(mettere parte sezione 1.2.1)


Interestingly Von Neumann entropy is additive for the tensor product of states:

$$H(\rho \ctimes \sigma) = H(\rho) + H(\sigma)$$

One can verify this property simply by diagonalizing both density operators and resorting to the additivity of the joint Shannon entropies of the eigenvalues.