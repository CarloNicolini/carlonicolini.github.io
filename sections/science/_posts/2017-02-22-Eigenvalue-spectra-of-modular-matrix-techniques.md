---
layout: post
title: Eigenvalue spectra of modular matrix techniques and calculations
categories: science
published: false
date: 2017-02-12
--- 

# RANDOM NOTES ABOUT RANDOM GRAPHS AND EIGENVALUES, NOT TO BE TAKEN SERIOUSLY

# 1
Network with $$N$$ nodes, 2 blocks of size $$n_A$$ non connected by any link.
Remember that 
$$\det( \mathbf{M} - \lambda \mathbf{I})=0$$

is like 
$$ \det( \mathbf{A} - \lambda \mathbf{I}) \det(\mathbf{A} + \lambda \mathbf{I}) = 0$$
where $$\mathbf{A}$$ is the submatrix with $$n_a$$ nodes.


# 2
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

### Notes about Von Neumann entropy

Notes from Wilde, Quantum Information Theory, Cambridge University Press.

- $$H(\rho) \geq 0$$ 
- $$H(\rho)$$ is zero whenever the density operator is a pure state. The minimum value equivalently occurs when the eigenvalues of a density operator are distributed with all the mass on one value and zero on the others, so that the density operator is rank one and corresponds to a pure state. Why should the entropy of a pure quantum state vanish? It seems that there is quantum uncertainty inherent in the state itself and that a measure of quantum uncertainty should capture this fact. This last observation only makes sense if we do not know anything about the state that is prepared. But if we know exactly how it was prepared, we can perform a special quantum measurement to verify that the quantum state was prepared, and we do not learn anything from this measurement because the outcome of it is always certain.
- $$H(\rho)$$ maximum is $$\log(N)$$ where $$N$$ is the size of the system (number of nodes in the graph).
- $$H(\rho)$$ is **concave** in the density operator, in other words entropy can never decrease under a mixing operation.
- $$H(\rho)$$ is **invariant** under unitary operators (rotations, whatever it means for a graph...)

It may seem that Von Neumann entropy is completely equal to the classical Shannon entropy. This is not true though. In fact the Shannon entropy of the joint distribution of two variables is never smaller than the Shannon entropy of the single variables.

(mettere parte sezione 1.2.1)

Interestingly Von Neumann entropy is additive for the tensor product of states:

$$H(\rho \otimes \sigma) = H(\rho) + H(\sigma)$$

One can verify this property simply by diagonalizing both density operators and resorting to the additivity of the joint Shannon entropies of the eigenvalues.

Therefore the minimum Von Neumann entropy of a graph is $$S=log(n_c)$$ where $$n_c$$ is the number of connected components.

# Facts about eigenvalues of Laplacian

Link at https://www.seas.upenn.edu/~jadbabai/ESE680/Laplacian_Thesis.pdf

- All eigenvalues of the Laplacian are positive or equal to zero. Its eigenvalues are $$\lambda_1,\lambda_2,\cdot,\lambda_N$$. The number of zero eigenvalues of $$L$$ is the number of connected components.

- Eigenvalue spectra of Laplacian matrix of a graph is invariant under vertex permutations. In other words, you can call the vertices with any names, but the graph remain the same. This is also true for the spectrum of the adjacecny matrix of a graph. You can get convinced with this following matlab code:

	{% highlight matlab %}
    N = 2000; % number of nodes
    B = 4; % number of blocks
    N1 = randperm(N); % random permutation of the nodes
    O = randomModularGraphPinPout(N,B,0.5,0); % generate the graph with intracluster density 0.5, intercluster density 0
    O1 = O(N1,N1); % permute the nodes randomly
    % You can see that the spectra of eigenvalues are the same.
    plot(1:N,eig(graph_laplacian(O)),'r',1:N,eig(graph_laplacian(O1)),'ob');
    {% endhighlight %}


- The product of nonzero eigenvalues of $$L$$ is the number of vertices times the number of spanning trees of $$G$$.
- Large values of $$\lambda_2$$ are associated with graphs that are hard to disconnect.
- $$(-1)^{i+j}\det(L_{[i,j]}) = t(G)$$ where $$t(G)$$ is the number of spanning trees of $$G$$ and $$L_{[i,j]}$$ is the Laplacian with i row and j column removed.
- $$\lambda_N(G^c) \leq N$$ with equality if and only if $$G^c$$ is disconnected. $$G^c$$ is the complement of the graph.
- The secondl largest eigenvalue (also called Fiedler eigenvalue) of the cartesian product of two graphs $$G_1,G_2$$ is the minimum between the second largest eigenvalues of $$L(G_1)$$ or $$L(G_2)$$.    
Recall that the Cartesian product of two graphs $$G_1$$ and $$G_2$$ defined as the graph $$G_1 \times G_2$$, with vertex-set $$V(G_1) \times V(G_2)$$; $$(i_1,j_1)$$ and $$(i_2,j_2)$$ are connected by an edge if and only if $$i_1=i_2$$ and $$j_1=j_2$$jl -.c, j2, or jl = j2. It

- In fact it can be shown that the set of eigenvalues of the kronecker product of $$G_1$$ and $$G_2$$ $$L(G_1 \otimes G_2)$$ is 
$$\{ \lambda_i(G_1) + \lambda_j(G_2) \| 1 \leq i \leq n_1, 1 \leq j \leq n_2 \}$$

- $$\lambda_2 \geq \frac{1}{N \textrm{diam}(G)}$$ where $$\textrm{diam}$$ is the diameter of $$G$$.
- $$\frac{\delta_{max}(L)}{\sqrt{n \log n}} \rightarrow \sqrt{2}$$ for $$n$$ large.

**Question**
Is the spectrum of Laplacian of a random modular graph be described by the Tracy Wisdom distribution?
https://www.wired.com/2014/10/tracy-widom-mysterious-statistical-law/
Leggere qui:
https://arxiv.org/pdf/1201.0425.pdf (guardare GOE)
https://arxiv.org/pdf/1011.2608.pdf (parla di spettro del laplaciano del random graph ER)

Sembra che lo spettro del Laplaciano del grafo random converga ad una convoluzione libera fra Gaussiana e legge del semicerchio di Wigner. La convoluzione libera (free convolution) leggere qui: Anderson, G.W.; Guionnet, A.; Zeitouni, O. (2010). An introduction to random matrices. Cambridge: Cambridge University Press. ISBN 978-0-521-19452-5.

Importante vedere anche questa pagina: 
https://en.wikipedia.org/wiki/Wishart_distribution
dove descrive qual'è la Kullback Leibler divergence fra due matrici Wishart distributed.

Vedere articolo Newman Phys Rev E 012803 (2013)



Notare che lo spettro del Laplaciano normalizzato per il random graph è uguale a 1+ lo spettro della matrice di adiacenza normalizzata come D^(-0.5)*A*D^(-0.5) e punta alla Wigner semi circle law. 


Notare e cercare di linkare il pdf sotto qit/matlab/rmtool/docs/ che dice che la limiting distribution della density matrix in pratica è la Wishart distribution, questo vuol dire che la density matrix è parametrizzabile con la Wishart distribution, cioè la distribuzione delle matrici di covarianza!!! e era calcolata la KL divergence.