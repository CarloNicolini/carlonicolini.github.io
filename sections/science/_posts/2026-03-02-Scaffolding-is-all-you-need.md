---
layout: post
title: Scaffolding is all you need
description: "When recursive LLM scaffolds improve reliability—and when they cannot."
date: 2026-03-25
published: true
categories:
  - science
  - language-physics
---

## Toward a reliability theory of AI compound systems

Recursive LLM stacks are everywhere: plan, decompose, call tools, merge partial answers.
The common hope is that splitting work beats one long chain of thought. This happens every time an AI agent prepares a plan before acting.

This note argues that branching is not a free reliability gain.
What matters is the semantics of the branch, the quality of local verification, and the timing of commitment.

This post sketches the setup: what a scaffold is, why it is a stochastic branching process, and how reliability decomposes into local pieces that we can reason about.

## What is a scaffold?

Following the formulation of reasoning as a Markov Decision Process (MDP), let us fix a state space $\mathcal{S}$ and an action space $\mathcal{A}$, where both can be represented as strings over an alphabet $\Sigma$. A reasoning task begins at an initial state $s_0 \in \mathcal{S}$ (the prompt or problem). A single LLM call implements a conditional transition policy $\pi_{\mathrm{ref}}(a \mid s)$ over valid next actions $a \in \mathcal{A}$. A **scaffold** is everything you wrap around that kernel: prompts that decide whether to continue reasoning, procedures that sample candidate actions, search mechanisms (like backtracking from dead ends at the scaffold control level), verifiers, and compositors that evaluate if a goal state has been reached.

The abstract object we study is a **node-local answer-or-decompose policy** $\Pi$.
At each state $s_u$, you see a local control prompt $Q_u$ (system hints, tools, memory), and a binary mode $M_u \in \{\mathrm{ans},\mathrm{dec}\}$.
If $M_u=\mathrm{ans}$, you sample a sequence of terminal actions to form an answer $y_u$ from an answer kernel $q_{\mathrm{ans}}(\cdot \mid s_u,Q_u)$, transitioning directly toward a goal.
If $M_u=\mathrm{dec}$, you sample a finite tuple of candidate actions $(a_{u,1},\ldots,a_{u,K_u})$ from an exploration kernel $q_{\mathrm{dec}}(\cdot \mid s_u,Q_u)$. Each action produces a new child state $s_{u,i} = s_u \oplus a_{u,i}$ (where $\oplus$ denotes string concatenation), and then you recurse on each child with its own control prompt. This represents the usual plan-and-execute, tree search, or agent loop pattern, stripped to the control flow.

Correctness is defined against an MDP reward function acting as a ground-truth verifier $R^\star(x,y) \in \{0,1\}$ and the correctness set $\mathcal{S}^\star(x) = \{y : R^\star(x,y)=1\}$.
The object $R^\star$ is idealized and usually unavailable in full.
It states whether the terminal trajectory or answer $y$ for task $x$ is correct.
For open-ended tasks that object is clearly not observable without extra assumptions, which is exactly why deployed systems replace it with tests, theorem provers, preference models, or human judgments.
The point of keeping $R^\star$ in the formalism is not realism but identifiability: it separates truth from the imperfect judges that a scaffold can actually use.

The scaffold's kernels need not equal $\pi_{\mathrm{ref}}$ exactly; the theory only needs well-defined probabilities over the MDP transitions.

### Story of a random tree

Running $\Pi$ on a root task $x$ does **not** produce a fixed tree but a **random rooted tree** $T_\Pi(x)$: the branching factor $K_u$, the child prompts, and the mode choices are all draws from the policy and the LLM.
Think of it as a **branching process** induced by stochastic policies: each node flips a coin (answer vs decompose), and if it decomposes it draws how many children and what they are.
In applications you usually enforce finiteness almost surely (depth cap, token budget, or a policy that eventually answers with probability one).

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

