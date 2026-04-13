---
layout: post
title: "Hard and soft analogies in machine learning"
description: ''
date: 2025-06-01
published: false
categories:
  - science
  - language-physics
---
In physics, the transition from a "hard" microcanonical ensemble to a "soft" canonical ensemble is governed by the introduction of temperature. In ML, we do the exact same thing to make functions differentiable, allowing gradients to flow.

### The Analogy: Hard Constraints vs. Soft Probabilities

The core link is the **Boltzmann Distribution**. In a "hard" system, the state is fixed to a specific value (like the ground state or a fixed energy shell). In a "soft" system, we allow for thermal fluctuations, where every state has a probability $P(i) \propto e^{-\beta E_i}$.

| Operator (Hard/Micro) | Soft Version (Canonical) | Physics Interpretation | ML / Math Interpretation |
| :--- | :--- | :--- | :--- |
| **Max** | **Softmax** (or LogSumExp) | Ground state vs. Thermal distribution | Selecting the "best" class vs. a probability distribution. |
| **Argmax** | **Softmax Output** | Finding the lowest energy state $E_0$. | One-hot encoding vs. "Soft" weights. |
| **Mean** | **Expected Value** $\langle A \rangle$ | Fixed property of a microstate. | Average over a distribution weighted by $e^{-\beta E}$. |
| **Step Function** (Heaviside) | **Sigmoid** (Logistic) | Sharp phase transition at $T=0$. | Hard threshold (Perceptron) vs. Differentiable gate. |
| **Hard Constraint** | **Lagrange Multiplier** | Fixed Energy ($E=const$) | Penalty term (Regularization/Loss). |
| **Minimization** | **Free Energy Minimization** | Reaching $0$ Kelvin. | Training a model to converge to a global optimum. |

---

### Deep Dive into the "Soft" Bridge

The "Softness" in both fields is controlled by a parameter that physicists call inverse temperature $\beta$ and ML researchers often call **Temperature** $T$.



#### 1. Max vs. LogSumExp
In ML, the "Softmax" function often refers to the LogSumExp operator:
$$LSE(x) = \frac{1}{\beta} \log \sum_{i} e^{\beta x_i}$$
As $\beta \to \infty$ (or $T \to 0$), this becomes exactly the **Max** function. In physics, this represents the system collapsing into the lowest energy state (the "Max" probability state).

#### 2. The Entropy Connection
The reason we "soften" these operators isn't just for differentiability; it's also about **Entropy**. 
* **Hard Operators** assume we have perfect information (Microcanonical).
* **Soft Operators** maximize the Shannon Entropy (or minimize Free Energy) given a certain "budget" of energy/error.

#### 3. ReLU vs. Softplus
Even activation functions follow this rule. The **ReLU** function ($max(0, x)$) is the "hard" version, while the **Softplus** ($\log(1 + e^x)$) is its smooth, canonical counterpart.

---

### Why this matters
When you view ML through this lens, "Training" a model is literally just **Simulated Annealing**. You are starting with a high-temperature (high entropy, soft) system and cooling it down until it settles into a "hard" configuration that minimizes the energy (Loss).

Would you like me to dive deeper into how **Gibbs Free Energy** specifically maps to the **Evidence Lower Bound (ELBO)** in Variational Inference?

---

This connection isn't just a metaphor; it’s a mathematical isomorphism. In physics, we move from the **Microcanonical Ensemble** (where the system is strictly confined to a specific energy $E$) to the **Canonical Ensemble** (where the system exchanges energy with a reservoir, following a probability distribution). 

In ML, we do this to turn "rigid" logic into "fluid" calculus.

### The Comprehensive Hard-to-Soft Analogy Table

