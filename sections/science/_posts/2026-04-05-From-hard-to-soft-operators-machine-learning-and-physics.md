---
layout: post
title: "From hard to soft operators: between machine learning and statistical physics"
date: 2026-04-05
published: true
categories:
  - science
  - language-physics
---

## An academic exploration of deep learning, statistical mechanics, and category theory

As a computational physicist, turned deep learning engineer, I've always found that sometimes the limits between the two disciplines are so blurred that one should not even consider them as part of two different curricula,.
It is no wonder that Giorgio Parisi calls for "a new generation of smart and curious" physicists to develop new intuitions for building new powerful AI algorithms

It is under this perspective that I tend to see so many parallels among what I call hard and soft operators.
By hard operators I mean functions that have sharpe domains, that are combinatorially simply explainable and rarely have their derivatives well defined over each set.
Hard operators tend to emerge for example in the treatment of optimization problems via equality constraints, or in physics in dealying with the microcanonical ensemble, where the exact constraints of the energy makes most of the calculations very difficult.
An example of hard calculation is also related to the identification of the entropy as the logarithm of the number of microstates, a combinatorially complex calculation when involving more that some tens of particles and where doing physics becomes doing combinatorics (a branch of math I rather like indeed).

In physics your are teached that the complexity of calculations of the microcanonical ensemble can often be simplified by requiring constraints that hold "on average". 
It's clear that when one considers a very large number of particles, most of the quantities can be described by Gaussians and smoother functions. This give rise to the canonical ensemble.
Everytime I see an $\exp^{\cdot}$ in machine learning I say: this is an exponential family coming from some application of Jaynes Maximum Entropy principle, and somewhere one has obtained this by application of some constraints that should hold on average.

As a computer scientist, I learned to treat the “softening” of an operator—replacing discrete `argmax` with continuous `softmax` is more that an engineering trick required by backpropagation: everytime people talks me about softmax I think about the canonical ensemble because I recognize the same constructions as thermal fluctuations in a statistical ensemble.

$$
\textrm{argmax}(\mathbf{x}) \approx \textrm{softmax}(\mathbf{x}) = \frac{\exp{x_i}}{\sum_{x_i} \exp{x_i}} \tag{1}
$$

Training a neural network means navigating tension between the **Hard** and the **Soft**. We ask models for discrete, decisive answers (*cat or dog?*), yet optimization by gradient descent needs smooth, continuous landscapes. This note argues that “hard” and “soft” paradigms fit together as the two sides of a categorical bridge: we are not only writing code; we are engineering statistical thermodynamics.

### The microcanonical and the canonical

The bridge joins two regimes. In physics, the step from a “hard” to a “soft” picture comes with a heat bath, fixed by temperature $T$ or inverse temperature $\beta = 1/k_B T$.

In the **microcanonical ensemble**, the system is isolated. Its energy $E$ is fixed. There is no slack. In machine learning, the analogue is a hard constraint: weights that must satisfy an equality, or a logic gate that outputs only $0$ or $1$.

In the **canonical ensemble**, the system exchanges energy with a reservoir. Energy is not fixed; thermal fluctuations give each state $i$ a weight from the Boltzmann distribution

$$ P(i) = \frac{e^{-\beta E_i}}{Z}. $$

Machine learning uses the same move to turn rigid logic into smooth calculus. The table below records a useful dictionary:

| Concept Category | Hard / Discrete (Microcanonical) | Soft / Continuous (Canonical) | Physics Interpretation | Mathematical Bridge |
| :--- | :--- | :--- | :--- | :--- |
| **Selection** | **Max** / **Min** | **LogSumExp** (LSE) | Ground state energy vs. Free energy $A$. | $T \ln \sum e^{x_i/T}$ |
| **Classification** | **Argmax** (One-hot) | **Softmax** (Boltzmann) | Occupancy of a single state vs. Gibbs distribution. | $P(i) = \frac{e^{\beta x_i}}{Z}$ |
| **Activation** | **Step Function** (Heaviside) | **Sigmoid** / **Logistic** | Sharp phase transition vs. Smooth Fermi-Dirac transition. | $(1+e^{-x})^{-1}$ |
| **Sparsity** | **ReLU** | **Softplus** | Sharp threshold (ionization energy) vs. smooth state. | $\ln(1+e^x)$ |
| **Constraint** | **Box Constraint** ($x \in [a, b]$) | **Log-Barrier / Penalty** | Infinite potential well vs. Soft potential barrier. | Interior point methods |
| **Average** | **Arithmetic Mean** | **Expectation Value** $\langle X \rangle$ | Property of a single microstate vs. Ensemble average. | $\sum x_i P(x_i)$ |
| **Topology** | **Minkowski Distance** ($L_\infty$) | **$L_p$ Norm** (Soft-max) | Rigid geometry vs. Approximation of the max norm. | $(\sum \|x_i\|^p)^{1/p}$ |

