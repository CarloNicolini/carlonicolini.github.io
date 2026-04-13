---
layout: post
title: Probabilistic Language Programming, turning craft into solid science
description: "PLP: semantics for LLM scaffolds—traces, proposals, verifiers, branching."
date: 2026-03-01
published: true
categories:
  - science
  - language-physics
---

## Assigning semantic meaning to probabilistic programs

A familiar pattern in modern AI scaffolds is easy to state. Repeat the same prompt, sample several chains of thought, run a judge or verifier, keep the best answer, or retry when the output looks promising.
That template covers much of what people call *agentic AI*—for example Claude Code (its full source code is now public) or [OpenClaw](https://github.com/openclaw).

I call **scaffolds** the prompting setups that place the cognitive component—the LLM—inside a programmatic, deterministic runtime.

Self-consistency, Tree-of-Thoughts, and many agent loops are variations on the same template {% cite wang2022self %} {% cite yao2023tree %}: deterministic scaffolds built on top of a cognitive engine driven by one or more LLMs.

Yet these techniques rest heavily on trial and error. They read more like craft than like science.

In recent work I have tried to narrow that gap. The shift followed a conversation with a friend in reliability engineering outside software: before you improve a compound system, ask what can fail, how failures compose, and what signal actually measures success.

That led to a focused question:

> AI systems still lack a reliability theory in the usual engineering sense. Can we build a mathematical theory of reliable AI in which uncertainty around LLMs is compressed and bounded by clear tools and predictions?

The core issue is not software engineering as such. It is **semantics**: does what we sample from these engines match what we want as the final outcome?
If it does, can we assign a probability that the final result is **correct**?
How does uncertainty in each component compound and propagate?

This post sketches a semantics-first view of inference-time LLM systems that I have been developing. The view rests on **P**robabilistic **L**anguage **P**rogramming (PLP): a framework meant to unify several real-world uses of complex AI systems under one theory.

### The scaffold is the unit

The basic object is not the prompt alone but the **scaffold**: a deterministic host-language program that orchestrates stochastic model calls, tool calls, checks, retries, and aggregation.
A scaffold may be a simple best-of-$K$ loop, a retry-with-judge routine, an agent implemented as a while-loop over LLM calls and tool execution, or a richer tree-search controller.

## Setup

The sections below outline the main ideas of PLP.
A little background in probabilistic programming helps (for example NumPyro, PyMC, or Stan), but it is not required.

Formally, let $\tau$ be the execution trace of a run, and let $\pi_{\mathcal{D}}(\tau \mid x)$ be the proposal law induced by deployment $\mathcal{D}$ on input $x$.
In plain terms, the proposal is direct sampling access to an LLM with a fixed parameter set $\mathcal{D}$.
An LLM maps a string input to a string output. Sampling an answer $y$ from prompt $x$ means

$$
y \propto \pi_{\mathcal{D}}(\tau \mid x).
$$

*Running* the trace forward yields a string $Y=\operatorname{Out}(\tau)$; interpretive meaning lives in a separate projection of the trace, $Z=R(\tau)$.
We may call $R$ the *reward* under a (soft) reinforcement-learning view {% cite blondel2025autoregressive levine2018reinforcement %} or the *energy* under a statistical-physics view.

The trace—not the final string—is the primary unit of analysis.
More precisely, the object of interest is the **distribution** of traces.
A single completion $y$ is one draw from a generator; it does not represent the full distribution.
We need many traces, not a single repetition dressed up as certainty.

We never observe the reference distribution $y \sim \pi_{\rm{ref}}(\cdot \mid x)$ directly for a given prompt $x$.
We can approximate it only through repeated sampling.

### Support before selection

Once you think in traces, the first question is not “how do I pick the best answer?” but “does the scaffold reach the right region at all?” That is the **support** problem.

Let $\Phi(\tau) \ge 0$ be a verifier potential. The **target** distribution reweights the proposal by that potential:

\begin{equation}
p_{\mathcal{D}}(\tau \mid x) \propto \pi_{\mathcal{D}}(\tau \mid x)\,\Phi(\tau, x).
\end{equation}

This proposal–target split matches recent probabilistic treatments of language-model steering, from twisted SMC to sequential Monte Carlo for constrained generation {% cite zhao2024probabilistic %} {% cite loula2025syntactic %}.

The functional form implies that extra sampling from $\pi$ cannot fix missing support.
If correct traces carry almost no mass under $\pi_{\mathcal{D}}$, a sharper judge only rejects wrong candidates more cleanly.

Define a support gap as

\begin{equation}
\text{Gap}_\epsilon(\pi, p^\star; x) = p^\star\!\bigl(\{\,\tau : \pi(\tau \mid x) \le \epsilon\,\} \mid x\bigr).
\end{equation}

When the gap is large, more samples simply repeat the same blind spot.

An optimal-transport view of test-time verification {% cite mukherjee2025test %} refines the picture.
Coverage is not binary; it falls into three regimes.
In a low-coverage **transport regime**, the generator cannot place enough mass on the target.
In a middle **policy-improvement regime**, stronger verification can convert available coverage into lower sub-optimality.
In a high-coverage **saturation regime**, extra coverage barely helps because the verifier or the target geometry limits what selection can do.

That picture suggests when to stop adding branches.
When coverage is tight, rejection-style search is usually appropriate.
When coverage is already broad, best-of-$N$ selection can work. The crossover depends on the verifier’s ROC: a noisy judge can stall the system even when the proposal looks broad on paper.

The practical lesson is simple. Retrieval, decomposition, better context, and prompt edits are **proposal** interventions. Judges and tests are **selection** interventions. Confuse the two and you debug the wrong layer.

### Judges are measurements, not oracles

Many systems rely on an LLM judge, a heuristic grader, or a learned verifier. In PLP, that device is a **measurement channel**, not an oracle.

Let $C \in \{0,1\}$ denote ground-truth correctness and $\widehat{C}$ the judge’s label. The stable object is the channel $\Pr(\widehat{C}\mid C)$, summarized by sensitivity and specificity:

$$
q_1 = \Pr(\widehat{C}=1 \mid C=1), \qquad q_0 = \Pr(\widehat{C}=0 \mid C=0).
$$

The usual ROC quantities follow immediately:

$$
\text{TPR} = \Pr(\widehat{C}=1 \mid C=1) = q_1, \qquad
\text{FPR} = \Pr(\widehat{C}=1 \mid C=0) = 1-q_0,
$$

and the **Youden index** is

$$
J = \text{TPR} - \text{FPR} = q_0 + q_1 - 1.
$$

When the judge is imperfect, the raw positive rate is a biased proxy for true accuracy.
Calibration and reporting matter here, as recent work on LLM-as-a-judge evaluation stresses {% cite lee2025judge %}.
In [another post](2026-03-02-scaffolding-is-all-you-need.md) I show that if the Youden index satisfies $J>0$, a suitable decomposition strategy can raise scaffold reliability—the probability that the task is solved correctly.

The correction is standard:

$$
\widehat{\theta}=
\frac{\widehat{p}_J+\widehat{q}_0-1}{\widehat{q}_0+\widehat{q}_1-1},
\qquad
\widehat{p}_J=\frac{1}{n}\sum_{i=1}^n \widehat{C}_i.
$$

It is the usual judge-calibration story, but it weighs more here because the judge sits inside the system, not beside it.

Stable judge error propagates: the scaffold inherits the bias. If the judge beats chance only weakly, the system can still help—but only if the selection stage is designed for that regime.

### Dependence is the hidden tax

Repeated sampling helps only when the draws are not the same mistake with different wording.
That is the hidden cost behind why self-consistency gains appear only when reasoning paths are genuinely diverse {% cite wang2022self %}.

Let $K$ be the sample count and $\rho$ the pairwise dependence between correctness indicators. A useful summary is the effective sample size

$$
K_{\mathrm{eff}}=\frac{K}{1+(K-1)\rho}.
$$

In short: *more width adds mandatory gates; it does not by itself add alternatives.*

If $\rho$ is high, best-of-$K$ saturates quickly.
The system may look busy while replaying one latent misconception.
That is why some diversity mechanisms help and others do not.
A temperature tweak that only rephrases the same answer is often cosmetic.
A different decomposition, retrieval set, or plan family can cut dependence in a way that changes inference.
Methods that iteratively refine answer distributions—not merely draw more samples—can be read as efforts to spend repeated draws more efficiently {% cite zheng2023progressive %} {% cite pal2024refining %}.

The engineering question is therefore not “can I sample more?” but “what kind of diversity changes the error structure?”

### Trees are not magic

Trees, graphs, multi-agent setups, and branch-and-bound loops are often sold as if depth were the secret.
It is not.
Tree-of-Thoughts, uncertainty-aware tree search, and language-agent tree search instantiate the pattern in different ways, yet all obey the same compositional constraints {% cite yao2023tree %} {% cite mo2023uncertain %} {% cite zhou2024lats %}.

The real split is between **OR** semantics and **AND** semantics. Under OR, one correct branch suffices. Under AND, the task succeeds only if local decisions compose.

Consider a decomposition tree with node-level error budgets $\delta_v$. A conservative global guarantee takes the form

$$
\Pr(\text{final error}) \le \sum_{v} \delta_v \le \Delta.
$$

This is the usual union-bound picture. It is enough for the main point: a tree helps when it replaces one hard global judgment with many smaller judgments, each slightly better than chance.

If subproblems stay coupled in a hidden way, the tree is decorative. If the verifier acts only at the root, the tree can worsen matters by spreading uncertainty across more parts.

Vague “multi-agent” talk therefore buys little. Specify where the proposal changes, where the verifier sits, what independence you assume, and which failure mode should shrink. Without that, the tree is only a metaphor.

### The four failure modes of AI scaffolds

Treating scaffolds as probabilistic programs yields four failure modes. Each calls for a different fix:

1. **Coverage (support) failure.** The proposal $\pi_{\mathcal{D}}$ places little mass on correct traces. Reranking cannot retrieve answers that were never proposed. Intervene on retrieval, context, decomposition, or proposal diversity. In EBM terms, you are sampling the wrong region.
2. **Selection failure.** Correct traces appear among candidates, but the verifier potential $\Phi$ or the judge fails to pick them reliably. The verifier may disagree with ground truth or be too noisy on hard cases. Intervene with judge training, retrieval-augmented rubrics, multi-critic panels, and calibrated thresholds.
3. **Dependence failure.** Repeated samples are not independent evidence: they share a latent misconception, missing evidence, or bias. Majority voting then amplifies a systematic error. Reduce the correlation $\rho$ with diverse prompts, personas, reasoning strategies, model ensembles, or *latent steering*.
4. **Composition failure.** Components look reliable alone, but their interaction breaks global assumptions. Subproblems may couple invisibly; modules may carry conflicting inductive biases; interface mismatches may cascade errors. Audit conditional independencies, add cross-module consistency checks, or re-decompose the task.

Search, voting, decomposition, and verification amplify competence that already lives in the proposal and judge primitives. PLP’s diagnostic role is to map a failure to one of these four modes so you adjust the right lever instead of defaulting to “sample more.”

### Practical checklist

Under this lens, I would write down three objects before tuning compute: the proposal law $\pi$ (model and deployment choices), the verifier potential (verification methods and tools), and the trace projection or reward $R$ that maps execution to task meaning.

Then I would ask, in order: does the proposal cover the right region? Is the judge calibrated enough to trust? Does repeated sampling buy independent evidence? Only after those checks would I spend more compute on search.

That order matters: it stops every failure from looking like a search problem.

The strongest claim is also the shortest: inference-time LLM systems become legible when you treat them as probabilistic programs over auditable traces.
Then you stop asking whether a scaffold is “smart” in the abstract and start asking whether it has the right support, the right verifier, and enough independence for extra compute to pay off.

---

## References

{% bibliography --cited %}
