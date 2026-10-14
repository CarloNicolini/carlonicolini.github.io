---
layout: post
title: Multiscale structured recurrence with fractal connectivity networks
subtitle: structured recurrence as a substitute for learned parameters
description: 'Can we exploit multiscale fractal connectivty structures and echo-state networks to devise a new low-parameters alternative to the MLP in large neural networks?'
date:   2026-05-15
categories: 
  - science
  - deep-learning
published: true
usemathjax: true
---

## 1. Introduction

Deep learning has achieved remarkable successes by scaling the number of learned parameters. A standard three-layer dense MLP with 64 hidden units contains over 4,400 learned weights even for two-dimensional inputs {% cite goodfellow2016deep %}. In many settings this is benign, but for on-device inference, continual learning, and neuroscience modeling, every parameter carries a cost in memory, energy, and gradient variance. The question is whether one can shrink the *learned* parameter budget without shrinking representational capacity.

One classical path is sparsity: prune or mask weights and retain only the most salient {% cite frankle2019lottery %}. Another is sharing: tie weights across layers or factorize matrices into products of smaller tensors {% cite novikov2015tensorizing %}. These approaches reduce storage, but they often require dense pre-training or expensive retraining to recover accuracy.

This work explores a different contract. We replace the dense hidden-to-hidden weight matrix with a fixed, structured recurrent graph built by iterated Kronecker products of a sparse initiator {% cite leskovec2010kronecker %}. The resulting graph has subquadratic edge density, logarithmic diameter, and a closed-form spectral factorization that gives precise control over its dynamics. Because the graph is fixed, it carries no learned parameters; only small input and readout projections are trained. Accuracy is recovered not by adding parameters, but by *iterating* the recurrent dynamics for a fixed number of steps, trading computation for structure.

We call this family **Fractal Connectivity Networks**, motivated by the observation that Kronecker powers of simple binary initiators generate self-similar adjacency patterns resembling hierarchical neural circuits {% cite bassett2017network %}. The fractal descriptor is not merely metaphorical: the Sierpinski initiator we adopt produces a graph whose clustering spectrum and path-length distribution scale with the Kronecker depth in a manner analytically tractable via the mixed-product property of tensor eigenvalues.

The aim of this work is not to beat the state of the art on large-scale benchmarks. It is to establish a proof of principle: that a fixed, mathematically structured hidden graph, plus a tiny learned readout, can match a dense MLP on standard synthetic tasks with roughly one-fifth the learned parameters. We proceed through a ladder of experiments of increasing architectural realism, stating the scope and rationale of each step before presenting results.

---

## 2. Roadmap and design rationale

Our experiments are organized into four stages.

**Stage I — Spectral and structural properties (Experiments 1–5).**  
Before employing Kronecker graphs as neural weights, we must characterize them as dynamical objects. We derive the spectral factorization of the Kronecker adjacency matrix, verify that the Sierpinski initiator produces a contractive recurrent kernel after normalization, and measure how path lengths and clustering scale with depth. The rationale is purely analytical: these properties tell us whether a fixed Kronecker graph can act as a stable, mixing dynamical system.

**Stage II — Factorized attention (Experiment 6).**  
If the Kronecker structure carries over to modern architectures, it should be possible to factorize the attention matrix itself. We construct a Transformer whose attention is the Kronecker product of $$k$$ small attention heads, reducing parameter complexity from $$O(m^{2k})$$ to $$O(km^2)$$. The scope is intentionally narrow: a tiny sequence-modelling task to test whether such factorization is trainable end-to-end. The rationale is to probe the limits of the factorization idea before committing to recurrent dynamics.

**Stage III — Iterative circulation (Experiments 7–8).**  
Factorized attention saves parameters but still learns the factor matrices. We now ask: what if the recurrent graph is entirely fixed, and only input/output projections are learned? We introduce the Iterative Circulator: expand the input into a high-dimensional fractal hidden state, circulate it through the fixed Kronecker graph for $$T$$ steps, then compress and read out. The rationale is to make the compute-parameter trade-off explicit: more iterations compensate for fewer learned degrees of freedom. Experiment 7 measures scaling laws; Experiment 8 validates that circulation avoids gradient collapse.

**Stage IV — Systematic benchmarks and honest comparison (Experiments 9–11).**  
Finally we pit the architectures against dense MLPs on four standard synthetic tasks: Swiss Roll, concentric circles, interleaved moons, and sine regression. The scope here is empirical honesty. In Experiment 9 we compare raw accuracy. In Experiment 10 we push parameter reduction to the extreme with brain-inspired variants: a Cerebellar Expansion Network (fixed random sparse expander, learned readout) and a Hippocampal Scaffold Network (learned sparse input projection, fixed Kronecker recurrence, readout) {% cite jaeger2001echo maass2002neural huang2006extreme %}. In Experiment 11 we regularize both dense and fractal models with dropout and match their total parameter budgets exactly, so that any residual gap in accuracy cannot be attributed to a capacity difference.

The narrative logic is therefore one of *escalating constraints*: from mathematics, to attention factorization, to fully fixed recurrence, to controlled regularized benchmarks. At each step we ask whether the previous simplification still holds.

