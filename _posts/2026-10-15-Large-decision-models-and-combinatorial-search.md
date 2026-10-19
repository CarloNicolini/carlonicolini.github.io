---
layout: post
title: "Large decision models and combinatorial search"
description: "Notes on using Jev and other decision models as branching oracles: Sudoku, A* tie-breaking, and the experiments needed to tell useful guidance from expensive guesswork."
date: 2026-10-15
published: true
permalink: "/sections/science/2026/10/15/Large-decision-models-and-combinatorial-search.html"
categories:
  - science
  - ai
  - math
---
{% assign previous_notes = site.posts | where: "slug", "Branch-and-bound-with-large-decision-models" | first %}
In my {% if previous_notes %}[previous notes on branch-and-bound and Jev]({{ previous_notes.url | relative_url }}){% else %}previous notes on branch-and-bound and Jev{% endif %}, I was walking the ESCO skills taxonomy. A CV supplied the context, Jev assigned probabilities to the children of a taxonomy node, and a classical search algorithm decided which groups still deserved a visit. That left me with a question I kept coming back to: how much of this arrangement survives when the problem has explicit constraints and an objective that exists independently of the model?

A Sudoku has legal assignments. A shortest-path problem has distances. A knapsack has a capacity and item values. In each case, a solver already knows how to check its work. What it often cannot know cheaply is which of several perfectly legal decisions will save it the most work later.

That is the opening I want to explore with large decision models. Give the model a small menu at a branching point, let it order the alternatives, and leave the state transitions and constraint checks in ordinary code. A bad recommendation can make the search slower. With the right interface, it need not make the answer wrong.

These are working notes around a small experiment in `jevsearch`. The repository currently contains exact backtracking for Sudoku and A* for grid navigation, with a separate decision-policy interface. Its saved offline report checks the machinery; it contains **no model calls and no evidence of a model advantage**. I want to keep that boundary visible while thinking through what would make the experiment interesting.

## From a taxonomy score to a search policy

There is a difference from the ESCO walk that deserves a little care. In that earlier setup, the search objective was a product of model probabilities along a taxonomy path. An exact search could recover the highest-scoring leaves under that definition. Whether those scores represented the right skills was a separate empirical question.

Here, the model has less authority. The objective might be the length of a path, and the model cannot redefine a metre.

Let a search state be $$s\in\mathcal S$$, with admissible actions $$A(s)$$ and deterministic transitions

$$
s'=T(s,a).
$$

The solver constructs the action set. A decision oracle receives a compact representation $$\phi(s)$$ and returns a policy

$$
\pi_\theta(a\mid\phi(s),A(s)).
$$

We can sort the actions by this policy, or sample an ordering without replacement. Backtracking still tries the remaining alternatives when the first one fails. Even an action given zero probability remains available to the exact search.

