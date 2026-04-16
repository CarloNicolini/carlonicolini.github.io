---
layout: post
title: Latent traces and Landau free energy
description: "Chain-of-thought as latent-variable inference, with a conjectural grand-canonical extension."
date: 2026-04-05
published: false
categories:
  - science
  - language-physics
---

## Latent traces, not narrated ODEs

Chain-of-thought is easier to understand once we stop treating it as a discretized ODE solver. The cleaner reading is probabilistic. A reasoning chain is an ordered latent trace that mediates between prompt and answer, and answer selection is then a marginalization problem over that trace.

That reading already has support in the literature. Blondel et al. show that an autoregressive model can be viewed as an energy-based model in function space, with next-token logits that already contain a soft Bellman look-ahead term {% cite blondel2025autoregressive %}. Phan et al. formalize chain-of-thought training as latent-variable inference over rationales, and Wang et al. interpret self-consistency as sampling multiple reasoning paths before aggregating at the answer level {% cite phan2023training wang2022self %}.

The question I want to push one step further is what happens when the number of reasoning tokens is itself variable. My conjecture is that this is the right place for a grand-canonical construction. A thermodynamic purist would reserve nearby names such as grand potential for related equilibrium settings. Here I want an effective coarse-grained landscape over families of traces, so I will call the resulting scalar a **Landau free energy** throughout this note.

## From Jaynes to Bellman

Fix a prompt sequence $\mathbf{x}$ and let $\mathbf{u}$ denote a complete continuation ending in `EOS`. Let $p_0(\mathbf{u}\mid \mathbf{x})$ be a reference autoregressive model and let $R(\mathbf{x},\mathbf{u})$ be a verifier reward or sequence score. The usual Jaynesian, KL-regularized target is

$$
p_{\alpha}(\mathbf{u}\mid \mathbf{x})
=
\frac{1}{Z_{\alpha}(\mathbf{x})}
p_0(\mathbf{u}\mid \mathbf{x})
\exp\!\left(\frac{R(\mathbf{x},\mathbf{u})}{\alpha}\right),
$$

with

$$
Z_{\alpha}(\mathbf{x})
=
\sum_{\mathbf{u}}
p_0(\mathbf{u}\mid \mathbf{x})
\exp\!\left(\frac{R(\mathbf{x},\mathbf{u})}{\alpha}\right).
$$

This is standard maximum-entropy control with a nonuniform reference measure {% cite levine2018reinforcement %}. If we absorb the reference model into the total sequence score

$$
S(\mathbf{x},\mathbf{u})
:=
R(\mathbf{x},\mathbf{u}) + \alpha \log p_0(\mathbf{u}\mid \mathbf{x}),
$$

then the same distribution becomes a Gibbs law over complete continuations,

$$
p_{\alpha}(\mathbf{u}\mid \mathbf{x})
=
\frac{\exp\!\left(S(\mathbf{x},\mathbf{u})/\alpha\right)}
{\sum_{\mathbf{u}'} \exp\!\left(S(\mathbf{x},\mathbf{u}')/\alpha\right)}.
$$

Blondel et al. show that when this score decomposes along the emitted sequence, the local autoregressive logits obey a soft Bellman recursion. If $s_t := \mathbf{x} \oplus \mathbf{u}_{<t}$ is the current prefix and

$$
S(\mathbf{x},\mathbf{u}) = \sum_{t=1}^{|\mathbf{u}|} r_{\mathrm{tot}}(s_t,u_t),
$$

then the optimal token score can be written as

$$
q^\star(s_t,u_t)
=
\frac{1}{\alpha} r_{\mathrm{tot}}(s_t,u_t) + V(s_t \oplus u_t),
$$

where

$$
V(s) = \log \sum_{v \in \mathcal{V}\cup\{\mathrm{EOS}\}} \exp\!\big(q^\star(s,v)\big).
$$

The important point is conceptual. The quantity $V(s)$ is the log-partition over all admissible suffixes reachable from the prefix $s$. In that sense, the model is not scoring the next token in isolation. It is scoring the next token together with the future mass that the token opens up.

If I translate that log-partition into my present language, the prefix-level Landau free energy is

$$
\mathcal{F}_{\mathrm{L}}(s) := -\alpha V(s).
$$

So the local autoregressive score already contains a contribution from the effective free-energy landscape of future continuations.

## Chain-of-thought as latent-variable marginalization

Now split a full continuation into an ordered reasoning trace and a final answer:

$$
\mathbf{u} = \mathbf{z} \oplus \mathbf{y},
\qquad
\mathbf{z}=(z_1,\dots,z_N),
\qquad
\mathbf{y}=(y_1,\dots,y_M).
$$

