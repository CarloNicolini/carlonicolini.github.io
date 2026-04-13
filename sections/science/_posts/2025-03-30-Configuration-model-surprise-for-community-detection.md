---
layout: post
title: Configuration-model Surprise for community detection
description: "Surprise vs configuration null for community detection; stubs and pairings."
date: 2025-03-30
published: true
categories:
  - science
  - complex-networks
---

## From vertex pairs to stubs

A few years ago I tried to adapt Surprise to a degree-corrected null model.
The intuition was simple and, I still think, correct: if hubs are expected to connect more often, then the null should not count vertex pairs uniformly.
It should count stubs.

The place where my old derivation went wrong was more subtle.
I replaced vertex pairs by stubs, but I kept the wrong combinatorics.
I was counting assignments of stubs to vertices, not pairings of stubs into edges.

This post is the cleaned-up derivation.

I will stay with the simplest goal: community detection only.
So the question is not whether a partition explains a full block matrix, but only whether it creates unusually many internal edges once the degree sequence is kept fixed.

## Ordinary Surprise revisited

Let $G$ be an undirected simple graph with $n$ nodes and $m$ edges, and let $g$ be a partition of the nodes into communities.
Write

- $m_\zeta(g)$ for the number of internal edges of the partition,
- $p_\zeta(g)=\sum_c \binom{n_c}{2}$ for the number of internal vertex pairs,
- $p=\binom{n}{2}$ for the total number of vertex pairs.

Original Surprise asks for the probability that a uniform graph in $G_{nm}$ with the same $n$ and $m$ has at least as many internal edges as the observed partition {% cite aldecoa2011deciphering %}:

$$
S(g) = -\log \sum_{i=m_\zeta(g)}^m
\frac{\binom{p_\zeta(g)}{i}\binom{p-p_\zeta(g)}{m-i}}{\binom{p}{m}}.
\tag{1}
$$

This is already a neat one-sided exact test.
But it is degree blind: every vertex pair is treated equally.

## What degree correction should mean

Now keep the observed degree sequence $k_1,\dots,k_n$ fixed and denote

$$
\sum_{i=1}^n k_i = 2m.
$$

For each community $c$, define the community stub mass

$$
K_c = \sum_{i: g_i=c} k_i,
\qquad
\sum_c K_c = 2m.
\tag{2}
$$

At this point the basic entities are not vertex pairs anymore.
They are stubs.
A configuration-model sample is obtained by pairing the $2m$ labeled stubs uniformly at random.

This is the first crucial correction to my old note: the size of the sample space is not a multinomial coefficient.
It is the number of perfect matchings of $2m$ labeled stubs,

$$
|\Omega_{CM}| = (2m-1)!! = \frac{(2m)!}{2^m m!}.
\tag{3}
$$

The multinomial coefficient $\binom{2m}{k_1,\ldots,k_n}$ only counts how many ways one can assign $2m$ stub labels to vertices with multiplicities $k_i$.
It does not count how many ways those stubs can be paired into edges.
That was the bug.

To keep the derivation exact and transparent, I work in the microcanonical configuration model given by random stub pairings.
This ensemble naturally allows self-loops and multiedges.
Conditioning on simple graphs is possible, but it destroys the closed form and does not change the leading asymptotic expression in the sparse regime.

## Exact counting at the block level

Even if the final goal is community detection only, the right exact derivation passes through the block edge counts.

For $r \le s$, let $m_{rs}$ be the number of edges between communities $r$ and $s$, with $m_{rr}$ the number of edges internal to community $r$.
These counts must satisfy

$$
2m_{rr} + \sum_{s \ne r} m_{rs} = K_r
\qquad\text{for every } r.
\tag{4}
$$

Now fix a feasible matrix $\{m_{rs}\}$.
How many stub pairings realize it?

The counting is straightforward once written in the right order.

For each community $r$:

1. Split its $K_r$ labeled stubs into one internal bucket of size $2m_{rr}$ and one bucket of size $m_{rs}$ for every $s \ne r$.
   This gives
   $$
   \frac{K_r!}{(2m_{rr})!\prod_{s\ne r} m_{rs}!}.
   $$

2. Pair the $2m_{rr}$ internal stubs among themselves.
   This gives
   $$
   (2m_{rr}-1)!! = \frac{(2m_{rr})!}{2^{m_{rr}} m_{rr}!}.
   $$

3. For each pair $r<s$, pair the $m_{rs}$ stubs selected in block $r$ with the $m_{rs}$ stubs selected in block $s$.
   This gives $m_{rs}!$ matchings.

Multiplying everything and simplifying yields the exact number of labeled-stub pairings compatible with the block matrix:

