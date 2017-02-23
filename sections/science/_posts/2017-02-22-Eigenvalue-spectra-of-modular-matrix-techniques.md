---
layout: post
title: Community detection in the modular structure of brain functional connectivity networks
categories: science
<!-- published: false -->
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

