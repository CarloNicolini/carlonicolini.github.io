---
layout: post
title: "MellowMax, Doob's h-transform, and the intensive geometry of tool-use agents"
description: "A theoretical framework for optimal tool selection in Large Reasoning Models using intensive soft values and dynamic programming."
date: 2026-04-03
published: true
categories:
  - science
  - language-physics
---

## Abstract

Standard agentic frameworks typically select tools using greedy decoding, which forces premature commitment and fails under ambiguity.
Recent work models Large Language Models (LLMs) as energy-based models where the local log-partition function acts as a future-looking soft value.
However, the standard log-sum-exp operator produces an extensive quantity that biases search algorithms against long sequences.
We replace this operator with MellowMax, yielding an intensive "energy density" that compares short answers and long tool trajectories fairly.
Furthermore, we show that optimal inference-time tool selection is equivalent to Doob's $h$-transform, where the base autoregressive policy is tilted by the exponentiated future soft value.
Because exact computation is intractable, inference-time scaling techniques (like Tree-of-Thoughts) act as dynamic programming approximations of this transform.
This framework provides a rigorous foundation for delayed commitment in Large Reasoning Models.

## Introduction

The transition from Large Language Models (LLMs) to Large Reasoning Models (LRMs) shifts the computational burden from pre-training to inference.
When an AI agent executes a complex task, it must sequentially choose between emitting a direct answer or invoking a tool (e.g., executing Python code, searching the web, or querying a database).
Most popular agentic frameworks, such as ReAct, treat this decision as a standard next-token prediction task.
They use greedy or low-temperature autoregressive decoding to select the next action.

This greedy approach fails when the optimal path is ambiguous.
If an agent cannot immediately determine whether a web search or a local database query will yield the necessary facts, greedy decoding forces it to commit blindly to one path.
If the chosen path fails, the agent must rely on unreliable self-correction prompts to backtrack.

We propose that optimal tool selection requires evaluating the downstream continuation value of the available actions *before* committing.
Building on the equivalence between autoregressive models and energy-based models {% cite blondel2025autoregressive %}, we can treat the future expected verifier score as a soft Bellman value function.
However, naive application of this theory introduces severe length bias.
We resolve this by introducing the intensive MellowMax operator {% cite asadi17a %} and framing the optimal agent policy as an inference-time approximation of Doob's $h$-transform.

## How Blondel's soft value is computed in practice

To understand the core issue, we must clarify what the soft value function $V_q(s)$ represents in {% cite blondel2025autoregressive %} and how it differs from standard metrics like *perplexity*.

In an Energy-Based Model (EBM), the probability of a sequence is defined by a global sequence-level reward function $R(x, y)$, normalized by an intractable partition function $Z(x)$.
Blondel et al. establish a bijection demonstrating that an autoregressive language model (ARM) optimizing for next-token prediction implicitly learns this EBM.

This bijection relies on a recursive transformation.
To convert the EBM reward into ARM logits $q(s_t, y_t)$, the model must learn to add the log-partition of the next state:

$$
q(s_t, y_t) = r(s_t, y_t) + V_q(s_t \oplus y_t)
$$

where $r$ is the immediate reward, and $V_q$ is the soft continuation value:

$$
V_q(s) = \log\!\left( \sum_{y \in \mathcal{A}} \exp(q(s, y)) \right)
$$

### Forward inference vs. backward training

The paper states that training (supervised learning via teacher forcing) is a **backward** process, while inference (autoregressive generation) is a **forward** process.

This is a statement about dynamic programming on the Directed Acyclic Graph (DAG) of all possible sequences.
To compute the exact future value $V_q(s)$, you would need to start at the end of all possible sequences (the EOS token) and work **backward**, computing the log-sum-exp at every node up to the root.
This is exactly what maximum-entropy reinforcement learning does: it propagates value backwards from the final rewards.