This is a natural fit for Jev's interface. TypeSafe's [Choice documentation](https://docs.typesafe.ai/primitives/choice) describes a question over a fixed menu, returning a selected option and probabilities for every option, with up to 255 choices. Those probabilities are useful inputs to a policy; their calibration for *search effort* remains something to measure.

Learning branching rules already has a substantial history. For example, [Gasse and colleagues](https://arxiv.org/abs/1906.01629) trained a graph neural network to select branch-and-bound variables by imitating strong branching. My question is narrower: can a pretrained decision model provide useful guidance across problems through this small interface, before training a separate policy for each domain?

The guarantee belongs to the surrounding algorithm. For a finite backtracking problem, sound propagation and exhaustive exploration preserve completeness regardless of the ordering. Branch-and-bound additionally needs valid bounds. A run stopped by a node or time budget may leave the question unresolved, and its output should say so.

## Start with Sudoku, and resist making it too clever

Sudoku is a convenient first test because the rules fit in a paragraph and a completed board is easy to verify. It also has a trap: an easy puzzle can be solved entirely by propagation, leaving the model with nothing to do.

The implementation propagates naked and hidden singles until it reaches a fixed point. If a row already contains a digit twice, or a cell has no possible value, the branch fails. Otherwise, the solver selects a cell using minimum remaining values, breaking ties by the number of unassigned peers and then by position.

For this first comparison, **only the value order changes**. All policies see the same propagation and the same variable-selection rule. If the selected cell allows 2, 5, and 8, the question is which of those values to try first. Asking the model to select the cell as well would be a sensible later intervention, but it would change two things at once.

The abstraction is small enough to write down:

```python
from typing import Callable, Mapping

Oracle = Callable[[Decision], Mapping[str, float]]
```

Here `Decision` contains the state summary, instructions, and legal actions with stable IDs. The callable returns a weight for every ID. A policy wrapper checks that the weights are finite and nonnegative, normalizes them, and produces a complete ordering. Unknown IDs, missing actions, or a failed request cause a recorded fallback to the classical order.

The backtracking routine only sees that ordering:

```python
# Schematic: propagation and verification belong to the problem.
def visit(state):
    state = problem.propagate(state)
    if state is None:
        return None
    if problem.is_goal(state):
        return state

    decision = problem.decision(state)
    for action_id in policy.order(decision):
        answer = visit(problem.transition(state, action_id))
        if answer is not None:
            return answer
    return None
```

There is no HTTP client in this recursion. That makes the experiment easy to vary: a deterministic heuristic, seeded random ordering, and a remote model can all occupy the same slot. It also makes failures inspectable. A solved board after ten failed requests establishes that fallback works; it says nothing about the model's Sudoku ability.

For the inexpensive prototype, the transport is configured for [`inception/mercury-decide:free` on OpenRouter](https://openrouter.ai/inception/mercury-decide:free), using Python `requests`. That choice keeps Jev as the motivation while allowing a different model to test the interface. Results from Mercury would be results from Mercury, and would need to be repeated with Jev before saying anything specific about Jev.

## What the first offline checks actually tell me

The saved report, `results/offline.md`, runs classical and seeded random policies on a few selected Sudoku fixtures. All returned boards pass verification. The easy 9×9 puzzle is solved in one visit to the backtracking routine, with no policy calls. So is a fixture named `nine_branch`, which is a useful reminder that a filename is not a measurement of difficulty.

The small 4×4 fixtures exercise one or two decisions, but they do not distinguish the policies by search effort in this report. Their purpose is to catch wiring mistakes. They are too forgiving to support a claim about a better branching rule.

Before a model comparison, I need puzzles where the fixed classical solver actually backtracks. The important selection criterion is observable ambiguity *after the same propagation*, rather than the puzzle's advertised difficulty. I would keep separate instance sets for developing the prompts and evaluating the final policy, and include a cheap least-constraining-value baseline. Random order is a useful control, though it is a low bar.

I would also test unsatisfiable instances. With fixed variable selection, exhaustive backtracking, and no order-dependent learning or pruning, changing the value order generally just rearranges the work needed to prove failure. Finding the first solution offers a much clearer opportunity for an ordering policy to save nodes.

## A* gives the model a smaller job

Grid navigation makes the same idea easier to watch. Imagine a warehouse floor with walls, a start, and a destination. For four-neighbour movement with unit costs, A* uses

$$
f(n)=g(n)+h(n),
\qquad
h(n)=|x_n-x_\star|+|y_n-y_\star|.
$$

Manhattan distance is a lower bound on the remaining path length in this setting. Walls can force a detour, but they cannot make the goal closer than that bound.

I let the policy choose **among frontier nodes with equal minimum $$f$$**. It receives the map and the candidate nodes, including their $$g$$ and $$h$$ values. It can prefer a corridor that looks promising, while A* retains its primary priority rule.

This is slightly different from asking “north, south, east, or west?” The candidates are states already waiting in the frontier; they can lie in different parts of the map. The search has a memory of alternatives that a single greedy walk lacks.

The implementation presents a bounded window of tied candidates to keep the question small. Unselected nodes return to the queue, and candidates outside the window remain there too. Improved paths reopen states. The solver accepts a goal when it removes it for expansion. Under the usual A* assumptions, these rules preserve optimality; on the finite unit-cost grids, breadth-first search independently checks the returned cost.

The offline expansion counts are already instructive:

| Grid fixture | A*, FIFO ties | A*, smaller-$$h$$ ties |
|---|---:|---:|
| Open room | 45 | 13 |
| Detour | 40 | 28 |
| Warehouse | 52 | 17 |

These are three selected smoke fixtures, using the repository's expansion counter, which includes the goal. There is no model in either column. On an open grid, a large part of the frontier can have the same $$f$$; preferring smaller $$h$$ pushes the search toward the destination along that plateau. A simple numerical rule already saves many expansions.

That is the comparison a model has to earn. Beating FIFO while losing to the smaller-$$h$$ rule would teach me about tie-breaking, without establishing a useful reason to call an API.

For a TypeScript visualization, I would show the expansion trace beside the map: the equal-$$f$$ candidates, the chosen node, and the frontier left waiting. The final shortest path alone hides most of the experiment. Two policies may return the same path after exploring very different regions. A trace should also label model choices and fallback choices separately. This applet is a next step, rather than a result of the offline checks described here.

## Where fewer nodes might become useful

A tiny grid is almost designed to make a remote oracle look uneconomical. Local expansions take very little time. A policy can save half of them and still lose badly once request latency is included.

A rough accounting is

$$
T_{\rm guided}
\approx N_{\rm guided}\,\bar t_{\rm expand}
+\sum_{j=1}^{K}t_{\rm oracle,j}
+T_{\rm bookkeeping}.
$$

This ignores overlap between requests and search, but it exposes the tradeoff. Expensive expansion makes guidance more attractive. So does a policy that can be queried rarely, at consequential branching points. Calling the model after propagation leaves one legal move buys nothing.

Branch-and-bound is a better place to look for an amplified effect. In 0–1 knapsack,

$$
\max_{x\in\{0,1\}^n}\sum_i v_ix_i
\quad\text{subject to}\quad
\sum_i w_ix_i\leq W,
$$

a good early feasible solution raises the incumbent value, allowing valid upper bounds to prune more of the tree. The model could choose an undecided item to branch on, or decide which of its include/exclude branches to try first. The capacity check and bound calculation stay explicit.

Here the question “which variable should I branch on?” differs from “which items belong in the optimum?” A variable can be useful to branch on because either outcome sharply constrains what remains.

Dynamic programming is less automatically promising. If an acyclic exact DP evaluates every reachable state and every transition anyway, changing their order may save no evaluations at all. Memoization avoids repeated work; a persuasive model ranking does not add another saving by itself. Guidance becomes relevant when it helps establish bounds, supports early termination, or allocates a limited computation budget.

## Back to skills, then toward SAT

The ESCO connection suggests a more semantic test. Suppose an occupation requires skills $$U$$, and course $$i$$ covers $$C_i\subseteq U$$ at cost $$c_i$$. A basic training-plan model is weighted set cover:

$$
\min_{x_i\in\{0,1\}}\sum_i c_ix_i,
\qquad
\bigcup_{i:x_i=1}C_i\supseteq U.
$$

A numerical baseline can rank courses by newly covered skills per euro. A decision model can also read course descriptions and the learner's background. Perhaps that context helps it suggest branches that lead to a good feasible plan earlier.

I would want to know exactly what information produced the advantage. If prerequisites matter, they need explicit constraints. If semantic suitability matters to the final objective, it needs an operational definition. Otherwise the model can quietly optimize a preference the solver never agreed to measure. A useful ablation would compare numerical features alone with those same features plus descriptions.

{% assign ksat_notes = site.posts | where: "slug", "K-SAT-and-Survey-propagation" | first %}
My work on {% if ksat_notes %}[K-SAT and survey propagation]({{ ksat_notes.url | relative_url }}){% else %}K-SAT and survey propagation{% endif %} makes Boolean search an obvious temptation too. In DPLL, a policy can choose a branching variable or polarity while unit propagation and exhaustive backtracking retain responsibility for the answer.

For backtracking survey propagation, I would try a smaller intervention: preserve the message equations and let a policy select among candidate variables to unfreeze when progress stalls. Survey biases and recent backtracking history would enter the state summary. That would test an algorithmic policy change, and would need comparisons at matched computational cost. BSP itself does not acquire an exhaustive SAT solver's completeness guarantee from this interface.

Random K-SAT also strips away much of the language information that might justify a pretrained model. If the prompt only repackages occurrence counts and survey statistics, a cheap learned numerical rule may be the stronger choice. Structured planning problems give a semantic model more to work with. I would be interested in either outcome, provided the comparison makes that distinction visible.

## The experiment I would trust

The main measurement is search effort under a fixed continuation policy. For a state $$s$$ and a candidate first action $$a$$, write

$$
N(s,a)=\text{nodes visited when trying }a\text{ first,
with the remaining policy fixed}.
$$

On small instances, the solver can explore several such counterfactuals and provide supervision for a branching policy. Computing those labels costs search too. It belongs in the training budget, and states from one puzzle should not leak across training and test splits.

An XGBoost predictor could use ordinary numerical features, then add the model's choice scores as extra inputs. The useful test would be whether those scores improve held-out predictions or search outcomes beyond the numerical model alone. “XGJev” becomes an experimentally meaningful idea at that point.

For the hosted-policy runs, I would report solved fraction under fixed budgets and verified solution quality, alongside expanded nodes and total elapsed time. Request latency, call count, and fallback frequency belong in the same results. A free endpoint removes a monetary charge for a particular run; it does not remove inference time. Missing usage information should remain missing rather than becoming a reported zero cost.

The first results here have mostly helped sharpen the question. Easy Sudoku can remove the decision problem before the oracle sees it. A* can benefit greatly from a tie-breaker that fits on one line. Both observations make the eventual model comparison more demanding, which is useful.

What I want to find is a family of search states where context helps a pretrained decision model choose better than cheap local rules, often enough to repay the cost of asking. The classical solver gives me a way to test that claim without entrusting the model with the definition of a valid answer. For now, that seems like a good reason to keep the interface small and collect the traces.
