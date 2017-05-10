---
layout: post
title: Surprise to support configuration model
categories: science
published: false
date: 2017-05-08
---

Let's start with some notation:

- $$G$$ undirected graph, unweighted, no self-loops, no multiedges.
- $$n$$ number of nodes
- $$m$$ number of edges
- $$C$$ number of communities (or blocks)
- $$c$$ index of c-th community (or block)
- $$p$$ number of node pairs $$p=\binom{n}{2}$$.
- $$n_c$$ number of nodes in community $$c$$.
- $$m_c$$ number of edges in community $$c$$.
- $$p_c$$ number of pairs in community $$c$$.
- $$m_\zeta$$ total number of intracluster edges $$m_\zeta=\sum_c m_c$$.
- $$p_\zeta$$ total number of intracluster pairs $$p_\zeta=\sum_c p_c$$.
- $$m-m_\zeta$$ total number of intercluster edges.
- $$p-p_\zeta$$ total number of intercluster pairs.

The discrete version of Surprise is then defined as:

$$ S = \sum \limits_i ^{m_\zeta} \dfrac{\binom{p_\zeta}{i}  \binom{p-p_\zeta}{m-i} }{\binom{p}{m}}$$

This version considers an urn model with two types of balls, i.e. an urn model where the balls (node pairs) are of two kinds, edges or non-edges.
In total there are $$p-p_\zeta$$ black balls and $$p_\zeta$$ white balls. One extracts **without replacement** $$m$$ balls and is interested in the probability to have at least $$m_\zeta$$ white balls.

The implicit null model upon which Surprise is based is the $$G_{nm}$$ model (and not the $$G_{np}$$) because the number of edges is fixed (you can see it as a microcanonical version of the $$G_{np}$$ model). The cardinality of the $$G_{nm}$$ set with exactly $$n$$ nodes and $$m$$ edges is represented by the denominator of Surprise. It is the number of all possible graphs with exactly $$m$$ edges and $$p=\binom{n}{2}$$ pairs of edges.

A problem of Surprise is that it does not depend on the actual distribution of intra- and inter- cluster edges. 
It is possible to define a multivariate variant of Surprise that considers edges between each community separately. 
Instead of only two kind of balls (intra- and inter- cluster) this model has a total of $$C^2$$ kind of balls, meaning one for each pair of communities and reads:

$$S_M = \prod \limits_{r,s}^{C^2} \dfrac{\binom{n_r n_s}{m_{rs}}}{\binom{p}{m}}$$

This last formulation of Surprise $$S_M$$ resembles the SBM but it does not work very well and includes high degree nodes in the same communities.
Indeed, the $$G_{nm}$$ model upon which Surprise is based, does not take the degrees sequence into consideration (the normalization factor $$\binom{p}{m}$$ counts the total number of graphs with exactly $$m$$ edges over $$p$$ pairs of nodes).

It is shown by Traag 2015, that both the original Surprise and the multivariate version of it can be approximated (their logarithms, to be exact) to a formulation that uses the relative entropy between the observed fraction of intracluster edges $$q$$ and the expected fraction of intracluster edges $$\left< q \right> $$:

$$ -\log({S}) \sim m D_{KL}(q \| \left< q \right>)$$

In the case of the original formulation of Surprise $$q=\frac{m_\zeta}{m}$$ and $$\left< q \right> = \frac{p_\zeta}{p}$$, because the balls are just of two colors (intracluster or intercluster) and one uses the **binary** Kullback-Leibler divergence, namely:

$$D_{KL}(q \| \left<q\right >) = x \log \left( \frac{q}{\left<q\right >} \right ) + (1-q)\log\left( \frac{1-q}{1-\left<q\right >}\right),$$

while for the multivariate variant of Surprise $$S_M$$, the observed and expected fraction of edges are $$q=m_{rs}/m$$ and $$\left< q \right> = n_r n_s /n^2$$ and the sum runs over all pairs of communities:

$$-\log({S_M}) \sim m D_{KL}\left(q \| \left<q\right >\right ) =  m \sum_{rs} \dfrac{m_{rs}}{m} \log\left(\dfrac{m_{rs}/m}{n_r n_s/n^2} \right)$$

These last two formulations are extremely similar to the uncorrected stochastic block model introduced by Newman and Karrer as in Equation 7 in their paper [https://arxiv.org/abs/1008.3926v1](https://arxiv.org/abs/1008.3926v1).
When the degree-correction is included, the resulting log-likelihood is 

$$ \mathcal{L}(G | \sigma) = m \sum_{rs} \dfrac{m_{rs}}{2m} \log\left(\dfrac{m_{rs}/{2m}}{(K_r/2m)(K_s/2m)} \right)$$

I wanted to replicate the reasoning by Karrer and Newman backwards, starting from this last equation of the degree corrected SBM, to go back to an hypergeometric formulation like the one in Surprise.
What I think is important in developing a degree corrected Surprise is to consider edge stubs as the basic entities instead of node pairs.
Then to start, one has to compute how many possible distinct graphs there are in the configuration model (at this moment the information of clustering is not yet considered).
From combinatorial arguments [[Radicchi 2010](#Radicchi2010)], the cardinality of the configuration model ensemble $$| \Omega_{CM}|$$ is the total number of possible rewirings given the degree sequence and it can be computed (but I am definitely **not** sure it is correct) as: 

$$
| \Omega_{CM} | = \binom{2m}{k_1, \ldots k_n} = \dfrac{(2m)!}{\prod \limits_i^n (k_i)!}
$$
