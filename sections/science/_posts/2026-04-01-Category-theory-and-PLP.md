---
layout: post
title: "Category theory and PLP: keeping the theory in order"
description: "A small categorical vocabulary for PLP: kernels, potentials, decomposition, free energy, and steering—without replacing probability on path space."
date: 2026-04-01
published: true
permalink: /2026-04-01-Category-theory-and-PLP.html
categories:
  - science
  - language-physics
---

## Why use category theory here?

Recent posts developed one story from several angles: probabilistic language programs as semantics, recursive scaffolds as reliability, the same target as an energy-based model, prefix values as free energy, and steering via Schrödinger bridges.

The risk is that five angles read like five unrelated theories.
The shared object is always the same: a verifier-reweighted probability law over execution traces.

Category theory helps only if we use it with discipline.
It is not the foundation of PLP.
The foundation remains probability on path space.
Category theory supplies vocabulary for **composition**: how programs compose, how decompositions compose, how weights compose, and where exact semantics stops and approximation begins.

This post does not recast PLP as abstract category-theory theater.
It uses a small categorical layer to keep the pieces aligned.

<figure>
<img src="/static/postfigures/category_theory_plp_layers.svg" alt="Layered view of PLP and category theory">
<figcaption>
<strong>Figure 1.</strong> Read the five recent posts as layers of one theory, not as five competing theories. The categorical layer is bookkeeping on top of path-space probabilistic semantics.
</figcaption>
</figure>

## Glossary: categorical terms in plain language

The list below fixes the few categorical terms used later.

- **Object.** A typed thing you can reason about. Here, objects are spaces of prompts, prefixes, traces, answers, or tuples of subtasks.
- **Morphism** or **arrow.** A map from one object to another. In deterministic mathematics this is often an ordinary function. In PLP it is often a stochastic map: one input yields a distribution over outputs.
- **Category.** Objects and arrows such that arrows compose and every object has an identity arrow that changes nothing.
- **Functor.** A map between categories that preserves identity and composition. Informally, it sends structure to structure without breaking how compositions match up.
- **Commutative diagram.** A diagram commutes when two routes through it yield the same result. That is how we state that two constructions agree.
- **Monoid.** A set with an associative binary operation and a neutral element. Example: nonnegative numbers under multiplication, with unit $1$. In PLP, weights and likelihood ratios multiply.
- **Monoidal structure.** A way to place systems side by side—think of a tensor-like product. In PLP it matters for independent particles, tuples of child tasks, or batched traces.
- **Operad** or **multicategory.** Ordinary morphisms have one input and one output. An operad tracks operations with many inputs and one output. That shape matches decomposition trees, where one parent answer often comes from several child answers.
- **Lax.** Exact preservation is an equality. Lax preservation keeps structure only up to a controlled comparison map, inequality, or approximation. Here **lax** signals approximate inference, not exact equivalence.
- **Natural transformation.** A coherent way to compare two functors. The current PLP story does not need that language yet.

One non-categorical term is essential:

- **Markov kernel.** A stochastic map: given input $x$, it returns a distribution over outputs. This is the right notion of “arrow” for probabilistic programs.

## The base layer is stochastic semantics, not category theory

Fix a deployment setup $\mathcal{D}$, an input $x$, and a complete execution trace $\tau$.
The first exact semantic object of PLP is the proposal law

$$
\pi_{\mathcal{D}}(\tau \mid x).
$$

Running the scaffold—with the model, tools, router, decoding policy, and the rest of the runtime—induces this distribution.

A scaffold therefore denotes a stochastic arrow from an input space $X$ to a trace space $T$.
If you want a categorical home, use a stochastic category such as `Stoch`: objects are measurable spaces, arrows are Markov kernels.

The idea is concrete: a scaffold is not “a prompt plus a vibe.”
It maps each prompt to a distribution over traces.

Add a verifier, judge, test, or heuristic score.
In PLP this is a nonnegative potential

$$
\Phi(\tau,x) \ge 0.
$$

The semantic target is the change of measure

$$
p_{\mathcal{D}}(\tau \mid x)
=
\frac{\pi_{\mathcal{D}}(\tau \mid x)\Phi(\tau,x)}
{Z_{\mathcal{D}}(x)},
\qquad
Z_{\mathcal{D}}(x)=\sum_{\tau} \pi_{\mathcal{D}}(\tau \mid x)\Phi(\tau,x).
$$