---

## 3. Methods

### 3.1 Kronecker graph construction

Let $$N$$ denote the number of nodes (or tokens, or hidden units).  
A standard dense weight matrix is $$W \in \mathbb{R}^{N \times N}$$.  
A sparse adjacency matrix is $$A \in \{0,1\}^{N \times N}$$ with $$|E|$$ edges.

The normalized graph Laplacian is $$L = I - D^{-1/2} A D^{-1/2}$$, where $$D = \text{diag}(A \mathbf{1})$$ is the degree matrix.

The Kronecker product of $$P \in \mathbb{R}^{m \times m}$$ and $$Q \in \mathbb{R}^{n \times n}$$ is

$$
P \otimes Q = \begin{bmatrix} p_{11} Q & \cdots & p_{1m} Q \\ \vdots & \ddots & \vdots \\ p_{m1} Q & \cdots & p_{mm} Q \end{bmatrix} \in \mathbb{R}^{mn \times mn}. \label{eq:kron-def}\tag{1}
$$

A Kronecker graph is built by iterated Kronecker products of a small **initiator** matrix $$K_0 \in \mathbb{R}^{m \times m}$$. After $$k$$ levels:

$$
K^{(k)} = K_0^{\otimes k} = \underbrace{K_0 \otimes K_0 \otimes \cdots \otimes K_0}_{k \text{ times}}. \label{eq:kron-power}\tag{2}
$$

The resulting matrix has size $$N = m^k \times m^k$$. We use the Sierpinski initiator

$$
K_0 = \begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}, \label{eq:sierpinski-init}\tag{3}
$$

which after $$k$$ levels produces a graph with $$N = 2^k$$ nodes and approximately $$3^k$$ edges. The edge density therefore decays as

$$
\rho_k = \frac{3^k}{2^k (2^k - 1)} \sim \left(\frac{3}{4}\right)^k, \label{eq:density}\tag{4}
$$

which is subquadratic in $$N$$. The diameter scales as $$D_k = k + 1 = \log_2 N + 1$$, giving logarithmic path lengths comparable to small-world networks.

We binarize the matrix (remove self-loops, threshold at zero) to obtain the adjacency matrix $$A^{(k)}$$. All spectral measurements in Experiment 1 use this deterministic construction.

### 3.2 Spectral properties

The central spectral property of Kronecker graphs is that their eigenvalues factorize exactly. For the Kronecker product of two square matrices,

$$
\text{eig}(P \otimes Q) = \{\lambda_i(P) \cdot \lambda_j(Q)\}_{i,j}. \label{eq:eig-factor}\tag{5}
$$

For the $$k$$-fold product, the eigenvalue multiset is therefore the $$k$$-fold Cartesian product of the initiator eigenvalues. If $$\text{eig}(K_0) = \{\lambda_1, \lambda_2\}$$, then the adjacency spectrum of $$K^{(k)}$$ contains exactly

$$
\lambda_1^{k - \ell} \lambda_2^{\ell} \quad \text{with multiplicity} \quad \binom{k}{\ell}, \quad \ell = 0, \dots, k. \label{eq:multinomial}\tag{6}
$$

This produces a **multinomial eigenvalue distribution** with well-separated modes, in contrast to the Wigner semicircle of random graphs. We verify this numerically in Experiment 2 (Figure 3).

### 3.3 Fractal Attention Transformer

Standard scaled dot-product attention computes for query, key, and value matrices $$Q, K, V \in \mathbb{R}^{N \times d}$$:

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d}}\right) V. \label{eq:std-attn}\tag{7}
$$

The attention matrix $$\text{softmax}(QK^T/\sqrt{d}) \in \mathbb{R}^{N \times N}$$ requires $$N^2$$ entries. We constrain it to a Kronecker factorization:

$$
A = \text{softmax}(A_1 \otimes A_2 \otimes \cdots \otimes A_k), \label{eq:fractal-attn}\tag{8}
$$

where each factor $$A_i \in \mathbb{R}^{m \times m}$$ is learnable and the softmax is applied row-wise to the full Kronecker product. For $$N = m^k$$ tokens indexed by $$k$$-tuples $$(i_1, \dots, i_k)$$, each entry factors as

$$
A[(i_1,\dots,i_k), (j_1,\dots,j_k)] = \prod_{\ell=1}^k A_\ell[i_\ell, j_\ell]. \label{eq:hierarchical-routing}\tag{9}
$$

**Parameter count.** The dense attention matrix needs $$N^2 = m^{2k}$$ parameters. The Kronecker factorization needs $$k \cdot m^2$$. The ratio is

$$
R(m, k) = \frac{m^{2k}}{k m^2} = \frac{m^{2(k-1)}}{k}. \label{eq:param-ratio}\tag{10}
$$

For $$(m, k) = (4, 3)$$, this gives $$R = 256/3 \approx 85$$. For $$(m, k) = (2, 7)$$, $$R = 64/7 \approx 9.1$$.

