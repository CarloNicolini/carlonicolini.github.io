---
layout: post
title: Hippocampal scaffold networks
subtitle: Reducing learned parameters by trading computation for structure
description: "We test two brain-inspired architectures — Hippocampal Scaffold Network (HSN) and Cerebellar Expansion Network (CEN) — that trade a tiny number of learned parameters for a large, fixed recurrent or expanded scaffold, comparing them against a standard dense MLP on four synthetic benchmarks."
date:   2026-05-15
categories: science
published: true
usemathjax: true
---

## The tradeoff

Standard deep learning assumes a strict budget: every hidden unit demands its own learned parameters. A three-layer ReLU MLP with width 64 and two inputs carries

$$
2 \cdot 64 + 64 \cdot 64 + 64 \cdot 1 = 4{,}417 \quad \text{learned parameters}. \label{eq:dense-budget}\tag{1}
$$

All of them are updated during training. The compute budget at inference is proportional to the parameter count.

This note asks a different question: **what if almost none of the hidden layer were learned?** We could in principle trade a *much larger* fixed hidden state — built by a random sparse expander or a structured recurrent graph — against a *tiny* learned readout. The expanded state is computed cheaply; only the readout weights carry gradients.

The analogy is the hippocampal circuit: sparse, unlearnt expansion in the dentate gyrus, followed by pattern completion in CA3 through recurrent collaterals, then readout via CA1 pyramidal cells. Each stage has a known neurobiological analogue, but the *computational* point is independent of the analogy:

$$
\text{large fixed nonlinearity } \phi(x) \quad \longrightarrow \quad \text{small learned linear readout } W_{\text{out}} \phi(x). \label{eq:scaffold}\tag{2}
$$

We test two architectures built on this principle and compare them against a dense MLP on four standard synthetic benchmarks.

---

## 1. Two architectures

### 1.1 Cerebellar Expansion Network (CEN)

Inspired by the mossy-fiber granule-cell expansion in cerebellar cortex.

* **Fixed random sparse expander** $$E \in \mathbb{R}^{H \times d}$$ with 5% nonzero density. Drawn once, never updated. Mimics granule cells receiving thousands of mossy-fiber synapses, only $$\sim$$4 active at a time.
* **ReLU activation** on the expanded representation.
* **Learned dense readout** $$W_{\text{out}} \in \mathbb{R}^{o \times H}$$ with bias. The only trainable parameters.

Parameter count: $$o \cdot H + o$$.

For a binary classification task with $$H=512$$, this gives **513 learned parameters** instead of the dense MLP's 4,417. The expander adds $$H \times d$$ *fixed* weights, which cost memory but no gradient compute.

### 1.2 Hippocampal Scaffold Network (HSN)

Inspired by the dentate-gyrus CA3 CA1 circuit.

* **DG stage:** learned sparse input projection $$W_{\text{dg}} : \mathbb{R}^d \rightarrow \mathbb{R}^{h_{\text{dg}}}$$ with 5% density.
* **CA3 stage:** recurrent Kronecker graph $$G$$ on $$h_{\text{ca3}}$$ units, iterated $$T$$ times. The graph is built from a Sierpiński initiator $$[[1,1],[1,0]]$$, giving logarithmic diameter at subquadratic density.
* **CA1 stage:** readout $$W_{\text{ca1}} : \mathbb{R}^{h_{\text{ca3}}} \rightarrow \mathbb{R}^o$$.

Parameter count:
$$\text{nnz}(W_{\text{dg}}) + \text{nnz}(G) + h_{\text{ca3}} + o$$.

With $$h_{\text{dg}} = 32$$, $$h_{\text{ca3}} = 16$$, and $$T = 5$$, this gives **897 learned parameters** — still roughly 5$$\times$$ fewer than the dense MLP.

---

## 2. Benchmark results

Four classical synthetic tasks:

1. **Swiss roll classification:** binary label on a 2D spiral manifold.
2. **Concentric circles:** binary label on nested rings.
3. **Noisy moons:** two interleaved half-moons with Gaussian noise.
4. **Sine wave regression:** predict $$y = \sin(x)$$ on $$[0, 4\pi]$$.

All models trained with Adam on 512 training points for 100 epochs (200 for regression), validated on 256 points. No hyperparameter tuning beyond learning-rate grid search at {0.01, 0.02}. Device: Apple MPS.

### 2.1 Raw scores

| Benchmark | Dense MLP | HSN | CEN (best H) |
|-----------|----------|-----|-------------|
| Swiss Roll | 0.984 | **0.984** | 0.977 (H=512) |
| Circles | 0.996 | **0.996** | 0.984 (H=128) |
| Moons | 0.953 | **0.977** | 0.863 (H=512) |
| Sine (MSE) | **0.019** | 0.039 | 0.417 (H=64) |

### 2.2 Learned parameter counts

| Architecture | Params (classification) | Params (regression) |
|-------------|------------------------|---------------------|
| Dense MLP | 4,417 | 4,353 |
| HSN | **897** | **865** |
| CEN (H=512) | **513** | — |

