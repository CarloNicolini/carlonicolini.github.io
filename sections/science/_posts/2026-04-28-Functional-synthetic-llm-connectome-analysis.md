---
layout: post
date: 2026-04-28
title: Functional synthetic LLM connectome analysis
description: "How we can link transformers way of processing information to biological brains"
categories:
  - science
  - deep-learning
published: false
---

## Connections to network neuroscience

This post is the empirical companion to [How skip connections define graphs in deep networks]({% link sections/science/_posts/2026-04-28-Skip-connections-and-graph-analysis.md %}).
There, the graph comes from the residual recursion and the hypothesis that useful RYS blocks behave like stable residual flows.
Here, the graph comes from the actual RYS performance matrices: every edge or region is grounded in a benchmark-changing intervention, not only in representational correlation.

We get a fascinating comparative dictionary between two apparently disparate worlds.

| Concept | Network Neuroscience (fMRI) | Transformer Network Topology |
| :--- | :--- | :--- |
| **Nodes** | Brain Regions (e.g., Amygdala, Prefrontal Cortex) | Layers, Sub-layers, or specific Attention Heads |
| **Edges** | BOLD signal temporal correlation | Representation similarity (Cosine / CKA) of activations |
| **Dynamics** | Hemodynamic response to stimuli | Activation propagation of token embeddings |
| **Graph Type** | Undirected, weighted functional connectome | Directed (or undirected via similarity), weighted DAG |

We can apply the methods of network neuroscience, including all the classical preprocessing steps to transformers networks topologies.
Specifically we are interested in:

