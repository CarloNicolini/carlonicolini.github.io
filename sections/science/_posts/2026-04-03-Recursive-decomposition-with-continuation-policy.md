---
layout: post
title: Recursive decomposition with a continuation policy
description: "Adding an abstain action to a recursive scaffold shows how delayed commitment can help, but only in a narrow ambiguity regime."
date: 2026-04-03
published: true
categories:
  - science
  - language-physics
---

## Abstract

The earlier notes in this series argued that a scaffold should not always answer immediately and should not always decompose.
It should sometimes delay commitment.
In this post I report a small implementation of that idea in a recursive scaffold.

The new scaffold extends the previous answer-or-decompose policy with a third action, `ABSTAIN`.
When the local direct-answer and decomposition values are too close, the scaffold does not commit.
Instead, it probes both routes, gathers two candidate answers, and resolves them into a final answer at the parent.
This makes delayed commitment an actual control action rather than a slogan.

The result is mixed but informative.
On genuinely broad tasks, the abstain action can preserve useful structure that a one-shot answer would flatten too early.
On bounded memo-style tasks, the same action can overcomplicate the problem and import a worse bias from the decomposition branch.
So delayed commitment is real, but it is not free.

## 1. Where this note sits

This post continues the sequence started in [Probabilistic Language Programming]({% link sections/science/_posts/2026-03-01-Probabilistic-Language-Programming.md %}), [Scaffolding is all you need]({% link sections/science/_posts/2026-03-02-Scaffolding-is-all-you-need.md %}), and [Test-time inference, language models and energy based models]({% link sections/science/_posts/2026-03-27-PLP-and-Energy-Based-Models.md %}).
Those notes introduced the proposal-target split, the essential-node tax of decomposition, and the connection to Blondel et al.'s ARM/EBM equivalence.

[PLP is inference-time approximation of free energy]({% link sections/science/_posts/2026-03-31-PLP-is-inference-time-approximation-of-free-energy.md %}) identified the main object as the continuation partition

$$
Z(s)=\sum_{\tau \succ s}\pi_{\mathcal{D}}(\tau \mid s)\Phi(\tau),
\qquad
V(s)=\log Z(s).
$$