This equation is central in [Probabilistic Language Programming]({% link sections/science/_posts/2026-03-01-Probabilistic-Language-Programming.md %}).
Later posts elaborate parts of the same construction.

The first categorical observation that really bites is this.

The proposal $\pi_{\mathcal{D}}$ is an arrow of stochastic semantics.
The potential $\Phi$ is not another arrow of the same kind.
It is an **effect** on traces: it assigns a nonnegative weight to each trace.
The right algebra for such effects is a monoid.
Indeed, $\mathbb{R}_{\ge 0}$ with multiplication and unit $1$ is a commutative monoid, so factors compose by multiplication:

$$
\Phi_{\mathrm{tot}}(\tau)=\Phi_1(\tau)\Phi_2(\tau)\cdots \Phi_m(\tau).
$$

In log coordinates the structure is additive:

$$
R(\tau)=\log \Phi(\tau), \qquad R_{\mathrm{tot}}=R_1+\cdots + R_m.
$$

The monoidal picture is equally simple: sometimes we place several probabilistic objects side by side.
For particles, that means a product measure.
For child tasks, a typed tuple.
This helps only when independence and typing assumptions are explicit.

So category theory pays off in a small but real way:
PLP has a two-sorted semantics—stochastic arrows plus multiplicative effects.
That split already explains why `sample` and `factor` are not the same kind of thing.

<figure>
<img src="/static/postfigures/category_theory_plp_semantics.svg" alt="From scaffold syntax to target measures and continuation values">
<figcaption>
<strong>Figure 2.</strong> Main semantic pipeline in PLP. A scaffold denotes a proposal law on traces. Potentials reweight that law into the semantic target. Prefixwise marginalization yields the continuation partition function $Z(s)$ and free energy $V(s)=\log Z(s)$. When $Z$ is known exactly, it twists the local kernel by Doob’s $h$-transform.
</figcaption>
</figure>

## Where a functor really appears

Use the word **functor** sparingly.
One use fits well.

At the syntactic level we write scaffold programs with primitives such as `sample`, `factor`, branching, tool calls, and possibly decomposition.
At the semantic level those programs denote kernels, weights, and reweighted trace laws.

A semantics map

$$
\mathcal{S} : \text{Scaffolds} \longrightarrow \text{Stochastic semantics}
$$

deserves the name functor if it preserves composition:

$$
\mathcal{S}(B \circ A) = \mathcal{S}(B) \circ \mathcal{S}(A),
\qquad
\mathcal{S}(\mathrm{id})=\mathrm{id}.
$$

In words: running scaffold $A$ and then scaffold $B$ should match composing their semantic kernels.

That is the right use of category theory in PLP.
Semantics is not a bag of interpretations.
It is a composition-preserving translation from programs to probabilistic objects.

There is a caveat.
PLP mixes generative steps and weighting steps, so kernels alone do not capture the semantic target.
A fully clean presentation would use a stochastic category enriched by an effect algebra or a weight structure.
Hence the modest claim:
PLP has a **functorial core**, but full semantics is richer than bare stochastic composition.

## Decomposition is operad-like, not yet a finished operad

[Scaffolding is all you need]({% link sections/science/_posts/2026-03-02-Scaffolding-is-all-you-need.md %}) adds the main structural complication: decomposition.

A direct answer has one input task and one output answer.
A decomposition node differs.
It takes one parent task, emits several child tasks, solves them, and recomposes the child answers into one parent answer.

That is not the shape of a standard one-input/one-output morphism.
It matches multicategories and operads.

The idea is easy to state without jargon.
An operad formalizes many-to-one composition.
Use it when an operation takes several inputs and returns one output, and when you substitute one operation into the slots of another.

That is the shape of recursive scaffolding:

1. decompose one task into several child tasks,
2. solve each child,
3. compose the child answers into one parent answer.

Decomposition is **operad-like**.
That wording is fair and useful.
Stop there for now.

A genuine operad claim needs at least three specifications:

1. types of tasks and answers,
2. the substitution rule for plugging a scaffold into each child slot,
3. associativity and coherence laws so repeated decomposition does not depend on how substitutions are parenthesized.