- **Community detection (Newmans' modularity):** In standard ResNets and Transformers, similarity matrices consistently reveal distinct block-diagonal structures. Algorithms like Louvain community detection would identify clear modules. For instance, the first 20% of layers often form a "syntax and local context" community, while the middle layers form a highly synchronized "world knowledge and factual recall" community.
- **Betweenness centrality:** In a graph of layer activations, betweenness centrality would highlight the "hub" layers. In LLMs, there are often specific bottleneck layers where the representational flow sharply pivots from gathering context to generating the next-token prediction. An attention head with high betweenness centrality acts as a critical router of information, much like the thalamus in the human brain.
- **Semantic synchronization:** Because of skip connections, researchers have observed that representations can become highly correlated across vast depths of the network (e.g., layers 15 through 30 might all share a cosine similarity of $$0.95$$) {% cite ng2026rsys %}. In graph terms, this is a tightly knit clique. The network has reached a "representational plateau" where it has decided on the semantic meaning of a token and is simply passing that synchronized state forward without mutating it.

<figure>
<img src="/static/postfigures/network-neuroscience.webp" alt="network_neuroscience">
<figcaption>
<strong>Figure 2: The representations of large-scale network features</strong> Brain networks can be labelled and analyzed as graphs encompassing a group of nodes (neurons, brain regions) and a collection of edges (structural connections or functional relationships). The organization of nodes and edges defines the topological properties of the brain network. A node relatively high number of edges called high-degree often referred as hubs. Functional segregation (i.e., clustering coefficient) designated by strong functional coupling within modules/clusters (red) with little or no functional coupling across communities.
</figcaption>
</figure>

To push this framework even further we could even consider how standard fMRI constructs a single connectivity graph for a given task.
In their classical usage Transformers process thousands of tokens simultaneously.
Specific adjacency matrices could be constructed by averaging the cosine similarities over an entire corpus of text, and one could study how dynamic, token-specific graphs evolve to see how the network's "brain state" changing token-by-token?

## Research questions

Here are some of the most interesting questions that I would like to analyze with the newly developed framework

### Does community detection analyses correlate with domain-specific reasoning?

In fMRI, distinct cognitive tasks recruit specific modular brain networks (e.g., the Default Mode Network for social cognition, the Frontoparietal Network for math/logic etc...).
Since David Ng found that the functional block for Math in Qwen3.5-27B is wider (layers 24–35) than the block for EQ (layers 29–34, we could pass datasets from the `MATH` and `EQ` benchmarks through the model, thus generating long streams of layers activations. After having computed the layer-to-layer cosine similarity adjacency matrix for *each* task separately, we could run the Louvain community detection algorithm on these two task-evoked connectomes to understand how topology of cosine similarity induced networks affects the downstream task performance.

**Hypothesis:** The `MATH` connectome should show a distinct, highly weighted community spanning nodes 24–35, while the `EQ` connectome will show a tighter, distinct sub-clique in 29–34. I expect to associate the Newmans' modularity score $$Q$$ of the middle layers during different benchmarks. A higher modular segregation of the math module should directly correlate with a higher score on the `MATH` leaderboard.

### Betweenness centrality and the "Sapir-Whorf" translation bottleneck

[Betweenness centrality](https://en.wikipedia.org/wiki/Betweenness_centrality) identifies "hubs" that act as bridges between different communities.
In this comparative LLM neuroanatomy framework, Ng’s *Sapir-Whorf* experiment shows that early layers (0–5) are highly language-dependent (English vs. Chinese vs. Python), while middle layers (10–50) are entirely format-agnostic, representing pure semantic thought.
As an experiment I propose to compute the functional connectivity matrix across a highly multilingual dataset and calculate the betweenness centrality for all nodes (layers).

- **Hypothesis:** The boundary layers (e.g., layers 5–10 and layers 50–55) should exhibit massive betweenness centrality.
If they act as the "thalamus" of the LLM, their role is to funnel surface-level syntax into the universal reasoning space, and vice versa.
Experimentally I would like to correlate the centrality of these specific boundary nodes with the model’s performance on multilingual translation benchmarks (like **FLORES-200**) or cross-lingual reasoning (like **XNLI**).
If these high-centrality boundary nodes are perturbed (or skipped), cross-lingual reasoning should collapse while monolingual reasoning might remain intact.

### Network diameter and efficiency and chain-of-thought

In graph theory, the diameter or average path length of a community dictates how many "hops" information takes to traverse it. Eff
**The LLM Translation:** The success of the *RYS* technique (duplicating middle layers) is mathematically equivalent to artificially increasing the path length and density of the "Universal Reasoning" module.
**The Experiment:**

- **Method:** Compare base models with their RYS-expanded counterparts (e.g., Qwen3.5-27B vs. RYS-Qwen3.5-27B). Generate their functional connectomes.
- **Hypothesis:** The RYS models will display a larger network diameter specifically within the reasoning community (since those nodes are duplicated and sequentially connected).
- **Measurable Correlation:** Map the *intra-module path length* of the reasoning block to benchmarks requiring deep logical iteration, such as **BBH (BIG-Bench Hard)** or **MuSR (Multi-Step Reasoning)**. You can prove mathematically that hard arithmetic requires a minimum graph diameter within the semantic space to resolve correctly.

### Edge weight variance and model confidence

In LLMs, functional connectivity graphs frequently show that edge weights (cosine similarities) between adjacent middle layers are extremely high (often $$\sim0.95+$$), indicating that activations change minimally across these layers. This phenomenon forms a "representational plateau"—a kind of semantic stasis where the model’s internal state is stable.

**Functional Interpretation:** When this plateau emerges early during token processing, it suggests the model has resolved the semantics and is confident in its prediction (i.e., it has "made up its mind").
Conversely, high variation in these edge weights signals instability, corresponding to uncertainty or potential hallucination.
Experimentally, for various prompts, we could calculate the variance of cosine similarities between the middle layers (the reasoning clique) across the input sequence.

- **Hypothesis:** When the LLM handles well-known factual information, the middle-layer edges will be uniformly strong (low variance; a rigid plateau). When dealing with unfamiliar input or potentially hallucinating, these edge weights will fluctuate significantly (high variance; representational instability).

We then measure the average edge weight variance (or density) in the reasoning block to performance on truthfulness benchmarks such as **TruthfulQA** or **GPQA**.
Stable plateaus (high density, low variance) should correlate with accurate, confident responses while greater variance within the plateau predicts a higher risk of hallucination or factual error.
