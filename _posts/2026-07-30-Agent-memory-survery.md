---
layout: post
title: "Memory in the age of AI agents: forms, functions, and dynamics"
description: "A readable tour of the Hu et al. survey on agent memory—formalization, the forms/functions/dynamics taxonomy, and the methods that matter most."
date: 2026-07-30

tags: agents, memory, LLM, survey
published: true
permalink: "/sections/tech/2026/07/30/Agent-memory-survery.html"
categories:
  - science
  - ai
---
Agent systems keep promising long-horizon competence—personal assistants that remember you, researchers that keep notes across sessions, coding agents that learn from yesterday's failures. The missing piece is almost always the same: *memory*. Not a bigger context window, and not a static document store, but a state that forms, evolves, and gets retrieved while the agent acts.

Hu and colleagues recently published a large survey that tries to put this sprawling literature back on a map {% cite hu2026memory %}. The paper is nearly a hundred pages long. What follows is the gist: how they formalize the problem, how they cut the design space into forms / functions / dynamics, and which technical ideas actually move the needle.

## Why a new taxonomy

Older surveys often leaned on the familiar short-term versus long-term split. That distinction is still useful as a *usage pattern*, but it is a poor taxonomy for today's systems. Two papers can both claim "long-term memory" while one is dumping dialogue into a vector database, another is editing LoRA adapters, and a third is compressing KV caches. The survey's main contribution is to separate three orthogonal questions:

1. **Form** — what carries the memory?
2. **Function** — what job does it do for the agent?
3. **Dynamics** — how is it written, revised, and read over time?

Before those axes, they also clean up a conceptual mess: agent memory is related to, but not identical with, LLM memory, RAG, and context engineering.

## A compact formalization

Start from an agent–environment loop. At time $$t$$ the environment is in state $$s_t$$, the agent receives an observation $$o_t$$ (possibly history-conditioned), and produces an action $$a_t$$ from a heterogeneous space: text, tool calls, plans, environment edits, messages to other agents. The environment then transitions

$$
s_{t+1} \sim \Psi(s_{t+1} \mid s_t, a_t).
$$

Memory enters as an evolving state $$M_t \in \mathcal{M}$$. The survey deliberately leaves $$\mathcal{M}$$ open: a text buffer, key–value store, vector index, graph, parameter set, or hybrid are all allowed. What matters is the *lifecycle*, expressed with three operators:

$$
M^{\mathrm{form}}_{t+1} = F(M_t, \phi_t),
\qquad
M_{t+1} = E(M^{\mathrm{form}}_{t+1}),
\qquad
m_t = R(M_t, o_t, Q).
$$

Here $$\phi_t$$ are informational artifacts produced at step $$t$$ (tool outputs, traces, feedback), $$F$$ is *formation* (what becomes a memory candidate), $$E$$ is *evolution* (merge, conflict resolution, forgetting, restructuring), and $$R$$ is *retrieval* (build a query and return a memory signal $$m_t$$). The policy is then

$$
a_t = \pi(o_t, m_t, Q),
$$

with $$Q$$ the task specification. Short-term versus long-term effects are not separate modules in this picture. They emerge from *when* you call $$F$$, $$E$$, and $$R$$: once at the start of a task, continuously inside a trial, or at task boundaries across trials {% cite hu2026memory %}.

That single loop is enough to locate most systems. Reflexion-style verbal feedback is formation plus retrieval inside a trial {% cite shinn2023reflexion %}. MemGPT-style paging is aggressive evolution and retrieval under a context budget {% cite packer2024memgpt %}. Experience banks that survive across tasks are just $$M_t$$ with a slower write schedule {% cite zhao2024expel %}.

## Not RAG, not KV tricks, not context packing

Three neighboring fields keep getting confused with agent memory.

**LLM memory** in the narrow sense is about the model's *internal* capacity: KV-cache management, long-context architectures, recurrent state. When those tricks only expand the transformer's representational horizon, they are LLM memory. When the same tricks are used to keep a task-local scratchpad coherent, they start behaving like agent working memory. The survey's rule of thumb is useful: if the goal is persistent, environment-driven, cross-task cognitive state—not just a longer attention span—call it agent memory {% cite hu2026memory %}.

**RAG** shares engineering ingredients (indexes, embeddings, graphs), but classical RAG retrieves from a mostly *external, static* corpus for a single query {% cite lewis2021rag %}. Agent memory accumulates traces of the agent's *own* interaction and is expected to change as the agent acts. Agentic RAG sits in the middle: an agent controls retrieval, but the store is still often an outside knowledge base rather than a self-evolving experience substrate.

**Context engineering** treats the context window as a scarce resource to be packed optimally. Agent memory uses that packing as an implementation layer, but its ambition is larger: what the agent knows, what it has learned to do, and how that identity persists beyond any single window.

## Forms: what carries memory?

### Token-level memory

This is still the dominant practical form: discrete, inspectable units outside the weights—snippets, summaries, profiles, trajectories, tool docs, graph nodes. The survey organizes it by topology.

- **Flat (1D).** Bags or streams of units with little structure. MemoryBank and Mem0 summarize and index user/dialogue facts {% cite zhong2023memorybank chhikara2025mem0 %}. Experiential pools store trajectories or distilled insights, as in ExpeL {% cite zhao2024expel %} and Reflexion {% cite shinn2023reflexion %}. Voyager stores executable skills as a growing code library {% cite wang2023voyager %}. Flat stores are easy to ship and easy to audit; they struggle when relations among memories matter.
- **Planar (2D).** One explicit relational layer: trees or graphs. A-MEM links memory notes into an evolving graph {% cite xu2025amem %}; HippoRAG-style systems use knowledge-graph structure for multi-hop recall {% cite gutierrez2025hipporag %}; Mem0's graph variant extracts entity–relation triples from conversation. Structure buys better multi-hop retrieval and conflict handling at the cost of construction noise.
- **Hierarchical (3D).** Multiple layers with cross-layer links—raw traces below, abstractions above. Hierarchies help when agents must zoom from episode details to reusable schemas without stuffing everything into the prompt.