### The Rosetta Stone functor

Physics names the objects; category theory names the maps. Formalize the picture as follows.

Two categories of computation sit side by side. **$\mathcal{H}$ (the hard category)** is the microcanonical world: discrete sets, strict logical constraints, and rigid morphisms such as `Max`, `Argmax`, and the Heaviside step. **$\mathcal{S}$ (the soft category)** is the canonical world: probabilistic manifolds, statistical ensembles, and smooth morphisms such as `LogSumExp`, `Softmax`, and the sigmoid.

A **functor** $F_T : \mathcal{H} \to \mathcal{S}$, with control parameter $T$ (temperature), links them. The functor should preserve the compositional structure of the network: discrete design maps to a differentiable manifold on the soft side.

```text
       Category H (Microcanonical)                Category S (Canonical)
      [ Strict Logic / Discreteness ]            [ Fluid Calculus / Ensembles ]
      
                Argmax                                     Softmax
              (One-hot)                                  (Boltzmann)
                  |                                           |
                  |                                           |
                  |====== F_T (The Softening Functor) =======>|
                  |                                           |
                  v                                           v
                 Max                                      LogSumExp
            (Winner-Take-All)                           (Free Energy A)
                  |                                           |
                  +-------------------------------------------+
                        Universal Property of Log-Partition
```

Functors send objects to objects and morphisms to morphisms. Here, changing $T$ behaves like a **natural transformation** between functors.

> As $T$ changes, the computational geometry deforms smoothly. At high temperature ($T \to \infty$, $\beta \to 0$), the morphism “melts” toward maximum entropy: Softmax approaches a uniform distribution. In the opposite limit $T \to 0$, the soft category $\mathcal{S}$ collapses toward the hard category $\mathcal{H}$. Softmax freezes to Argmax, and the system locks into its ground state.

### The universal property of the log-partition function

The partition function $Z = \sum e^{-\beta E_i}$ anchors the soft category $\mathcal{S}$; it appears in every Softmax denominator. In practice we often use $\ln Z$, i.e. the `LogSumExp` operator.

The logarithm is not a numerical convenience alone. Categorically, $\ln Z$ behaves like a **generating potential**: its gradient $\nabla \ln Z$ gives expectations (means), and its Hessian $\nabla^2 \ln Z$ encodes fluctuations (variance).

The contrast with bare `Max` ties to the **density of states**. A hard `Max` reads only the highest peak. `LogSumExp` aggregates a volume. If one state sits at height $10.0$ and a thousand states sit near $9.9$, `Max` returns $10.0$; $\ln Z$ can reflect that the mass near $9.9$ dominates the landscape. In that sense Softmax is ensemble-aware rather than peak-only.

### Deep structural analogies: from sorting to attention

The functorial picture extends beyond activation functions to routing, memory, and structure.

| Operator / Concept | Hard Version ($\mathcal{H}$) | Soft Version ($\mathcal{S}$) | Physical Intuition |
| :--- | :--- | :--- | :--- |
| **Attention** | **Hard Attention** | **Soft Attention** | Picking a single particle vs. Computing an interaction field. |
| **Clustering** | **K-Means** (Voronoi) | **Gaussian Mixture (GMM)** | Particles fixed in cells vs. Overlapping wavefunctions. |
| **Sorting** | **Standard Sort** | **SoftSort / Optimal Transport** | Ordering particles vs. Computing a continuous flux distribution. |
| **Ranking** | **Integer Rank** | **Soft Rank** | Discrete energy levels vs. Density of states. |
| **Logic** | **Boolean AND** | **T-Norm / Product** | Simultaneous rigid constraints vs. Overlapping probabilities. |
| **Branching** | **Decision Tree** | **Mixture of Experts (MoE)** | Hard bifurcation vs. Continuous fluid dynamic flow. |
| **Sampling** | **Categorical Draw** | **Gumbel-Softmax Trick** | Discrete quantum state collapse vs. Continuous path integral. |
| **Loss Function**| **0-1 Error** | **Cross-Entropy Loss** | Microstate counting ($W$) vs. Gibbs Entropy optimization ($S$). |

