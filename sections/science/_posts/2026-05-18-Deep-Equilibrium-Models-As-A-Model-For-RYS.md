---
layout: post
title: Deep Equilibrium Models as a model for RYS
description: Using deep-equilibrium-models can be a way to improve the theory behind the CKA-based prediction about which are the best sequences of layers to repeat
date: 2026-05-18
categories:
- science
- deep-learning
published: false
---

In the last two posts I tried to put David Ng's Repeat-Your-Self construction into a geometric language. In [How skip connections define graphs in deep networks]({% link sections/science/_posts/2026-04-28-Skip-connections-and-graph-analysis.md %}) I started from the residual recursion

$$
x_{l+1}=x_l+F_l(x_l)
$$

and treated a Transformer as a weighted directed graph over residual-stream states. In [Similarity of neural networks representations]({% link sections/science/_posts/2026-04-29-Similarity-of-neural-networks-representations.md %}) I replaced raw cosine similarity with linear CKA and found that the central high-similarity plateau of Qwen3.6-27B overlaps with the RYS windows that improve MATH in Ng's intervention map {% cite ng2026rys kornblith2019similarity %}.

That already gives a useful prior: choose RYS windows inside the representational plateau. The prior is still incomplete. High CKA can mean a meaningful iterative computation, or it can mean a block that is close to doing nothing. The next question is therefore sharper:

> Can we predict which high-CKA layer windows are safe and useful to repeat before running the expensive behavioural sweep?

This post proposes a dynamical-systems answer. A good RYS window should behave like a quasi-equilibrium operator: stable enough to be iterated, active enough to refine the representation, and compatible enough with the downstream decoder that the final logits remain calibrated.

The analogy is Deep Equilibrium Models (DEQs), where a network is defined by a fixed point

$$
z^{\star} = f_\theta(z^{\star},x)
$$

instead of a fixed, explicit stack of distinct layers. A DEQ asks for a self-consistent latent state. RYS gives us a different object, because the model was trained as a finite feed-forward Transformer and the repeated block is a finite sequence of distinct layers. Still, the central RYS observation smells like equilibrium dynamics: some middle layer blocks can be traversed more than once, and the model becomes better at some reasoning tasks without changing a single weight.

The safe claim is a quasi-DEQ hypothesis:

> Benchmark-positive RYS windows are finite Transformer blocks whose composition acts as an iteratable refinement map on a central representational manifold.

The rest of the post turns that sentence into mathematical predictions and empirical tests.

## From a Layer Window to an Iterated Operator

Fix a contiguous block of residual layers

$$
B=[i,j)
$$

and write its composite map as

$$
T_B
= T_{j-1}\circ T_{j-2}\circ \cdots \circ T_i,
\qquad
T_l(x)=x+F_l(x).
$$

The base model applies this block once:

$$
z_0=x_i,\qquad z_1=T_B(z_0),\qquad x_j=z_1.
$$

RYS applies the same block twice:

$$
z_2=T_B(z_1)=T_B(T_B(z_0)).
$$

The natural generalisation is the iterated trajectory

$$
z_{n+1}=T_B(z_n).
$$

This is the object we should study. A duplicated block succeeds when the sequence

$$
z_0,z_1,z_2,\ldots
$$

stays near the internal manifold expected by the later layers while continuing to move in directions that help the task.

The DEQ comparison gives two immediate diagnostics. First, if the trajectory is near a fixed point, then the increments

$$
\Delta_n(B)
=
\frac{\|z_{n+1}-z_n\|_F}{\|z_n\|_F}
$$

should shrink or remain controlled. Second, if the repeated block preserves the internal geometry, then the representation similarity

$$
\mathrm{CKA}(z_{n+1},z_n)
$$

should remain high for the first few iterations.

A block that has high CKA and a vanishing $$\Delta_0$$ is probably inert. A block with high CKA, measurable $$\Delta_0$$, and controlled $$\Delta_1/\Delta_0$$ is the interesting case. That is the regime where the second traversal can act as extra refinement instead of arbitrary drift.

## The Goldilocks Window

The previous CKA post derived the plateau approximation

$$
1-\mathrm{CKA}_{ij}
\approx
\frac{1}{2}\mathcal Q_{i,j}^2\sin^2\Psi_{i,j}
$$

where $$\mathcal Q_{i,j}$$ measures the kernel-level size of the residual perturbation and $$\Psi_{i,j}$$ measures its angle relative to the existing similarity geometry.

This immediately creates a Goldilocks condition for RYS:

$$
0 < 1-\mathrm{CKA}_{ij} \ll 1.
$$