Token memory wins on editability and transparency. That is exactly why it shows up in high-stakes or personalized settings: you can delete a wrong fact.

### Parametric memory

Here memory lives in weights. The survey splits it into *internal* edits of the base model and *external* attachments (adapters, LoRAs, side networks). Timing matters: pretrain, mid-train on early experience, or post-train personalization and model editing. Parametric memory can give stronger assimilation and cheaper inference—no retrieval round-trip—but updates are slower, harder to reverse, and prone to catastrophic interference. External modules soften that trade-off by keeping the backbone frozen while routing among memory adapters.

### Latent memory

Latent memory sits between tokens and parameters: continuous states that the model can carry without turning them into prose.

- **Generate.** Learn to produce compact latent tokens or vectors that summarize long inputs (gist tokens are the canonical example) {% cite mu2024gist %}.
- **Reuse.** Keep raw internal activations—especially KV pairs—and retrieve them later with nearest-neighbor style mechanisms.
- **Transform.** Compress or restructure those activations: heavy-hitter retention {% cite zhang2023h2o %}, importance-based KV selection {% cite li2024snapkv %}, merging and projection schemes.

Latent memory is attractive for long context, multimodality, and edge latency. It is harder to inspect and harder to manually correct. Figure 5 in the survey is worth internalizing: token memory for transparency, parametric memory for deep capability shifts, latent memory for machine-native compression {% cite hu2026memory %}.

## Functions: why the agent needs memory

Forms answer *where*; functions answer *why*. The survey replaces the coarse temporal dichotomy with three jobs.

### Factual memory — what does the agent know?

Declarative facts about the user and the environment: preferences, commitments, entity states, world knowledge gathered along the way. Cognitively, this sits on the episodic–semantic continuum: raw event logs get summarized, reflected, and induced into reusable facts. Good factual memory buys consistency (no contradictory persona), coherence (topical continuity), and adaptability (personalization). Systems such as MemoryBank, Mem0, and graph memories are mostly solving this problem {% cite zhong2023memorybank chhikara2025mem0 xu2025amem %}.

### Experiential memory — how does the agent improve?

This is the part that turns interaction into competence. The survey splits it cleanly:

- **Case-based.** Keep high-fidelity episodes or solutions for replay and few-shot reuse {% cite zhao2024expel shinn2023reflexion %}.
- **Strategy-based.** Abstract patterns, workflows, and insights that transfer across tasks.
- **Skill-based.** Callable procedures: code snippets, scripts, APIs, tool wrappers. Voyager's skill library is the clearest popular example {% cite wang2023voyager %}.

If factual memory is a notebook, experiential memory is a playbook that gets better with practice.

### Working memory — what is the agent thinking about now?

Working memory is the capacity-limited scratchpad for the current task. Single-turn variants mostly compress or abstract the input. Multi-turn variants consolidate state across steps: rolling summaries, hierarchical folding, intermittent retrieval, cognitive planning buffers. This is where agent memory and context engineering nearly coincide. ReAct-style traces are already a primitive working memory {% cite yao2023react %}; modern systems add compression and selective recall so the scratchpad does not drown the policy.

The important architectural point is the loop among the three functions: interaction outcomes are encoded into factual/experiential stores; working memory retrieves from those stores to reason; new outcomes write back again {% cite hu2026memory %}.

## Dynamics: how memory moves

Even with the right form and function, systems live or die on the write/read schedule.

**Formation.** Raw $$\phi_t$$ rarely should be stored verbatim. The main recipes are semantic summarization (MemGPT, Mem0, RL-optimized summarizers), knowledge distillation into facts or strategies, structured construction into graphs or hierarchies, latent encoding, and parametric internalization {% cite packer2024memgpt chhikara2025mem0 %}.

**Evolution.** Once candidates exist, the store must stay useful: consolidate near-duplicates, update stale facts, forget low-value entries. Forgetting policies are more interesting than they sound—time decay, access frequency (LRU/LFU), and importance scoring are all in active use, sometimes combined.

**Retrieval.** Retrieval is no longer "embed and top-$$k$$." The survey walks through lexical matching, dense semantic search, graph traversal, generative retrieve-then-rewrite, and hybrids. Timing also matters: retrieve once at task start, on demand when uncertainty rises, or continuously. Query construction—rewriting the observation into a memory-seeking query—is often half the battle.

A frontier theme appears again and again: memory is shifting from *lookup* toward *generation*. Instead of pasting retrieved fragments, the agent synthesizes a context-specific memory representation from what it retrieves—or even from latent state alone {% cite hu2026memory %}.

## What to take away

If you only remember a few lines from a hundred-page survey, remember these.

Agent memory is a persistent state $$M_t$$ coupled to the decision loop through formation, evolution, and retrieval—not a synonym for RAG or a longer context window. Design choices factor cleanly into form (token / parametric / latent), function (factual / experiential / working), and dynamics (write, revise, read). Most production systems today are still token-level factual stores plus some working-memory compression; the research frontier is experiential memory that actually improves policies, latent/generative memory that stays cheap, and memory managers that learn their own write/read policy instead of following hand-written rules.

Memory, in this framing, is not an accessory. It is the substrate that lets a static generator become an agent that persists, adapts, and compounds experience over time.

---

## References

{% bibliography --cited %}
