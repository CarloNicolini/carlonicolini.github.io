---
layout: post
title: Draft notes (PLP / scaffolding)
description: ''
date: 2026-04-01
published: false
categories:
  - science
  - language-physics
---
Yes. I think this is a very strong direction, and in fact it is already latent in the two texts you pointed to.

In `plp_paper.tex`, `factor` is explicitly a log-potential on traces, and the program-synthesis section already has the shape `sample -> interact(exec) -> factor`. In `sections/science/_posts/2026-03-31-PLP-is-inference-time-approximation-of-free-energy.md`, you already make the stronger move that `τ` can include scaffold architectures, not just final responses. So your idea is not a departure from PLP. It is the natural next extension.

The one thing I would sharpen is this: I would not speak of a literal gradient with respect to `τ` unless you first introduce a continuous relaxation. Traces and Python scaffolds are discrete, variable-length objects. The clean mathematical object is not “gradient on `τ`” but inference or optimization over a distribution on scaffold programs and their executions.

## Clean Formalization

If the scaffold itself is variable, it is cleaner to split the trace into:

- `a`: the scaffold program or architecture
- `τ`: the execution trace produced by running that scaffold

Then the PLP target becomes hierarchical:

$$
p(a,\tau \mid x)\propto p_0(a\mid x)\,q(\tau\mid a,x)\,\Phi(a,\tau,x)
$$

where:

- `p_0(a|x)` is a prior or proposal over scaffold programs
- `q(\tau|a,x)` is the frozen-LLM-induced execution law under scaffold `a`
- `\Phi(a,\tau,x)` is the verifier potential

This immediately gives the marginal over programs:

\[
p(a\mid x)\propto p_0(a\mid x)\,Z(a,x),
\qquad
Z(a,x)=\sum_{\tau} q(\tau\mid a,x)\Phi(a,\tau,x)
\]

That is the key object.

So the outer optimization problem is not just “find a good trace.” It is:

\[
a^\star(x)=\arg\max_a \Bigl[\log p_0(a\mid x)+\log Z(a,x)\Bigr]
\]

This is Bayesian model selection over scaffolds, or equivalently evidence maximization over algorithms.

If you want the single best scaffold-trace pair, then the MAP problem is:

\[
(a,\tau)^\star
=
\arg\max_{a,\tau}
\Bigl[
\log p_0(a\mid x)+\log q(\tau\mid a,x)+\log \Phi(a,\tau,x)
\Bigr]
\]

That is the precise version of your “look for points of maximum target distribution.”

Two useful special cases:

- If `\Phi` is a hard verifier, then `Z(a,x)=\Pr_{q(\cdot\mid a,x)}(\text{success}\mid x)`. So the scaffold score is literally solve probability.
- If `\Phi=\exp(R)`, then `\log Z(a,x)` is an entropic or soft-value objective, closer to control-as-inference than to vanilla policy gradient.

## Where Policy Gradient Still Appears

There is still a very clean policy-gradient analogue, but it is not a gradient with respect to the discrete trace itself. It is a gradient with respect to parameters `\psi` of a proposal over scaffolds, `q_\psi(a\mid x)`.

Then:

\[
Z_\psi(x)=\sum_a q_\psi(a\mid x)\sum_\tau q(\tau\mid a,x)\Phi(a,\tau,x)
\]

and

\[
\nabla_\psi Z_\psi(x)
=
\mathbb{E}_{a\sim q_\psi,\;\tau\sim q(\cdot\mid a,x)}
\Bigl[
\Phi(a,\tau,x)\,\nabla_\psi \log q_\psi(a\mid x)
\Bigr]
\]

This is literally a REINFORCE-style score-function estimator on the meta-controller that selects scaffold architectures, while the base LLM parameters stay frozen.

So I would say:

- vanilla policy gradient reappears at the level of the scaffold proposer
- the PLP semantic target remains a Boltzmann-reweighted distribution over scaffolded executions
- the exact analogue is closer to soft RL / control-as-inference than to plain expected-reward PG