The lower bound matters because a perfectly unchanged representation has no extra computation to harvest. The upper bound matters because a large representational jump is likely to move the model out of the distribution that the downstream decoder expects.

The same idea can be written with the residual force

$$
\rho_{i,j}
=
\frac{\|S_{i,j}\|_F}{\|x_i\|_F},
\qquad
S_{i,j}=\sum_{k=i}^{j-1}F_k(x_k).
$$

Useful RYS windows should have small but measurable $$\rho_{i,j}$$: small enough for the second pass to remain on-manifold, large enough to make the doubled residual meaningful.

This is the first place where the DEQ analogy becomes operational. DEQs need an update map that is sufficiently stable to converge. RYS needs a block map whose first few iterates are stable enough to remain decodable.

## Mathematical Prediction 1: Quadratic Amplification with Repeat Count

The earlier post showed that duplicating a small-residual block approximately doubles the cumulative residual and therefore quadruples the CKA deviation:

$$
1-\mathrm{CKA}^{\mathrm{RYS}}_{ij}
\approx
4(1-\mathrm{CKA}^{(0)}_{ij}).
$$

The iterated-operator view predicts the natural extension. If the repeated block is locally stationary across the first $$n$$ traversals, then

$$
z_n
\approx
z_0+nS_B(z_0)
$$

for $$n\rho_B \ll 1$$. Substituting this into the same small-residual expansion gives

$$
\boxed{
1-\mathrm{CKA}(z_n,z_0)
\approx
n^2\left(1-\mathrm{CKA}(z_1,z_0)\right).
}
$$

This is a clean mathematical prediction. In a good quasi-equilibrium window, the early repeat-count curve should be quadratic in $$n$$. In an unstable window, the curve should bend upward faster than $$n^2$$. In an inert window, it should stay near numerical noise.

This gives a cheap pre-benchmark test: apply each candidate block 1, 2, 3, and 4 times on a small prompt set, then fit

$$
1-\mathrm{CKA}(z_n,z_0)
\sim
an^2.
$$

The windows worth evaluating should be those with good quadratic fit, nonzero $$a$$, and no early collapse in final-logit quality.

## Mathematical Prediction 2: Contraction of Successive Updates

Near a fixed point $$z^\star$$, write

$$
e_n=z_n-z^\star.
$$

Linearising the block map gives

$$
e_{n+1}
\approx
J_B(z^\star)e_n,
\qquad
J_B=\frac{\partial T_B}{\partial z}.
$$

If the dominant singular value of $$J_B$$ is below one in the directions explored by the prompt distribution, then the distance to the local equilibrium shrinks. We do not need a perfect global contraction. RYS only asks for a few stable iterates in the region reached by natural prompts.

The measurable version is

$$
r_n(B)
=
\frac{\Delta_{n+1}(B)}{\Delta_n(B)}.
$$

The prediction is:

$$
r_n(B) < 1
\quad\text{or at least}\quad
r_n(B)\approx 1
$$

for high-performing middle blocks. Decoder blocks and boundary-crossing blocks should show larger or more erratic ratios.

This also explains why single-layer duplication often fails in Ng's experiments. A single layer has little internal diameter. It can perturb the stream, but it does not expose a full refinement circuit. A block has a multi-step residual sub-DAG, and the second traversal can reuse that sub-DAG as a coherent operator.

## Mathematical Prediction 3: Decoder Tolerance Bounds the Benefit

Stability inside the block is necessary. It is not sufficient.

The downstream layers consume $$x_j$$ during ordinary inference. After RYS they receive $$z_2$$. A useful repeated block must keep $$z_2$$ close enough to the base layer-$$j$$ distribution for the decoder to operate normally.

One simple diagnostic is

$$
D_{\mathrm{dec}}(B)
=
1-\mathrm{CKA}(z_2,x_j).
$$

Another is the logit KL divergence between the base and repeated model:

$$
D_{\mathrm{KL}}
\left(
p_{\mathrm{base}}(\cdot\mid x)
\;\|\;
p_{\mathrm{RYS}(B)}(\cdot\mid x)
\right).
$$

The prediction is a bounded-change regime. Good RYS windows should create visible movement inside the reasoning block while keeping final-logit KL moderate. Very low KL means the intervention did almost nothing. Very high KL means the model is no longer following its learned decoding path.

This suggests a second Goldilocks condition:

$$
\Delta_0(B)>0,
\qquad
r_0(B)\leq 1+\epsilon,
\qquad
D_{\mathrm{dec}}(B)\leq \tau,
\qquad
D_{\mathrm{KL}}(B)\in[\kappa_{\min},\kappa_{\max}].
$$

