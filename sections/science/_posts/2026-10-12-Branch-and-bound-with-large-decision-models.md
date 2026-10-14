---
layout: post
title: Merging branch-and-bound with large decision models
description: "Walking ESCO with a Choice-only oracle: classical branch-and-bound, path-product bounds, and why you should ignore shallow leaves."
date: 2026-10-12
published: false
categories:
  - science
  - deep-learning
---

I spent a while trying to map Italian CVs onto [ESCO](https://esco.ec.europa.eu/) without letting a chat model invent skill names.
Fourteen thousand skill leaves.
Groups that fan out past two hundred children.
The usual RAG-plus-LLM pipeline works until it does not, and then you are debugging poetry that almost looks like a taxonomy ID.

So I flipped the interface.
The only model in the loop is a large *decision* model (Jev): Choice questions, calibrated probabilities, menu size capped around 255, including an honest `none of these`.
No free text.
No embedding index.
Just "which of these children fits this CV?" asked again and again while walking the tree.

The interesting part is not the API call.
It is what you do when the good leaf is two hops under a sibling you were about to ignore.

## The score is a product, on purpose

Every edge gets a probability $$p$$ from Jev.
A leaf's score is the product along the path from the root:

```text
score(leaf) = Π p(edge) along root → … → leaf
```

In logs, that is a sum, which is what you actually store:

```python
logp = logp + math.log(max(prob, 1e-12))
```

Products are mean.
Miss early and you pay forever.
Nail the last Choice and you still inherit every doubtful ancestor.
That is the point: the taxonomy path is a hypothesis, not a bag of local hits.

The search goal is then boring in a good way: return the top-$$k$$ leaves under that score, using as few Choice calls as you can get away with.

## Greedy is a trap; beam is a softer trap

Greedy descent: always take $$\arg\max p$$.
One path.
Fast.
Wrong as soon as the root is ambiguous, which is most of the time on real CVs.

Beam search: keep the best $$B$$ nodes per level, drop the rest.
Looks responsible in a PR.
The drop is the bug.
A node you prune at depth two can hide a leaf whose full path product beats everything under the survivors.
You never reopen it.
In a bushy taxonomy that is not an edge case; it is the default failure mode.

I wanted the CLRS move: keep the pruned nodes around with an optimistic bound, and reopen them when the incumbent set looks weak.

## Branch and bound, with Jev on the edges

Every probability is at most 1, so the path product at an internal node upper-bounds every leaf beneath it.
No descendant can outscore its ancestor.
That is the admissible bound.

Hold a set $$L$$ of the best $$k$$ complete leaves so far.
Let $$c$$ be the $$k$$-th best score (or $$-\infty$$ until $$L$$ is full).
Any waiting group whose bound sits under $$c$$ is dead.
Any waiting group that still clears $$c$$ must be expanded, even if you left that sector an hour of wall-clock ago.
That reopening *is* the backtracking.

Jev only ever ranks siblings inside one Choice.
Branch and bound turns those local rankings into a global walk with a stopping rule you can defend.
On trees this is the lazy form of the usual DP recurrence:

```text
best(u) = max over children v of  p(v|u) * best(v)
best(leaf) = 1
```

You just do not fill the table.
You expand the open nodes whose bound can still win.

<img src="/static/postfigures/branch_and_bound_jev.png" alt="Best-first branch-and-bound with a Choice oracle, algorithm2e pseudocode" style="width:100%; display:block; margin: 0 auto; margin-bottom: 0.5em;">

The queue is keyed by bound (I keep $$-\sum\log p$$ so a heap works).
Each round pops a small batch, asks Jev in parallel, pushes child groups, and admits deep leaves into $$L$$.
Stop when the queue cannot beat $$c$$, or when the request budget dies.
Softmax over the survivors is makeup for the JSON output.
It does not touch the bound.
If you softmax inside the search you have broken the proof and you will not notice until a demo.

A sketch of the leaf update, minus the batching noise:

```python
if info[child]["kind"] == "group":
    heapq.heappush(waiting, (-logp, -depth, child, depth))
elif depth >= min_depth:
    found[child] = (logp, conf)
    heapq.heappush(best, (logp, child))
    if len(best) > top_k:
        found.pop(heapq.heappop(best)[1])
```

## The depth footgun

Path products like short paths.
ESCO hangs a lot of transversal skills higher than the sector-specific ones.
If those shallow leaves fill $$L$$, $$c$$ gets tight, the bound prunes the deep sectors, and your "optimal" answer is `solve problems` for every CV on earth.
Ask me how I know.

The fix is unfashionable and works: ignore leaves shallower than the deepest leaf level of the tree when updating the incumbent set.
Groups still expand.
Only deep leaves set $$c$$.
You force the walk to the bottom before anyone gets to declare victory.

```python
if min_depth is None:
    min_depth = max_leaf_depth(children, info)  # 5 on ESCO skills
# ...
if depth < min_depth:
    continue  # do not let shallow transversals set the cutoff
```

On a logistics CV that single guard moved the top hits from "organise information / solve problems / lead others" to logistics, petroleum, direct distribution.
Same oracle.
Same bound.
Different admission rule.

## What I am actually after

I want a taxonomy walk that is honest about uncertainty and cheap on real documents.
Honest: every edge weight is a Choice probability, and you stop for the classical reason (bound below cutoff) or because you ran out of money.
Cheap: on the order of ten API rounds per tree in practice.
Most of the bush dies without a request.

The bet underneath is simple enough for a comment thread.
Large *decision* models as local oracles inside old search algorithms are a different design point from large *language* models asked to invent the answer.
Keep the discrete structure.
Keep the search guarantee (top-$$k$$ under a path product, modulo the depth floor).
Ask the model only the question it is good at: pick among a short, named menu.

Branch and bound is not new.
Wiring a calibrated Choice model into every branching factor is the part I am poking at.
If the taxonomy is the state space and Jev is the local kernel, the rest is lazy DP with a pruning rule you can draw on a napkin.