The key point is that $\mathbf{z}$ is ordered. Chain-of-thought is not an unordered hidden state. It is a sequential latent process.

Under this factorization, the relevant answer law is the marginal

$$
p_{\alpha}(\mathbf{y}\mid \mathbf{x})
=
\sum_{\mathbf{z}}
p_{\alpha}(\mathbf{z},\mathbf{y}\mid \mathbf{x}).
$$

This is why the clean comparison is not "short answer versus long answer," but "direct constrained inference versus marginalization over latent traces." In that language, zero-shot behaves like a restricted family in which the trace is collapsed, whereas chain-of-thought opens an explicit latent channel that a finite model can use to carry intermediate constraints, partial abstractions, or subgoals.

Self-consistency fits naturally into the same picture. It does not prove that any one verbalized rationale is the true internal computation. What it does is sample multiple traces and use those samples to approximate the answer marginal more faithfully {% cite wang2022self %}.

## Why faithfulness matters

At this point one caveat becomes essential. A textual chain-of-thought is not guaranteed to be a faithful transcript of the model's internal computation. Lanham et al. showed that the faithfulness of chain-of-thought varies substantially across tasks and models, and Arcuschin et al. showed that unfaithful chain-of-thought also appears in more realistic settings {% cite lanham2023faithfulness arcuschin2025wildfaithful %}.

This matters for the present note because it changes how $\mathbf{z}$ should be interpreted. The safest reading is not "the words the model prints are the real microscopic mechanism." The safer reading is "the model is using some latent reasoning state, and a printed chain is only one possible externalization of that state."

Quiet-STaR pushes in exactly that direction. It introduces hidden or partially hidden thought tokens that help prediction without requiring the entire reasoning process to be exposed as ordinary output text {% cite zelikman2024quietstar %}. For my purposes this is useful evidence. It suggests that variable reasoning length is more naturally understood as a latent-compute quantity than as a purely verbal one.

So from here on, $\mathbf{z}$ should be read as a latent reasoning trace first. In some settings it may be verbalized. In others it may remain partially or entirely hidden.

## Grand-canonical extension

Here the note leaves established literature and becomes conjectural.

If the reasoning trace has variable length $N$, then the natural extension is to assign a chemical potential $\mu$ to each latent reasoning token and define the fugacity

$$
\zeta := \exp(-\mu/\alpha).
$$

The corresponding grand-canonical partition over traces and answers is

$$
\Xi_{\alpha,\mu}(\mathbf{x})
=
\sum_{\mathbf{y}}
\sum_{N=0}^{\infty}
\sum_{\mathbf{z}\in\mathcal{V}^N}
p_0(\mathbf{z},\mathbf{y}\mid \mathbf{x})
\exp\!\left(\frac{R(\mathbf{x},\mathbf{z},\mathbf{y})-\mu N}{\alpha}\right).
$$

I then define the effective Landau free energy of the prompt as

$$
\mathcal{F}_{\mathrm{L}}(\mathbf{x})
:=
-\alpha \log \Xi_{\alpha,\mu}(\mathbf{x}).
$$

The same construction can be written answer by answer:

$$
\Xi_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x})
=
\sum_{N=0}^{\infty}
\sum_{\mathbf{z}\in\mathcal{V}^N}
p_0(\mathbf{z},\mathbf{y}\mid \mathbf{x})
\exp\!\left(\frac{R(\mathbf{x},\mathbf{z},\mathbf{y})-\mu N}{\alpha}\right),
$$

$$
\mathcal{F}_{\mathrm{L}}(\mathbf{y}\mid \mathbf{x})
:=
-\alpha \log \Xi_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x}).
$$

Within this conjectural ensemble, two consequences follow immediately.

First, the expected latent reasoning length is conjugate to fugacity:

$$
\mathbb{E}[N\mid \mathbf{x}]
=
\zeta \frac{\partial}{\partial \zeta} \log \Xi_{\alpha,\mu}(\mathbf{x}).
$$

In this sense, fugacity is not reasoning effort itself. It is the control parameter that governs expected reasoning effort.

Second, if I compare the variable-length family with the zero-shot slice $N=0$, then for any fixed answer $\mathbf{y}$,

$$
\Xi_{\alpha,\mu}^{(0)}(\mathbf{y}\mid \mathbf{x})
=
p_0(\emptyset,\mathbf{y}\mid \mathbf{x})
\exp\!\left(\frac{R(\mathbf{x},\emptyset,\mathbf{y})}{\alpha}\right),
$$

and therefore

