---
layout: post
date: 2026-05-08
title: "Graph metrics on task-evoked CKA connectomes: GSM8K vs MMLU philosophy"
description: "Can we build small world and hub structures in the functional connectome of a LLM when solving problems? \nThis post is a short empirical companion to two threads on this blog: the **CKA functional connectome** viewpoint in [Similarity of neural networks representations]({% link sections/science/_posts/2026-04-29-Similarity-of-neural-networks-representations.md %}), and the **network-neuroscience dictionary** for LLMs sketched in [Functional synthetic LLM connectome analysis]({% link sections/science/_posts/2026-04-28-Functional-synthetic-llm-connectome-analysis.md %})."
published: false
categories:
  - science
  - deep-learning
---

This post is a short empirical companion to two threads on this blog: the **CKA functional connectome** viewpoint in [Similarity of neural networks representations]({% link sections/science/_posts/2026-04-29-Similarity-of-neural-networks-representations.md %}), and the **network-neuroscience dictionary** for LLMs sketched in [Functional synthetic LLM connectome analysis]({% link sections/science/_posts/2026-04-28-Functional-synthetic-llm-connectome-analysis.md %}). There I argued in prose that Louvain modularity, betweenness, and path statistics are meaningful reads on layer graphs. Here I finally run a concrete pipeline—on real matrices, with the same tool chain fMRI papers use.

## Setup

**Nodes** are the $$L = 64$$ residual-stream depths of a single frozen decoder (the same backbone used across tasks in the `rys` experiments). **Edges** are **linear CKA** similarities between layers, evaluated on *generated* activations for two benchmarks:

- **GSM8K** — primary-school math word problems (`cka_gsm8k.parquet`).
- **MMLU philosophy** — multiple-choice philosophy items (`mmlu_philosophy.parquet`).

Each dataset yields a symmetric matrix $$W \in \mathbb{R}^{L\times L}$$ with $$W_{ij} \in [0,1]$$. I zero the diagonal so strengths and modular decompositions are not dominated by the trivial self-similarity.

