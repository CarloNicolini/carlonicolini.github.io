---
layout: post
title: Soft values, symmetry breaking, and random rooted trees
description: "A conjectural branching law for scaffolds from Blondel's soft values and Kappen's path-integral control."
date: 2026-04-02
published: true
categories:
  - science
  - language-physics
---

## A missing local law

Recent posts explored two aspects of recursive scaffolding.
[Probabilistic Language Programming]({% link sections/science/_posts/2026-03-01-Probabilistic-Language-Programming.md %}) defined a verifier-reweighted law over traces.
[Scaffolding is all you need]({% link sections/science/_posts/2026-03-02-Scaffolding-is-all-you-need.md %}) modeled recursive scaffolds as random rooted trees, demonstrating that branching does not automatically increase reliability.

However, a local probabilistic law remains missing.
Given a continuation value $V(s)$ for each prefix $s$, how does this value determine whether the node answers, decomposes, or waits?

Two distinct fields suggest a unified answer.
Blondel et al. demonstrate that autoregressive models and energy-based models are functionally equivalent; next-token prediction implicitly contains a future-looking soft value term {% cite blondel2025autoregressive %}.
Conversely, Kappen formulates the stochastic cost-to-go as a log partition function, showing that multimodal control exhibits symmetry breaking and delayed choice {% cite kappen2005linear kappen2005path %}.

We propose a simple conjecture:

> A recursive scaffold is a random rooted tree where soft continuation values drive the local branching law.

This note outlines a useful theoretical template rather than a formal theorem.

## The global object

Consider a deployment setup $\mathcal{D}$, an input prompt $x$, a complete execution trace $\tau$, and a trace prefix $s$.
The PLP target distribution is:

$$
p_{\mathcal{D}}(\tau \mid x)
\propto
\pi_{\mathcal{D}}(\tau \mid x)\Phi(\tau,x),
$$

where $\pi_{\mathcal{D}}(\tau \mid x)$ represents the proposal law induced by the deployed scaffold and $\Phi(\tau,x)\ge 0$ is the verifier potential.

For a prefix $s$, we define the continuation partition $Z(s)$ and the continuation value $V(s)$:

$$
Z(s)
:=
\sum_{\tau \succ s}\pi_{\mathcal{D}}(\tau \mid s)\Phi(\tau),
\qquad
V(s):=\log \left( Z(s) \right),
$$

where $\tau \succ s$ indicates that the complete trace $\tau$ extends $s$.
The continuation value $V(s)$ quantifies the future verifier-weighted mass reachable from $s$.

Previous posts argued for estimating $V(s)$ at inference time.
Blondel et al. theoretically justify this approach: in their ARM/EBM equivalence, local autoregressive decisions naturally incorporate a future-looking soft value term acting as a soft Bellman summary {% cite blondel2025autoregressive %}.
Crucially, because teacher-forcing pre-training solves the underlying backward dynamic programming problem, the autoregressive forward pass intrinsically caches this future energy. The model therefore provides a 1-step lookahead value without requiring explicit inference-time rollouts.
Similarly, Kappen's path-integral formulation derives the stochastic cost-to-go as a log partition over future trajectories rather than a myopic local score {% cite kappen2005linear kappen2005path %}.

## A soft Bellman branching process

Given a prefix $s$, assume the scaffold can perform two types of local moves:

- **Direct-answer:** A family $\mathcal{Y}(s)$ of terminal answers $y$.
- **Decomposition:** A family $\mathfrak{D}(s)$ of admissible decompositions $D=(s_1,\ldots,s_k)$.

A decomposition $D$ is a tuple of child prefixes.
Selecting $D$ transforms the current node into an internal node with $k=|D|$ children.

Let $q_{\mathrm{ans}}(y \mid s)$ denote the local proposal weight for answering directly with $y$, and let $w_{\mathrm{ans}}(y,s)\ge 0$ denote the verifier weight attached to that answer.
We define the direct-answer partition $Z_{\mathrm{ans}}(s)$ and its corresponding value $V_{\mathrm{ans}}(s)$:

$$
Z_{\mathrm{ans}}(s)
:=
\sum_{y\in \mathcal{Y}(s)}
q_{\mathrm{ans}}(y \mid s)\,
w_{\mathrm{ans}}(y,s),
\qquad
V_{\mathrm{ans}}(s):=\log \left( Z_{\mathrm{ans}}(s) \right).
$$