The constants $$\epsilon,\tau,\kappa_{\min},\kappa_{\max}$$ should be fit on a small calibration model, then frozen before testing larger models.

## A Pre-Benchmark RYS Score

Putting the pieces together, a candidate score for a window $$B=[i,j)$$ is

$$
\mathrm{Score}(B)
=
\underbrace{P(B)}_{\text{plateau}}
\cdot
\underbrace{A(B)}_{\text{activity}}
\cdot
\underbrace{S(B)}_{\text{stability}}
\cdot
\underbrace{D(B)}_{\text{decoder tolerance}}.
$$

One concrete version is:

$$
P(B)=\exp\left[-\alpha(1-\mathrm{CKA}(x_i,x_j))\right],
$$

$$
A(B)=\frac{\Delta_0(B)}{\Delta_0(B)+c},
$$

$$
S(B)=\exp\left[-\beta\max(0,r_0(B)-1)\right],
$$

$$
D(B)=\exp\left[-\gamma D_{\mathrm{dec}}(B)-\eta D_{\mathrm{KL}}(B)\right].
$$

The form is deliberately boring. The goal is not to learn a complicated predictor from many behavioural sweeps. The goal is to rank windows from a few forward passes and then see whether the top-ranked windows overlap with Ng-style benchmark improvements.

The falsifiable claim is:

> The top decile of $$\mathrm{Score}(B)$$, computed without benchmark labels, should contain a statistically significant enrichment of benchmark-positive RYS windows.

That is the bridge from representation geometry to behavioural prediction.

## Empirical Prediction 1: Three Classes of High-CKA Blocks

The quasi-DEQ view predicts that high CKA windows split into three classes.

**Inert plateaus.** These have

$$
1-\mathrm{CKA}\approx 0,
\qquad
\Delta_0\approx 0.
$$

Repeating them should have little effect.

**Iterative refinement blocks.** These have

$$
1-\mathrm{CKA}\ll 1,
\qquad
\Delta_0>0,
\qquad
r_0\leq 1+\epsilon.
$$

These are the best RYS candidates.

**Fragile high-similarity blocks.** These look stable under one comparison, yet their second or third iteration reveals drift:

$$
r_0>1
\quad\text{or}\quad
D_{\mathrm{KL}}\gg 0.
$$

These should degrade when repeated, especially near the decoder.

This is important because the current CKA plateau prior treats many high-similarity windows as equally plausible. The iterated-block diagnostics should separate passive similarity from useful computational recurrence.

## Empirical Prediction 2: Repeat Count Should Be Unimodal

If RYS extends a stable refinement dynamic, increasing the repeat count should initially help and then saturate or degrade.

For a good block $$B$$, benchmark performance as a function of repeat count $$n$$ should look roughly like:

$$
\mathrm{Perf}(n)
=
\mathrm{Perf}(1)
+ a(n-1)
- b(n-1)^2
+ \epsilon_n,
\qquad
a>0,\ b>0.
$$

The optimum might be at $$n=2$$, as in the original RYS construction, or at $$n=3$$ for smaller models. The key prediction is unimodality. A monotone increase across many repeats would point toward ordinary test-time compute scaling. Immediate degradation at $$n=2$$ would falsify the refinement interpretation for that block.

This is also a way to distinguish RYS from prompt-level chain-of-thought. Chain-of-thought gives the model more autoregressive steps. RYS gives the residual stream more internal refinement time before the next token distribution is read out.

## Empirical Prediction 3: The Best Blocks Should Be Task-Stable

The CKA post found that GSM8K and MMLU-Philosophy produce nearly the same large-scale layer anatomy. The quasi-DEQ hypothesis predicts a similar cross-task stability for the best windows.

The exact benchmark gain can remain task-specific. The candidate set should be stable:

$$
\mathrm{TopK}_{\mathrm{Score}}(\mathrm{GSM8K})
\cap
\mathrm{TopK}_{\mathrm{Score}}(\mathrm{MMLU})
$$

should be much larger than chance.

If a window scores highly only on one narrow prompt distribution, it may be exploiting a task-specific activation regime. If it scores highly across arithmetic, philosophy, code, and multilingual prompts, it is more likely to be part of the model's central reusable computation.

## Experiments to Run Next

The research path is straightforward.

### 1. Iterated-block probes without benchmarks

For each window $$B=[i,j)$$, run the base model once, cache $$x_i$$, and apply $$T_B$$ repeatedly for $$n=1,\ldots,4$$. Measure:

- $$\Delta_n(B)$$
- $$r_n(B)=\Delta_{n+1}/\Delta_n$$
- $$\mathrm{CKA}(z_n,z_0)$$
- $$\mathrm{CKA}(z_{n+1},z_n)$$
- $$D_{\mathrm{dec}}(B)=1-\mathrm{CKA}(z_2,x_j)$$
- final-logit KL against the base model

This experiment is cheap compared with a full benchmark sweep. It should already reject most windows.

### 2. Quadratic CKA amplification test

For each candidate, fit

$$
1-\mathrm{CKA}(z_n,z_0)=an^2+bn+c.
$$

The quasi-stationary theory predicts $$a>0$$, small $$b$$, and a good fit for the first few repeats. A large linear or super-quadratic residual indicates that the residual field is changing across traversals.

### 3. Jacobian stability by JVP/VJP

Estimate the dominant singular values of the block Jacobian $$J_B$$ with power iteration using Jacobian-vector and vector-Jacobian products. The full Jacobian is too large to materialise, but the leading spectrum is enough.

Prediction:

- good RYS blocks have controlled prompt-conditioned singular values;
- decoder blocks have larger anisotropic amplification;
- encoder-to-reasoning junction blocks may show structured expansion with a spectrum that differs from isotropic chaos.

The last case is especially interesting because the previous CKA analysis found a secondary peak near the encoder-to-reasoning boundary. That peak may require a separate junction theory instead of the plateau approximation.

### 4. Blinded benchmark validation

Freeze the scoring rule before looking at benchmark deltas. Pick:

- the top $$K$$ windows by $$\mathrm{Score}(B)$$;
- $$K$$ random high-CKA windows;
- $$K$$ random low-CKA windows;
- Ng's known best windows as positive controls when available.

Then run GSM8K, MATH, MuSR, and one non-reasoning control such as IFEval. The main statistical test is enrichment: top-score windows should contain more positive deltas than the matched high-CKA baseline.

### 5. Cross-model replication

Repeat the pipeline on smaller models first: Qwen, Llama, Mistral, and Gemma families. The strongest version of the hypothesis predicts that the exact layer numbers change, while the dynamical signature remains:

$$
\text{high CKA}
+ \text{nonzero update}
+ \text{controlled repeat dynamics}
+ \text{decoder tolerance}
\Rightarrow
\text{higher chance of RYS gain}.
$$

If the signature fails outside one model family, the RYS phenomenon may depend on architecture-specific training details. That outcome would still be useful.

## What Would Falsify This?

The hypothesis is easy to wound.

First, if high-scoring quasi-equilibrium windows fail to outperform random high-CKA windows, then CKA plus stability does not explain RYS. Second, if benchmark-positive windows have expanding $$\Delta_n$$, large decoder KL, or poor repeat-count curves, then the DEQ analogy is misleading. Third, if the best windows are consistently boundary-crossing instead of plateau-internal, the main action lies in phase transitions between modules instead of central iterative refinement.

The most decisive falsifier would be a model where the full pipeline gives a clean central plateau, controlled block dynamics, and a high predicted score, yet RYS duplication reliably hurts reasoning benchmarks. That would mean representational stability is compatible with behavioural degradation, forcing the theory to include information that CKA and local dynamics cannot see.

## Why This Matters

The practical goal is modest: reduce the $$O(L^2)$$ RYS search space to a short list of layer windows selected from a single activation pass and a few local repeat probes.

The scientific goal is more interesting. If the prediction works, then some Transformer middle blocks behave like finite, learned relaxation operators. Their role in reasoning would be closer to iterative refinement on a semantic manifold than to a one-way sequence of unrelated transformations.

That would connect four observations that currently live in separate boxes:

- residual networks approximate stable flows in the small-update regime {% cite marion2023implicit %};
- CKA exposes broad representational plateaus in trained models {% cite kornblith2019similarity davari2022reliability %};
- block-recurrent structure can recover much of a deep model's computation in vision models {% cite jacobs2025blockrecurrent %};
- RYS improves some language-model benchmarks by repeating selected middle blocks {% cite ng2026rys %}.

The DEQ lens adds one more piece: repeated computation can be understood as motion toward a self-consistent state. RYS gives us a way to ask whether ordinary feed-forward Transformers have already learned local pieces of that dynamics.

My current bet is that the answer is yes, but only in a weak and local sense. The central plateau is unlikely to be a true fixed-point solver. It may still contain blocks whose first two or three iterates act like a stable refinement process. That is enough for RYS to work, and it is enough to make a falsifiable prediction:

> The best RYS windows should be the high-CKA blocks whose repeated trajectories are stable, non-inert, and decodable.

The next experiment is to rank windows by that sentence before looking at the benchmark map.

---

## References

{% bibliography --cited %}
