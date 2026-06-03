---
layout: post
title: How skip connections define graphs in deep networks
description: How to extend the RYS (repeat-your-self) approach of repeating LLM layers with a centered-kernel-alignment metric and predict structural blocks to repeat
date: 2026-04-28
categories:
- science
published: false
---

## The hidden graphs behind residual connections

Let's start with your foundational definition.
In a Transformer block or ResNet, the state at layer $$l+1$$ is defined by the identity (the skip connection) plus the residual function $F_{\theta}$ (which contains the self-attention and feed-forward sub-layers, defined in a Transformer block):

$$
\mathbf{x}_{l+1} = \mathbf{x}_l + F_l(\mathbf{x}_l,\boldsymbol{\theta}_l), \qquad l = 0,1,\dots,L-1 \label{eq:recursion}\tag{1}
$$

where every symbol now has a single fixed meaning:

- $$\mathbf{x}_l \in \mathbb{R}^{d}$$ is the token-level activation at depth $$l$$ — what the mechanistic-interpretability literature calls the *residual stream* {% cite elhage2021mathematical %}. When we want to keep track of all $$N$$ tokens of a sequence at once we promote it to $$\mathbf{x}_l \in \mathbb{R}^{N\times d}$$.
- $$L$$ is the number of residual blocks; the model logits are read out from $$\mathbf{x}_L$$ via a linear unembedding head we never need to touch in this post.
- $$F_l : \mathbb{R}^d \times \Theta_l \to \mathbb{R}^d$$ is the $$l$$-th *transformer block* (LayerNorm $$\to$$ self-attention $$\to$$ LayerNorm $$\to$$ MLP, using the pre-norm convention common in modern LLMs).
Its parameters $$\boldsymbol{\theta}_l \subset \boldsymbol{\Theta}$$ are the slice of the full network weights that belong to block $$l$$ — every attention head's $$Q,K,V,O$$ matrix, every MLP gate, every LayerNorm scale and bias. We write $$F_l(\cdot,\boldsymbol{\theta}_l)$$ for the layer Transformer block.

A "vanilla" feed-forward stack without skip connections would read

$$
\mathbf{x}_{l+1} = F_l(\mathbf{x}_l,\boldsymbol{\theta}_l),
$$

forcing every bit of information to be re-encoded by every layer.
This is the regime of catastrophic representational drift that ResNets were designed to defeat.

<!-- 
### Two incoming connections per residual-stream node

It is convenient and clarifying to view the residual stream as a directed graph $$G=(V,E)$$ in which each layer state $$\mathbf{x}_{l+1}$$ has two components summed:

- an *identity edge* of constant weight $$1$$ from $$\mathbf{x}_l$$, transporting the previous state unchanged;
- a *residual edge* from $$\mathbf{x}_l$$ whose weight is the (non-linear, contractive on average, token- and direction-dependent) operator $$F_l(\cdot,\boldsymbol{\theta}_l)$$.

If we further split block $$l$$ into a residual-stream node $$\mathbf{x}_l$$ and a *function node* $$\mathbf{f}_l := F_l(\mathbf{x}_l,\boldsymbol{\theta}_l)$$, the local picture is

$$
\mathbf{x}_l \xrightarrow{F_l} \mathbf{f}_l \qquad\text{and}\qquad \mathbf{x}_l \xrightarrow{1} \mathbf{x}_{l+1} \xleftarrow{1} \mathbf{f}_l ,
$$

so that $$\mathbf{x}_{l+1}$$ is genuinely a *merge node* of two summed streams. The asymmetry between the two paths is what gives skip connections their power: the identity path is linear and norm-preserving, while the residual path is non-linear but, by training-induced regularisation {% cite marion2023implicit %}, typically much smaller in norm than the stream it perturbs. -->

### Unrolling the recursion

Telescoping the recursion \eqref{eq:recursion} from any earlier layer $$l$$ to any later layer $$l^{\prime} > l$$ gives the all-pairs identity:

$$
\mathbf{x}_{l^\prime} = \mathbf{x}_l + \sum_{k=l}^{l^\prime - 1} F_k  ( \mathbf{x}_k, \boldsymbol{\theta}_k ).
$$

