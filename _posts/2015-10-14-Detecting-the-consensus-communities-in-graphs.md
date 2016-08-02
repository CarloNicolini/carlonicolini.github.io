---
layout: default
title: Detecting the consensus communities in graphs
categories: science
date: 2015-10-14
---

Ensemble community detection


In these section we’ll address in depth an approach to making sense of
the mesoscopic structure of a network by means of non-deterministic
methods. We will take advantage of the methods of statistical physics
and treat with ensembles of partitions to assess the statistical
significance of community structure.

Stochastic optimization methods
-------------------------------

Many problems related to clustering, like graph partitioning and
community detection, are very often NP-hard problems @fortunato2010. In
this case, deterministic algorithms can be used only for very small
systems, but on larger instances, greedy approximation heuristics are
necessary tools to provide insightful solutions. Stochastic optimization
methods @hoos2004 are a class of heuristics that introduce randomness in
the search process to accelerate the optimization and escape local
minima of complex objective functions.

Even when the underlying structure of the data is precise and
well-defined, like the problem of finding the community structure on
regular graphs, non deterministic algorithms can accelerate the search
process and make it less dependent on modeling errors if considered on a
number of independent runs and their results averaged.

Non-deterministic nature of approximated methods implies that final
partitions may be different, particularly when the search space exhibits
many uncorrelated local optima, a phenomenon that is more acute when the
network structure is far from the community detectability threshold
@zhang2014 [@good2009].

Indeed, the set of multiple local optima partition obtained with non
deterministic methods is identified in statistical physics as the set of
*replicas* solutions, as shown in Figure \[fig:replica\_landscape\].
Many levels of structural information are encoded in the replicas. They
encode the effects of noise in the search process and intrinsic scales
of modules@ronhovde2009. Availability of a set of replica partitions,
greatly extends the knowledge on the network structure. It provides a
view on network structural instabilities (i.e. vertices oscillating
between communities over the replicas, due mostly to stochastic effects)
and on recursive hierarchies.

The study of the information-theory-based correlations of replicas,
allows to assess the quality of candidate solutions, and to compare them
to a ground-truth, where available. It’s worth noting that the very
efficient community detection algorithm of Ronhovde and Nussinov
@ronhovde2009 directly looks for that subset of highly similar replicas
as a way to justify the existence of community structure. They identify
the dominant solution as that described by the set of replicas with the
stronger correlation. This representative solution is selected as that
where stochastic effects introduced by non-deterministic optimization
methods are negligible and therefore provides a robust and statistically
reliable view on the mesoscopic structure of the network.

![A sketchy illustration of optimization in community detection
problems. The landscape of the quality function, is depicted as the blue
sheet, where the bumps represent its local optima. Replicas are the
colored marble, particular configurations of the landscape. They are
correlated via the represented springs, the stronger the spring the
higher the correlation.<span
data-label="fig:replica_landscape"></span>](images/replica.png)

Measures for replica correlation
--------------------------------

The existence of a multitude of replica solutions gives raise to the
problem of comparing partitions. The most well-grounded and performing
metrics are rooted in information theory@cover2006. The *Normalized
Mutual Information* @danon2005 and the *Variation of
Information*@meila2007 are the most widely used, despite it has been
recently found that both of them suffer of systematic errors due to the
finite size of the network @zhang2015. In the rest of the discussions we
ignore the limitation of finite size effects, by only working with
relatively large networks.

Normalized Mutual Information (NMI) and Variation of Information (VI)
assume that clustering comparison is a problem of message decoding.
Implicit in this, is the idea that if two partitions are similar,
inferring one partition from the other needs very little information.