## What It Reminds Me Of

The closest neighboring literatures are:

- `Control as inference / KL-regularized RL`: reward becomes a potential, and the optimal law is proportional to proposal times `exp(reward)`.
- `Probabilistic programming`: inference over execution traces is already the native object there; your move is to enlarge the trace so it includes algorithmic structure.
- `Cross-entropy method / adaptive importance sampling`: maintain a proposal over discrete structured objects, sample, score, and move the proposal toward high-weight regions. This is very close to what you want.
- `Genetic programming / program synthesis / execution-guided search`: search over executable artifacts using verifier feedback.
- `Rational metareasoning / value of computation`: choose which computations to perform under a finite compute budget. This is highly relevant and often underappreciated here.
- `Architecture search / hyper-heuristics / algorithm configuration`: the object being optimized is not the model weights but the inference algorithm wrapped around the model.
- `TextGrad / Reflexion / Self-Refine`: these are already heuristic forms of local ascent in trace space, but without a full posterior or evidence formalization.

If you want the most non-obvious but important connection, I would emphasize `rational metareasoning` and the `cross-entropy method`.

## What I Would Change In The Framing

I would avoid saying “gradient with respect to `τ`” and say one of these instead:

- search over program-trace space
- inference over a posterior on scaffolds and traces
- score-function optimization of a proposal over scaffolds
- MCMC/SMC/evolutionary optimization over program space

That is more precise, and it avoids forcing Euclidean differential language onto discrete Python code.

## Actionable Consequences

A few consequences fall out immediately.

- Start from a typed scaffold DSL, not arbitrary Python. Arbitrary Python makes the measure on program space messy because of nontermination, hidden state, and side effects. A DSL with nodes like `sample`, `factor`, `interact`, `plate`, `branch`, `repair`, `aggregate` is much easier to analyze.
- Add compute regularization explicitly. Use something like \(\tilde{\Phi}(a,\tau,x)=\Phi(a,\tau,x)\exp(-\lambda C(a,\tau,x))\). Otherwise the optimizer will prefer bloated scaffolds that win only by spending more budget.
- Compare scaffold families by estimating \(Z(a,x)\), not just by best-of-one reward. For a fixed scaffold `a`, \(\hat Z(a,x)=\frac{1}{K}\sum_{k=1}^K \Phi(a,\tau_k,x)\) with \(\tau_k\sim q(\cdot\mid a,x)\) is already a natural Monte Carlo estimator.
- Use outer-loop search over scaffolds and inner-loop search over traces. Outer loop: evolutionary search, CEM, bandits, Bayesian optimization. Inner loop: beam search, MCTS, SMC, self-consistency, or verifier-guided repair.
- Keep your distinction between target-defining factors and shaping factors. If you factor partial programs during search, the shaping terms should telescope, otherwise you change the target and double-count future mass.
- Treat verifier calibration as central, not secondary. If you optimize scaffold space against a weak `\Phi`, you will get scaffold hacking, not better reasoning.
- Measure dependence and basin collapse. A scaffold that produces ten near-identical traces is not the same as one that explores ten genuinely different semantic basins.

## The Strongest Formal Version

If you want one compact research statement, I think it is this:

For a scaffold family `\mathcal A`, define

\[
\mathcal L(a)
=
\sum_{i=1}^n
\log
\mathbb E_{\tau\sim q(\cdot\mid a,x_i)}
\bigl[
\Phi(a,\tau,x_i)\,e^{-\lambda C(a,\tau,x_i)}
\bigr]
\]

and search for

\[
a^\star=\arg\max_{a\in\mathcal A}\mathcal L(a)
\]

That is a frozen-model, inference-time analogue of architecture search, but the objective is semantic evidence rather than training loss.

I think this is genuinely promising. Conceptually, it says that inference-time scaffolding is not just search over answers, but search over computations. Mathematically, it turns “prompt engineering” into posterior inference over algorithms.

If you want, I can next help you turn this into a compact formal section for the post or paper, with definitions, one proposition, and 2-3 candidate optimization algorithms.