[Inference-Time Steering as a Discrete Schrödinger Bridge]({% link sections/science/_posts/2026-04-01-Inference-time-steering-Schrodinger-Bridge.md %}) then connected that object to Doob twisting and transport.
[Soft values, symmetry breaking, and random rooted trees]({% link sections/science/_posts/2026-04-02-Soft-values-symmetry-breaking-and-random-rooted-trees.md %}) proposed a local branching law with three regimes: answer, delay commitment, and commit.
[MellowMax, Doob's h-transform, and the intensive geometry of tool-use agents]({% link sections/science/_posts/2026-04-03-Mellowmax-doob-and-agentic-tool-use.md %}) argued that the corresponding local value should often be treated as an intensive quantity.
Finally, [Short-prefix soft values: a null result]({% link sections/science/_posts/2026-04-04-Short-prefix-soft-values-a-null-result.md %}) showed that trivial one- or two-token prefixes are the wrong empirical regime.

The natural next step was therefore not another short-prefix benchmark.
It was an action-level scaffold with an explicit delayed-commitment mode.

## 2. The policy

The previous recursive scaffold in `examples/example_rrt2.py` had only two control modes:

1. `ANSWER`
2. `DECOMPOSE`

That is too rigid.
If the two local values are close, a forced binary choice creates the very early-commitment failure that the theory warns about.

The updated scaffold uses the local quantity

$$
\Delta(s) := V_{\mathrm{dec}}(s) - \Lambda - V_{\mathrm{ans}}(s),
$$

where $\Lambda$ is the decomposition tax.
But instead of branching on the sign of $\Delta(s)$ alone, it introduces a small ambiguity band $\varepsilon$:

$$
M(s)=
\begin{cases}
\mathrm{ANSWER} & \text{if } \Delta(s) < -\varepsilon \\
\mathrm{ABSTAIN} & \text{if } |\Delta(s)| \le \varepsilon \\
\mathrm{DECOMPOSE} & \text{if } \Delta(s) > \varepsilon.
\end{cases}
$$

This is only a proxy for the more principled criterion in the April 2 note, where delayed commitment should depend on both $\Delta(s)$ and an effective multiplicity $N_{\mathrm{eff}}(s)$.
In the current implementation, the ambiguity band plays the role of a cheap surrogate for a high-$N_{\mathrm{eff}}$ regime.

## 3. What the abstain action actually does

The important design choice is that `ABSTAIN` does not mean "refuse to answer".
It means "do not already decide".

Operationally, the abstaining node performs four steps:

1. It generates a short note explaining why the direct-answer and decomposition routes are hard to separate.
2. It produces a direct-answer candidate.
3. It produces a decomposition candidate by recursively solving two subtasks and synthesizing them back upward.
4. It resolves the two candidate answers into a single final answer at the parent.

The last step is crucial.
Without it, the scaffold would only defer the decision locally.
With it, information gathered below the node is processed back up to the root.
That is the recursive analogue of "wait, inspect both basins, then commit later".

This differs from the explicit `W` action in `examples/test_symmetry_breaking.py`.
There, waiting reveals a new clue from the environment.
Here, waiting reveals internal evidence by probing two routes of the reasoning tree before making the root decision.

## 4. The symmetry-breaking pilot still matters

The explicit waiting experiment in `examples/test_symmetry_breaking.py` provides a useful control.
The pilot result stored in `examples/symmetry_breaking_results_pilot.json` contains only one task, so it is not a benchmark.
But it makes one point very cleanly.

On the `instrument_bow` task:

- `fraction_wait_best_pre = 1.0`
- `fraction_pre_commit_correct = 0.0`
- `fraction_post_correct = 1.0`
- `fraction_delay_helped = 1.0`

The direct reading is simple.
Before the extra clue, the best immediate commitment among concrete options is wrong.
The best action is to wait.
After the clue, the best commitment flips to the correct candidate, and the correct probability rises by about `0.54`.

What is interesting is what the pilot does **not** show.
The saved metrics do not exhibit a clean concentration story.
In the pilot:

- the top-two gap decreases after the reveal
- the effective number of actions increases rather than decreases

So the benefit of waiting is not captured by a naive "entropy must go down" rule.
The benefit is operational.
The explicit delay changes which commitment is best.
That is enough.

This point matters for the recursive scaffold as well.
Delayed commitment need not always look like a simple collapse onto one sharper peak.
Sometimes it works by giving the scaffold time to build a better root-level comparison.

## 5. Qualitative results from the recursive scaffold

The new scaffold is still a pilot.
I have not attached an automatic verifier to the final answers, so the evidence here is qualitative.
But the qualitative behavior is already informative.

### 5.1 A broad curriculum task

Consider the curriculum task from `examples/rrt_tasks.json`:

> Outline a curriculum for a 12-week intensive bootcamp covering full-stack web development, data structures, algorithms, and technical interview preparation.

With `\Lambda = 1.0` and an abstain band of `1.5`, the root action becomes `ABSTAIN`.
The local values are close enough that the scaffold refuses to commit immediately:

$$
V_{\mathrm{ans}} \approx 22.57,\qquad
V_{\mathrm{dec}} \approx 22.24,\qquad
\Delta \approx -1.33.
$$

The tree then does exactly what the theory asks for.
It generates:

- a direct answer candidate
- a decomposition candidate with two child solves
- a synthesized root answer that combines the two

The resulting answer is more structured than the baseline direct answer.
It looks less like a raw continuation and more like a curriculum assembled after inspecting two plausible routes.

I do not want to overstate this.
This is not proof that delayed commitment improves correctness.
But it is evidence that the abstain action changes the *type* of answer produced.
It preserves option value long enough for the root to integrate more structure.

### 5.2 A bounded startup memo

Now consider a narrower task:

> Draft a two-paragraph recommendation on whether a 10-person startup should start with a monolith or microservices for its first product.

With `\Lambda = 1.0` and an abstain band of `1.0`, the root also abstains:

$$
V_{\mathrm{ans}} \approx 22.63,\qquad
V_{\mathrm{dec}} \approx 22.76,\qquad
\Delta \approx -0.87.
$$

But here the qualitative effect is worse.
The final abstention-resolved answer overcommits to microservices and loses the more balanced tone of the baseline direct answer.
In other words, the scaffold delayed commitment, spent extra compute, and still moved the answer in the wrong direction.

This is a useful failure.
It shows that delayed commitment should not be treated as a universal improvement.
On bounded tasks with a reasonably good direct-answer route, the decomposition branch can inject a worse prior than the one-shot answer.

## 6. What I think this means

The abstain action makes the recursive scaffold more faithful to the theory in the April 2 and April 3 notes.
There really is now a third control mode.
The system can:

1. answer directly
2. decompose immediately
3. delay commitment and compare both routes

That is progress.
But the current experiments also sharpen the real question.
The main challenge is no longer "can we code an abstain action?"
It is "when should the scaffold trust it?"

At the moment, the answer is crude.
I use an ambiguity band on $\Delta(s)$.
That is only a practical stand-in for the richer geometry suggested by the theory:

- an effective number of viable basins
- a better estimate of the local continuation partition
- a branch-specific cost model, not a single constant $\Lambda$

So the experiments support the delayed-commitment idea in a limited but real sense.
They do not yet validate the full control law.

## 7. Relation to the null result

The April 4 null result argued that short token prefixes are often the wrong empirical regime because the semantic basin collapses too early.
This new scaffold moves closer to the right regime.

The alternatives are now not punctuation variants or one-token fragments.
They are structured macro-actions:

- direct answer
- recursive decomposition
- delayed commitment with later resolution

That makes the experiment more faithful to the theoretical object.
It also explains why the results are more mixed.
We are no longer testing a saturated problem.
We are testing a genuine control choice.

## 8. Limitations

Several caveats remain.

- The local value is still Blondel's ARM-side soft value, not a full verifier-weighted PLP rollout value.
- The same local model proposes, decomposes, synthesizes, and resolves abstention.
- The abstain band is heuristic.
- The decomposition tax is still a single scalar.
- The evaluation of the recursive scaffold is qualitative rather than judge-based.
- The symmetry-breaking pilot uses only one saved task, so its statistics are illustrative rather than stable.

These limitations matter.
They mean the current experiments should be read as a systems probe, not as a definitive empirical validation.

## Conclusion

The new recursive scaffold suggests a more realistic continuation policy than the earlier binary answer-or-decompose controller.
When the local values are well separated, the scaffold can commit.
When they are close, it can delay commitment, inspect both routes, and synthesize a better root-level answer.

The experiments also show why this third action is delicate.
Delayed commitment can preserve useful structure on broad tasks.
It can also import the wrong bias on bounded tasks.

So the scientific lesson is not "always abstain before deciding".
It is narrower and more useful:

> A recursive scaffold needs an explicit delayed-commitment mode, but that mode must itself be controlled by a better estimate of ambiguity than a raw answer-vs-decompose difference.

That is where I think the next work should go: estimating basin multiplicity more directly, calibrating branch-specific taxes, and attaching an explicit verifier at the root so the abstention policy can be studied quantitatively rather than only qualitatively.

---

## References

{% bibliography --cited %}