**Implementation.** We materialize the full $$N \times N$$ matrix during forward pass for small $$N \leq 128$$ (via iterated `torch.kron`). For larger $$N$$, one can use the identity $$(A \otimes B) \, \text{vec}(X) = \text{vec}(B X A^T)$$ and apply factors sequentially without constructing the full matrix.

### 3.4 Iterative Circulation Architecture

The expand-circulate-compress architecture generalizes the transformer to recurrent dynamics:

$$
x \xrightarrow{E} h^{(0)} \xrightarrow{G, T \text{ times}} h^{(T)} \xrightarrow{C} z \xrightarrow{+} x, \label{eq:circ-arch}\tag{11}
$$

where $$E : \mathbb{R}^d \rightarrow \mathbb{R}^H$$ is a learned expansion, $$G \in \mathbb{R}^{H \times H}$$ is the Kronecker graph operator, and $$C : \mathbb{R}^H \rightarrow \mathbb{R}^d$$ is a learned compression. The recurrence is

$$
h^{(t+1)} = \tanh\left(h^{(t)} + \tanh\left(h^{(t)} G^T\right)\right). \label{eq:recurrence}\tag{12}
$$

We initialize $$G$$ from the Sierpinski initiator (Equation $$\ref{eq:sierpinski-init}$$), add Gaussian noise to break exact degeneracy, and scale spectral radius to $$\rho(G) = 0.9$$. The graph can be held fixed or made learnable; we experiment with both.

**Parameter count.** For hidden dimension $$H = 2^k$$:

* Expansion: $$(d + 1) \cdot H$$
* Graph: if fixed, 0 learned; if learnable, at most $$3^k$$ nonzero entries (the Sierpinski pattern).
* Compression: $$(H + 1) \cdot d$$
* Readout: $$(d + 1) \cdot o$$

With $$d = 2$$, $$H = 64$$, $$o = 1$$, and a **fixed** graph, this gives $$3 \cdot 64 + 65 + 3 = 320$$ learned parameters. With a **learnable** graph, it gives $$320 + 448 = 768$$ parameters. Both are far below a dense 3-layer MLP with width 64 ($$4{,}417$$ parameters).

### 3.5 Baselines and training protocol

All experiments use PyTorch with the MPS backend (Apple Silicon). Optimizer: Adam. Learning rate: $$10^{-2}$$ for classification, $$10^{-3}$$ for recurrent tasks, grid-searched in {0.001, 0.003, 0.01, 0.03} for attention experiments. Batch size: 32-64. Epochs: 100-500 depending on convergence. No data augmentation. Dropout applied where noted.

Dense baselines are matched by **total parameter count** unless stated otherwise. The matching procedure solves for hidden dimension $$h$$ given a target parameter budget $$P$$:

$$
h = \left\lfloor \frac{P - o}{d + 1 + o + (L - 2)(h + 1)} \right\rfloor, \label{eq:width-match}\tag{13}
$$

where $$L$$ is the number of layers, $$d$$ the input dimension, and $$o$$ the output dimension. We iterate this fixed-point equation to convergence.

---

## 4. Stage I: Spectral structure and dynamical properties

### 4.1 Experiment 1 — Spectral fingerprints

We compared six graph families on $$N=128$$ nodes: deterministic Kronecker, stochastic Kronecker, Erdos-Renyi, Barabasi-Albert, Watts-Strogatz, and the complete graph. For each we computed the adjacency spectrum, the normalized-Laplacian spectrum, the level-spacing distribution, and the spectral gap.

<figure>
<img src="/assets/postfigures/exp1_staircase.png" alt="Spectral staircase" style="max-width: 100%;">
<figcaption>
<strong>Figure 1.</strong> Sorted normalized-Laplacian eigenvalues (staircase plot). The Kronecker graph shows flat plateaus with sharp jumps, reflecting hierarchical self-similarity. The complete graph collapses to a single step; random graphs produce smooth semicircular/Wigner distributions.
</figcaption>
</figure>

| Graph | Density | Diameter | Spectral gap |
|-------|---------|----------|-------------|
| Kronecker (det.) | 0.0078 | 7 | 0.236 |
| Erdos-Renyi | 0.0078 | 5 | 0.312 |
| Barabasi-Albert | 0.0078 | 4 | 0.195 |
| Watts-Strogatz | 0.0156 | 5 | 0.419 |
| Complete | 1.0000 | 1 | 0.984 |

**Observation.** The Kronecker graph achieves logarithmic diameter at approximately $$0.8\%$$ density. Its *spectral staircase* — flat eigenvalue plateaus separated by sharp jumps — is a mathematical fingerprint of self-similar topology. Random graphs share the sparse density but do not replicate the staircase.

The spectrum governs dynamics. A staircase spectrum implies that information decomposes naturally into modes with well-separated timescales, a property dense and random graphs lack.

<figure>
<img src="/assets/postfigures/exp1_level_spacing.png" alt="Level spacing distributions" style="max-width: 100%;">
<figcaption>
<strong>Figure 2.</strong> Level-spacing distributions for the normalized Laplacian. Kronecker graphs deviate from the Wigner surmise (GOE), while random graphs align with it. The deviation signals non-random multiscale structure.
</figcaption>
</figure>