Let us consider two generic partitions
$\mathcal{X}=(X_1,X_2,\ldots,X_{n_x})$ and
$\mathcal{Y}=(Y_1,Y_2,\ldots,Y_{n_y})$ of a graph $\mathcal{G}$ with
$n_X$ and $n_Y$ communities respectively. We indicate with $n$ the
number of graph vertices, with $n_i^X$ and $n_j^Y$ the number of
vertices in communities $X_i$ and $Y_j$, and with $n_{ij}$ the number of
vertices shared by clusters $X_i$ and $Y_j$, $n_{ij}=| X_i \cap Y_j|$.

Let us also consider the community assignments $\{ x_i\}$ and $\{ y_i\}$
for partitions $\mathcal{X}$ and $\mathcal{Y}$ respectively; we treat
the labels $x$ and $y$ as values of two random variables $X$ and $Y$
with joint distribution $P(x,y)=P(X=x, Y=y) = n_{xy}/n$, which implies
that $P(x)=P(X=x)=n_x^X/n$ and $P(y)=P(Y=y)=n_y^Y/n$. The mutual
information is then defined as $I(X,Y)=H(X) - H(X|Y)$ where
$H(X)=-\sum_x P(x) \log P(X)$ is the Shannon entropy of $x$. The mutual
information itself is not very useful, because hierarchically splitting
the clusters in $X$ would produce no change in the prior $H(X|Y)$ and
partitions with different hierarchies of the same clusters, would go
unnoticed. This observation led @danon2005 to define normalized mutual
information as
$$\textrm{NMI}(\mathcal{X},\mathcal{Y}) = \frac{2I(X,Y)}{H(X)+H(Y)}$$
Similar to NMI is the Variation of Information @meila2007,

$$\textrm{VI}(\mathcal{X},\mathcal{Y}) = H(X|Y) + H(Y|X)$$

which, has the desiderable property that it defines a metric on the
space of the partitions and it’s a distance. It is also a local measure,
i. e. the similarity of partitions differing only in a small portion of
a graph depends on the differences of the clusters in that region, and
not on the partition of the rest of the graph.

As noted by Karrer @karrer2008 VI is upper-bounded by a $\log(n)$
factor, so a simple normalization brings it in the $[0,1]$ range.
Importantly, VI is zero for maximally equal partitions and $1$ for
mostly dissimilar, a inversely to NMI.

What we are going to address in detail in the next paragraphs is a
community detection method that practically implements the replica
problem and is intrinsically stable and robust, able to approximate the
actual mesostructure of the graph better than the direct application of
a single algorithm, which we have shown to be affected by a multitude of
problems.

Consensus clustering
====================

Consensus clustering is the generic term to indicate a class of methods
that mitigate the variability effects of non-deterministic algorithms in
data clustering and that deliver a solution representing a *median* over
a set of partitions. In general consensus algorithms obtain stable
results out of a set of partitions produced by stochastic methods. In
this approach, a consensual community is identified as a subset of
vertices that are frequently sharing the same cluster through many
independent replicas. In this respect it’s important to stress that
consensus clustering does not provide partitions with better quality
functions, but instead it looks for the partition mostly similar to all
others.

In fact, consensus clustering implicitly changes the paradigm of
community detection. While traditionally methods seeks for best quality
partitions, consensus clustering looks for the *consensual partition*,
i.e. the one where the overall probability that vertices are coclustered
is higher.

The constituting element of consensus clustering is the *consensus
matrix* $\mathcal{P}\in \mathbb{R}^{n\times n}$, where every elements
counts the number of times that vertices $i$ and $j$ are clustered
together over the total number of independent replicas. Implicit in the
usage of the consensus matrix is the fact that, if multiple runs of a
community detection algorithm agree that a subset of nodes belong to a
community, then this is surely more significant than what found by a
single run.

An illustrative example that show the convenience of consensus
clustering is a graph $\mathcal{G}$ consisting of two partially
overlapping cliques $\mathcal{C}_1,\mathcal{C}_2$, as illustrated in
Figure \[fig:consensus\_cliques\]. For such simple graph, a
non-deterministic community detection algorithm will produce solutions
where the vertices in-between the two cliques will be sometimes assigned
to $\mathcal{C}_1$ and sometimes to $\mathcal{C}_2$. Consensual
combination of all these partial solutions, can detect the connector
vertex as the intersection of two overlapping communities and as a
source of potential instability in the network.