Transformer attention illustrates the point. Training builds a continuous interaction field from query–key inner products, scaled by temperature, instead of a hard lookup table.

### Free energy vs. loss: a functional parallel

The mapping suggests a tight analogy at the level of the objective. In statistical mechanics, the **Helmholtz free energy** is the energy available for useful work:

$$ A = U - TS, $$

with internal energy $U$, temperature $T$, and entropy $S$.

In machine learning, especially variational inference, we minimize objectives that mirror this split—for example the negative ELBO—schematically

$$ \text{Loss} \approx \text{Energy (error)} - \text{Entropy}. $$

The energy term measures misfit to data and should fall. The entropy term measures spread or uncertainty in parameters or latents. Backpropagation through a smooth network then resembles minimization of a free-energy functional: one term pulls the model toward the data; the entropy term keeps enough softness for differentiability and, often, for generalization.

### When ensemble equivalence fails

If $\mathcal{H}$ and $\mathcal{S}$ always gave the same macroscopic answers, the story would be pedagogy only. In textbook thermodynamics, **ensemble equivalence** holds in the **thermodynamic limit**: as the particle number $N \to \infty$, microcanonical (fixed energy) and canonical (fixed temperature) descriptions agree on intensive observables.

In physics and in deep learning, that equivalence **breaks** under sharp conditions. Those conditions are also where much of modern ML lives.

```text
      Equivalence Regime (Classical Stats)    ||  Broken Equivalence (Deep Learning)
   [ N -> ∞, Convex Maps, Local Interactions] || [ Finite N, Non-Convex, Global Attention ]
   -------------------------------------------||-------------------------------------------
                                              ||
    Microcanonical (Hard) ≈ Canonical (Soft)  ||   Microcanonical (Hard) ≠ Canonical (Soft)
        (Constraints = Penalties)             ||      (Constraints Produce Different 
                                              ||       Attractors than Penalties)
```

Three regimes matter.

**Non-convexity and phase structure.** In physics, equivalence can fail when the entropy $S(E)$ is not concave, as in some first-order transitions. A microcanonical description may show *negative heat capacity*; the canonical ensemble may need extra constructions to match that behavior. Deep networks face highly non-convex losses. “Hard” empirical risk minimization that chases exact zero training error can behave unlike “soft” stochastic gradient descent at finite temperature or learning rate: the soft dynamics can cross barriers that trap hard minimization.

**Small $N$ and finite-size effects.** Tiny clusters fluctuate as much as they mean; temperature is delicate. In learning, small data invite **overfitting**: a hard fit memorizes noise, while heavy $L_1$ or $L_2$ regularization in a canonical-style objective can over-smooth and wash out signal. In finite regimes, the choice between hard constraints and soft penalties reshapes the geometry of solutions.

**Long-range coupling and attention.** Classical equivalence often assumes short-range interactions. Gravity violates that picture; **Transformers** violate it through self-attention. Global coupling makes energy non-additive in the naive sense ($E_{\text{total}} \neq E_1 + E_2$). The Softmax attention matrix is not merely a relaxed categorical lookup: it builds a globally coupled field. The shared denominator—the “log $Z$” of attention—can dominate the dynamics.

### Conclusion: engineering thermodynamics

Once ensemble equivalence is not automatic, architecture and optimization need different bookkeeping.

A **hard constraint** (for example, strict orthogonality of a weight matrix) places the model in the microcanonical picture ($\mathcal{H}$). A **soft penalty** (for example, adding $\lambda \|W^\top W - I\|$ to the loss) lives in the canonical picture ($\mathcal{S}$). In non-convex, finite-data, long-range regimes, **these two recipes need not land in the same basin**. That tension helps explain why explicit weight decay and $L_2$ penalties diverge in behavior under adaptive optimizers such as Adam: the algorithms trace different effective ensembles.

We use Softmax not only because we need a derivative. We use it because a temperature-parameterized map $F_T$ carries discrete logical intent into a continuous, thermodynamic description and lets optimization seek something like free-energy balance in a rough landscape.

The next time you write a loss, you might read it as a Hamiltonian. As work on **energy-based models** makes the density $P(x) \propto e^{-E(x)}$ explicit, the lines between computer scientist, category theorist, and physicist may blur further still.