All graph quantities below come from [**BCTpy**](https://github.com/aestrivex/bctpy), the Python port of the Brain Connectivity Toolbox {% cite rubinov2010complex %}.

## Why BCT, and one preprocessing choice

Weighted **betweenness** in BCT is defined on a **length** matrix: high similarity must map to *short* distance. I follow the library’s documented convention and feed **`invert(W)`** into `betweenness_wei`, so hub layers are those that lie on many *short* paths when distance is inversely related to CKA.

The CKA graphs are **almost complete**: off-diagonal similarities on GSM8K range from about $$0.09$$ to $$0.996$$ (median $$\approx 0.58$$); on philosophy from about $$0.055$$ to $$0.993$$ (median $$\approx 0.54$$). In a dense clique, **binary** shortest-path length is nearly useless (diameter one). For `betweenness_bin` and for **characteristic path length** I therefore keep the **top quartile** of off-diagonal weights as a binary **backbone** (fixed $$q = 0.75$$), which holds edge density at $$0.25$$ on the upper triangle by construction. The two backbones overlap strongly: **Jaccard index $$\approx 0.83$$** on edge sets—so the “heavy” CKA couplings are largely shared across tasks even when scalar summaries differ.

## Global summaries ($$\gamma = 1$$ Louvain, fixed seed)

| Quantity | GSM8K | MMLU philosophy |
| :--- | ---: | ---: |
| Louvain communities $$K$$ | 3 | 3 |
| Optimised modularity statistic $$q$$ | $$0.107$$ | $$0.136$$ |
| Mean weighted clustering (`clustering_coef_wu`) | $$0.515$$ | $$0.469$$ |
| Mean participation coefficient (w.r.t. Louvain $$c_i$$) | $$0.588$$ | $$0.571$$ |
| Weighted global efficiency (`efficiency_wei` on $$\mathrm{invert}(W)$$) | $$3.94$$ | $$5.10$$ |
| Backbone characteristic path length $$\lambda$$ | $$3.31$$ | $$3.02$$ |
| Backbone binary global efficiency | $$0.488$$ | $$0.501$$ |

**Reading.** At the *default* Louvain resolution both tasks split the depth axis into **three** modules—not a fine-grained “every layer is its own community” picture, but not a single blob either. Philosophy attains a **higher** $$q$$ than GSM8K at the same $$\gamma$$ and RNG seed, which is consistent with **slightly stronger modular segregation** in the similarity graph for that benchmark. Mean clustering is **higher** on GSM8K, while weighted global efficiency (on the inverted-length view) is **higher** on philosophy—those two numbers are not directly comparable in magnitude to fMRI papers (the scale depends on how `invert` rescales your weights), but the **ordering across tasks** is stable in the notebook re-runs.

## Task alignment at the level of individual layers

To ask “is layer $$l$$ a hub in both tasks?”, I join the two node tables on $$l$$ and compute Pearson correlation between GSM8K and philosophy columns.

| Node metric | Pearson $$r$$ | Two-sided $$p$$ |
| :--- | ---: | ---: |
| Strength | $$+0.990$$ | $$\ll 10^{-40}$$ |
| Weighted clustering | $$+0.990$$ | $$\ll 10^{-40}$$ |
| Eigenvector centrality | $$+0.993$$ | $$\ll 10^{-40}$$ |
| Participation coefficient | $$+0.479$$ | $$6\times 10^{-5}$$ |
| Within-module degree $$z$$-score | $$+0.655$$ | $$4\times 10^{-9}$$ |
| Binary betweenness (backbone, normalised) | $$+0.661$$ | $$3\times 10^{-9}$$ |
| Weighted betweenness (normalised) | $$+0.372$$ | $$2.5\times 10^{-3}$$ |

**Interpretation I would defend in a methods section.** Strength, clustering, and eigenvector centrality are **almost perfectly correlated** across tasks. That pattern screams **shared backbone geometry**: the model’s residual stream mixes depth in a way that is largely *architecture-first*, independent of whether you are doing grade-school algebra or philosophy multiple choice.

By contrast, **weighted betweenness**—the quantity closest to the “thalamus bottleneck” story in the April-28 post—only shows **modest** cross-task correlation ($$r \approx 0.37$$). Participation and module $$z$$-scores sit in between. That is exactly what you want if **task-specific rerouting** perturbs *which* layers bridge modules without tearing down the overall clique-like coupling structure.

## $$\Delta W$$: where philosophy strengthens or weakens CKA

Elementwise $$\Delta_{ij} = W^{\mathrm{phil}}_{ij} - W^{\mathrm{GSM}}_{ij}$$ has mean about $$-0.039$$ and standard deviation about $$0.046$$ on off-diagonal pairs: globally, this slice of philosophy items is **slightly less uniformly CKA-glued** than GSM8K, but the effect is small compared to pair-to-pair heterogeneity. Localised hot spots in $$\Delta$$ (visible as red/blue blocks in the notebook heatmap) are the right object for a follow-up that ties **specific layer bands** to item difficulty or to sub-scores within philosophy.

## Resolution sweep (Louvain $$\gamma$$)

Repeating `community_louvain` for $$\gamma \in [0.6, 1.8]$$ shows the expected **resolution trade-off**: small $$\gamma$$ merges almost everything (here, a single community at $$\gamma = 0.6$$ with the chosen seed), while large $$\gamma$$ **over-partitions** into dozens of micro-modules and drives the reported $$q$$ toward **zero or slightly negative**—a sign that the modularity objective is no longer a good summary at that scale. The **$$\gamma = 1$$** default used in the table above sits in a middle regime where **three** communities are stable for *both* tasks, which is the sweet spot for reporting in a first paper-style figure.

## Reproducibility

The numbers and Plotly panels are generated in `notebooks/bct_connectome_graph_analysis.ipynb` in the `rys` research repository (same machine-readable Parquet inputs). Dependencies are pinned there via `uv`; graph routines call **BCTpy** directly rather than re-implementing Brandes-type recursions in notebook code.

## What I would do next

1. **Align communities across tasks** with a partition-distance or optimal-transport match, then test whether philosophy systematically **relocates** the same physical layers into different modules (the raw $$c_i$$ vectors already hint at this, but a formal distance is cleaner for a paper).

2. **Swap the backbone rule** (fixed quantile vs. disparity filter vs. multiscale null) and verify that the qualitative ordering—architecture-dominated strength/eigenvector vs. task-sensitive betweenness—is robust.

3. **Token-level dynamics**: these matrices are *task-averaged* summaries. The April-28 post’s dream of a token-by-token evolving connectome is still open; CKA on sliding windows would make the graph a **time series of graphs**, which BCT can still summarise layer-wise if one commits to a pooling rule.

---

The practical punchline for the **RYS / skip-connection** storyline in [How skip connections define graphs in deep networks]({% link sections/science/_posts/2026-04-28-Skip-connections-and-graph-analysis.md %}) is conservative: **task changes the medium-strength wiring enough to move modular statistics and betweenness**, but **does not reshuffle the gross hub ordering** of layers when hubness is measured by strength or eigenvector centrality. That split—**stable integrators, movable bridges**—is testable in ablations: if you believe the table, interventions that target high-participation layers should transfer less cleanly across benchmarks than interventions that target high-strength cores.

## References

{% bibliography --cited %}
