---
layout: post
title: Probabilistic Language Programming
date: 2026-03-01
published: true
---


## Probabilistic Language Programming

A familiar pattern in LLM systems is simple enough: sample a few trajectories, run a judge, keep the best one, maybe retry if the answer looks ok.

The popular hope is that enough branches, enough agents, or enough retries will turn uncertainty into reliability.

*That hope is too vague to be a theory.*
What matters instead is semantics: what is being sampled, what is being verified, which signal is noisy, and where dependence quietly eats the value of extra compute.

This post sketches a semantics-first view of inference-time LLM systems: the trace law induced by a scaffold, the proposal-target split, why support comes before selection, why judge outputs are measurements rather than truth, and why trees help only when they actually decompose the task.

### A scaffold is the unit

The basic object is not the prompt in isolation. It is the **scaffold**: a deterministic host-language program that orchestrates stochastic model calls, tool calls, checks, retries, and aggregation.
A scaffold can be an agent (just a while loop over LLM calls with tool execution), or any other more complex architecture involving LLM sampling at multiple sites, like in recursive language modeling for example.

## Setup

Formally, let $\tau$ be the execution trace of a run, and let $q_{\mathcal{D}}(\tau \mid x)$ be the proposal law induced by deployment $\mathcal{D}$ on input $x$.
The run produces an output string $Y=\operatorname{Out}(\tau)$, but the task meaning usually lives in a separate projection $Z=\pi(\tau)$.

$$
\Omega \to \tau \to (Y, Z)
$$

That is the usual control flow of an agent, stripped to its basic semantics.
The trace is the real unit of analysis, not the final string.

Think about it.
A single model completion is like sampling one point from a random generator and pretending you learned the whole distribution. You did not. You are interested in the trace of sampling over multiple repetitions.
Since you have only access to an imaginary reference distribution $y \sim \pi_{\rm{ref}}(\cdot \mid x)$ given a prompt $x$, the only way to access it is via repeated sampling.

### Support before selection

Once you think in traces, the first question is not “how do I pick the best answer?” but “does the scaffold even reach the right region?” This is the support problem.

Let $\Phi(\tau) \ge 0$ be a verifier potential. The **target** distribution is the proposal reweighted by that potential:

$$
p_{\mathcal{D}}(\tau \mid x) \propto q_{\mathcal{D}}(\tau \mid x)\,\Phi(\tau, x).
$$

The slogan is blunt: *extra selection cannot rescue missing support.* If the correct traces are nearly absent from $q_{\mathcal{D}}$, then a better judge only gives you a more precise way of rejecting the wrong things.

One useful way to say this is with a support gap:

$$
\text{Gap}_\epsilon(q, p^\star; x) = p^\star\!\bigl(\{\,\tau : q(\tau \mid x) \le \epsilon\,\} \mid x\bigr).
$$

When that gap is large, more samples just give you more shots at the same blind spot.

A recent optimal-transport view of test-time verification (see reference 1 below) sharpens this point. 
Coverage is not a binary property; it moves through three regimes. 
In a low-coverage **transport regime**, the main problem is simply that the generator cannot reach enough of the target mass. 
In a middle **policy-improvement regime**, better verification can turn the available coverage into lower sub-optimality. 
In a high-coverage **saturation regime**, extra coverage stops changing much because the verifier or the target geometry has already become the bottleneck.

That picture is useful because it tells you when to stop asking for more branches. 
When coverage is tight, rejection-style search is usually the right instinct. When coverage is already broad, best-of-$N$ style selection can work well. The exact crossover depends on the verifier’s ROC: a noisy judge can leave you stuck even when the proposal is broad enough on paper.

The practical implication is straightforward. Retrieval, decomposition, better context construction, and prompt changes are proposal interventions. Judges and tests are selection interventions. If you confuse the two, you will debug the wrong layer.

### Judges are measurements, not oracles

Many systems use an LLM judge, a heuristic grader, or a learned verifier. In PLP, that is a **measurement channel**, not an oracle.

Write $C \in \{0,1\}$ for ground-truth correctness and $\widehat{C}$ for the judge’s label. The stable object is the channel $\Pr(\widehat{C}\mid C)$, summarized by sensitivity and specificity:

$$
q_1 = \Pr(\widehat{C}=1 \mid C=1), \qquad q_0 = \Pr(\widehat{C}=0 \mid C=0).
$$

From these, the more familiar ROC quantities are immediate:

$$
\text{TPR} = \Pr(\widehat{C}=1 \mid C=1) = q_1, \qquad
\text{FPR} = \Pr(\widehat{C}=1 \mid C=0) = 1-q_0,
$$

and the **Youden index** is

$$
J = \text{TPR} - \text{FPR} = q_0 + q_1 - 1.
$$

If the judge is imperfect, the raw positive rate is biased for true accuracy. 
In [another blog post](2026-03-02-scaffolding-is-all-you-need.md) I demonstrate that if the Youden index is $J>0$ then using a proper decomposition method could improve the reliability of   the scaffold in solving a task, meant as the probability that the task correctly succeeds.

The correction is elementary:

$$
\widehat{\theta}=
\frac{\widehat{p}_J+\widehat{q}_0-1}{\widehat{q}_0+\widehat{q}_1-1},
\qquad
\widehat{p}_J=\frac{1}{n}\sum_{i=1}^n \widehat{C}_i.
$$

That is the usual judge-calibration story, but it matters more here because the judge is part of the system, not an afterthought.

If the judge is wrong in a stable way, the whole scaffold inherits that bias. If the judge is only weakly better than chance, the system can still be useful, but only if you design the selection process carefully.

### Dependence is the hidden tax

Repeated sampling only helps if the samples are not all saying the same thing in different costumes.

Let $K$ be the number of samples and $\rho$ the pairwise dependence between their correctness indicators. Then a useful approximation is the effective sample size

$$
K_{\mathrm{eff}}=\frac{K}{1+(K-1)\rho}.
$$

The slogan is simple: *more width adds mandatory gates; it does not automatically add alternatives.*

If $\rho$ is high, best-of-$K$ saturates fast. The system may look busy while really replaying the same hidden misconception. This is why some diversity mechanisms work and others do not. A different temperature that only changes phrasing is often cosmetic. A different decomposition, a different retrieval set, or a different plan family can reduce dependence in a way that actually changes inference.

So the engineering question is not “can I sample more?” It is “what kind of diversity changes the error structure?”

### Trees are not magic

Trees, graphs, multi-agent setups, and branch-and-bound loops are often sold as if depth itself were the trick. It is not.

The real distinction is between OR semantics and AND semantics. In an OR setting, you hope one branch is right. In an AND setting, the task only succeeds if the local decisions compose.

Write a decomposition tree with node-level error budgets $\delta_v$. Then a conservative global guarantee has the form

$$
\Pr(\text{final error}) \le \sum_{v} \delta_v \le \Delta.
$$

That is the usual union-bound picture, and it is enough to make the main point: a tree helps only when it turns one hard global judgment into many smaller judgments that are each slightly better than chance.

If the subproblems are still coupled in a hidden way, the tree is decorative. If the verifier only works at the root, the tree may even make things worse by spreading uncertainty across more moving parts.

This is why I am skeptical of vague “multi-agent” language. Tell me where the proposal changed, where the verifier sits, what independence you are assuming, and what failure mode you expect to shrink. Otherwise the tree is just a metaphor.

### What I would ship

If I were building an inference-time system under this lens, I would start by writing down three objects explicitly: the proposal law, the verifier potential, and the trace projection that turns execution into task meaning.

Then I would ask, in order: does the proposal cover the right region, is the judge calibrated enough to trust, and is repeated sampling actually buying independent evidence? Only after that would I spend more compute on search.

That order matters. It keeps you from treating every failure as a search problem. Some failures are coverage failures. Some are selection failures. Some are dependence failures. Some are composition failures. Those are different bugs.

The strongest version of the claim is also the simplest one: inference-time LLM systems become legible when you treat them as probabilistic programs over auditable traces. Once you do that, you stop asking whether a scaffold is “smart” in the abstract and start asking whether it has the right support, the right verifier, and enough independence to make extra compute worthwhile.

---

## References

- [Test-time Verification via Optimal Transport:
Coverage, ROC, & Sub-optimality](https://arxiv.org/pdf/2510.18982)
- [How to Correctly Report LLM-as-a-Judge Evaluations](https://arxiv.org/abs/2511.21140v3)
