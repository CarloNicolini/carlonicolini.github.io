---
layout: post
title: Scaffolding is all you need
date: 2026-03-25
published: true
---

Recursive LLM stacks are everywhere: plan, decompose, call tools, merge partial answers. The hope is that splitting work beats one long chain of thought. 
A theory note I am writing says otherwise in general: *branching is not a free reliability gain*. 
What matters is whether your *semantics* of merging children match how you can verify and select. 

This post sketches the setup: what a scaffold is, why it is a stochastic branching process, and how reliability decomposes into local pieces you can reason about.

### What is a scaffold?

Fix a task space $\mathcal{X}$ and a response space $\mathcal{Y}$. A single LLM call implements some conditional law $\pi_{\mathrm{ref}}(\cdot \mid x)$ over answers. A **scaffold** is everything you wrap around that kernel: prompts that decide whether to answer or split, procedures that emit child tasks, verifiers, and compositors that stitch child outputs back into a parent answer.

The abstract object we study is a **node-local answer-or-decompose policy** $\Pi$. At each node you see a task prompt $x_u$, a local control prompt $Q_u$ (system hints, tools, memory), and a binary mode $M_u \in \{\mathrm{ans},\mathrm{dec}\}$. If $M_u=\mathrm{ans}$, you sample an answer $Y_u$ from an answer kernel $q_{\mathrm{ans}}(\cdot \mid x_u,Q_u)$. If $M_u=\mathrm{dec}$, you sample a finite tuple of child prompts $(x_{u,1},\ldots,x_{u,K_u})$ from a decomposition kernel $q_{\mathrm{dec}}(\cdot \mid x_u,Q_u)$, then recurse on each child with its own control prompt. That is the usual plan-and-execute, tree search, or agent loop pattern, stripped to the control flow.

Correctness is defined against a ground-truth verifier $r^\star(x,y) \in \{0,1\}$ and the correctness set $\mathcal{S}^\star(x) = \{y : r^\star(x,y)=1\}$. 
The ground truth verifier is the most important object that we can only approximate. 
It says that the LLM answer $y$ for the task $X$ is correct or not.
Think about it.
The ground-truth verifier is a mind-reading oracle and we try to approximate it with the internal LLM knowledge. 
For example, who says that the answer to an open-ended question is better than another one? 
Nonetheless we need to have this object in our arsenal. 
In classical training-time alignment algorithms, the ground-truth verifier is often fed by means of Lean theorem proving, code tests or even human-based preferences. 
Here we try to use the LLM internal text generation abilities to extend it to any test-time task.

The scaffold's kernels need not equal $\pi_{\mathrm{ref}}$ exactly; the theory only needs well-defined probabilities.

### A random tree, not a fixed diagram

Running $\Pi$ on a root task $x$ does **not** produce a fixed tree. It produces a **random rooted tree** $T_\Pi(x)$: the branching factor $K_u$, the child prompts, and the mode choices are all draws from the policy and the LLM. Think of it as a **branching process** induced by stochastic policies: each node flips a coin (answer vs decompose), and if it decomposes it draws how many children and what they are. In applications you usually enforce finiteness almost surely (depth cap, token budget, or a policy that eventually answers with probability one).

So "recursive decomposition" in production is really **random recursive decomposition**. Reliability analysis has to average over that randomness, not over a single hand-drawn tree.

### Reliability and three separate success bits

Write $Z_u \in \{0,1\}$ for "node $u$ succeeded" under $r^\star$. Root reliability is
$$
R_\Pi(x) := \mathbb{P}_\Pi(Z_\varnothing = 1 \mid x).
$$

At a **decomposition** node, three things matter and should not be collapsed into "the model failed":

1. **Decomposition validity** $V_u$: whether the child tasks are an admissible split of the parent task.
2. **Child success** $Z_{u,i}$: whether each child subtree reaches a correct answer for its subtask.
3. **Composition** $C_u$: whether the merge or selector turns child outputs into a correct parent answer.

The composer can be deterministic, another LLM, or a learned ranker; the theory summarizes it by an **effective rule** $\Psi_u(z_1,\ldots,z_K) \in [0,1]$: the probability that composition succeeds given validity and a vector of child success bits. On a decomposition node, $Z_u$ tracks $V_u$ and $C_u$ together with the children (see the note for the exact indicator).