Next, let $q_{\mathrm{dec}}(D \mid s)$ represent the proposal weight for a decomposition $D\in \mathfrak{D}(s)$.
We introduce a local tax $\Lambda(s,D)\ge 0$ for decomposition.
This tax absorbs costs not reflected in the child values, such as compute cost, decomposition invalidity, or composition fragility.

Assuming the child subtrees are conditionally independent given $D$, we approximate the decomposition partition $Z_{\mathrm{dec}}(s)$ as:

\begin{equation}
Z_{\mathrm{dec}}(s)
:=
\sum_{D\in \mathfrak{D}(s)}
q_{\mathrm{dec}}(D \mid s)\,
\exp \left(-\Lambda(s,D)\right)
\prod_{i=1}^{|D|} \exp \left(V(s_i)\right).
\label{eq:dec_partition}
\tag{1}
\end{equation}

Equivalently, we can write:

$$
Z_{\mathrm{dec}}(s)
=
\sum_{D\in \mathfrak{D}(s)}
q_{\mathrm{dec}}(D \mid s)\,
\exp \left(\sum_{i=1}^{|D|}V(s_i)-\Lambda(s,D)\right),
\qquad
V_{\mathrm{dec}}(s):=\log \left( Z_{\mathrm{dec}}(s) \right).
$$

The natural recursive closure combines both branches:

$$
Z(s)\approx Z_{\mathrm{ans}}(s)+Z_{\mathrm{dec}}(s),
\qquad
V(s)\approx \log \left(Z_{\mathrm{ans}}(s)+Z_{\mathrm{dec}}(s)\right).
\label{eq:soft-bellman-tree}
\tag{2}
$$

Equation \eqref{eq:soft-bellman-tree} forms the core conjecture of this theory: a soft Bellman recursion for recursive scaffolds.
The direct-answer branch contributes terminal mass, while each decomposition contributes the product of child masses corrected by the local tax.

This recursion directly yields the node probabilities. The probability of answering directly is:

$$
\mathbb{P}(M=\mathrm{ans}\mid s) \approx \frac{Z_{\mathrm{ans}}(s)}{Z_{\mathrm{ans}}(s)+Z_{\mathrm{dec}}(s)} = \exp \left(V_{\mathrm{ans}}(s)-V(s)\right).
$$

For a specific decomposition $D$, the probability is:

$$
\mathbb{P}(M=\mathrm{dec},D \mid s) \approx \frac{q_{\mathrm{dec}}(D \mid s)\, \exp \left(\sum_{i=1}^{|D|}V(s_i)-\Lambda(s,D)\right)}{ \exp \left(V(s)\right)}.
\label{eq:local-dec-law}
\tag{3}
$$

Equation \eqref{eq:local-dec-law} translates soft values into a local branching law.
Consequently, the scaffold operates as a random rooted tree where each internal node samples its offspring from this distribution.

## Tree geometry from soft values

Two local metrics summarize the tree's geometry.

First, the expected offspring number at $s$ acts as the local branching ratio:

$$
m(s) := \sum_{D\in \mathfrak{D}(s)} \mathbb{P}(M=\mathrm{dec},D \mid s)\,|D|.
$$

If $m(s)\approx 0$, the node effectively functions as a leaf.
If $m(s)\gg 1$, the tree rapidly expands.

Second, conditional on deciding to decompose, we define the normalized decomposition law:

$$
\mathbb{P}(D \mid s,\mathrm{dec})
:=
\frac{
q_{\mathrm{dec}}(D \mid s)\,
\exp \left(\sum_{i=1}^{|D|}V(s_i)-\Lambda(s,D)\right)
}{
Z_{\mathrm{dec}}(s)
}.
$$

The inverse participation ratio of this law yields the effective number of decomposition basins:

$$
N_{\mathrm{eff}}(s) := \frac{1}{\sum_{D\in \mathfrak{D}(s)} \mathbb{P}(D \mid s,\mathrm{dec})^2 }.
$$

These two metrics capture distinct properties:

- $m(s)$ measures the drive to expand.
- $N_{\mathrm{eff}}(s)$ quantifies the number of qualitatively distinct, viable decomposition skeletons.