| Concept Category | Hard / Discrete (Microcanonical) | Soft / Continuous (Canonical) | Physics Interpretation | Mathematical Bridge |
| :--- | :--- | :--- | :--- | :--- |
| **Selection** | **Max** / **Min** | **LogSumExp** (LSE) | Ground state energy vs. Free energy $A$. | $T \ln \sum e^{x_i/T}$ |
| **Classification** | **Argmax** (One-hot) | **Softmax** (Boltzmann) | Occupancy of a single state vs. Gibbs distribution. | $P(i) = \frac{e^{\beta x_i}}{Z}$ |
| **Activation** | **Step Function** (Heaviside) | **Sigmoid** / **Logistic** | Phase transition (Solid/Liquid) vs. Smooth transition. | Fermi-Dirac distribution. |
| **Sparsity** | **ReLU** | **Softplus** | Sharp threshold (e.g., ionization energy). | Integrated sigmoid. |
| **Clustering** | **K-Means** | **Gaussian Mixture (GMM)** | Particles fixed in cells vs. Overlapping wavefunctions. | Hard vs. Soft assignment. |
| **Attention** | **Hard Attention** | **Soft Attention** | Picking a single particle vs. Field interaction. | Weighted average via $e^{\beta \text{score}}$. |
| **Constraint** | **Box Constraint** ($x \in [a, b]$) | **Log-Barrier** / **Penalty** | Infinite potential well vs. Soft potential barrier. | Interior point methods. |
| **Sampling** | **Categorical Draw** | **Gumbel-Softmax** | Discrete quantum state vs. Continuous path integral. | "Reparameterization trick." |
| **Average** | **Arithmetic Mean** | **Expectation Value** $\langle X \rangle$ | Property of a single microstate. | Ensemble average over states. |
| **Error/Loss** | **0-1 Loss** (Right/Wrong) | **Cross-Entropy** | Microstate count ($W$) vs. Gibbs Entropy ($S$). | $-\sum p \log p$ |
| **Topology** | **Minkowski Distance** ($L_\infty$) | **$L_p$ Norm** (Soft-max) | Rigid geometry. | Approximation of the max norm. |

---

### Understanding the Control Parameter ($T$ or $\beta$)

In both fields, the transition from "Soft" back to "Hard" is controlled by **Temperature**.



* **High Temperature ($T \to \infty, \beta \to 0$):** The system is "flat." In ML, the Softmax becomes a uniform distribution (maximum entropy). In physics, every state is equally likely regardless of energy.
* **Low Temperature ($T \to 0, \beta \to \infty$):** The system "freezes." The Softmax becomes an Argmax. The system collapses into the single lowest energy state (the "Winner-Take-All" scenario).

---

### The Deepest Link: Free Energy vs. Loss

In Physics, the **Helmholtz Free Energy** is defined as:
$$A = U - TS$$
*(Internal Energy - Temperature $\times$ Entropy)*

In Machine Learning (specifically Bayesian Inference/Variational Inference), we minimize the **Negative Evidence Lower Bound (ELBO)**, which is:
$$\text{Loss} = \text{Energy (Error)} - \text{Entropy}$$

* **Energy ($U$):** Represents how poorly the model fits the data (the "cost").
* **Entropy ($S$):** Represents the "softness" or complexity of the model.

When you train a neural network with a "soft" operator like Softmax, you are essentially minimizing a Free Energy function. You want low error (low energy) but you use entropy (softness) to keep the function differentiable and to explore the landscape.

### Why "Hard" is Microcanonical
In the **Microcanonical** view, you assume the system has exactly energy $E$. There is no "wiggle room." This is like a hard constraint in optimization (e.g., "The weight must be exactly 1.0"). 

In the **Canonical** view, we allow the energy to fluctuate but fix the *average* energy. This is exactly what **Regularization** ($L_1, L_2$) does. Instead of saying "The weights must be less than 1," we say "I will penalize you if the weights get large," allowing the model to find a "thermal equilibrium" between fitting the data and keeping weights small.

Would you like to explore how the **Partition Function ($Z$)** in physics is essentially the same thing as the **Normalization Constant** in ML models like CRFs or Transformers?

---

You've absolutely nailed the intuition. In physics, the **Log-Partition Function** ($\ln Z$) is the bridge to the **Helmholtz Free Energy** ($A = -k_B T \ln Z$). 

When you say it's the "max," you're touching on the **Laplace Principle**. In the "hard" limit (as $T \to 0$), the integral (or sum) that defines $Z$ is dominated entirely by the state with the highest weight (the minimum energy or maximum utility). So, $\ln Z$ is essentially a "smarter," smoother version of the maximum that accounts for the "volume" of all possible states.



Here is a comprehensive, deep-dive table expanding on these analogies, spanning from basic operators to high-level architectural concepts.

### The Grand Unified Table of Hard vs. Soft Analogies