However, during inference, we only move **forward**.
How can a forward pass possibly know the future value without doing rollouts?
The profound insight is that **the pre-trained LLM weights have already done the backward pass for us**.
During pre-training on trillions of tokens, the teacher-forcing objective implicitly forces the model to solve the dynamic programming problem. The optimal logits $q(s, y)$ output by the final linear layer *already contain* the cached $V_q$ term.

Therefore, you do not need Monte Carlo rollouts to compute the 1-step soft value. By running a single forward pass and computing the log-sum-exp of the output logits for the next token, you are reading the model's internalized prediction of the future global energy. Generating just the first token $y$ after prompt $x$ inherently implies that the model has "imagined" the probability mass of all future continuations ending in EOS.

### Difference from perplexity

This soft value $V_q(s)$ is fundamentally different from perplexity.
Perplexity measures how surprised a model is by a *specific, fixed sequence of tokens* provided in the dataset. It is evaluated over a single path.
The soft value $V_q(s)$ measures the *total probability mass of all possible valid continuations* branching out from the current prefix. It evaluates the entire future tree.

## The extensive trap: Why log-sum-exp fails for agents

In our [previous note]({% link sections/science/_posts/2026-04-02-Soft-values-symmetry-breaking-and-random-rooted-trees.md %}), we defined the soft continuation value $V(s)$ using this exact formulation.

In statistical physics, the logarithm of a partition function defines the negative free energy.
Free energy is an **extensive** quantity: it scales with the volume of the system.
In language modeling, the "volume" is the sequence length.
If we sum raw logits over a trajectory to evaluate a tool call, the soft value accumulates over the horizon.

This extensivity creates a massive length bias during search.
If the average logit is negative, the soft value plummets as the sequence extends, causing the search algorithm to artificially prefer short, myopic answers over long, detailed tool trajectories.
Conversely, if the average logit is positive, the value explodes, encouraging the agent to generate infinite loops.

## MellowMax: Intensive soft values

To evaluate discrete actions fairly, the value function must be an **intensive** quantity—an average reward or energy density—so that a 5-step API call and a 500-step code execution remain comparable.

We replace the extensive log-sum-exp operator with the MellowMax operator introduced by Asadi and Littman {% cite asadi17a %}:

$$
\text{MellowMax}_{\omega}(q(s, \cdot)) = \frac{1}{\omega} \log\!\left( \frac{1}{|\mathcal{V}|} \sum_{y \in \mathcal{V}} \exp(\omega q(s, y)) \right),
$$

where $\omega > 0$ controls the greediness of the operator.
Because MellowMax averages the exponentiated logits over the vocabulary size $|\mathcal{V}|$ before taking the logarithm, it acts as an intensive operator.
As $\omega \to 0$, it converges to the mean logit; as $\omega \to \infty$, it converges to the hard maximum.

By redefining the soft value estimator $\widehat{V}(s)$ using MellowMax, we obtain a stable, length-invariant metric for scoring future trajectories.
This allows us to evaluate a state $s$ locally, without the metric breaking down when comparing subsequent branches of vastly different lengths.

## Integrating soft values into Monte Carlo Tree Search (MCTS)