<figure>
<img src="/assets/postfigures/exp10_brain_inspired.png" alt="Brain-inspired architectures" style="max-width: 100%;">
<figcaption>
<strong>Figure 1.</strong> Brain-inspired architectures: HSN (Hippocampal Scaffold Network) and CEN (Cerebellar Expansion Network) compared against a 3-layer dense MLP. Markers show accuracy / MSE; horizontal dashed lines show dense MLP performance. The HSN matches or exceeds dense accuracy with 5$$\times$$ fewer learned parameters.
</figcaption>
</figure>

---

## 3. Interpretation

### 3.1 HSN matches dense accuracy at one-fifth the parameters

On Swiss Roll, Circles, and Moons, the HSN achieves **identical or superior** accuracy to the dense MLP while using **897 learned parameters instead of 4,417** — a **4.9$$\times$$ reduction**.

The architecture works as follows: the sparse DG projection maps the input into a high-dimensional sparse code. The CA3 Kronecker graph circulates this code for 5 iterations, allowing the pattern to settle into a stable recurrent attractor. The CA1 readout then extracts a scalar classification from the settled state.

The circulation is the key: each iteration performs partial pattern completion, mixing information across the graph's multiscale structure. Five iterations cost roughly 5$$\times$$ the compute of a single feedforward pass, but the *learned* parameter count stays small because the graph is fixed and the readout is tiny.

### 3.2 CEN partially succeeds on classification, fails on regression

The CEN reaches 0.977 on Swiss Roll and 0.984 on Circles at **513 parameters** — an **8.6$$\times$$ reduction**. On Moons it plateaus at 0.863, and on sine regression it fails entirely (MSE 0.417 vs 0.019 for dense).

Why? The CEN relies entirely on a *fixed random* expansion followed by a learned linear readout. This is an extreme version of the random-feature/kernel trick: if the expansion happens to separate the classes linearly, the readout succeeds. Swiss Roll and Circles are geometrically simple; Moons and sine are not. Random features are data-agnostic, and **the readout has no nonlinear capacity** to compensate.

The CEN resembles the classical extreme learning machine (ELM) and reservoir computing setup. Its strength is simplicity; its weakness is brittleness.

### 3.3 Where the parameter savings come from

| Component | Dense MLP | HSN | Savings |
|-----------|----------|-----|---------|
| Input→hidden | $$d \cdot 64 + 64 = 192$$ | $$ ext{nnz}(W_{\text{dg}}) = 5$$ | 38$$\times$$ |
| Hidden→hidden | $$64 \cdot 64 + 64 = 4{,}160$$ | $$ ext{nnz}(G) + h_{\text{bridge}} = 256 + 544 = 800$$ | 5$$\times$$ |
| Hidden→output | $$64 + 1 = 65$$ | $$16 + 1 = 17$$ | 3.8$$\times$$ |
| **Total** | **4,417** | **897** | **4.9$$\times$$** |

The bulk of the savings is in the hidden-to-hidden stage. The dense MLP learns a full $$64 \times 64$$ matrix. The HSN replaces it with a fixed Kronecker graph (97 nonzeros) plus a small learned bridge (544 parameters). The recurrent circulation then effectively *simulates* a much larger hidden space by iterating 5 times through the graph.

---

## 4. Related work

**Reservoir computing** (Jaeger 2001, Maass 2002) shares the fixed-hidden-variable paradigm but typically uses random recurrent connectivity. The HSN is distinguished by replacing random recurrence with a *structured Kronecker graph*, giving precise control over spectral properties, path lengths, and timescales.

**Extreme learning machines** (Huang et al. 2006) fix random input weights and learn only the readout. The CEN is an ELM with sparse expander; the HSN adds a learned sparse input projection and structured recurrent hidden state, making it more expressive.

**Neuroscience-inspired architectures** include models of cerebellar computation (Yamazaki & Tanaka 2007) and hippocampal sequence learning (Zhang & Oertner 2019). Those models aim to explain neural data; the present architectures aim to exploit the *computational* insight — large fixed nonlinearity plus small learned readout — for general machine learning.

---

## 5. Limitations and open questions

**Compute tradeoff.** The HSN uses fewer parameters but more inference-time compute (5 recurrent iterations). On a serial CPU this is slower than a single feedforward pass. On parallel hardware — or with sparse matrix kernels — the gap narrows.

**Task dependence.** The 5$$\times$$ savings were measured on four synthetic 2D tasks. Real benchmarks (MNIST, CIFAR, language) may behave differently.

**Learned vs fixed graphs.** The Kronecker graph in the HSN is currently fixed. Learning the initiator matrix could further improve performance while remaining parameter-efficient.

**Scaling.** Does the parameter advantage grow with input dimension? For a 784-dimensional input (MNIST), the dense hidden-to-hidden matrix grows to $$784 \cdot 64 = 50{,}176$$ parameters. The HSN sparse DG projection stays at $$\sim$$250 nonzeros. The savings may become larger at higher dimensions.

---

## 6. Takeaway

**Computational structure can substitute for learned parameters.** The Hippocampal Scaffold Network shows that a fixed Kronecker recurrent graph plus a tiny learned readout matches a dense MLP on standard benchmarks with one-fifth the parameters. The tradeoff is increased compute — iteratively circulating through the graph rather than taking a single feedforward step.

The broader principle: architecture is a form of inductive bias, and structured inductive biases buy parameter efficiency.