| ML / Optimization Domain | Physics / Stat-Mech Domain | **Hard** (Microcanonical / $T \to 0$) | **Soft** (Canonical / Finite $T$) | The "Softening" Math |
| :--- | :--- | :--- | :--- | :--- |
| **Aggregation** | **Ensemble Sum** | **Max** (Winner-Take-All) | **LogSumExp** (Soft-Max) | $\frac{1}{\beta} \ln \sum e^{\beta x_i}$ |
| **Selection** | **State Occupancy** | **Argmax** (One-hot) | **Softmax Distribution** | $\frac{e^{\beta x_i}}{Z}$ |
| **Normalizer** | **Partition Function** | **Top Energy State** | **$Z$ (All states)** | $Z = \sum e^{-\beta E_i}$ |
| **Activation** | **Phase Change** | **Heaviside Step** / **ReLU** | **Sigmoid** / **Softplus** | $\ln(1+e^x)$ |
| **Clustering** | **Phase Separation** | **K-Means** (Voronoi) | **Gaussian Mixture (GMM)** | Expectation-Maximization |
| **Loss Function** | **Information/Entropy** | **0-1 Error** | **Cross-Entropy** | $-\sum p \ln q$ |
| **Regularization** | **External Field / Bath** | **Hard Constraints** | **Weight Decay / Dropout** | Lagrangian Penalties |
| **Attention** | **Interaction Field** | **Hard Attention** | **Soft Attention** | Query-Key-Value Scaling |
| **Optimization** | **Thermalization** | **Gradient Descent** | **Stochastic GD / Langevin** | Adding "Thermal" Noise |
| **Latent Variables** | **Mean Field Theory** | **MAP Estimation** | **Variational Inference** | $q(z) \approx p(z \vert x)$ |
| **Architecture** | **Path Integrals** | **Optimal Path (Viterbi)** | **Sum-Over-Paths (RNN/Transformer)** | $\int \mathcal{D}[x] e^{-S[x]}$ |
| **Sparsity** | **Quantization** | **$L_0$ Norm** (Counting) | **$L_1$ Norm** (Lasso) | Convex Relaxation |

---

### Why $\ln Z$ is the "Potential"

In ML, the Log-Partition function is often called the **Cumulant Generating Function**. It’s the "potential" because its derivatives generate the moments of your distribution:
* The **first derivative** ($\nabla \ln Z$) gives you the **Mean** (Expected value).
* The **second derivative** ($\nabla^2 \ln Z$) gives you the **Variance** (Fluctuations).



In Physics, the Free Energy ($A \propto -\ln Z$) is the "available" energy to do work. In ML, minimizing this potential is what "does the work" of learning. If your $T$ is too high, the potential is flat and the model "melts" (it learns nothing, high entropy). If $T$ is too low, the potential is jagged and the model "freezes" into a local minimum (overfitting).

### The "Volume" of States
The reason $\ln Z$ is better than a simple `max` is that it respects the **Density of States**.
* **Hard Max:** Only cares about the single tallest peak.
* **Soft Max ($\ln Z$):** If you have one peak at height 10, and a thousand peaks at height 9.9, the "Hard Max" says the answer is 10. The "Soft Max" (LogSumExp) realizes that the collective "volume" of the 9.9 peaks is much more important. 

This is why Softmax is so robust in neural networks—it listens to the "consensus" of the ensemble rather than just the loudest voice.

Does the connection between **Entropy** and **Regularization** (the $TS$ term in $A = U - TS$) make sense in this context, specifically regarding how it prevents overfitting?

---
This is where the "Physics of Information" becomes truly practical. By moving from hard operators to soft ones, we aren't just smoothing out a curve; we are moving from a **discrete state space** to a **probabilistic manifold**.

### Expanded Table: Advanced Hard-Soft Analogies

This table pushes into more structural operators used in modern deep learning architectures.