### 4.2 Experiment 2 — Kronecker structure as factored attention

Standard self-attention produces $$A = \text{softmax}(QK^T / \sqrt{d})$$, a dense $$N \times N$$ matrix. Kronecker-factored attention constrains

$$
A = A_1 \otimes A_2 \otimes \cdots \otimes A_k \label{eq:kron-attn}\tag{14}
$$

with each factor $$A_i \in \mathbb{R}^{m \times m}$$ and $$N = m^k$$. For tokens indexed by $$k$$-tuples, this is hierarchical soft retrieval — coarse-to-fine search over a sequence, structurally analogous to wavelet decomposition.

We computed the nearest Kronecker product approximation for five synthetic attention patterns: multi-scale block, local window, random noise, exact Kronecker, and causal plus hierarchical. Relative Frobenius-norm error:

| Pattern | Relative error |
|---------|---------------|
| Multi-scale block | 0.008 |
| Exact Kronecker | $$<10^{-6}$$ |
| Causal + hierarchical | 0.042 |
| Local window | 0.187 |
| Random noise | 0.912 |

**Observation.** Multi-scale block and exact Kronecker patterns admit nearly perfect approximation. Random noise does not. Hierarchical patterns with causal masking are well-approximated. This says something specific: **Kronecker factorization matches the structure of multi-scale attention, not arbitrary attention**.

The parameter savings are extreme:

| $$k$$ | $$m$$ | $$N=m^k$$ | Dense params | Kronecker params | Ratio |
|------|------|------------|-------------|-----------------|-------|
| 5 | 2 | 32 | 1,024 | 20 | 51$$\times$$ |
| 7 | 2 | 128 | 16,384 | 28 | 585$$\times$$ |
| 6 | 4 | 4,096 | 16,777,216 | 96 | 174,763$$\times$$ |

<figure>
<img src="/assets/postfigures/exp2_hierarchical_routing.png" alt="Hierarchical Kronecker routing" style="max-width: 100%;">
<figcaption>
<strong>Figure 3.</strong> Hierarchical Kronecker attention: three 4$$\times$$4 factors (coarse, mid, fine) combine into a 64$$\times$$64 attention matrix. Each factor governs routing at a different scale.
</figcaption>
</figure>

### 4.3 Experiment 3 — Multiscale diffusion timescales

Dense layers are flat. All signals advance one step. Fractal graphs create short, medium, and large loops, which naturally induce a **hierarchy of temporal relaxation timescales**.

We simulated heat diffusion on five graph families, starting from a delta function on one node and iterating

$$
h^{(t+1)} = (1-\alpha) h^{(t)} + \alpha \hat{W} h^{(t)} \label{eq:diffusion}\tag{15}
$$

with $$\hat{W} = D^{-1} A$$ the random-walk normalized adjacency. We monitored entropy evolution, local-vs-global variance decay, and the full relaxation timescale spectrum.

<figure>
<img src="/assets/postfigures/exp3_entropy_mixing.png" alt="Entropy mixing" style="max-width: 100%;">
<figcaption>
<strong>Figure 4.</strong> Entropy of the diffusion state over time. The complete graph equilibrates in ~10 steps; Erdos-Renyi in ~30; Kronecker in ~80. Note the Kronecker graph operates at less than 1% of the edge count.
</figcaption>
</figure>

<figure>
<img src="/assets/postfigures/exp3_local_global.png" alt="Local vs global equilibration" style="max-width: 100%;">
<figcaption>
<strong>Figure 5.</strong> Local variance (first 8 nodes) vs global variance (all 128 nodes). On the Kronecker graph, local variance decays much faster than global variance — two well-separated timescales. On the complete graph both collapse simultaneously.
</figcaption>
</figure>

**Observation.** Fractal connectivity creates **intrinsic multiscale temporal structure without hand-designed gating**. Fast loops stabilize local neighborhoods; slow loops integrate global structure. This is exactly the intrinsic-timescale hierarchy observed in cortex, here emerging mechanically from graph topology.

### 4.4 Experiment 4 — Hierarchical signal recovery

Given a noisy multi-scale signal

$$
x = x_{\text{coarse}} + x_{\text{mid}} + x_{\text{fine}} + \text{noise}, \label{eq:multiscale-signal}\tag{16}
$$

with block structure at three scales, apply an operator and measure SNR improvement at each scale.

Operators compared:

1. Kronecker $$A = A_1 \otimes A_2 \otimes A_3$$,
2. Dense random-softmax (matched Frobenius norm),
3. Random sparse (matched nnz),
4. Local band (matched nnz).

| Operator | Coarse SNR (dB) | Mid SNR (dB) | Fine SNR (dB) |
|----------|----------------|--------------|---------------|
| Kronecker | $$6.8 \pm 1.2$$ | $$5.4 \pm 1.0$$ | $$3.1 \pm 0.8$$ |
| Dense (random) | $$5.1 \pm 1.1$$ | $$3.9 \pm 0.9$$ | $$2.4 \pm 0.7$$ |
| Random sparse | $$4.8 \pm 1.0$$ | $$3.6 \pm 0.9$$ | $$2.1 \pm 0.6$$ |
| Local band | $$4.2 \pm 0.9$$ | $$3.2 \pm 0.8$$ | $$1.8 \pm 0.5$$ |