<figure>
  <img src="/static/postfigures/random_rooted_tree.svg" alt="recursive decomposition tree inducing a random rooted tree" style="width: 70%; display: block; margin: 0 auto;" />
  <figcaption>
    <strong>Figure 1.</strong> A scaffolded policy induces a random rooted tree: each node either answers directly or stochastically decomposes into child tasks. Leaves correspond to local answers, while internal nodes represent decomposition and subsequent composition. The branching factor, depth, and structure are random, reflecting node-local answer-or-decompose decisions. The root reliability emerges from the recursive aggregation of child successes under the chosen composition semantics.
  </figcaption>
</figure>

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

The baseline message is simple: are we branching into alternatives that can be verified (OR), or into substeps that must all pass (AND)?

### Verifiers and the Youden index

To improve the local answer law, a minimal device is **reject sampling**: draw from the model, accept with an imperfect verifier $\hat r(x,y)$. The post-acceptance mass on correct answers is
$$
\nu_x(\mathcal{S}^\star(x)) = \frac{\alpha_x p_x}{\alpha_x p_x + \beta_x(1-p_x)},
$$
where $p_x$ is the raw correctness rate, $\alpha_x$ is the true positive rate, and $\beta_x$ the false positive rate. For $0 < p_x < 1$, filtering **strictly improves** correctness iff $\alpha_x > \beta_x$, i.e. the Youden index $\alpha_x - \beta_x$ is positive. That is the precise sense in which "a better verifier" helps the OR-style branch.

### Global picture: essential nodes

A **finite-tree** bound packages local failures: if you can identify a set of *essential* nodes such that root failure implies failure at one of them, then root failure probability is bounded by the sum of local failure probabilities (union bound). If every essential node fails with probability at most $\varepsilon$ and there are $O(1)$ of them in expectation, you get $R \ge 1 - O(\varepsilon)$; under a family of scaffolds with $\varepsilon \to 0$ and bounded essential complexity, $R_\Pi(x) \to 1$.

The engineering takeaway is the same: **essential steps are a tax**. Branch when OR-style search or verification pays for the extra width; do not add AND-style depth without a compensating gain.

### Delayed commitment is a control action

The binary answer-or-decompose formalism is the right abstraction for analysis.
In deployment there is usually a third useful move: delay commitment.
Instead of answering immediately or launching a brittle AND-style split, the scaffold can spend compute to clarify the task, retrieve evidence, or keep a small OR frontier alive.
In the free-energy language of [PLP is inference-time approximation of free energy]({% link sections/science/_posts/2026-03-31-PLP-is-inference-time-approximation-of-free-energy.md %}), this move preserves option value by keeping several continuation basins available.

Kappen's path-integral formulation of stochastic control makes the same point in a cleaner mathematical setting {% cite kappen2005path %}.
In his symmetry-breaking examples, the optimal controller does not always commit early to one route.
When noise and time-to-go are large, it can be better to delay the decision and commit only later, once the landscape becomes easier to separate.
The same logic applies to reasoning scaffolds.
When several global solution basins remain plausible, an early hard decomposition can be the wrong control action.

### An optimal-control decomposition policy

Putting the reliability and control viewpoints together suggests a simple policy.

1. Answer directly when the direct branch is reliable enough and the remaining horizon is short.
2. Use OR-style search when several whole-solution alternatives can be checked or ranked.
3. Delay commitment when ambiguity is high and extra evidence is still cheap to gather.
4. Use AND-style decomposition only when child tasks are locally verifiable and the composition interface is stable.
5. Collapse the frontier only after one basin clearly dominates, or when the remaining budget no longer justifies more search.

In short, branching is valuable when it buys optionality or verification.
It is costly when it creates essential steps.
The best scaffold is therefore not "always decompose".
It is a controller that knows when to answer, when to search, when to wait, and when to commit.

---

## References

{% bibliography --cited %}