For example, a node might strongly favor decomposition ($m(s)$ is large) but possess only one dominant skeleton ($N_{\mathrm{eff}}(s)\approx 1$).
Conversely, a node might exhibit a modest expected width while distributing mass across several comparable basins.

## Symmetry breaking and delayed commitment

Kappen's multimodal control experiments demonstrate a crucial qualitative behavior: when multiple trajectories remain viable, an optimal stochastic controller delays commitment.
Instead of deciding early, the controller maintains probability mass near a symmetric center. It breaks symmetry only when the geometry of future paths clarifies {% cite kappen2005path %}.

In Kappen's multimodal Laplace approximation, the control-side soft value exhibits a log-sum-exp structure:

$$
J(\xi,t)\approx -\lambda \log \left( \sum_{\alpha}\exp \left(-\frac{S_{\alpha}(\xi,t)}{\lambda}\right) \right),
$$

where $\alpha$ indexes competing deterministic strategies, and $S_{\alpha}(\xi,t)$ represents the action of strategy $\alpha$ from state $\xi$ at time $t$ {% cite kappen2005path %}.
Symmetry breaks precisely when one strategy dominates the mixture.

Equation \eqref{eq:local-dec-law} predicts identical behavior for scaffold trees.
If several decomposition tuples $D$ yield similar scores,

$$
\sum_{i=1}^{|D|}V(s_i)-\Lambda(s,D),
$$

then $\mathbb{P}(D \mid s,\mathrm{dec})$ remains broad and $N_{\mathrm{eff}}(s)>1$.
Under these conditions, the optimal move preserves options rather than collapsing prematurely onto a single skeleton.

As information accumulates and conditions sharpen, a single decomposition tuple may dominate, driving $N_{\mathrm{eff}}(s)\to 1$.
This transition represents a discrete analogue of symmetry breaking: the tree shifts from exploring many viable skeletons to committing to just one.

This control interpretation provides a practical heuristic:

- **High uncertainty or long horizons:** Keep multiple decomposition basins active.
- **Low uncertainty or short horizons:** Allow a single skeleton to dominate and commit.

Kappen terms this phenomenon *delayed choice*; in the context of recursive scaffolds, we call it *delayed commitment*.

## Temperature, horizon, and phase transitions

We can generalize this framework using a tempered target distribution:

$$
p_{\beta}(\tau \mid x)
\propto
\pi_{\mathcal{D}}(\tau \mid x)\Phi(\tau,x)^{\beta},
\qquad
0\le \beta \le 1.
$$

For a prefix $s$, we define the tempered continuation partition $Z_{\beta}(s)$ and value $V_{\beta}(s)$:

$$
Z_{\beta}(s)
:=
\sum_{\tau \succ s}\pi_{\mathcal{D}}(\tau \mid s)\Phi(\tau)^{\beta},
\qquad
V_{\beta}(s):=\log \left( Z_{\beta}(s) \right).
$$

Consequently, all local metrics become $\beta$-dependent.
The direct-answer objects update to:

$$
Z_{\mathrm{ans},\beta}(s)
:=
\sum_{y\in \mathcal{Y}(s)}
q_{\mathrm{ans}}(y \mid s)\,
w_{\mathrm{ans}}(y,s)^{\beta},
\qquad
V_{\mathrm{ans},\beta}(s):=\log \left( Z_{\mathrm{ans},\beta}(s) \right).
$$

The decomposition objects update to:

$$
Z_{\mathrm{dec},\beta}(s)
:=
\sum_{D\in \mathfrak{D}(s)}
q_{\mathrm{dec}}(D \mid s)\,
\exp \left(\sum_{i=1}^{|D|}V_{\beta}(s_i)-\beta \Lambda(s,D)\right),
\qquad
V_{\mathrm{dec},\beta}(s):=\log \left( Z_{\mathrm{dec},\beta}(s) \right).
$$

The normalized conditional law becomes:

$$
\mathbb{P}_{\beta}(D \mid s,\mathrm{dec})
\propto
q_{\mathrm{dec}}(D \mid s)\,
\exp \left(\sum_{i=1}^{|D|}V_{\beta}(s_i)-\beta \Lambda(s,D)\right).
$$

At low $\beta$, the local law remains diffuse, encouraging exploration.
At high $\beta$, the law sharpens, driving exploitation.
This mechanism mirrors the role of temperature in stochastic control and maximum-entropy reinforcement learning {% cite levine2018reinforcement kappen2005path %}.

