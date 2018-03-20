---
layout: post
title: Plugging the weighted random graph into Surprise
categories: science
published: true
date: 2017-05-10
---

Surprise is based on the calculation of the number of simple graphs with $$n$$ nodes and $$m$$ edges exactly.
This null model is called $$G_{nm}$$ model and it is the microcanonical version of the Erdos-Renyi model also called $$G_{np}$$.
To be more precise, Surprise does not compare against a fixed null model, but the null model is dependent on the partition itself. In other words, the expected fraction of intracluster edges is given by $$p_\zeta/p$$ and it is clearly dependent on the partition it self. For this reason Surprise is more similar to the Constant Potts Model than to a model where intracluster density is compared to a fixed constant.

In order to extend the definition of Surprise to support weighted random graphs, i.e. graphs carrying possibly more than one edge between two nodes, we first have to figure out how many topological configurations are there in the $$G_{nm}$$ model and then to annotate their multiplicity, based on combinatorial considerations.
In other words, the number of topological configurations is the same as in the $$G_{nm}$$ model, but each configuration has a number of possible ways to distribute the multi-edges upon the already existing edges.

Let us introduce some notation:

- $$G$$ undirected graph, weighted but no self-loops.
- $$n$$ number of nodes
- $$m$$ number of edges
- $$C$$ number of communities (or blocks)
- $$c$$ index of c-th community (or block)
- $$p$$ number of node pairs $$p=\binom{n}{2}$$.
- $$n_c$$ number of nodes in community $$c$$.
- $$m_c$$ number of edges in community $$c$$.
- $$w_c$$ total weight of edges in community $$c$$.
- $$p_c$$ number of pairs in community $$c$$.
- $$m_\zeta$$ total number of intracluster edges $$m_\zeta=\sum_c m_c$$.
- $$p_\zeta$$ total number of intracluster pairs $$p_\zeta=\sum_c p_c$$.
- $$w_\zeta$$ total weight of intracluster edges.
- $$m-m_\zeta$$ total number of intercluster edges.
- $$p-p_\zeta$$ total number of intercluster pairs.


This means that one has to compute the product between the number of topological configurations of the $$G_{nm}$$ which is $$\binom{\binom{n}{2}}{m}$$ and the number of ways to obtain each configuration given a certain total edge weight.
If we apply the ''Stars and bars'' method by W.Feller [(here explained)](https://en.wikipedia.org/wiki/Stars_and_bars_%28combinatorics%29), we notiche that 
the number of ways to distribute $$w$$ multilinks on $$m$$ edges is exactly the same as the number of ways to put $$w$$ indistinguishable balls into $$m$$ distinguishable bins.

Hence, each of the $$\binom{\binom{n}{2}}{m}$$ configurations can exist in $$\binom{w-1}{m-1}$$ different sub-configurations of links, as this is the number of possible distinct partitions of an integer (in this case $$w$$) into $$m$$ parts, or in other words, the number of ways to arrange $$w$$ indistinct marbles into $$m$$ distinct boxes.

We must stress the term ''distinguishable configuration'' here, as it is important that every edge is seen as a separate entity, being this is a vertex-labeled graph, with each edge a distinct entity.

The probability to observe **exactly** $$m_c$$ intracluster links and **exactly** $$w_c$$ intracluster edges is given by the hypergeometric distribution:

$$
P_{WRG}(m_i=m_c, w_i=w_c)=\dfrac{\binom{p_c}{m_i}\binom{w_i-1}{m_i-1} \binom{p-p_c}{m-m_i}\binom{(w_t-w_i)-1}{(m-m_i)-1}}{ \binom{p}{m} \binom{w_t-1}{m-1}}
$$

To find the probability to have **at least** $$m_c$$ internal edges and **at least** $$w_c$$ internal weight on edges, then we need to look at the cumulative distribution on edges and weights.
A **temptative** formula for this probability can be called **MultiSurprise**, a multilink (or WRG) version of Surprise is the following:

$$
S_{WRG} = \sum \limits_{w_i = w_\zeta}^{w_T}  \sum \limits_{m_i = m_\zeta}^{m}\dfrac{  \binom{p_\zeta}{m_i} \binom{w_i - 1}{m_i - 1} \binom{p-p_\zeta}{m-m_i}\binom{w_t - (w_i-1)}{m-(m_i-1)}}{\binom{p}{m}\binom{w_T-1}{m-1}}
$$

or alternatively the summation must be carried in parallel over the indices of edges and weights?

$$
S_{WRG} = \sum \limits_{w_i = w_\zeta, m_i = m_\zeta}^{w_T,m}\dfrac{\binom{p_\zeta}{m_i} \binom{w_i-1}{m_i-1}\binom{p-p_\zeta}{m-m_i}\binom{w_t - w_i-1}{m-m_i-1}}{\binom{p}{m}\binom{w_T-1}{m-1}}
$$

<!-- 
# Binomial version of standard Surprise

The hypergeometric version of standard Surprise is:

$$
P(i=m_c) = \dfrac{\binom{p_c}{i}\binom{p-p_c}{m-i}}{\binom{p}{m}}
$$

This is the probability to extract **exactly** $$m_c$$ edges from an urn **without** replacement.
In the limit of large $$p$$ at $$\langle q \rangle = \frac{p_c}{p}$$ and $$q=\frac{m_c}{m}$$ kept fixed then is possible to approximate the hypergeometric to a binomial like:

$$
\lim \limits_{p \rightarrow \infty} P_{hyper}(i=m_c) = P_{binomial}(i=m_c) = \binom{m}{m_c} \langle q \rangle ^{m_c} (1-\langle q \rangle)^{m-m_c}
$$

This is the probability to extract **exactly** $$m_c$$ edges from an urn with replacement.
The probability instead to have **at least** $$m_\zeta = \sum_c m_c$$ intracluster edges is the cumulative of the binomial:

$$
\lim \limits_{p \rightarrow \infty} P_{hyper}(i \geq m_\zeta) = P_{binomial}(i \geq m_\zeta) = \sum \limits_{i=m_\zeta}^m \binom{m}{i} \langle q \rangle ^{i} (1-\langle q \rangle)^{m-i}
$$

We can use the Stirling approximation of binomial coefficients which reads:

$$
\log \binom{a}{b} \approx a \log a - b\log b - (a-b)\log(a-b)
$$

Then taking the logarithm of this with the Stirling approximation it results:
 -->