![Consensus partition of two intersecting cliques<span
data-label="fig:consensus_cliques"></span>](images/consensus_cliques.pdf)

A widely used approach for consensus community detection in networks is
the one of Lancichinetti et al @lancichinetti2012. The method is
iterative: firstly the consensus matrix is built from $n_p$ repetitions
of some non deterministic algorithm $\mathcal{A}$ and then, iteratively
$\mathcal{A}$ is run on progressively thresholed consensus matrices till
convergence is established.

A clustering algorithm $\mathcal{A}$ that supports weighted graphs is in
order, because it must run on the weighted consensus matrix until it
turns into a block-diagonal matrix, whose elements are $1$ for vertices
in the same block and $0$ for vertices in different blocks. The authors
show numerically that convergence is guaranteed in a few (typically 50)
iterations. A high level description of the algorithm of Lancichinetti
is given in Algorithm \[alg:consensus\_lancichinetti\].

\[htb!\]

1.  Apply $\mathcal{A}$ on $G$ $n_p$ times to get $n_p$ partitions

2.  Compute the consensus matrix $P$ where $P_{ij}$ is the average
    number of times that vertex $i$ and $j$ are clustered together.

3.  Set to zero all entries of $P$ under a chosen threshold $\tau$

4.  Apply $\mathcal{A}$ on $P$ $n_p$ times to get $n_p$ partitions.

5.  If all partitions are equal stop, otherwise go to step 2
    and reiterate.

Crucial to above described method is the choice of the threshold
parameter $\tau \in [0,1]$ applied at every iteration to keep the
consensus matrix relatively sparse. Lancichinetti @lancichinetti2012
empirically finds that the choice of $\tau$ is dependent on the specific
algorithm $\mathcal{A}$ and typically, when $\mathcal{A}$ is the Louvain
method @blondel2008, a value of $\tau \approx 0.4$ suffices to ensure
convergence in $~50$ iterations.

Another study of Campigotto on consensus clustering @campigotto2013
shows that consensual communities appear in a large range of the
threshold parameter $\tau$, and that consensus based approaches allow to
distinguish graphs with real community structure from graphs where
communities arise just as finite size effect or random fluctuations.

Quantification of the consensus matrix allows one to better define
functional clusters of a network as subsets of tightly connected
vertices which are clustered together most of the times and to find out
which vertices are more probably part of two different communities or
act as communities connectors, switching from one community to the
other. Consensus matrix allows to extend classic community detection to
the problem of overlapping communities, if one

The seemingly easy approach of the consensus matrix, presents some
difficulties though.

A first question that may arise is at which level should one consider
two nodes to be in the same community, or equivalently, the problem of
selecting the threshold $\tau$. The approach of Lancichinetti exploits
the convergence of the consensus matrix that is only empirically
guaranteed. Wheter $\tau$ and $n_p$ can be selected a-priori depending
on the network and algorithm intrisic properties, is still an open
question.

Comparing community structure in graphs
---------------------------------------

A large number of functions for comparing similarities and differences
between partitions of a network have been proposed in the past. They are
used to provide quantitavely a number that tells how two partitions are
similar. Usually the result is normalized in the $[0,1]$ range, being
towards $1$ for very similar clusterings and toward $0$ when mostly
dissimilar. These metrics are adopted especially in the benchmarking of
community detection methods, when the specific outcome of some algorithm
is compared with a ground truth partition, usually a-priori determined.

In this respect, we stick to the widely used “Normalized Mutual
Information” (NMI), but we want also want to focus more locally on
similarity of single communities between two assignments. It’s worth
noting that the majority of the aforementioned metrics do not take in
consideration comparison of pairs of communities between two partitions,
but they insist on finding overall similarity.