The current PLP posts do not yet supply that fully axiomatized layer.
They give the right intuition and much of the structure, not the full operadic formalization.

<figure>
<img src="/static/postfigures/category_theory_plp_decomposition.svg" alt="Decomposition as an operad-like structure in PLP">
<figcaption>
<strong>Figure 3.</strong> Recursive scaffolding is many-to-one composition: one parent task splits into a tuple of child tasks, child answers are produced, and a compositor maps the tuple to one parent answer. Operad-like language fits naturally. The AND and OR cases use different composition laws; they are not automatically categorical products and coproducts.
</figcaption>
</figure>

This clarifies the reliability discussion.
The local recursion equation

$$
R_u = p_u^{\mathrm{ans}} a_u + p_u^{\mathrm{dec}} d_u
$$

shows that “answer” and “decompose” are different semantic branches.
Inside $d_u$, the validity of the split, child reliabilities, and compositor success interact.

Under AND-like composition, extra children add mandatory gates.
Under OR-like composition, extra children add alternatives a selector may use.
That is a real compositional distinction.
It does **not** imply that the two cases are the categorical product and coproduct.
That stronger claim would need more structure and tighter assumptions.

## Prefixes, backward messages, and the exact invariant

The next step comes from [PLP and Energy-Based Models]({% link sections/science/_posts/2026-03-27-PLP-and-Energy-Based-Models.md %}) and [PLP is inference-time approximation of free energy]({% link sections/science/_posts/2026-03-31-PLP-is-inference-time-approximation-of-free-energy.md %}).

Fix a prefix or partial state $s$.
The central backward object is

$$
Z(s)=\sum_{\tau \succ s} \pi_{\mathcal{D}}(\tau \mid s)\Phi(\tau),
\qquad
V(s)=\log Z(s).
$$

This is the exact continuation partition function and its log.
The same quantity appears later as soft value, log-evidence, or free energy, depending on convention.

Category theory helps here only if we stay modest.
Prefixes form a preorder under extension: $s \preceq t$ if $t$ extends $s$.
That preorder is a very small category.
Then $Z$ is a backward valuation on prefix structure: it reports how much verifier-weighted mass remains downstream of the current prefix.

The object feels “backward” because the value at the present prefix sums over futures.
If you want categorical vocabulary, call the flow **contravariant**: semantic information moves from extensions back to the current state.
Do not lean on the word.
The equation for $Z(s)$ carries the content.

That equation matters for the [Schrödinger bridge post]({% link sections/science/_posts/2026-04-01-Inference-time-steering-Schrodinger-Bridge.md %}).
If the state is Markovized by the full prefix—or by a rich enough augmented hidden state—the exact backward message

$$
h(s)=Z(s)=e^{V(s)}
$$

twists the local proposal by Doob’s $h$-transform:

$$
\pi(y \mid s)=\pi_{\mathcal{D}}(y \mid s)\frac{h(s \oplus y)}{h(s)}.
$$

This is one of the cleanest unifications in the sequence.

- In PLP, $Z(s)$ is the continuation partition function.
- In the EBM view, $V(s)=\log Z(s)$ is the soft value or free energy.
- In the steering view, $h(s)=Z(s)$ is the twisting function for the optimally steered local kernel.

These are not three unrelated quantities.
They are three views of one backward object.

## What “lax” should mean here

The term **lax** matters because deployed algorithms are rarely exact.

A lax map preserves intended structure up to controlled slack, not as a literal equality.
That matches finite-compute inference.

The ideal chain would be:

1. exact proposal $\pi_{\mathcal{D}}$,
2. exact potential $\Phi$,
3. exact target $p_{\mathcal{D}}$,
4. exact continuation value $Z(s)$,
5. exact Doob-twisted kernel $\pi(\cdot \mid s)$.

Practical scaffolds do not have the full chain.
They use approximations:

- an imperfect judge, so $\Phi$ is judge-relative rather than truth-relative,
- finite particles or beams, so the target is only approximately represented,
- a heuristic value estimator $\widehat{V}(s)$ instead of exact $\log Z(s)$,
- support mismatch, so some high-value traces are unreachable,
- transport or truncation error when steering is approximate.

