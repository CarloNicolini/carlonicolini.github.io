---
layout: post
title: Detectability of communities and the quantum density matrix.
categories: science
published: false
date: 2017-03-10
---

# Some observations about the spectra of random modular networks and the Stochastic Block model

In the framework of spectral information entropy [ [1] ](#dedomenico2016), that with comparison of an observed network with a model, one has to minimize the Kullback-Leibler divergence in order to obtain maximum likelihood estimates of the model parameters that **fit** the graph.

I did the following.
I've generated a graph with $$N=250$$ nodes and two blocks of the same size.
I could control the intra- and inter- block densities, modeled as ER subnetworks, whose degree distribution is Poissonian.

Maximum entropy principle [[3](#jaynes1957a)] helps to estimate the $$\beta$$ parameter as the solution with respect to beta of the following equation:

$$\sum \limits_{i=1}^n e^{- \beta \lambda_i}(\lambda_i - \frac{1}{n})=0$$

(but this is not sure as DeDomenico told me that it may be different)

$$\sum_{i=1}^n \left(  \lambda_i \left(e^{-\beta \lambda_i}-\frac{1}{n}\right) \right) = 0$$


It is known that communities are detectable in the two groups SBM [[5,](#krzakala2013)[6](#zdeborova2015)] as long as:

$$|k_{in} - k_{out}| > 2 \sqrt{(k_{avg})}$$

I designed an optimization algorithm for the KL minimization that finds the optimal $$p_{in}$$ and $$p_{out}$$. Convexity of the KL divergence is of help. The KL minimization algorithm is based on *Expectation-Maximization*, basically it is a coordinate descent method, where the variables of optimization are alternatively greedily optimized, until convergence to the global minimum.

What I've observed is in line with the detectability threshold indeed.

I've verified that as long as the communities are in the detectability threshold, the global minimum of the KL divergence lies exactly at the modeled $$p_{in}, p_{out}$$ whereas when the detectability threshold is exceeded, then the global optimum lies in another valley.

# Planted structure detectable

Here I plot the landscape of $$D_{KL}$$ as a function of $$p_{in},p_{out}$$ at $$\beta^*$$ as selected from MaxEnt principle.

{% highlight matlab %}
N=360;
B=4;
pinstar=0.25;
poutstar=0.05;
k_in_star = N*pinstar;
k_out_star = N*poutstar;
k_star = (k_out_star + k_in_star)/2;
is_detectable = abs(k_in_star - k_out_star) > B*sqrt(k_star);
{% endhighlight %}



# Paralleling inference, learning, optimization, statistical mechanics

Some of the words for the machine learning, statistics and physics communities are representing the same concepts:

| Physics | Neuroscience | Machine learning | Information theory |
|--------------------------------------------|------------------|--------------------|---------------------------------------|
| Ising model | Hopfield network | Boltzmann Machine |  |
| Bethe-Peierls approximation, Cavity method | / | Belief propagation | Sum-product algorithm message passing |
| Boltzmann weighting factor $$e^{-\beta E(x)}$$| / | Probability of $$G$$ given parameters $$x$$ | 
| Energy $$E(x)$$ | $$-\log(P)$$  | |
| Most likely labeling = Ground state | Maximum a Posteriori (MAP) estimate |


## Notes
Never say "the likelihood of the data" but "the likelihood of the parameters". The likelihood function is not a probability distribution. If you want to mention the data that a likelihood function is associated with, you may say "the likelihood of the parameters given the data".


## Variational methods
Interested in $$P(x)=\frac{1}{Z}P^*(\mathbf{x})=\frac{1}{Z}\exp{-E(\mathbf{x})}$$

$$E(x)$$ is simple but not simple enough. Idea approximate $$P(x)$$ with another function $$Q(x)$$ such that the Kullback-Leibler divergence $$D_{KL}(P(x)\| Q(x)$$ is small. To do so it must be that $$Q(x)$$ closely follows $$P(x)$$ in the areas where $$P(x$)$$ is more concentrated, while maintaining zero in areas where $$P(x)$$ is zero, otherwise $$D_{KL}$$ incurs in a large penalty.

## Analogies between inference and physics
| Probability | Physics |
|-------------|----------|
| Probability of $$G$$ given $$\theta$$: $$P(G| \theta)$$ | $$

# References:
1. <a name="dedomenico2016"></a>De Domenico, M., Biamonte, J., 2016. Spectral entropies as information-theoretic tools for complex network comparison 41062, 1–13. [doi:10.1103/PhysRevX.6.041062](http://dx.doi.org/doi:10.1103/PhysRevX.6.041062)

2. <a name="estrada2014"></a>Estrada, E., De La Peña, J.A., Hatano, N., 2014. Walk entropies in graphs. Linear Algebra Appl. 443, 235–244. [doi:10.1016/j.laa.2013.11.009](http://dx.doi.org/doi:10.1016/j.laa.2013.11.009)

3. <a name="jaynes1957a"></a>Jaynes, E.T., 1957. Information theory and statistical mechanics. Phys. Rev. 106, 620–630. [doi:10.1103/PhysRev.106.620](http://dx.doi.org/doi:10.1103/PhysRev.106.620)

4. <a name="jaynes1957b"></a>Jaynes, E.T., 1957. Information theory and statistical mechanics. II. Phys. Rev. 108, 171–190. [doi:10.1103/PhysRev.106.620](http://dx.doi.org/doi:10.1103/PhysRev.106.620)

5. <a name="krzakala2013"></a>Krzakala, F., Moore, C., Mossel, E., Neeman, J., Sly, A., Zdeborová, L., Zhang, P., 2013. Spectral redemption in clustering sparse networks. Proc. Natl. Acad. Sci. U. S. A. 110, 20935–20940. [doi:10.1073/pnas.1312486110](http://dx.doi.org/doi:10.1073/pnas.1312486110)

6. <a name="zdeborova2015"></a>Zdeborová, L., Krzakala, F., 2015. Statistical physics of inference: Thresholds and algorithms. arXiv:1511.02476 1–62. [doi:10.1080/00018732.2016.1211393](http://dx.doi.org/doi:10.1080/00018732.2016.1211393)

7. <a name="estrada2012"></a>Estrada, E., Hatano, N., Benzi, M., 2012. The physics of communicability in complex networks. Phys. Rep. 514, 89–119. [doi:10.1016/j.physrep.2012.01.006](http://dx.doi.org/doi:10.1016/j.physrep.2012.01.006)