$$
\mathcal{F}_{\mathrm{L}}(\mathbf{y}\mid \mathbf{x})
=
\mathcal{F}_{\mathrm{L}}^{(0)}(\mathbf{y}\mid \mathbf{x})
-
\alpha \log\!\left(
1+\frac{\Xi_{\alpha,\mu}^{(>0)}(\mathbf{y}\mid \mathbf{x})}
{\Xi_{\alpha,\mu}^{(0)}(\mathbf{y}\mid \mathbf{x})}
\right)
\le
\mathcal{F}_{\mathrm{L}}^{(0)}(\mathbf{y}\mid \mathbf{x}),
$$

provided the zero-shot term is positive and the grand sum is finite.

This is the precise part of the intuition that survives scrutiny. Allowing extra latent trace families lowers the effective Landau free energy of a fixed answer because it enlarges the phase space contributing to that answer. But that alone does **not** prove that accuracy must improve. Every answer can gain extra phase space. What matters is which answer gains more.

The corresponding answer law is

$$
p_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x})
=
\frac{\Xi_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x})}
{\sum_{\mathbf{y}'} \Xi_{\alpha,\mu}(\mathbf{y}'\mid \mathbf{x})}.
$$

That relative comparison then appears directly in the answer odds:

$$
\log \frac{p_{\alpha,\mu}(\mathbf{y}_1\mid \mathbf{x})}
{p_{\alpha,\mu}(\mathbf{y}_2\mid \mathbf{x})}
=
-\frac{1}{\alpha}
\left[
\mathcal{F}_{\mathrm{L}}(\mathbf{y}_1\mid \mathbf{x})
-
\mathcal{F}_{\mathrm{L}}(\mathbf{y}_2\mid \mathbf{x})
\right].
$$

So the conjectural story is not "more reasoning always helps." It is "variable latent reasoning helps when it lowers the effective Landau free energy of the correct answer more than it lowers the same quantity for its competitors."

## what prompts can and cannot do

Within this picture, a prompt such as "think step by step" should not be treated as a proved thermodynamic theorem. The prompt changes the conditional law of the model. In practice that means it may reshape the prior over latent traces, and it may also act like a phenomenological reduction in the **effective** chemical penalty for useful intermediate states.

But that last step is an interpretation, not an identification theorem. The prompt does not literally reveal a physical reservoir parameter. It changes the deployed conditional distribution, and the grand-canonical language is a way of describing the resulting shift in an effective landscape.

The same caution applies to convergence. The grand sum over $N$ is only meaningful if it is finite. In the present language, runaway looping corresponds to a regime in which longer and longer traces keep receiving enough net weight that the effective Landau free energy is no longer well defined. That is a useful implication of the model, but it also shows that the model needs an explicit stability assumption.

## what this conjecture buys us

Even with those caveats, the grand-canonical picture seems useful to me for three reasons.

First, it gives a sharper vocabulary for variable test-time compute. Instead of vaguely saying that a model "thinks harder," we can say that the model is exploring a larger latent ensemble, with a larger expected reasoning length and a different effective Landau landscape over answers.

Second, it fits naturally with the faithfulness evidence. If visible chains are not always faithful, then the real fluctuating object was probably latent all along. Quiet-STaR makes that possibility concrete by showing that hidden thought tokens can improve performance even when they are not simply exposed as ordinary text {% cite zelikman2024quietstar %}.

Third, it clarifies what an empirical test should look like. The key observable is not merely whether a prompt yields longer text. The key observable is whether the prompt shifts probability mass toward latent traces that reduce the effective Landau free energy gap of the correct answer relative to plausible competitors.

## conclusion

The established part of the story is already strong. Jaynes gives the reference-measure Gibbs law. Blondel explains why local autoregressive logits can carry future continuation mass through a soft Bellman term. Latent-variable interpretations of chain-of-thought and Monte Carlo interpretations of self-consistency are already in the literature {% cite blondel2025autoregressive levine2018reinforcement phan2023training wang2022self %}.

The new step in this post is a conjecture. Once variable reasoning length is taken seriously, I think it is natural to model latent traces with a grand-canonical ensemble and to describe the resulting effective landscape with a Landau free energy. That move is not yet backed by direct literature. It is a proposal for how to think about fluctuating latent compute, not a settled theorem about how language models must work.

What would make the conjecture worthwhile is not its elegance alone. It would be worthwhile if it helps us measure something real: how prompts, hidden thought tokens, and verifier-guided search change the effective trace ensemble, the expected reasoning length, and the relative Landau free-energy gaps between correct and incorrect answers. That, to me, is the right empirical frontier.

---

## References

{% bibliography --cited %}