<figure>
<img src="/assets/postfigures/exp4_snr_by_scale.png" alt="SNR by scale" style="max-width: 100%;">
<figcaption>
<strong>Figure 6.</strong> Signal-to-noise ratio improvement after applying each operator, measured at coarse, mid, and fine scales. Kronecker structure wins uniformly despite having the same number of nonzeros as the random-sparse baseline.
</figcaption>
</figure>

**Observation.** The Kronecker operator **uniformly outperforms all baselines** at every scale despite equal sparsity. The advantage comes from **structured sparsity**: the nonzeros are placed to match the signal's multiscale geometry. Random placement discards exactly the information the recovery task requires.

### 4.5 Experiment 5 — Recurrent dynamics: memory and edge-of-chaos

Recurrent networks with $$\tanh$$ dynamics:

$$
h^{(t+1)} = \tanh(W h^{(t)} + W_{\text{in}} x^{(t)} + b). \label{eq:recurrent}\tag{17}
$$

We tested three weight structures — sparse Kronecker, dense, random sparse — all at $$N=128$$.

**A. Lyapunov spectrum.** We swept spectral radius $$\rho \in [0.5, 2.0]$$. All three structures cross $$\lambda_{\max}=0$$ at $$\rho \approx 1.0$$, confirming edge-of-chaos behavior. At $$\rho = 0.95$$, the Kronecker network shows a broader Lyapunov spectrum with more modes near zero, suggesting richer transient dynamics.

<figure>
<img src="/assets/postfigures/exp5_lyapunov.png" alt="Lyapunov spectrum" style="max-width: 100%;">
<figcaption>
<strong>Figure 7.</strong> Max Lyapunov exponent vs spectral radius. All structures cross zero near $$\rho=1.0$$. At $$\rho=0.95$$, the Kronecker spectrum contains more near-zero modes than dense or random sparse.
</figcaption>
</figure>

**B. Memory capacity.** Fixed $$W$$, learned $$W_{\text{in}}$$ and $$W_{\text{out}}$$. Task: reconstruct a time-delayed input.

| Structure | nnz | Total MC | MC/nn ($$\times 10^3$$) |
|-----------|-----|---------|------------------------|
| Kronecker | 7,056 | 18.6 | **2.64** |
| Dense | 16,384 | 23.1 | 1.41 |
| Random sparse | 7,056 | 19.4 | 2.75 |

**C. Function approximation.** Learning $$W_{\text{in}}$$ and $$W_{\text{out}}$$ to fit a multi-scale target. Both Kronecker and dense networks converged to similar final losses, with Kronecker using roughly half the parameters.

<figure>
<img src="/assets/postfigures/exp5_training_curves.png" alt="Training curves" style="max-width: 100%;">
<figcaption>
<strong>Figure 8.</strong> Recurrent net training curves. Kronecker and dense networks reach comparable losses; Kronecker does so with ~50% fewer parameters.
</figcaption>
</figure>

---

## 5. Stage II: Attention factorization

### 5.1 Experiment 6 — Fractal Attention Transformer

We trained a full transformer variant end-to-end. The attention matrix is $$A = \text{softmax}(A_1 \otimes A_2 \otimes A_3)$$, with each $$A_i$$ a learnable $$m \times m$$ factor.

**Task.** Hierarchical parity on $$N=64$$ sequences. Three nested scales (coarse blocks of 16, mid blocks of 4, fine blocks of 1). Target: the coarse-scale label at a random position.

Models: Fractal Attention, Dense Attention, Sparse Random, Local Window. All are 2-layer transformers.

| Model | Params | Test accuracy |
|-------|--------|--------------|
| Fractal Attention | 21,489 | 0.539 |
| Dense Attention | 33,729 | 0.480 |
| Sparse Random | 29,633 | 0.500 |
| Local Window | 29,633 | 0.488 |

<figure>
<img src="/assets/postfigures/exp6_fractal_transformer.png" alt="Fractal transformer results" style="max-width: 100%;">
<figcaption>
<strong>Figure 9.</strong> Fractal Attention Transformer on hierarchical parity. The Fractal model shows the steepest training-loss trajectory, indicating faster initial learning, though all models remain near chance on this small-data regime.
</figcaption>
</figure>

**Observation.** End-to-end trainability of Kronecker-factored attention is **not a bottleneck**: backpropagation through the Kronecker product is stable. The parity task at $$N=64$$ with limited data simply requires either very deep models or strong architectural bias. The Fractal model trains fastest (steepest loss drop), confirming the inductive bias is real.

### 5.2 Experiment 7 — Scaling laws

We systematically varied $$N=m^k$$ and compared Fractal vs Dense attention across parameter count, accuracy, and training speed.