### Local recursion

Let $p_u^{\mathrm{ans}} = \mathbb{P}(M_u=\mathrm{ans}\mid x_u,Q_u)$ and $p_u^{\mathrm{dec}} = 1 - p_u^{\mathrm{ans}}$. Let $a_u$ be the probability that a direct answer lands in $\mathcal{S}^\star(x_u)$, and let $d_u$ be the probability of success at $u$ conditional on choosing to decompose.

Then reliability at node $u$ splits cleanly into modes:
$$
R_u = p_u^{\mathrm{ans}}\, a_u + p_u^{\mathrm{dec}}\, d_u.
$$

So "answer vs decompose" is explicit: you pay $a_u$ on the answer branch and $d_u$ on the decomposition branch, weighted by the policy.

**Conditional independence** (children solved in fresh interactions, dependence only through the decomposition draw) is the usual assumption: given child prompts and their local controls, $(Z_{u,1},\ldots,Z_{u,K})$ are independent Bernoullis with $\mathbb{P}(Z_{u,i}=1) = R_{u,i}$. Then $d_u$ is determined by $V_u$, the $\Psi_u$ rule, and those child reliabilities; exactly the place where AND vs OR semantics enter.

### AND semantics vs OR semantics

Under **conjunctive** (AND-like) composition, only the all-success pattern survives: schematically $\Psi_u(z) \propto \prod_i z_i$. Then (ignoring random $K$ for the slogan) reliability along the decomposition branch scales like a **product** of child reliabilities. Extra width adds **mandatory** gates; it does not add alternatives.

Under **search/select** (OR-like) composition, success needs **at least one** successful child and a trustworthy selector. With independent children and homogeneous per-child reliability $r$,
$$
d_u \approx c\,\mathbb{E}\bigl[1-(1-r)^{K_u}\bigr]
$$
in the idealized case (valid split, composition factor $c$). That is the "at least one success" probability: width can **help** because you are drawing multiple shots.

So the headline is not "trees good" or "trees bad," but: are you branching into **alternatives you can verify** (OR), or into **substeps that must all pass** (AND)?

### Verifiers and the Youden index

To improve the local answer law, a minimal device is **reject sampling**: draw from the model, accept with an imperfect verifier $\hat r(x,y)$. The post-acceptance mass on correct answers is
$$
\nu_x(\mathcal{S}^\star(x)) = \frac{\alpha_x p_x}{\alpha_x p_x + \beta_x(1-p_x)},
$$
where $p_x$ is the raw correctness rate, $\alpha_x$ is the true positive rate, and $\beta_x$ the false positive rate. For $0 < p_x < 1$, filtering **strictly improves** correctness iff $\alpha_x > \beta_x$, i.e. the Youden index $\alpha_x - \beta_x$ is positive. That is the precise sense in which "a better verifier" helps the OR-style branch.

### Global picture: essential nodes

A **finite-tree** bound packages local failures: if you can identify a set of *essential* nodes such that root failure implies failure at one of them, then root failure probability is bounded by the sum of local failure probabilities (union bound). If every essential node fails with probability at most $\varepsilon$ and there are $O(1)$ of them in expectation, you get $R \ge 1 - O(\varepsilon)$; under a family of scaffolds with $\varepsilon \to 0$ and bounded essential complexity, $R_\Pi(x) \to 1$.

The engineering takeaway is the same: **essential steps are a tax**. Branch when OR-style search or verification pays for the extra width; do not add AND-style depth without a compensating gain.

### What I would ship

When you lack a checker for every slice, prefer **diverse full solutions plus selection** over **default mandatory subtasks** that bake in AND risk. Invest in verifiers with positive Youden index for whatever you filter. Before decomposing ambiguous tasks, spend tokens on constraints and success criteria; that raises decomposition validity before you pay for a bad split. Treat decompositions that add essential steps as costly unless the expected benefit clearly dominates.

Recursive decomposition is not a reliability theorem by itself. It starts to behave like one when semantics, verification, and tree complexity line up, and when you know which nodes are truly essential.

---

*This post distills a working note on reliability in node-local answer-or-decompose scaffolds.*