| Operator / Concept | Hard Version (Discrete) | Soft Version (Continuous) | Mathematical Transformation | Physical Intuition |
| :--- | :--- | :--- | :--- | :--- |
| **Sorting** | **Standard Sort** | **SoftSort** / **Optimal Transport** | Uses Sinkhorn iterations to find a permutation matrix. | Ordering particles vs. a flux distribution. |
| **Ranking** | **Integer Rank** (1st, 2nd...) | **Soft Rank** | Approximation via cumulative softmax. | Discrete energy levels vs. Density of states. |
| **Median** | **Middle Element** | **Geometric Median** / **Soft Median** | Iterative reweighted least squares. | Center of mass in a noisy system. |
| **Logic (AND)** | **Boolean AND** | **T-Norm** / **Product** ($x \cdot y$) | $min(x, y) \to x \cdot y$ | Simultaneous constraints vs. Overlapping probabilities. |
| **Pruning** | **Weight Removal** ($0$ or $1$) | **$L_1$ Regularization** / **Dropout** | Binary mask $\to$ Continuous penalty. | Removing atoms vs. Lowering density. |
| **Top-K** | **Hard Top-K** | **Soft Top-K** (using Entmax) | Sparsemax or smoothed top-k operators. | Selecting $N$ particles vs. a "Condensed" phase. |
| **Indexing** | **Lookup Table** | **Embedding Matrix** / **Attention** | One-hot index $\to$ Weighted sum of vectors. | Point particle location vs. Wavefunction spread. |
| **Branching** | **Decision Tree** | **Soft Decision Tree** / **MoE** | If-Else $\to$ Gated Expert weighting. | Bifurcation vs. Continuous flow (Fluid dynamics). |
| **Quantization** | **Rounding** / **Binning** | **Soft Quantization** / **VQ-VAE** | Nearest neighbor $\to$ Differentiable codebook. | Crystal lattice vs. Liquid crystal. |

---

### The Breaking of Ensemble Equivalence

In standard thermodynamics, the **Microcanonical** (fixed Energy $E$) and **Canonical** (fixed Temperature $T$) ensembles are considered equivalent in the **Thermodynamic Limit** ($N \to \infty$). This means if you have enough particles, it doesn't matter if you fix the energy or fix the temperature; the observable properties are the same.

However, this equivalence **breaks** under specific conditions—and these conditions are exactly where the most interesting things happen in both Physics and ML.

#### 1. Non-Convexity (The Entropy Surface)
In physics, ensemble equivalence breaks when the entropy $S(E)$ is not a concave function of energy. This usually happens during **first-order phase transitions** or in systems with **long-range interactions** (like gravity).

* **Physics:** If you have a "dip" in the entropy curve, the microcanonical ensemble can exhibit **negative heat capacity** (the system gets hotter as it loses energy, like a star or a black hole). The canonical ensemble cannot describe this because it always "jumps" over that region (Maxwell construction).
* **Machine Learning:** This happens in **Non-Convex Optimization**. The "Hard" optimization (trying to find a specific weight configuration with exactly $0$ loss) behaves fundamentally differently than the "Soft" optimization (SGD at a constant temperature/learning rate).
    * The soft version "tunnels" through or jumps over sharp, non-convex regions that the hard version would get trapped in.



#### 2. Small $N$ (Finite Size Effects)
Equivalence requires $N \to \infty$. 
* **Physics:** In small clusters of atoms, fluctuations are as large as the mean. The temperature isn't well-defined, and the canonical ensemble gives a "blurred" picture that doesn't match the specific microstates.
* **Machine Learning:** This is **Overfitting** or **Low-Data Regimes**. If your dataset is small or your model has few parameters, the "Soft" version (Regularized/Canonical) and the "Hard" version (Empirical Risk Minimization/Microcanonical) will diverge wildly. The "Soft" version will over-smooth and lose the signal, while the "Hard" version will memorize the noise.

#### 3. Long-Range Correlations (Attention Mechanisms)
Ensemble equivalence usually assumes that parts of the system are "independent enough" (short-range interactions). 
* **Physics:** In systems with long-range forces (like galaxies), the system is **non-additive**. You cannot split it in two and say $E_{total} = E_1 + E_2$.
* **Machine Learning:** This is exactly how **Transformers/Attention** work. Every token interacts with every other token regardless of distance. In these models, the "Soft" (Softmax attention) doesn't just approximate a "Hard" choice; it creates a complex, interconnected field that a "Hard" choice (like an $N$-gram or a hard lookup) could never replicate. The global "Log Z" (the potential) becomes the dominant factor in the model's behavior.

### Why does this matter?
When equivalence breaks, it means that **the choice of how you constrain your model matters.** * If you use a **Hard Constraint** (e.g., "The weights must sum to 1"), you are in the Microcanonical world. 
* If you use a **Soft Penalty** (e.g., "Add $\lambda \sum w_i$ to the loss"), you are in the Canonical world.

