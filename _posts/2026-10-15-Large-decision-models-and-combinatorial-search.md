---
layout: post
title: "Large decision models and combinatorial search"
description: "Can a decision model choose better branches? I put Mercury Decide inside a solver, then test whether its advice accounts for what happens later."
date: 2026-10-15
last_modified_at: 2026-10-19
hide_date: true
published: true
permalink: "/sections/science/2026/10/15/Large-decision-models-and-combinatorial-search.html"
categories:
  - science
  - ai
  - math
---
A search algorithm can spend millions of steps regretting one perfectly legal choice. Anyone who has watched a backtracking solver explore the wrong branch knows the feeling. The CPU fan supplies the soundtrack.

I want to know whether a large decision model can help at that fork. Models such as Jev and Mercury Decide return probabilities over a menu of choices. I can use those probabilities as a *policy*: a rule for choosing the next action. Can I embed that policy into a search algorithm and find good answers with less work?

There is a second question hiding inside the first. Does the model account for what happens several choices later? A solver can repair bad advice, so a correct final answer alone tells me little about the model's planning ability.

In this post, I explain how I connect a decision model to an exact solver. I compare Mercury with cheap search rules, then use a controlled test to ask how far its advice reaches. The distinction matters: I want to measure both the usefulness of the combined solver and the quality of the advice itself.

## Where the model fits inside search

I treat the model as an *oracle*: a function that returns advice. I supply the current state and the legal actions. The model returns probabilities, which I use to order the actions. [Jev's Choice interface](https://docs.typesafe.ai/primitives/choice) supports this kind of question. My experiments use Mercury Decide, so the results concern Mercury alone.

For Sudoku, the solver selects an empty cell. Mercury orders its possible values. Every policy gets the same cell selection and constraint propagation, which removes values that the rules exclude. If a branch fails, backtracking tries another value. Even an action with zero model probability remains available.

For A\*, a shortest-path search method, Mercury chooses between waiting states with the same minimum priority. A\* keeps its distance bound and all remaining candidates. I independently compare the returned path length with breadth-first search.

![The solver supplies legal choices, the oracle orders them, and the solver tests each branch.]({{ '/assets/media/postfigures/search-policy-loop.svg' | relative_url }})

*The oracle controls the order. The solver retains the rules and the other branches.*

This arrangement gives the experiment a useful safety net. Exhaustive search can recover from poor advice, although a fixed computation budget can stop it before recovery. I can then ask whether the policy saves enough search work to justify each request.

## Does the policy help the solver?

I compare policies on 12 Sudoku puzzles and eight mazes. Each attempt gets at most 32 expanded states, including the root and goal. An expansion counts as one unit of search work.

| Test | Cheap heuristic: solved | Mercury, highest probability first: solved |
|---|---:|---:|
| Sudoku | 11/12 | 10/12 |
| Maze navigation | 7/8 | 7/8 |

The Sudoku heuristic tries values that leave more choices for other cells. For A\*, the heuristic prefers a tied state with a smaller estimated distance to the goal. On solved mazes, Mercury takes a median of 13 expansions, compared with 15 for the heuristic. These medians exclude unsolved attempts.

I see no clear advantage on this small sample. Fewer expansions also do not establish a speed gain, because remote requests take time. The wider study is incomplete: 395 of 435 tasks are saved, and the request budget is exhausted. The remaining 40 tasks are pending, not failed solutions.

The comparison tests the combined solver. To examine the advice itself, I need a problem where I know exactly which choice leads to success.

## How do I test planning ability?

I use chains of binary variables, where every value is 0 or 1. Each link requires two variables to be equal or different. A final rule fixes the last bit:

```text
A = B, B != C, C = D, D = 1
```

The correct first choice is `A = 0`. Every value after that is forced. Starting with `A = 1` passes the first link but eventually conflicts with `D = 1`.

The model sees the whole problem and chooses the first value. I disable backtracking so that the solver cannot rescue a mistake. I then measure the probability that Mercury assigns to the correct choice. Here, that probability is also the chance of completing the chain when I sample the first action.

I test 40 chains at each length, with both possible final bits. Changing only the final bit reverses the correct first choice. This tests whether the advice responds to the goal. I also randomize variable names and the order of links and choices.

The complete study contains 280 chains and 728 responses, including controls. It gives me a direct question: as the decisive rule gets farther away, does the first choice still account for it?

## What happens when the final rule is farther away?

| Links to the final rule | Mean probability on correct choice | 95% interval |
|---:|---:|---:|
| 2 | 83.3% | 76.6–89.9% |
| 4 | 57.9% | 51.2–64.7% |
| 8 | 46.4% | 42.7–50.2% |
| 16 | 51.4% | 48.5–54.0% |
| 32 | 50.0% | 49.6–50.5% |
| 64 | 51.1% | 49.5–53.7% |
| 128 | 49.9% | 48.6–51.0% |

![Mercury assigns 83.3 percent to the correct action at two links, then stays near the 50 percent uniform reference at longer distances.]({{ '/assets/media/postfigures/mercury-chain-distance.png' | relative_url }})

*Intervals come from resampling whole chains, with both final bits kept together. They describe variation across chains, not repeated calls to one prompt.*

A uniform choice gives 50%. Mercury clearly beats that reference at two links. At four, the evidence is weaker: the interval includes 50% after adjustment for all seven distances. From eight links onward, even the intervals in the table include 50%. A coin remains competitive, despite its complete lack of an API key.

I interpret this as a limit of the policy on this problem family. It does not reveal how many internal reasoning steps Mercury uses. Longer chains also produce longer inputs, so this test cannot fully separate constraint reasoning from input handling. An exact solver can solve every chain by propagating backward from the final bit in linear time.

## What if several decisions must all succeed?

A useful first choice still leaves the rest of the problem. I calculate the chance of completing several distinct chains when I sample one first action for each. Each policy sees only its own chain, and every chain must succeed. These calculations use saved probabilities, without additional model trials.

Even for two-link chains, complete success averages 47.4% across four chains and 3.85% across sixteen. Errors accumulate quickly without recovery. This helps explain why I want to embed policies into search: backtracking gives useful but imperfect advice another chance.

The [chain statistics]({{ '/assets/media/postfigures/mercury-chain-statistics.csv' | relative_url }}) and [combined success probabilities]({{ '/assets/media/postfigures/mercury-chain-composition.csv' | relative_url }}) are available for anyone who wants to examine the numbers.

## Where I go from here

I can use a large decision model as a policy inside an exact search algorithm. Whether that policy earns its place remains an experimental question. Mercury helps with the shortest chains, but its advice approaches chance as the final constraint gets farther away. The small search comparison gives me no clear gain over cheap heuristics. I want to test problems with expensive branches, where good advice has more time to repay its cost. If you know someone who builds solvers, share this post with them. Which branching decision would they trust to a model, and what test would convince them that it helps?