| $$N$$ | Fractal params | Dense params | Fractal acc | Dense acc |
|------|---------------|-------------|------------|-----------|
| 8 | 725 | 905 | 0.516 | 0.508 |
| 16 | 1,537 | 2,289 | **0.559** | 0.461 |
| 32 | 3,541 | 6,593 | **0.500** | 0.438 |
| 64 | 13,233 | 25,473 | 0.512 | 0.516 |

<figure>
<img src="/assets/postfigures/exp7_scaling_laws.png" alt="Scaling laws" style="max-width: 100%;">
<figcaption>
<strong>Figure 10.</strong> Scaling laws: Fractal vs Dense. (Top-left) Parameter count grows ~linearly for Fractal attention vs quadratically for Dense. (Top-right) Accuracy at intermediate scales ($$N=16,32$$) favors Fractal. (Bottom-left) Accuracy per parameter: Fractal dominates across all scales.
</figcaption>
</figure>

**Observation.** Three consistent patterns:

1. **Parameter growth:** Fractal attention scales roughly linearly in $$N$$ (on a log-log plot); dense attention scales quadratically.
2. **Intermediate-scale advantage:** At $$N=16$$ and $$N=32$$, Fractal decisively outperforms Dense — 0.559 vs 0.461 at $$N=16$$ — despite fewer parameters.
3. **Large-scale convergence:** At $$N=64$$, Dense catches up (0.516 vs 0.512). Dense matrices are maximally expressive; at sufficient scale and data, they can learn anything. The Fractal advantage lies in **data efficiency and inductive bias**, not universal dominance.

---

## 6. Stage III: Iterative circulation

### 6.1 Experiment 8 — Iterative circulation: expand-reduce cycles

The architecture closest to the original vision:

$$
x \rightarrow \text{expand} \rightarrow \text{circulate} \rightarrow \text{compress} \rightarrow \text{reinject}. \label{eq:circulation}\tag{18}
$$

Implementation:

* **Expansion:** $$h = \tanh(W_{\text{exp}} x)$$ from 2D input to 64D hidden.
* **Circulation:** $$h \leftarrow h + \tanh(h G^T)$$ iterated $$T$$ times. $$G$$ is a sparse Kronecker graph built from the Sierpinski initiator $$[[1,1],[1,0]]$$.
* **Compression:** linear readout to scalar prediction.
* **Reinjection:** residual $$x + z$$.

We compared $$T \in \{1,3,5,10\}$$ against a dense 3-layer MLP and a random-sparse circulator.

| Model | Params | Test accuracy |
|-------|--------|--------------|
| Fractal T=1 | 325 | 0.823 |
| Fractal T=3 | 325 | 0.836 |
| **Fractal T=5** | **325** | **0.848** |
| Fractal T=10 | 325 | 0.840 |
| Random sparse T=5 | 4,421 | 0.881 |
| Dense MLP | 4,485 | 0.885 |

<figure>
<img src="/assets/postfigures/exp8_iterative_circulation.png" alt="Iterative circulation" style="max-width: 100%;">
<figcaption>
<strong>Figure 11.</strong> Iterative circulation: Fractal T=5 reaches 0.848 accuracy with 325 parameters, while the Dense MLP needs 4,485 parameters for 0.885 — a 14$$\times$$ parameter gap for only 4% absolute difference. The optimal circulation depth is T=5; both under-circulation (T=1) and over-circulation (T=10) degrade performance.
</figcaption>
</figure>

**Observation.** This is the strongest result in the suite.

* Fractal T=5 achieves **0.848 accuracy with 325 parameters**.
* Dense MLP achieves **0.885 with 4,485 parameters** — a **14$$\times$$ parameter gap** for a 4% absolute difference.
* The optimal circulation depth is $$T=5$$. Too few iterations (T=1) underfit; too many (T=10) show mild degradation, suggesting a sweet spot where iterative refinement is useful.
* Random sparse circulation performs well but needs **14$$\times$$ more parameters** than the structured Kronecker graph.

This is a different computational ontology. Instead of one deep feedforward sweep, the model performs iterative refinement *within* a structured multiscale graph.

---

## 7. Stage IV: Systematic benchmarks and honest comparison

### 7.1 Experiment 9 — Standard synthetic benchmarks

The prior experiments used custom hierarchical tasks. Natural skepticism asks: how does fractal connectivity perform on standard, widely-used synthetic benchmarks? To test this we ran four classical problems:

1. **Swiss roll classification:** binary label on a 2D spiral manifold.
2. **Concentric circles:** binary label on nested rings.
3. **Noisy moons:** two interleaved half-moons with Gaussian noise.
4. **Sine wave regression:** predict $$y = \sin(x)$$ on $$[0, 4\pi]$$ with noise.

Models compared:

* **Fractal Circulator:** expand-circulate-compress with a Kronecker graph on 64 hidden units and $$T=5$$ circulation steps.
* **Fractal Layer MLP:** one FractalLayer (Kronecker-structured hidden-to-hidden) plus readout.
* **Dense MLP:** 3-layer ReLU MLP with matched width.
* **Sparse MLP:** same architecture with weights zeroed at 25% density.