$$
N(\{m_{rs}\}\mid K)
=
\frac{\prod_r K_r!}
{\left(\prod_r 2^{m_{rr}} m_{rr}!\right)
 \left(\prod_{r<s} m_{rs}!\right)}.
\tag{5}
$$

Therefore the exact probability of a block matrix under random stub pairing is

$$
\mathbb{P}_{CM}(\{m_{rs}\}\mid K)
=
\frac{N(\{m_{rs}\}\mid K)}{(2m-1)!!}.
\tag{6}
$$

This is the exact microcanonical degree-corrected object.
It is the correct replacement for the old ad hoc denominator.

## Marginalizing back to communities only

For community detection only, I do not want the full block matrix.
I only want the total number of internal edges

$$
M_\zeta = \sum_r m_{rr}.
\tag{7}
$$

So the exact configuration-model probability of observing exactly $t$ internal edges is obtained by marginalizing the block law:

$$
\mathbb{P}_{CM}(M_\zeta=t \mid K) = \sum_{\{m_{rs}\} \in \mathcal{M}_t(K)} \mathbb{P}_{CM}(\{m_{rs}\} \mid K), \tag{8}
$$

where the quantity $M_t ( K )$ is the set of all feasible matrices satisfying the degree-balance constraints in Eq. (4) and $\sum_r m_{rr}=t$.

This is the point where the structure differs from ordinary Surprise.
In $G_{nm}$, the exact null is hypergeometric because one samples vertex pairs without replacement from two bins: internal pairs and external pairs.
In the configuration model, one samples pairings of stubs, and those pairings are globally coupled.
The exact law is no longer hypergeometric.

That leads to the natural degree-corrected analogue of Surprise:

$$
S_{CM}^{\mathrm{disc}}(g) = -\log \sum_{t=m_\zeta(g)}^m \mathbb{P}_{CM}(M_\zeta=t \mid K(g)). \tag{9}
$$

This is the exact one-sided p-value style score: how surprising is it to see at least this many internal edges under random stub pairing with the observed degree sequence?

## The expected internal mass under the configuration model

To get an asymptotic approximation, the first quantity to compute is the null internal fraction.

Take any two stubs belonging to the same community $c$.
Under a uniform random pairing, the probability that they are paired together is $1/(2m-1)$.
Summing over all same-community stub pairs gives

$$
\mathbb{E}_{CM}[M_\zeta \mid K] = \frac{1}{2m-1} \sum_c \binom{K_c}{2}. \tag{10}
$$

Therefore the expected internal edge fraction is

$$
\langle q \rangle_{CM} = \frac{\mathbb{E}_{CM}[M_\zeta \mid K]}{m} = \frac{\sum_c K_c(K_c-1)}{2m(2m-1)}. \tag{11}
$$

If $m$ is large, this becomes

$$
\langle q \rangle_{CM} = \sum_c \left(\frac{K_c}{2m}\right)^2 + O(m^{-1}). \tag{12}
$$

This is exactly the degree-corrected replacement of $p_\zeta/p$.
Ordinary Surprise uses the fraction of internal vertex pairs.
The degree-corrected version uses the fraction of same-community stub pairs.

## Asymptotic configuration-model Surprise

Now define the observed internal fraction

$$
q = \frac{m_\zeta(g)}{m}.
\tag{13}
$$

The exact discrete law in Eq. (8) is cumbersome because of the pairing dependencies.
But once everything is coarse-grained to the binary question "internal or external", the leading large-deviation term is the same binary relative entropy that appears in Asymptotical Surprise {% cite traag2015detecting %}.
This is the same approximation step used in moving from discrete Surprise to its asymptotic form: keep the leading entropy term and drop the subleading combinatorial corrections.

That gives the natural asymptotic degree-corrected score

$$
S_{CM}^{\mathrm{asym}}(g) = m\,D_{KL}\!\left(q \,\middle\|\, \langle q \rangle_{CM}\right), \tag{14}
$$

with

$$
D_{KL}(x\|y)=x\log\frac{x}{y}+(1-x)\log\frac{1-x}{1-y}. \tag{15}
$$

In explicit form,

$$
S_{CM}^{\mathrm{asym}}(g) = m_\zeta \log\frac{q}{\langle q \rangle_{CM}} + (m-m_\zeta)\log\frac{1-q}{1-\langle q \rangle_{CM}}. \tag{16}
$$

This is the clean community-only, degree-corrected analogue of Asymptotical Surprise.

The meaning is exactly the one I wanted years ago:
the score is large when the partition concentrates more edges inside communities than random stub mixing would predict from the degree sequence alone.

## G-test interpretation

There is another way to read the same formula. Under the degree-corrected null, the observed counts are

