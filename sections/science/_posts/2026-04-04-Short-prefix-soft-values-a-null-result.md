---
layout: post
title: 'Short-prefix soft values: a null result'
description: "A small experiment shows that easy tasks saturate too quickly to test the predictive power of short-prefix soft values."
date: 2026-04-03
published: true
categories:
  - science
  - language-physics
---

## Abstract

I ran a small experiment to test a simple question.
If we sample only one or two tokens after a prompt, does the local soft value at that short prefix predict the quality of the final continuation?
The answer from the current experiment is negative, but not because Blondel's theory fails.
The experiment saturates too early.
On all eight tasks, the model reaches the correct answer almost immediately, every downstream rollout succeeds, and every correlation becomes undefined because the success labels have zero variance.
This is therefore a useful null result.
It identifies the wrong experimental regime for testing the predictive power of short-prefix soft values.

## 1. Why I ran this experiment

Several recent notes in this sequence argue that inference-time scaffolds can be understood through continuation partition functions and soft values, in close dialogue with the ARM/EBM perspective of Blondel et al. {% cite blondel2025autoregressive %}.
[Probabilistic Language Programming]({% link sections/science/_posts/2026-03-01-Probabilistic-Language-Programming.md %}) defines the trace-level target.
[PLP is inference-time approximation of free energy]({% link sections/science/_posts/2026-03-31-PLP-is-inference-time-approximation-of-free-energy.md %}) treats the continuation log-partition as the main object.
[Soft values, symmetry breaking, and random rooted trees]({% link sections/science/_posts/2026-04-02-Soft-values-symmetry-breaking-and-random-rooted-trees.md %}) turns that object into a local branching law.
[MellowMax, Doob's h-transform, and the intensive geometry of tool-use agents]({% link sections/science/_posts/2026-04-03-Mellowmax-doob-and-agentic-tool-use.md %}) argues that the corresponding local quantity should be made intensive when actions have very different lengths.

The natural empirical question is then the following.
Suppose a model emits a short continuation $y$ after a prompt $x$.
Can a local soft-value readout at the prefix $x \oplus y$ predict the downstream semantic value of the full continuation tree rooted at that prefix?

This is not the same as asking whether the local soft value exactly equals the value of one final answer.
The correct test is weaker and more useful.
It asks whether the local quantity has **predictive power** for the Monte Carlo estimate of downstream success.

## 2. Experimental setup

The script `~/workspace/plp/examples/test_predictive_power.py` implements the following procedure.

1. Start from a prompt $x$.
2. Sample a short rollout $y$ of one or two tokens.
3. Compute an intensive soft-value readout at $x \oplus y$ using MellowMax over the next-token logits.
4. Sample several full completions from the same short prefix.
5. Evaluate those full completions with a simple verifier.
6. Estimate the downstream semantic continuation value by Monte Carlo.

Formally, the experiment compares a local readout

$$
\widehat{V}_{\mathrm{local}}(x \oplus y)
$$

with a downstream Monte Carlo estimate

$$
\widehat{Z}_{\Phi}(x \oplus y)
:=
\frac{1}{M}\sum_{j=1}^{M}\Phi\!\left(\tau^{(j)}\right),
\qquad
\tau^{(j)} \sim \pi(\cdot \mid x \oplus y).
$$

The script then computes Pearson and Spearman correlations between the local soft value and the downstream success rate.

The experiment used:

- model: `Qwen/Qwen2.5-1.5B-Instruct`
- device: `mps`
- tasks: 8
- sampled short prefixes: 64 in total
- downstream completions per prefix: 12

The tasks were intentionally simple: arithmetic and one-word factual questions.

## 3. Main result

The result is a null result in the strict statistical sense.

- Every task achieved a downstream success rate of `1.0` for every sampled short prefix.
- Every per-task Pearson correlation was `NaN`.
- Every per-task Spearman correlation was `NaN`.
- The overall correlations were also `NaN`.

This happened for a simple reason.
The downstream verifier had no variance to explain.
Once the short prefix had been sampled, the model had already collapsed onto the correct answer basin.
Every full continuation remained correct.
The experiment therefore measured no ranking problem, because there was nothing left to rank.

This is not evidence that the soft-value idea is wrong.
It is evidence that the chosen tasks are too easy for the chosen model and the chosen rollout length.

## 4. What the JSON output actually shows

The JSON file contains one striking pattern.
For arithmetic tasks such as `17 + 28`, the short prefix is already the full correct answer: `"45"`.
All downstream completions remain `"45"`.
The same happens for subtraction, multiplication, and the one-word factual prompts.

One task is especially instructive.
For the France question, some short prefixes are `"Paris"` and others are `"Paris."`.
Those two prefixes have different local soft values, but both achieve a downstream success rate of `1.0`.

This detail matters.
It shows that once the prefix already identifies the correct semantic basin, the local value can still move because of surface-form or punctuation effects.
So the current experiment is probing a regime in which the semantic problem is already solved, while the local value is still sensitive to lexical details.

That is exactly the wrong regime for testing predictive power.

## 5. Interpretation

The present experiment does not test whether Blondel's local soft value predicts which basin is better.
It tests whether the value distinguishes prefixes **after the basin has already collapsed**.
That is a much weaker and less interesting question.

Seen this way, the null result is informative.
It tells us that the predictive-power experiment must be moved earlier in the decision process.
If the short rollout already contains the entire answer, then the experiment no longer studies continuation value.
It studies a nearly terminal state.

This also clarifies an important conceptual point from the previous posts.
The useful regime for testing continuation values is not a regime where the first one or two tokens already solve the task.
It is a regime where different short prefixes still correspond to genuinely different future basins.

## 6. What would count as a real test

The next experiment should introduce variance at the semantic level, not only at the surface level.
Several changes would help.

### 6.1 Harder tasks

The first fix is to move from trivial arithmetic and one-word factual prompts to tasks where early prefixes do not already determine the answer.
Examples include:

- multi-step arithmetic with distractors
- short proofs or derivations
- code generation with unit tests
- retrieval questions where the first action must decide which source to consult

### 6.2 Earlier evaluation

The second fix is to shorten the short rollout.
For many tasks, one token is already too late if the model immediately emits the correct answer.
The experiment should evaluate the prefix before the model has written the final semantic object.

### 6.3 Structured actions instead of free text prefixes

The most important fix is to stop sampling arbitrary short token prefixes and instead define a finite action set.
For agentic systems, the relevant alternatives are not free BPE fragments.
They are structured actions such as:

- `ANSWER`
- `DECOMPOSE`
- `<tool_call>search</tool_call>`
- `<tool_call>python</tool_call>`
- `<tool_call>retrieve</tool_call>`

This is the setting discussed in [MellowMax, Doob's h-transform, and the intensive geometry of tool-use agents]({% link sections/science/_posts/2026-04-03-Mellowmax-doob-and-agentic-tool-use.md %}).
In that regime, the local value is attached to a meaningful macro-action, not to punctuation.

### 6.4 Nontrivial verifier geometry

The verifier must also create a real continuation problem.
If every downstream completion is accepted, then the empirical estimate of the continuation partition function becomes constant.
At that point, no method can exhibit predictive power.

## 7. Why this still supports the overall theory

At first sight, a null result can feel disappointing.
I think this one is clarifying.

The main theory in the previous posts never claimed that every local soft-value readout should always show predictive discrimination on every task.
The claim is subtler.
The local value is useful when the prefix still leaves open several possible future basins and the scaffold must choose where to allocate compute.

The current experiment simply did not enter that regime.
It entered a regime in which the model had already solved the task before the measurement became interesting.

So the correct takeaway is not:

> short-prefix soft values do not work.

It is:

> short-prefix soft values cannot be meaningfully tested on tasks whose semantic uncertainty collapses in the first one or two tokens.

That is a much better conclusion.
It says the experimental design must match the theoretical object.

## 8. The next experimental step

The next experiment should be framed at the action level.
For each prompt $x$, define a finite set of candidate actions $a \in \mathcal{A}(x)$.
For each action, compute a local intensive value estimate and compare it with a Monte Carlo estimate of the downstream verifier-weighted continuation mass:

$$
\widehat{Q}(x,a)
\quad \text{vs.} \quad
\widehat{Z}_{\Phi}(x \oplus a).
$$

That experiment would directly test the action-selection theory developed across the 2026 notes.
It would also connect naturally to the random-rooted-tree view, to Doob twisting, and to MCTS-style search over structured actions rather than over arbitrary strings.

## Conclusion

The current predictive-power experiment does not validate or falsify the soft-value thesis.
It saturates too quickly.
All 64 sampled short prefixes lead to perfect downstream success, so every correlation becomes undefined.

This is still a useful scientific result.
It shows that the present benchmark is too easy and too late in the rollout to probe continuation geometry.
The correct next step is to move from trivial answer prefixes to structured action choices with genuine downstream uncertainty.

That is the regime in which continuation soft values should matter, and it is also the regime in which inference-time reasoning begins to look like a real numerical integration method over future semantic mass.

---

## References

{% bibliography --cited %}