The chain rule applied to the same telescoped form yields the Jacobian of the late state with respect to the early state:

$$
\mathbf{J}_{l,L'} := \frac{\partial \mathbf{x}_{L'}}{\partial \mathbf{x}_l} = \mathbf{I} + \sum_{k=l}^{L'-1} \frac{\partial F_k(\mathbf{x}_k,\boldsymbol{\theta}_k)}{\partial \mathbf{x}_l},\tag{2}\label{eq:unrolledrecursion}
$$

where each $$\partial F_k/\partial \mathbf{x}_l$$ is itself computed by composition through every intermediate state $$\mathbf{x}_l,\dots,\mathbf{x}_k$$. The leading $$\mathbf{I}$$ guarantees a *gradient highway* that bypasses every block in $$[l,L'{-}1]$$ — the classical reason gradients survive in deep ResNets and Transformers.

<!-- 
### Edge weights as the "force" of the residual stream

A purely binary adjacency $$A_{i,j}\in\{0,1\}$$ is too coarse: every residual block has *some* effect on every downstream layer, but the magnitudes vary by orders of magnitude. We promote the binary edge to a *weighted* edge that measures how strongly node $$i$$ pushes node $$j$$. Three weights are natural, each capturing a different physical intuition:

1. **Local push-forward force.** The relative norm of the residual contribution that block $$i$$ injects directly into the stream at layer $$i+1$$:

   $$
   f_i := \frac{\|F_i(\mathbf{x}_i,\boldsymbol{\theta}_i)\|}{\|\mathbf{x}_{i+1}\|}.
   $$

   Empirically, in trained Transformers $$f_i \ll 1$$ for the bulk of middle layers — this is the small-residual regime that justifies the neural-ODE limit of the next subsection {% cite marion2023implicit %}.

2. **Long-range projected weight.** The signed projection of block $$i$$'s output onto a downstream state $$\mathbf{x}_j$$:

   $$
   w_{i\to j} := \frac{\langle F_i(\mathbf{x}_i,\boldsymbol{\theta}_i),\, \mathbf{x}_j\rangle}{\|\mathbf{x}_j\|^2}.
   $$

   This is the fraction of $$\|\mathbf{x}_j\|^2$$ attributable to block $$i$$. Telescoping the unrolled recursion gives the additive decomposition

   $$
   \sum_{i=l}^{j-1} w_{i\to j} = 1 - \frac{\langle\mathbf{x}_l,\mathbf{x}_j\rangle}{\|\mathbf{x}_j\|^2},
   $$

   so the long-range weights *literally partition* the late state's energy among the residual contributions and the carried-over identity term.

3. **Differential edge weight.** The operator norm of the Jacobian block $$\kappa_{i,j} := \|\partial \mathbf{x}_j/\partial F_i\|_{\text{op}}$$, which measures how a perturbation of block $$i$$'s output propagates to layer $$j$$. For purely additive residuals $$\kappa_{i,j} \equiv 1$$, but with LayerNorm and downstream non-linearities one obtains a non-trivial decay profile.

In what follows we use $$w_{i\to j}$$ as the canonical edge weight: it is signed (so it aggregates by simple addition along the stream), dimensionless, and — crucially — it has a clean analytical relationship with the cosine similarity that we measure empirically in the next section.
-->

### Complex networks view: layers are nodes

If we model the network as a weighted directed graph $$G=(V, E)$$, the nodes $$V=(\mathbf{x}_0, \mathbf{x}_1, \ldots, \mathbf{x}_L )$$ represent the residual-stream states at each depth.
An edge $$(i,j) \in E$$ exists when $$\mathbf{x}_i$$ directly contributes to the computation of $$\mathbf{x}_j$$.

A vanilla feed-forward stack has the binarized adjacency

$$
A_{i,j} = \begin{cases} 1 & j = i+1,\\ 0 & \text{otherwise},\end{cases}
$$

i.e. a single non-zero on the first super-diagonal of the upper-triangular adjacency matrix (rows index sources, columns index targets) — the topology of a simple directed path.

In a residual network the unrolled recursion \eqref{eq:unrolledrecursion} shows that node $$i$$ has a direct functional edge to *every* subsequent node, and the binary adjacency is replaced by the dense weighted upper-triangular matrix.
We denote this matrix $$\mathbf{W}$$ having weights $$w_{ij}$$

$$
W_{i,j} = w_{i\to j}\text{for } i < j \; \qquad W_{i,j} = 0 \text{ otherwise}.
$$

This transformation between the 1-D lattice (line graph) into a **weighted feedforward directed acyclic graph (DAG)** defines the reach of information flow from every earlier layer to later layers in a single hop.
Combinatorially, an $$L$$-block residual network is therefore not a single deep pathway but an ensemble of $$2^L$$ unique source-to-sink paths interacting in parallel as at each block the signal can either take the identity edge or the residual edge, giving $$2^L$$ binary choices {% cite veit2016residual %}.

Recent work shows that this DAG structure prevents *representational rank collapse*, ensuring deep Transformers do not over-smooth data into uniform noise {% cite orhan2017skip %}.

But how do we *measure* the weights $$w_{ij}$$ in this graph?

<figure>
<img src="/static/postfigures/network-machine-neuroscience.svg" alt="network_machine_neuroscience">
<figcaption>
<strong>Figure 1: Graph topology induced by residual connections</strong> Resulting adjacency matrix
</figcaption>
</figure>

## Layer activations and their similarity matrix

In a conceptual leap between the math of skip connections and network neuroscience, and taking inspiration from **mechanistic interpretability** we can study a new kind of object that could help us shed light on the network a transformer.

We treat the Transformer as a dynamically evolving system, more precisely as a system processing information token by token, that defines a stream of activations at each layer for every appended token.
We view the layer's $$\mathbf{x}_l$$ as Regions of Interest (ROIs) whose cosine similarity (a proxy of semantic similarity between activations) gets shaped in a square **correlation matrix**, to define a functional connectivity matrix of a Transformer!

### Functional connectivity matrix of a Transformer

In fMRI, a functional connectivity matrix is built by calculating the Pearson correlation between the BOLD time-series of different brain regions.
In a Transformer, the *time-series* is the geometry of the activation spaces across a dataset of tokens, in the autoregressive generation settings.
During the autoregressive token generation process one ends up with a large tensor.
Each activation $$F_k$$ has dimension $$d$$ for every token it generates, hence on $$N$$ generated tokens and $$L$$ layers one has a three axis tensor with shape $$\mathbf{X} \in \mathbb{R}^{(L,N,d)}$$.

If we let $$\mathbf{x}_i \in \mathbb{R}^{N \times d}$$ stack the $$d$$-dimensional activation vectors of layer $$i$$ over $$N$$ tokens of a corpus, we can define the **functional connectivity** between layer $$i$$ and layer $$j$$ via cosine similarity (or, equivalently up to centring, linear CKA, which is preferred in ML for comparing high-dimensional representations {% cite davari2022reliability %}):

$$
C_{ij} = \frac{\langle \mathbf{x}_i, \mathbf{x}_j \rangle_F}{\|\mathbf{x}_i\|_F \|\mathbf{x}_j\|_F},
$$

where $$\langle \cdot, \cdot \rangle_F$$ is the Frobenius inner product since the actual dot product should work on single vectors but $$F$$ are actual matrices over multiple tokens $$N$$ and latent dimension $$d$$.

> By computing this for every $$(i,j)$$ pair, we obtain an $$L \times L$$ symmetric weighted adjacency matrix $$C$$, the *functional connectome* of the model.

Because of the skip connections that constantly inject $$x_i$$ into downstream computations, this matrix is automatically a **fully connected, weighted graph** rather than a sparse, sequentially connected chain.
We can in fact say something much stronger: the functional weight $$C_{ij}$$ has an *exact analytical form* derivable from the structural recursion.

### From skip-connection forces to cosine similarity

Let now derive the main formula for the cosine similarity that we are intested in to give shape to the task-evoked functional connectome.

We define the quantity $$\mathbf{S}_{i,j}$$ (with $$i<j$$) 

$$
\mathbf{S}_{ij} = \sum_{k=i}^{j-1} F_k(\mathbf{x}_k,\boldsymbol{\theta}_k)
$$

to be the cumulative residual *force* injected between layers $$i$$ and $$j$$, so that the unrolled recursion reads $$ \mathbf{x}_j=\mathbf{x}_{i} + \mathbf{S}_{ij} $$.
This quantity is similar to what is being measured by David Ng in his heatmaps.
Define two summary statistics that characterise this segment of the residual stream:

$$
\rho_{i,j} := \frac{\|\mathbf{S}_{i,j}\|_F}{\|\mathbf{x}_i\|_F},
\qquad
\cos\phi_{i,j} := \frac{\langle \mathbf{x}_i, \mathbf{S}_{i,j}\rangle_F}{\|\mathbf{x}_i\|_F\,\|\mathbf{S}_{i,j}\|_F},
$$

i.e. $$\rho_{i,j}$$ is the *relative force* (magnitude of accumulated residual relative to the carry-over identity) and $$\phi_{i,j}$$ is the angle between the identity stream and the accumulated residual injection. Substituting $$\mathbf{x}_j = \mathbf{x}_i + \mathbf{S}_{i,j}$$ into the cosine similarity and dividing through by $$\|\mathbf{x}_i\|_F^2$$ yields

$$
\boxed{
C_{ij} = \frac{\langle\mathbf{x}_i,\,\mathbf{x}_i+\mathbf{S}_{i,j}\rangle_F}{\|\mathbf{x}_i\|_F\,\|\mathbf{x}_i+\mathbf{S}_{i,j}\|_F} = \frac{1 + \rho_{i,j}\cos\phi_{i,j}}{\sqrt{1 + \rho_{i,j}^{\,2} + 2\rho_{i,j}\cos\phi_{i,j}}}}
$$

Two regimes are immediate from this closed form:

- **Plateau / small-force regime.**
When $$\rho_{i,j}\to 0$$, the skip connections dominate. The layer straightforwardly passes its parent information to the next layer, potentially bypassing any modification it could apply.
In this case the $$C_{ij}$$ correlation can get approximated as:

$$
C_{ij} = 1 - \tfrac{1}{2}\,\rho_{i,j}^{\,2}\sin^2\phi_{i,j} + \mathcal{O}(\rho_{i,j}^{\,3}).
$$

The cosine sits arbitrarily close to $$1$$ and depends *quadratically* on the residual force, with the angle modulating the rate.
The middle layers are not deciding much, they are letting the identity edge do the carrying, and the residual injections $$F_k$$ are small relative to $$\mathbf{x}_k$$.
This should correspond to areas of high very high correlation, plus or minus a minor perturbation.

- **Active or large-force regime.** When the relative force $$\rho_{i,j}$$ becomes comparable to or greater than 1, and the alignment $$\cos\phi_{i,j}$$ is not close to 1, the cosine similarity $$C_{ij}$$ drops rapidly. In the limit where $$\rho_{i,j}$$ becomes very large (with $$\phi_{i,j}$$ fixed), $$C_{ij}$$ approaches $$\cos\phi_{i,j}$$ meaning the network's state at layer $$j$$ loses memory of the original $$\mathbf{x}_i$$ and instead aligns with the sum of residual updates $$\mathbf{S}_{i,j}$$.

So *every* edge of the empirically measured cosine connectome is, analytically, a smooth scalar function of two summary statistics of the underlying structural recursion: the cumulative relative force $$\rho_{i,j}$$ and the residual-vs-identity alignment $$\phi_{i,j}$$.
The functional graph and the structural graph are not two independent objects but they are a single object viewed through two lenses.

## Relation to RYS framework

Ng's work on the [RYS (**R**epeat **Y**our**S**elf)](https://dnhkng.github.io/posts/rys/) {% cite ng2026rsys %} empirically proves that LLMs possess a three-phase anatomy in their layer structure: *Encoding*, *Universal Reasoning* and *Decoding* and that duplicating specific middle blocks enhances specific skills (e.g., repeating layers 24–35 boosts `MATH`, while 29–34 boosts `EQ`).

> If we treat these layers as nodes in a functional connectome, we can ask whether augmenting specific submodules by repeating their transformer blocks $$F_l$$ is mathematically responsible for the changes in downstream task performance and we can answer the question, not just pose it!

## RYS as edge augmentation in the skip-connection graph

We now have the language to formalise what Ng's *Repeat-Your-Self* construction actually does to the residual-stream graph.
The headline claim is simple: **RYS does not change any weights and does not add any nodes; it adds edges, and only inside the central reasoning block.**

The main thing that RYS does is studying what linear subset of consecutive layers can help improving downstream performance when stacked multiple times.
To do this, the author did a number of remarkable ablation studies, arriving at a striking conclusion: replicating layers in the middle is like a form

Fix two indices $$i < j \le L$$.
The standard forward pass traces the path $$0 \to 1 \to \cdots \to L$$.
The RYS-$$(i,j)$$ model traces, instead, the augmented path:

$$
0 \to 1 \to \cdots \to (j{-}1) \to j \Longrightarrow \overline{i} \to \overline{i+1} \to \cdots \to \overline{j-1} \to \overline{j} \Longrightarrow (j{+}1) \to \cdots \to L,
$$

where $$\overline{\,\cdot\,}$$ denotes the *second pass* through the same parameters $$\boldsymbol{\theta}_i,\dots,\boldsymbol{\theta}_{j-1}$$.
No new weights are allocated, only **pointers are reused**.
Let $$\mathbf{x}_l^{(0)}$$ denote first-pass activations and $$\mathbf{x}_l^{(1)}$$ second-pass activations.
The RYS recursion then reads: 

$$
\begin{aligned}
\mathbf{x}_{l+1}^{(0)} &= \mathbf{x}_l^{(0)} + F_l(\mathbf{x}_l^{(0)},\boldsymbol{\theta}_l),  & l&=0,\dots,j-1,\\[2pt]
\mathbf{x}_i^{(1)} &= \mathbf{x}_j^{(0)},\\[2pt]
\mathbf{x}_{l+1}^{(1)} &= \mathbf{x}_l^{(1)} + F_l(\mathbf{x}_l^{(1)},\boldsymbol{\theta}_l), & l&=i,\dots,j-1,\\[2pt]
\mathbf{x}_l &= \mathbf{x}_l^{(1)} + \sum_{k=j}^{l-1} F_k(\mathbf{x}_k,\boldsymbol{\theta}_k), & l&=j+1,\dots,L.
\end{aligned}
$$

Telescoping the first two passes, the input to layer $$j$$ in the RYS model is

$$
\mathbf{x}_j^{(1)} = \mathbf{x}_i + \underbrace{\sum_{k=i}^{j-1} F_k(\mathbf{x}_k^{(0)},\boldsymbol{\theta}_k)}_{\mathbf{S}^{(0)}_{i,j}} + \underbrace{\sum_{k=i}^{j-1} F_k(\mathbf{x}_k^{(1)},\boldsymbol{\theta}_k)}_{\mathbf{S}^{(1)}_{i,j}},
$$

versus the standard model's $$\mathbf{x}_j = \mathbf{x}_i + \mathbf{S}_{i,j}$$. The difference is exactly one extra copy of the cumulative residual,

$$
\mathbf{x}_j^{(1)} - \mathbf{x}_j = \mathbf{S}^{(1)}_{i,j},
$$

evaluated on the *displaced* trajectory. Linearising each $$F_k$$ around $$\mathbf{x}_k^{(0)}$$,

$$
F_k(\mathbf{x}_k^{(1)},\boldsymbol{\theta}_k) = F_k(\mathbf{x}_k^{(0)},\boldsymbol{\theta}_k) + \mathbf{J}_{F_k}\,\bigl(\mathbf{x}_k^{(1)} - \mathbf{x}_k^{(0)}\bigr) + \mathcal{O}\!\bigl(\|\Delta_k\|^2\bigr),
$$

shows that to first order in the relative force,

$$
\mathbf{S}^{(1)}_{i,j} = \mathbf{S}^{(0)}_{i,j} + \mathcal{O}\!\bigl(\rho_{i,j}\,\|\mathbf{S}^{(0)}_{i,j}\|\bigr).
$$

So **to leading order RYS doubles the cumulative residual force inside the duplicated block** while leaving the average direction of injection unchanged:

$$
\boxed{\rho_{i,j}^{\text{RYS}} \approx 2\,\rho_{i,j}, \qquad \cos\phi_{i,j}^{\text{RYS}} \approx \cos\phi_{i,j}.}
$$

### What this does to the functional cosine connectome

Plugging the doubled relative force into the closed form derived above, the RYS-induced functional edge between layers $$i$$ and $$j$$ becomes

$$
C_{ij}^{\text{RYS}} \approx \frac{1 + 2\rho_{i,j}\cos\phi_{i,j}}{\sqrt{1 + 4\rho_{i,j}\cos\phi_{i,j} + 4\rho_{i,j}^{\,2}}}.
$$

For small $$\rho_{i,j}$$ (the plateau regime, where the base model has $$C_{ij}\approx 1 - \tfrac{1}{2}\rho^2\sin^2\phi$$) the RYS perturbation is *quadrupled*:

$$
1 - C_{ij}^{\text{RYS}} \approx 4\,\bigl(1 - C_{ij}\bigr) + \mathcal{O}(\rho^3).
$$

The plateau is broken precisely in the duplicated range, whic is the block the original model spent in semantic *stasis* is now where RYS injects the most representational displacement. 
Outside the block (for any pair with $$i' < i$$ and $$j' > j$$, or both inside $$[0,i)$$, or both inside $$[j,L]$$) the recursion is unchanged and so is $$C_{i'j'}$$.

### What this does to the structural edge graph

In the structural DAG of section 1 with edges $$\{(\mathbf{x}_i,\mathbf{x}_j)\}_{i<j}$$ weighted by the long-range force $$w_{i\to j}$$, the RYS-$$(i,j)$$ surgery has a clean graph-theoretic reading:

- it *adds* $$j-i$$ new internal edges within the duplicated block (each $$\mathbf{x}_k^{(1)}$$ for $$k\in[i,j]$$ is a new node connected back to $$\mathbf{x}_k^{(0)}$$ via the parameters $$\boldsymbol{\theta}_k$$);
- it *adds* $$2^{j-i}$$ new ensemble paths from any $$\ell \le i$$ to any $$m \ge j$$ — each first-pass skip path is paired with a second-pass twin, so the Veit-style ensemble count for the reasoning block jumps from $$2^{j-i}$$ to $$2^{2(j-i)}$$ {% cite veit2016residual %};
- crucially, **no edge incident on a node outside $$[i,j]$$ is added or removed**: the encoder $$[0,i)$$ and the decoder $$[j,L]$$ inherit exactly the structural graph of the base model.

<figure>
<img src="/static/postfigures/rys_adjacency_matrix.svg" alt="rys_adjacency_matrix">
<figcaption>
<strong>Figure 4: Structural adjacency matrix expansion caused by RYS.</strong> The left panel shows the standard $$N \times N$$ upper-triangular adjacency matrix of a ResNet DAG. The right panel shows the $$(N+k) \times (N+k)$$ adjacency matrix after a block of $$k$$ layers is duplicated. Because every node in Pass 1 structurally precedes every node in Pass 2, a fully dense $$k \times k$$ bipartite block of new feedforward edges is injected into the graph (deep orange). The RYS sub-DAG becomes twice as deep but has three times as many internal structural edges, drastically increasing the multi-hop paths available for reasoning.
</figcaption>
</figure>

The benchmark improvements Ng documents — concentrated in mathematical reasoning (MATH +8.16%) and multi-step inference (MuSR +17.72%) — are then naturally read as a structural intervention that *augments only the edges incident on the central reasoning module*, leaving the syntactic encoder and the de-tokenising decoder untouched. In Ng's vocabulary, the encoder stays "in-distribution"; in our vocabulary, only the central reasoning sub-DAG has been densified. The reasoning cortex has been given a wider DAG to think in.

<figure>
<img src="/static/postfigures/rys_chain_graph.svg" alt="rys_chain_graph">
<figcaption>
<strong>Figure 3: Topology of the RYS augmentation on the skip-connection graph.</strong> The top panel shows the standard residual DAG topology, where the central reasoning module computes the cumulative residual $\mathbf{S}^{(0)}_{i,j}$$. The bottom panel illustrates the RYS augmented topology: by reusing the same parameters $$\boldsymbol{\theta}_k$$ without allocating new weights, the reasoning module loops back onto itself. This densifies the sub-DAG structurally—effectively doubling the residual force so that $$\mathbf{S}^{(1)}_{i,j} \approx \mathbf{S}^{(0)}_{i,j}$ while maintaining the integrity of the encoder and decoder boundaries. In other words the decoder is sufficiently robust to tolerate slight changes from the reasoning block even if that is not the one that the model has been pretrained specifically on.
</figcaption>
</figure>

### Why single-layer duplication tend to fail

David Ng in his [second blogpost](https://dnhkng.github.io/posts/rys/) reports that duplicating *one* middle layer almost always degrades performance, while duplicating a *block* of seven layers near the middle is what produces the leaderboard-topping `RYS-XLarge`.
The math above explains why immediately.

For a single-layer duplication $$j = i+1$$ the cumulative residual is $$\mathbf{S}_{i,i+1} = F_i(\mathbf{x}_i,\boldsymbol{\theta}_i)$$, a single non-linear injection.
Doubling it perturbs $$\rho_{i,i+1}$$ by $$\mathcal{O}(f_i)$$ and contributes essentially nothing to the long-range edges $$w_{i\to m}$$ for $$m > i+1$$.
The rest of the network was trained to expect the un-doubled distribution at layer $$i+1$$ and is pushed out of distribution by an amount that the bulk of the DAG cannot absorb.

RYS works on a *block of layers* because only a block has non-trivial diameter inside it: only then does $$\mathbf{S}_{i,j}$$ contain a *composition* of residual functions, and only then does duplicating the block double an aggregate residual flow that itself encodes a multi-step reasoning circuit.

In other words: **the unit of cognition that pre-training carved out of the layer stack is a sub-DAG, not a node**, and only a sub-DAG-level intervention augments the structural graph in a way the rest of the network can still consume.

## From mechanism to testable connectomics

The mathematical story above should be read as a mechanistic hypothesis, not yet as a proof of why RYS works.
It says that a useful RYS block should behave like a stable residual flow on a shared semantic manifold: the first traversal moves the representation in a task-relevant direction, and the second traversal applies approximately the same kind of update without throwing the downstream decoder out of distribution.
This gives several concrete measurements that can turn the story into falsifiable science.

### 1. Residual-field stationarity

The most direct prediction is that good RYS blocks should satisfy a stationarity condition.
For a duplicated block $$[i,j)$$, compare the cumulative residual from the first pass,

$$
\mathbf{S}^{(0)}_{i,j} = \sum_{k=i}^{j-1}F_k(\mathbf{x}_k^{(0)},\boldsymbol{\theta}_k),
$$

with the cumulative residual from the second pass,

$$
\mathbf{S}^{(1)}_{i,j} = \sum_{k=i}^{j-1}F_k(\mathbf{x}_k^{(1)},\boldsymbol{\theta}_k).
$$

If my interpretation is right, high-performing RYS blocks should have both

$$
\frac{\|\mathbf{S}^{(1)}_{i,j}\|_F}{\|\mathbf{S}^{(0)}_{i,j}\|_F} \approx 1,
\qquad
\frac{\langle \mathbf{S}^{(0)}_{i,j},\mathbf{S}^{(1)}_{i,j}\rangle_F}{\|\mathbf{S}^{(0)}_{i,j}\|_F\|\mathbf{S}^{(1)}_{i,j}\|_F} \approx 1.
$$

In words: the second traversal should not invent a totally new update; it should reapply a similar residual field to a nearby point on the same manifold.
Bad RYS blocks should fail this test by either shrinking, exploding, or rotating the residual update.

### 2. Distribution-mismatch at the loop junction

The dangerous point in RYS is the jump from the end of the duplicated block back to its beginning.
Layer $$i$$ was trained to consume states distributed like $$\mathbf{x}_i$$, not arbitrary future states.
So the relevant question is whether $$\mathbf{x}_j$$ still lies close to the normal input manifold of layer $$i$$.

This can be measured with a covariance-normalized distance, maximum mean discrepancy, or any other two-sample statistic between ordinary layer-$$i$$ activations and the RYS junction activations.
The prediction is simple: successful RYS windows should have low junction mismatch, while windows that cross encoder/decoder boundaries should show large mismatch.
This connects directly to Ng's language-agnostic-middle argument: middle layers can be repeated because their input and output distributions are already unusually compatible.

### 3. Jacobian stability of the duplicated block

Let the whole block map be

$$
T_{i:j}(\mathbf{x}) = \mathbf{x} + \mathbf{S}_{i,j}(\mathbf{x}).
$$

Standard inference applies $$T_{i:j}$$ once; RYS applies it twice.
The block is useful only if this second application is stable.
Empirically this suggests estimating the spectrum of the block Jacobian,

$$
\mathbf{J}_{i:j} = \frac{\partial T_{i:j}}{\partial \mathbf{x}},
$$

or cheaper Hutchinson/Lanczos approximations to its dominant singular values.
Good reasoning blocks should be neither dead identities nor chaotic expanders: they should move representations enough to refine them, but not amplify perturbations so much that the decoder receives an alien state.

### 4. Centered functional connectivity instead of raw cosine

The cosine formula derived earlier is exact for $$\mathbf{x}_j=\mathbf{x}_i+\mathbf{S}_{i,j}$$, but raw cosine can be dominated by the shared "I am at layer $$l$$" component of the residual stream.
This is why the RYS-II and Sapir-Whorf analyses become clearer after per-layer centering.
For empirical graph construction, the safer default is therefore centered cosine or linear CKA:

$$
C^{\mathrm{centered}}_{ij}
=
\frac{\langle \mathbf{x}_i-\bar{\mathbf{x}}_i,\mathbf{x}_j-\bar{\mathbf{x}}_j\rangle_F}
{\|\mathbf{x}_i-\bar{\mathbf{x}}_i\|_F\|\mathbf{x}_j-\bar{\mathbf{x}}_j\|_F}.
$$

This strips away global anisotropy and leaves the task-specific geometry that should matter for RYS.

### 5. Causal edges, not only similarity edges

The functional connectome is useful, but similarity is still a correlation.
The stronger object is a causal influence graph whose edge $$i\to j$$ measures how much perturbing or patching layer $$i$$ changes layer $$j$$ or the final answer.
Activation patching, residual-stream ablation, and blockwise replacement between base and RYS runs can all define such edge weights.

This matters because Ng's RYS matrices are not just correlation heatmaps.
They are surface-level benchmark intervention maps: each pixel corresponds to a concrete architectural surgery and an observed performance delta.
That makes them closer to causal lesion/augmentation maps than to ordinary representation-similarity matrices.

## Companion graph-theoretic analysis

The natural next step is the companion post, [Functional synthetic LLM connectome analysis]({% link sections/science/_posts/2026-04-28-Functional-synthetic-llm-connectome-analysis.md %}).
The present post derives a candidate mechanism from the residual recursion; the companion post treats the actual RYS performance matrices as empirical connectomes.
This distinction is important.
Here, edges come from activation geometry and mathematical decomposition.
There, edges come from benchmark-improving interventions: which duplicated layer windows improve MATH, EQ, MuSR, or cross-lingual reasoning.

That means the graph-theoretic quantities in the companion analysis have a different evidential status from a pure correlation graph:

- **Modularity** asks whether benchmark-improving RYS windows form coherent communities in layer space, such as a broad math community around layers 24-35 and a tighter EQ community around 29-34.
- **Betweenness centrality** asks whether encode/reason/decode boundary layers act as bridges between communities, as predicted by the Sapir-Whorf language-to-semantics transition.
- **Intra-module path length and diameter** ask whether RYS helps reasoning tasks by increasing the effective depth of the middle semantic module.
- **Edge-weight variance** asks whether stable plateaus predict confident, factual behavior, while fluctuating middle-layer connectivity predicts uncertainty or hallucination.

The strongest version of the overall hypothesis is therefore not simply that "highly correlated layers are useful to repeat."
It is that benchmark-positive RYS windows should coincide with stable residual fields, low junction distribution mismatch, centered semantic communities, and graph modules whose topology changes in task-specific ways.
If those four measurements agree, the skip-connection graph, the RYS heatmap, and the synthetic LLM connectome become three views of the same underlying object.

---

## References

{% bibliography --cited %}