$$
O_{\mathrm{in}}=m_\zeta, \qquad O_{\mathrm{out}}=m-m_\zeta, \tag{17}
$$

while the expected counts are

$$
E_{\mathrm{in}}=m\langle q \rangle_{CM}, \qquad E_{\mathrm{out}}=m(1-\langle q \rangle_{CM}). \tag{18}
$$

The binary G-test statistic is then

$$
G
=
2\left[
O_{\mathrm{in}}\log\frac{O_{\mathrm{in}}}{E_{\mathrm{in}}}
+
O_{\mathrm{out}}\log\frac{O_{\mathrm{out}}}{E_{\mathrm{out}}}
\right]
=
2m\,D_{KL}(q\|\langle q\rangle_{CM}).
\tag{19}
$$

So the asymptotic score is simply half of a binary likelihood-ratio statistic.
That is not an accident.
Surprise, asymptotic Surprise, and degree-corrected asymptotic Surprise are all measuring deviations from a null by the same large-deviation geometry.
What changes is the null ensemble.

## Relation to the degree-corrected SBM

This also clarifies the connection with the degree-corrected stochastic block model of Karrer and Newman {% cite karrer2011stochastic %}.

The degree-corrected SBM keeps the full matrix of block edge counts $\{m_{rs}\}$ and compares it to the degree-based expectation.
In that more detailed model, the score is multivariate.
My community-only construction instead collapses the whole matrix to one scalar,

$$
m_\zeta = \sum_r m_{rr},
\tag{20}
$$

and asks only whether internal connectivity is larger than expected.

So the relationship is:

- the exact block law in Eq. (6) is the microcanonical degree-corrected object;
- the exact community-only score in Eq. (9) is its marginal over all block matrices with the same diagonal sum;
- the asymptotic score in Eq. (14) is the binary, assortative projection of the degree-corrected SBM likelihood ratio.

In this sense, the configuration-model version of Surprise is not a different planet from the DCSBM.
It is its community-only shadow.

## Comparison with Tiago Peixoto's approach

This is exactly where Tiago Peixoto's work becomes the right benchmark {% cite peixoto2014hierarchical,peixoto2017nonparametric %}.

Peixoto's microcanonical and Bayesian SBM program keeps the full block matrix and treats the problem as generative model selection.
One does not ask only whether a given partition has an unexpectedly high internal edge density.
One asks which partition, which number of groups, and which level of hierarchy best compress the whole adjacency pattern.

That leads to a few important differences.

1. **Objective.**  
   My $S_{CM}^{\mathrm{disc}}$ is a one-sided significance score specialized to assortative community detection.
   Peixoto optimizes posterior probability or description length.

2. **Statistic.**  
   My score depends on the coarse scalar $m_\zeta$.
   Peixoto keeps the whole matrix $\{m_{rs}\}$.
   That means he can represent assortative, disassortative, bipartite, core-periphery, and hierarchical structures in a unified way.

3. **Model complexity.**  
   Surprise-style scores do not automatically include an Occam penalty for the number of groups.
   Peixoto's Bayesian formulation does.
   This is one of the reasons his approach is much more robust as a full inference framework.

4. **Interpretation.**  
   The construction here is closer in spirit to the original Surprise: it is a degree-corrected test of "too many internal edges".
   Peixoto's machinery is closer to a full probabilistic theory of block structure.

Seen this way, the present construction is not a competitor to Peixoto's program.
It is a deliberately simpler object.
If I want a degree-corrected score that preserves the original intuition of Surprise, this is the right object.
If I want the most expressive and statistically principled blockmodel inference, the natural next step is to stop collapsing to $m_\zeta$ and move all the way to Peixoto's microcanonical SBM.

## Final formula

If I had to summarize the result in one line, it would be this.

The exact degree-corrected, community-only Surprise is

$$
S_{CM}^{\mathrm{disc}}(g)
=
-\log \sum_{t=m_\zeta(g)}^m
\sum_{\{m_{rs}\}\in\mathcal{M}_t(K(g))}
\frac{1}{(2m-1)!!}
\frac{\prod_r K_r!}
{\left(\prod_r 2^{m_{rr}} m_{rr}!\right)
 \left(\prod_{r<s} m_{rs}!\right)},
\tag{21}
$$

and its clean asymptotic approximation is

$$
S_{CM}^{\mathrm{asym}}(g)
=
m\,D_{KL}\!\left(
\frac{m_\zeta(g)}{m}
\;\middle\|\;
\frac{\sum_c K_c(K_c-1)}{2m(2m-1)}
\right).
\tag{22}
$$

This is the derivation I wish I had written down the first time around.

---

## References

{% bibliography --cited %}
