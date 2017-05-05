---
layout: post
title: Extending Surprise to support the configuration model
categories: science
published: false
date: 2016-09-26
---

<blockquote>
"How to extend Surprise to include degree-based corrections?"
</blockquote>

Surprise is defined as

$$ S = \sum \limits_i ^{m_\zeta} \frac{\binom{p_\zeta}{i}  \binom{p-p_\zeta}{m-i} }{\binom{p}{m}}$$

we count the edge stubs and consider communities separately.

Every community $$c$$ has $$n_c$$ nodes, $$m_c$$ edges and $$k_c = \sum_{i \in c} k_i$$ stubs.
We separated intra-community and extra-community stubs.


- $$n$$ is the number of nodes
- $$m$$ is the number of edges
- $$k_i$$ is the degree of node $$i$$

1. Start with the total number of ways to arrange $$2m$$ stubs (since by the handshaking lemma $$\sum_i k_i = 2m$$). It is based on the multinomial coefficient

$$
\binom{2m}{k_1,\ldots,k_n} = \dfrac{(2m)!}{\prod \limits_i^n k_i!}
$$
this is the denominator.

Now consider how many possible combinations are possible for nodes in community $$c$$

$$
\binom{2m_c}{ \{k_i | i \in c \} } = \dfrac{(2m_c)!}{ \prod \limits_{i | i \in c} k_i!}
$$

then the product over all communities returns the multinomial configuration-model surprise

$$
\mathcal{S}_{CM} = \prod \limits_c \dfrac{ \binom{2m_c}{ \{k_i | i \in c \} } } {\binom{2m}{k_1,\ldots,k_n}}
$$

Let's take the logarithms of $$\mathcal{S}_{CM}$$ and try to replicate the same resoning to obtain an information theoretic based estimate of modularity using Kullback-Leibler divergence:

$$
\log \mathcal{S}_{CM} = \log \left( \prod \limits_c \dfrac{ \binom{2m_c}{ \{k_i | i \in c \} } } {\binom{2m}{k_1,\ldots,k_n}} \right ) = \sum_c \log \left( \binom{2m_c}{ \{k_i | i \in c \} } \right) - \log \left( \binom{2m}{k_1,\ldots,k_n} \right ) = 
$$

Applying the Stirling approximation to the multinomial coefficients that involves the Shannon entropy $$H(\mathbf{Y})= - \sum_i p(y_i)\log(p(y_i))$$,

$$
\log \left[  \binom{x}{y_1,\ldots,y_z} \right] = \log \left[  \frac{x!}{ \prod \limits_i^z y_i!} \right] \sim - x \sum_i \frac{y_i}{x}\log \left( \frac{y_i}{x}\right) = -x H(\mathbf{y}/x)
$$


we can obtain:

$$
\log \mathcal{S}_{CM} \approx \sum_c \left( - 2m_c \sum_{i \in c} \left( \frac{k_i}{2m_c}\log \frac{k_i}{2m_c} \right)  \right) 
- \left( - 2m \sum_{i} \left( \frac{k_i}{2m}\log \frac{k_i}{2m} \right)  \right) 
$$


<!-- $$\log \left( \binom{2m}{ k_1 \ldots k_n } \right) = \log \left( \frac{(2m)!}{\prod_i k_i!} \right) \sim 2m H\left( \frac{\prod \limits_i k_i!}{2m}\right)$$
where
$$H(x) = - \sum_i x_i\log(x_i) $$
we obtain:

$$
\sum_c \left[ 2m_c H\left(  \frac{\prod \limits_{i \in c} k_i!} {2m_c} \right ) - 2m H\left(  \frac{\prod \limits_{i} k_i} {2m} \right )  \right ] 
$$

$$
= \sum_c \left[ -2m_c \sum_{i \in c}\frac{k_i}{2m_c}\log\left( \frac{k_i}{2m_c} \right)  + 2m \sum_i\frac{k_i}{2m}\log\left( \frac{k_i}{2m} \right)  \right ] 
$$

Forgetting the part that not depends on the partitioning we obtain:

$$
\mathcal{S}_{CM} \approx - \sum_c 2m_c 
$$

$$
\sum_c \log \left( \binom{2m_c}{ \{k_i | i \in c \} } \right) - \log \left( \binom{2m}{k_1,\ldots,k_n} \right ) = 
$$ -->

<!-- to adapt this definition to the classical surprise I'd expect to instead of the configuration model use a constant expected wiring probability. -->

<!-- Every community has $$p_c = \binom{n_c}{2}$$ internal pairs and $$p-p_c$$ external pairs, in terms of stubs $$2p_c$$ possible internal stubs and $$2(p-p_c)$$ possible external stubs.

$$k_c = \sum_{i \in c} k_i = k_c^{int} + k_c^{ext}$$

the probability to pick exactly $$k_c^{int} = 2m_c $$ internal stubs from a community containing a total of $$k_c$$ stubs is

$$
\frac{ \binom{}{}\binom{}{} }{\binom{p}{m} }
$$
 -->