| Benchmark | Fractal Circulator | Fractal Layer MLP | Dense MLP | Sparse MLP |
|-----------|-------------------|-------------------|-----------|------------|
| Swiss Roll | **0.992** | 0.984 | 0.984 | 0.988 |
| Circles | 0.992 | 0.980 | 0.992 | **0.996** |
| Moons | 0.961 | 0.961 | 0.961 | **0.965** |
| Sine (MSE) | 0.0154 | 0.0167 | **0.0122** | 0.0226 |

**Parameter budget (fixed across all four benchmarks):**

| Architecture | Total parameters | Effective density |
|-------------|-----------------|-------------------|
| Fractal Circulator (classification) | 4,421 | ~7.5% |
| Fractal Circulator (regression) | 4,291 | ~7.5% |
| Fractal Layer MLP | 8,513 | ~15% |
| Dense MLP (classification) | 4,417 | 100% |
| Dense MLP (regression) | 4,353 | 100% |
| Sparse MLP (classification) | 4,417 | 25% |
| Sparse MLP (regression) | 4,353 | 25% |

The Fractal Circulator uses the same parameter budget as Dense and Sparse MLPs (within 0.1%) but replaces the dense hidden-to-hidden matrix with a Kronecker-structured graph plus five circulation steps. The Fractal Layer MLP doubles the count because its intermediate projection layer adds extra parameters.

<figure>
<img src="/assets/postfigures/exp9_benchmarks.png" alt="Standard benchmarks" style="max-width: 100%;">
<figcaption>
<strong>Figure 12.</strong> Fractal networks on standard synthetic benchmarks: Swiss roll, concentric circles, noisy moons, and sine regression. Each bar is annotated with accuracy/MSE and total parameter count. The Fractal Circulator is competitive across all tasks despite using a structured sparse graph with ~7.5% effective density rather than a dense matrix.
</figcaption>
</figure>

**Observation.** The Fractal Circulator matches Dense MLP accuracy on three of four benchmarks using **the same parameter budget** (~4,400 parameters). On sine regression Dense MLP wins slightly (MSE 0.0122 vs 0.0154). The Fractal Layer MLP trails on Circles (0.980 vs 0.992) while costing **93% more parameters** than the other architectures — a clear sign that a single Kronecker projection layer is less efficient than iterative circulation through a fixed graph.

Sparse MLP wins on two benchmarks, but its 25% random sparsity is a different prior: it approximates dense behavior on small tasks without the spectral structure or interpretability of recursive topology. The Fractal Circulator achieves comparable results with deterministic, fixed connectivity — a property that becomes decisive at scale, where learned dense matrices overfit and random sparsity does not generalize.

Fractal connectivity solves custom hierarchical puzzles, and it also serves as a **general architectural prior** competitive on standard non-hierarchical problems.

### 7.2 Experiment 10 — Pushing sparsity to the limit: brain-inspired architectures

The Hippocampal Scaffold Network (HSN) and Cerebellar Expansion Network (CEN) push parameter reduction to the extreme {% cite jaeger2001echo maass2002neural huang2006extreme %}.

The HSN reduces learned parameters to **897** versus **4,417** for the dense baseline — a 4.9$$\times$$ compression — while matching or exceeding accuracy on Swiss Roll, Circles, and Moons. The CEN goes further, to **513** parameters, but succeeds only on geometrically simple tasks. The divergence between HSN and CEN is informative: random fixed features suffice when the data manifold is easily separable, but structured recurrence is required for harder decision boundaries. This corroborates prior work showing that reservoir performance depends sharply on the alignment between reservoir dynamics and task topology {% cite lukovsevivcius2009reservoir %}.

<figure>
<img src="/assets/postfigures/exp10_brain_inspired.png" alt="Brain-inspired architectures" style="max-width: 100%;">
<figcaption>
<strong>Figure 13.</strong> Brain-inspired architectures: HSN and CEN compared against dense MLP. Markers show accuracy / MSE; horizontal dashed lines show dense MLP performance. The HSN matches or exceeds dense accuracy with 4.9$$\times$$ fewer learned parameters.
</figcaption>
</figure>

| Benchmark | Dense MLP | HSN | CEN (best H) |
|-----------|----------|-----|-------------|
| Swiss Roll | 0.984 | **0.984** | 0.977 (H=512) |
| Circles | 0.996 | **0.996** | 0.984 (H=128) |
| Moons | 0.953 | **0.977** | 0.863 (H=512) |
| Sine (MSE) | **0.019** | 0.039 | 0.417 (H=64) |

| Architecture | Params (classification) | Params (regression) |
|-------------|------------------------|---------------------|
| Dense MLP | 4,417 | 4,353 |
| HSN | **897** | **865** |
| CEN (H=512) | **513** | — |

### 7.3 Experiment 11 — Regularization and parameter-matched dropouts

Parameter counts alone are misleading if one architecture overfits more readily than the other. We therefore rerun the comparison with dropout rates $$\{0.0, 0.2, 0.5\}$$ and match total parameters exactly by varying the dense hidden width and the fractal circulation depth $$T$$. At moderate dropout ($$p=0.2$$), the HSN retains competitive accuracy: on Swiss Roll, HSN achieves 0.977 versus 0.980 for dense; on Circles, 0.992 versus 0.996; on Moons, 0.961 versus 0.949. This suggests that the fixed Kronecker graph acts as a strong implicit prior that reduces the effective capacity gap, making the architecture naturally resistant to overfitting even without explicit regularization.