<figure>
<img src="/static/postfigures/category_theory_plp_lax.svg" alt="Strict semantic picture versus lax algorithmic picture in PLP">
<figcaption>
<strong>Figure 4.</strong> The strict picture uses exact proposal laws, exact potentials, exact continuation values, and exact twisted kernels. Real algorithms are usually only lax: they approximate the intended structure under finite compute, imperfect judges, and support constraints.
</figcaption>
</figure>

Hence the phrase **lax categorical layer** instead of a stronger claim.
It matches the epistemic status.
Search, sampling, rejection, SMC, self-consistency, critique loops, and bridge-style steering are not exact realizations of semantic objects.
They are approximate numerical schemes for the same target.

Words such as “natural transformation” or “adjunction” are premature.
The existing structure is enough without heavier categorical packaging.

## A reading order for the whole theory

The five posts line up as follows.

1. [Probabilistic Language Programming]({% link sections/science/_posts/2026-03-01-Probabilistic-Language-Programming.md %}) defines the basic objects: trace law, proposal, verifier potential, target distribution, support gap, measurement error, and dependence.
2. [Scaffolding is all you need]({% link sections/science/_posts/2026-03-02-Scaffolding-is-all-you-need.md %}) adds recursive decomposition, node-local reliability, and the split between AND-like and OR-like composition.
3. [PLP and Energy-Based Models]({% link sections/science/_posts/2026-03-27-PLP-and-Energy-Based-Models.md %}) rewrites the same semantic target as a reference-measure energy-based model.
4. [PLP is inference-time approximation of free energy]({% link sections/science/_posts/2026-03-31-PLP-is-inference-time-approximation-of-free-energy.md %}) treats the continuation log-partition $V(s)=\log Z(s)$ as the main invariant approximated at inference time.
5. [Inference-Time Steering as a Discrete Schrödinger Bridge]({% link sections/science/_posts/2026-04-01-Inference-time-steering-Schrodinger-Bridge.md %}) reads support repair and value-guided twisting as a controlled transport problem.

In one sentence:

> PLP is compositional path-space semantics for inference-time computation: category theory organizes the syntax of composition; probability and control theory carry most of the mathematics.

## A minimal global diagram

The global picture is this chain:

$$
\text{scaffold syntax}
\;\xrightarrow{\;\mathcal{S}\;}
\pi_{\mathcal{D}}(\tau \mid x)
\;\xrightarrow{\;\times \Phi \text{ and normalize}\;}
p_{\mathcal{D}}(\tau \mid x)
\;\xrightarrow{\;\text{sum over continuations}\;}
Z(s),\,V(s)
\;\xrightarrow{\;\text{twist if } Z \text{ is known}\;}
\pi(\cdot \mid s).
$$

The first arrow is semantic interpretation.
The second is change of measure.
The third is backward marginalization over future traces.
The fourth is control: a global target over complete traces becomes a local steered kernel over next moves.

A literal commutative diagram would make the left half exact.
The right half is exact only when $Z$ is exact and the state carries enough information for Markovization.
With estimated values $\widehat{Z}$, the diagram commutes only in a lax, approximate sense.

That chain already links the five posts.
Heavier machinery can wait.

## What to claim, and what to postpone

**Claims that stand:**

- PLP admits a natural stochastic semantics in terms of trace laws and Markov kernels.
- Verifier factors live in a multiplicative monoid of nonnegative weights, or additively in log-space.
- Recursive decomposition is operad-like because it is many-to-one composition over typed child tasks.
- The free-energy, soft-value, and Doob-twist viewpoints meet at the same continuation object $Z(s)$.
- Practical inference algorithms are better described as lax approximations to ideal semantics than as exact realizations.

**Claims to avoid or defer:**

- that each post defines its own autonomous category,
- that AND and OR semantics are literally products and coproducts,
- that the theory already needs adjunctions or natural transformations,
- that the active-inference analogy is an equivalence rather than a careful comparison,
- that category theory is the true foundation of PLP.

The hierarchy is the opposite.
Path-space probability comes first.
Categorical structure follows, as a way to keep composition rules straight.

## Closing

The practical payoff is simple: category theory helps us keep kinds of composition apart.

- Sampling composes as stochastic propagation.
- Factors compose as multiplicative effects.
- Decomposition composes as many-to-one substitution.
- Value functions compose backward over futures.
- Practical algorithms preserve these structures only approximately.

That is enough order for now.