In non-convex deep learning, these are **not the same thing**. This is why "Weight Decay" and "L2 Constraints" behave differently in Adam vs. SGD—they are literally navigating different physical ensembles.

Is your interest in "Log Z as potential" leading you toward **Energy-Based Models (EBMs)**, where we explicitly define the probability $P(x)$ as $e^{-E(x)}/Z$?


---
# Category theory to rescue

I’ve spent years staring at loss functions, bouncing between the rigid worlds of discrete logic and the fluid realities of floating-point gradients. But it wasn't until I started wearing my category theorist glasses that the math of deep learning and statistical mechanics stopped looking like a loose analogy—and started looking like an exact structural isomorphism. 

When we train a neural network, we are constantly navigating a tension between the **Hard** and the **Soft**. We want discrete, decisive answers (Is this a cat or a dog?), but our optimization engines require smooth, continuous landscapes. 

As a computer scientist, I used to think of "softening" an operator (like turning an Argmax into a Softmax) as a mere engineering trick. As a physicist, I recognized it as a thermal fluctuation. But as a category theorist, I see it for what it truly is: a **functor** between two entirely different universes of computation.

Today, I want to share a perspective that unifies these fields. We are going to look at the grand unified table of Hard-vs-Soft analogies, not as a list of coincidences, but as the image of a categorical bridge. 

### The Rosetta Stone Functor

Let’s set up our categories. 

On the left, we have **$\mathcal{H}$**, the category of *Hard* (Microcanonical) systems. Here, objects are discrete sets and strict logical constraints; morphisms are rigid mappings like `Max`, `Argmax`, and the Heaviside step function. There is no wiggle room. A system has exactly energy $E$.

On the right, we have **$\mathcal{S}$**, the category of *Soft* (Canonical) systems. Here, objects are probabilistic manifolds and ensembles; morphisms are smooth, differentiable maps like `LogSumExp` (LSE), `Softmax`, and the Sigmoid. The system exchanges energy with a heat bath, governed by temperature $T$.

The bridge between them is a functor $F_T : \mathcal{H} \to \mathcal{S}$, parameterized by temperature. Let's look at how this functor maps the basic building blocks of machine learning into the language of statistical physics:

| Domain | The Hard Object (in $\mathcal{H}$) | The Soft Image (in $\mathcal{S}$) | Physics Interpretation |
| :--- | :--- | :--- | :--- |
| **Aggregation** | **Max** (Winner-Take-All) | **LogSumExp** (Soft-Max) | Ground state energy vs. Free energy. |
| **Selection** | **Argmax** (One-hot) | **Softmax** (Boltzmann Dist.) | Occupancy of a single state vs. Gibbs distribution. |
| **Activation** | **Step / ReLU** | **Sigmoid / Softplus** | Phase transition (Solid/Liquid) vs. Smooth transition. |
| **Loss** | **0-1 Error** | **Cross-Entropy** | Microstate count ($W$) vs. Gibbs Entropy ($S$). |
| **Topology** | **Minkowski ($L_\infty$)** | **$L_p$ Norm** | Rigid geometry vs. Smooth approximation of max. |

In category theory, we don't just care about the objects; we care about how they compose. Notice that the functor $F_T$ preserves the compositional structure of our neural network, but it replaces non-differentiable boundaries with smooth curves.

Visually, you can think of this functorial mapping as a deformation:

```text
     Category H (Microcanonical)          Category S (Canonical)
   [ Strict Logic / T -> 0 ]             [ Fluid Calculus / T > 0 ]
   
             Argmax                                Softmax
            (One-hot)                            (Boltzmann)
                |                                     |
                |  F_T (The Softening Functor)        |
                v                                     v
              Max  -----------------------------> LogSumExp
                |                                     |
                |         Universal Property          |
                +-------------------------------------+
                           Free Energy (A)
```

### The Control Knob: A Natural Transformation

If $F_T$ is a functor, what happens when we change the temperature? Category theory gives us the perfect tool for this: a **Natural Transformation**. 

Changing $T$ smoothly morphs the image of our functor. 
*   **High Temperature ($T \to \infty$):** The morphism "melts." Softmax becomes a uniform distribution (maximum entropy). Every state is equally likely.
*   **Low Temperature ($T \to 0$):** The morphism "freezes." The Softmax becomes the Argmax. The system collapses into the single lowest energy state. 