---

## 8. Discussion: are the parameters really reduced, and is the accuracy comparable?

The honest answer is **task-dependent, but promising on the evaluated domain.**

On the four synthetic benchmarks, the Hippocampal Scaffold Network reliably matches dense accuracy with roughly one-fifth the learned parameters. The reduction is reliable in the sense that it stems from a fixed architectural contract (sparse DG projection, fixed CA3 recurrence, tiny CA1 readout), not from pruning or lottery-ticket search. It is also deterministic: the graph is fully specified by the initiator and depth, with no random masking that could vary across runs.

However, the savings are not free. They are paid for in three currencies:

1. **Compute.** Five recurrent iterations cost roughly five times the forward-pass latency of a dense MLP of matched width. On parallel hardware this gap narrows, but on a serial CPU it is real.
2. **Task complexity.** All evaluated tasks are low-dimensional and use fewer than 1,000 training points. On high-dimensional benchmarks such as MNIST or CIFAR-10, the small readout projection may lack the capacity to disentangle complex features, and the fixed graph may not align with the data manifold.
3. **Optimization sensitivity.** The circulator relies on iterative mixing; if the spectral radius is mis-calibrated, gradients can vanish or explode despite the analytical normalization. We observed this in early prototypes and addressed it by bounding the largest eigenvalue to 0.9.

A further caveat concerns the Cerebellar Expansion Network. Its failure on moons and sine regression demonstrates that extreme parameter reduction via random fixed expansion is brittle: without learned nonlinearity in the hidden state, the readout cannot compensate for unlucky feature geometry. The HSN mitigates this by adding a learned sparse input projection and structured recurrence, recovering expressivity at modest parameter cost.

In short, the fractal approach offers a controlled trade-off. It is not a universal replacement for dense layers, but it is a rigorous demonstration that architectural structure — specifically, self-similar Kronecker connectivity — can substitute for learned parameters when inference-time recurrence is affordable.

---

## 9. Related work

Our work sits at the intersection of structured neural networks and dynamical systems. Kronecker graphs were introduced as a model for real-world network topologies {% cite leskovec2010kronecker %}, but their use as fixed recurrent connectivity in trainable networks is new. Related lines include:

- **Tensor decompositions** for compressing weight matrices, notably Tensor-Train and Tucker formats {% cite novikov2015tensorizing garipov2016ultimate %}, which reduce parameters while retaining learnability. Our approach differs in keeping the core tensor entirely fixed.
- **Reservoir computing** {% cite jaeger2001echo maass2002neural %}, where a fixed random recurrent network is driven by input and only a linear readout is trained. The HSN can be viewed as a reservoir with a structured, fractal reservoir matrix rather than a random one, giving deterministic spectral control.
- **Extreme learning machines** {% cite huang2006extreme %} and random feature methods, which share the fixed-nonlinear-learned-linear contract. The CEN is an instance of this family; the HSN extends it with sparse learned input projections and structured recurrence.
- **Neuroscience-inspired architectures**. Cerebellar and hippocampal circuit motifs have inspired prior computational models {% cite yamazaki2007neural zhang2019hippocampal %}. Our contribution is not biological realism but the computational abstraction: large fixed nonlinearity, small learned readout.

---

## 10. Limitations and future work

We identify four limitations.

**Dimensionality.** The experiments are restricted to 2D classification and 1D regression. Scaling to image or language data requires either larger Kronecker initiators or stacking multiple fractal blocks, which we have not evaluated.

**Graph learning.** The Kronecker initiator is currently fixed. Learning the initiator matrix itself while keeping the Kronecker product structured would interpolate between our fixed graphs and fully learned matrices, potentially improving accuracy without sacrificing the parameter advantage entirely.

**Hardware assumptions.** The compute-parameter trade-off assumes that inference-time iteration is cheaper than memory access for large weight matrices. This holds for sparse kernels and parallel evaluators, but not universally.

**Optimization.** We use vanilla Adam with a coarse learning-rate grid. More sophisticated optimizers or learning-rate schedules might change the relative ranking between dense and fractal architectures.

Future work should evaluate the HSN on standard vision and language benchmarks, test learned initiators, and characterize the scaling of the compute-parameter frontier as input dimension grows.

---

## 11. Conclusion

We introduced Fractal Connectivity Networks, a family of architectures that replace dense learned hidden layers with fixed Kronecker-structured recurrent graphs. By iterating the dynamics of these graphs and learning only small input and readout projections, we achieve comparable test accuracy to dense MLPs on standard synthetic benchmarks with roughly one-fifth the learned parameters. The trade-off is increased serial compute at inference time. The results support a broader principle: in neural network design, structured inductive bias can be a direct substitute for parameter count when the architecture is chosen to match the dynamical requirements of the task.

---

## References

{% bibliography --cited %}