Two specific diagnostics guide local decisions:

$$
\Delta_{\beta}(s)
:=
V_{\mathrm{dec},\beta}(s)-V_{\mathrm{ans},\beta}(s)
$$

and

$$
N_{\mathrm{eff},\beta}(s)
:=
\frac{1}{\sum_{D}\mathbb{P}_{\beta}(D \mid s,\mathrm{dec})^2 }.
$$

These quantities delineate three distinct decision regimes:

1. **Answer directly:** If $\Delta_{\beta}(s)<0$, the node lacks sufficient future value to justify the decomposition tax.
2. **Delay commitment:** If $\Delta_{\beta}(s)>0$ and $N_{\mathrm{eff},\beta}(s)>1$, the node should decompose or search without committing to a single skeleton.
3. **Commit:** If $\Delta_{\beta}(s)>0$ and $N_{\mathrm{eff},\beta}(s)\approx 1$, symmetry has broken, making commitment rational.

This local decision rule effectively unifies Blondel's soft values with Kappen's delayed-choice dynamics.

## Estimating probabilities in practice

To apply this theory, we must estimate the true continuation value $V(s)$. Let $\widehat{V}(s)$ denote this estimator.

We can define a practical, plug-in version of the tree law:

$$
\widehat{\mathbb{P}}(M=\mathrm{dec},D \mid s)
\propto
q_{\mathrm{dec}}(D \mid s)\,
\exp \left(\sum_{i=1}^{|D|}\widehat{V}(s_i)-\Lambda(s,D)\right).
$$

Researchers can derive the estimate $\widehat{V}(s)$ from various sources:

- A direct read of the internalized model logits, computing an intensive average like MellowMax over the one-step vocabulary to eliminate the severe length-bias intrinsic to raw extensive log-partitions.
- A learned soft-value head or logit correction {% cite blondel2025autoregressive %}.
- Verifier-weighted rollouts that approximate $Z(s)$ directly.
- Tree search, Sequential Monte Carlo (SMC), or importance-weighted sampling over future traces.
- A local critic calibrated against downstream verifier success.

Similarly, we must estimate the local tax $\Lambda(s,D)$.
This term isolates the friction of decomposition independent of child values, encompassing factors like decomposition validity, interface clarity, composition risk, and computational overhead.

Accounting for this tax prevents trivial expansion.
A scaffold should branch only when the combined promise of its children strictly outweighs the local decomposition tax.

## Testable predictions

A robust theory must offer falsifiable predictions. Our framework predicts the following scaffold behaviors:

1. Performance gains from decomposition correlate more strongly with $N_{\mathrm{eff}}(s)$ than with the raw number of sampled children.
2. Early commitment causes failures primarily when $\Delta_{\beta}(s)>0$ and $N_{\mathrm{eff},\beta}(s) \gg 1$.
3. As the computational horizon shrinks or the verifier temperature increases, the tree collapses from a broad exploratory frontier into a single dominant skeleton.
4. AND-style decompositions succeed only when the local tax $\Lambda(s,D)$ is sufficiently small to preserve child value gains.

Researchers can directly measure and test these hypotheses in empirical deployments.

## Limitations

We acknowledge several approximations in this framework:

- The child-independence assumption in Equation \eqref{eq:dec_partition} may fail if subtasks are highly entangled.
- The candidate set $\mathfrak{D}(s)$ might omit the optimal decomposition.
- The value estimator $\widehat{V}(s)$ inherits the biases of an imperfect verifier.
- Empirical phase transitions may blur due to estimation noise and strict budget constraints.

We therefore present these equations as a control-theoretic approximation rather than an exact semantics for all recursive architectures.

## Conclusion

Although Blondel et al. and Kappen analyze disparate systems, their local mathematics converge.
A myopic heuristic is insufficient; robust local decisions require a soft value over future continuations.

From this perspective, a recursive scaffold is not merely a branching prompt.
It is a random rooted tree whose geometry is entirely dictated by soft continuation values.
These values govern whether the tree stops, widens, or collapses.
Furthermore, they mathematically explain why effective scaffolds delay commitment during early uncertainty before crystallizing into a single dominant strategy.

This soft Bellman branching process supplies the missing local control law for recursive, inference-time scaffolding.

---

## References

{% bibliography --cited %}