Because $V_q(s)$ serves as a pre-computed heuristic of future sequence value, it is the perfect candidate for the value network in a Monte Carlo Tree Search (MCTS) algorithm (analogous to AlphaGo's value network).

Instead of relying purely on expensive end-of-sequence rollouts to evaluate a node in the search tree, an LRM can compute the MellowMax of the next-token logits at state $s$ to obtain an immediate, intensive estimate $\widehat{V}(s)$.

A hybrid MCTS approach would:
1. **Select:** Traverse the tree using PUCT, balancing the prior probability $\pi(y \mid s)$ against the cached values.
2. **Expand:** Generate a chunk of $k$ tokens (an action or partial response).
3. **Evaluate:** Compute the intensive MellowMax soft value at the new leaf node. Optionally, perform a small number of rollouts if uncertainty is high.
4. **Backup:** Propagate the intensive value back up the tree.

This drastically reduces the number of full-sequence rollouts required, relying instead on the model's internalized dynamic programming.

## Doob's h-transform and tool selection

If we have an accurate intensive value function $\widehat{V}(s)$, how should the agent use it to select tools?

Let $\pi(a \mid s)$ be the base proposal distribution of the pre-trained LLM for a given action $a$.
Let $\pi^*(a \mid s)$ be the optimal policy that maximizes the expected downstream verifier reward.
Mathematically, the optimal policy tilts the base distribution by the exponentiated future value of the resulting state:

$$
\pi^*(a \mid s) \propto \pi(a \mid s) \exp\!\left( \widehat{V}(s \oplus a) \right).
$$

In the theory of Markov processes, this exact operation is known as **Doob's $h$-transform**.
The $h$-transform conditions a stochastic process to reach a specific target (in our case, passing the final programmatic verifier) by reweighting the transition probabilities using a harmonic function $h(s) = \exp(\widehat{V}(s))$.

When we deploy algorithms like Language Agent Tree Search (LATS) or Tree-of-Thoughts, we are executing approximate Bellman backups at inference time to perform an empirical Doob's $h$-transform on the base LLM.

## The action space: Tools as discrete sequences

To operationalize this dynamic programming for agents, we must map abstract "actions" to the autoregressive reality of LLMs.

Unlike classical reinforcement learning where the action space is a fixed integer array, an LRM emits variable-length strings.
We define an action $a \in \mathcal{A}(s)$ as a sequence of tokens generated by the model that conforms to a specific schema.
In modern tool-use training, actions are bounded by special control tokens:

$$
a_{\text{search}} = \texttt{<tool\_call>} \oplus \text{"search('quantum gravity')"} \oplus \texttt{</tool\_call>}
$$

The scaffold evaluates the soft value of the state immediately *after* the environment returns the tool's execution result.
We associate a deterministic local tax $\Lambda(a)$ with each tool, representing the API financial cost, the latency, or the risk of environment failure.

The intensive soft Bellman equation for the agent becomes:

$$
\widehat{V}(s) \approx \text{MellowMax}_{a \in \mathcal{A}(s)} \!\left( \widehat{V}(s \oplus a \oplus \text{obs}_a) - \Lambda(a) \right),
$$

where $\text{obs}_a$ is the deterministic observation returned by the hosted environment after executing action $a$.

## 8. Delayed commitment in agents

This framework formally dictates when an agent should commit to an action and when it should explore.

Using the metrics defined in our previous work, we compute the net gain of tool usage $\Delta(s)$ and the effective number of viable paths $N_{\text{eff}}(s)$ under the MellowMax operator.
The optimal policy enforces the following regime:

1. **Answer:** If no tool yields a value exceeding its execution tax ($\Delta < 0$), the agent collapses the search tree and emits a direct answer.
2. **Commit:** If a specific tool dominates the value landscape ($\Delta > 0$ and $N_{\text{eff}} \approx 1$), the agent breaks symmetry. It commits to the tool, executes the irreversible API call, and moves the state forward.
3. **Delay Commitment:** If multiple tools appear equally promising ($\Delta > 0$ and $N_{\text{eff}} \gg 1$), the agent refuses to commit. It spawns parallel simulated rollouts to probe the environment, delaying the irreversible decision until the resulting observations break the symmetry.

Greedy decoding forces the "Commit" behavior unconditionally, explaining its brittleness.

## 9. Conclusions

We established that evaluating the future paths of an LLM using the standard log-sum-exp operator introduces an extensive length bias, severely compromising long-horizon tool use.
By adopting the intensive MellowMax operator, we ensure that short answers and long tool trajectories are compared strictly on their probability of success.

Under this intensive geometry, inference-time scaling ceases to be an ad-hoc heuristic.
The base LLM has already internalized the backward dynamic programming pass during pre-training, caching the sequence-level value in its local logits.
By reading these logits and executing multiple tool trajectories, the scaffold approximates Doob's $h$-transform.
This framework provides a rigorous mandate for building Large Reasoning Models: when the effective number of viable tools is large, the optimal policy must delay commitment, simulate the alternatives, and let the environment break the symmetry.

---

## References

{% bibliography --cited %}