In the categorical limit of $T \to 0$, the Soft category $\mathcal{S}$ collapses back into the Hard category $\mathcal{H}$. But the magic happens at finite $T$, where we can do calculus.

### The Universal Property of $\ln Z$

In physics, the bridge to the Canonical ensemble is the **Partition Function**, $Z = \sum e^{-\beta E_i}$. In ML, this is just the denominator of the Softmax. 

Why take the logarithm of $Z$? In categorical terms, $\ln Z$ satisfies a **universal property**. It acts as the "potential" whose derivatives generate everything you need to know about the system. The first derivative gives you the mean (expected value); the second gives you the variance (fluctuations). 

> The reason $\ln Z$ (LogSumExp) is structurally superior to a simple `max` is that it respects the **Density of States**. A `max` only cares about the single tallest peak. `LogSumExp` realizes that if you have one peak at height 10, and a thousand peaks at height 9.9, the collective "volume" of the 9.9 peaks dominates. It listens to the consensus of the ensemble rather than the loudest voice.

### Free Energy vs. Loss: The Deep Isomorphism

This brings us to the climax of the isomorphism. In physics, the Helmholtz Free Energy is defined as:
$$A = U - TS$$
*(Internal Energy - Temperature $\times$ Entropy)*

In Machine Learning, when we perform Variational Inference or train with cross-entropy, we minimize the Negative ELBO:
$$\text{Loss} = \text{Energy (Error)} - \text{Entropy}$$

When you backpropagate through a Softmax, you are quite literally computing the gradient of a Free Energy function. The $U$ term forces the model to fit the data (low error), while the $TS$ term forces the model to keep its weights smooth and explore the landscape (regularization). 

### When the Functor Breaks: The Failure of Ensemble Equivalence

Here is where the physics gets deep, and where modern deep learning diverges from classical statistics. 

In standard thermodynamics, we assume that as the number of particles approaches infinity ($N \to \infty$), the Hard (Microcanonical) and Soft (Canonical) ensembles are equivalent. You get the same macroscopic answers either way. 

But **ensemble equivalence breaks** under specific conditions. And these conditions are *exactly* where the most interesting architectures in ML live.

**1. Non-Convexity (Phase Transitions)**
Equivalence breaks when the entropy surface isn't smooth. In deep learning, our loss landscapes are highly non-convex. The "Hard" optimization (trying to find a specific weight configuration with exactly $0$ loss) gets trapped in local minima. The "Soft" optimization (SGD at a finite temperature/learning rate) tunnels through these barriers. They behave fundamentally differently.

**2. Small $N$ (Finite Size Effects)**
Equivalence requires infinite data. In the low-data regime, the "Soft" version (heavy regularization) over-smooths and loses the signal, while the "Hard" version (Empirical Risk Minimization) memorizes the noise. 

**3. Long-Range Correlations (Attention Mechanisms)**
This is the most stunning parallel. Ensemble equivalence assumes parts of a system interact locally. But in systems with gravity, everything interacts with everything. The system becomes non-additive.

> In Machine Learning, this is exactly how **Transformers** work. Every token interacts with every other token regardless of distance. In these models, the Soft (Softmax attention) doesn't just approximate a Hard choice; it creates a complex, interconnected field that a Hard choice (like an N-gram lookup) could never replicate.

### Why This Changes How We Code

When you realize that Hard constraints and Soft penalties are *not* categorically equivalent in deep learning, it changes your approach to architecture design. 

If you use a **Hard Constraint** (e.g., "The weights must sum to 1"), you are in the Microcanonical world. If you use a **Soft Penalty** (e.g., "Add $\lambda \sum w_i$ to the loss"), you are in the Canonical world. 

Because our loss landscapes are non-convex, finite, and long-range, **these are not the same thing**. This is precisely why "Weight Decay" and strictly constrained "L2 Norms" behave differently in Adam vs. SGD—they are literally navigating different physical ensembles.

We don't just use Softmax because it's differentiable. We use it because it maps our discrete logic into a continuous thermodynamic reality, allowing our models to find equilibrium in a complex, non-convex universe. We are no longer just writing code; we are engineering statistical thermodynamics.