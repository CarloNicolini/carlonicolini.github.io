---
layout: post
title: Chain-of-thought as grand-canonical inference in energy-based language models
description: "Jaynes, Blondel's soft Bellman recursion, and a grand-canonical view of latent reasoning traces."
date: 2026-04-05
published: false
categories:
  - science
  - language-physics
---

## From zero-shot decoding to grand-canonical reasoning

This note makes one claim precise. The right mathematical picture is not that chain-of-thought is a discretized ODE solver. The cleaner statement is that chain-of-thought introduces an ordered latent reasoning trace, and that answer selection should then be viewed as marginalization over that latent trace. Because the number of reasoning tokens is itself variable, the natural statistical-mechanics object is the grand canonical ensemble rather than the canonical one. I will denote its grand partition by $\Xi$ and its grand potential by $\Omega := -\alpha \log \Xi$, using the standard statistical-mechanics terminology rather than the less standard phrase "grand log-potential."

Blondel et al. recently showed that autoregressive models and energy-based models are equivalent in function space, and that the local next-token logits of an autoregressive model contain a soft Bellman look-ahead term {% cite blondel2025autoregressive %}. I will use that result as the token-level backbone of the argument. The global conclusion is simple: zero-shot decoding asks the model to compress the whole future partition function into one internal look-ahead computation, whereas explicit reasoning externalizes part of that computation into a sequence of latent tokens. In that sense, chain-of-thought is better understood as grand-canonical marginal inference over ordered latent states.

Two statements in this picture are rigorous. First, enlarging the latent family from zero-shot traces to variable-length reasoning traces can only decrease the optimal grand free energy. Second, self-consistency is a Monte Carlo approximation to the marginal answer law over latent traces {% cite phan2023training wang2022self %}. What is not automatic is that a prompt such as "think step by step" must improve accuracy. That depends on how the prompt reshapes the pretrained prior over traces and on whether the resulting grand partition remains finite.

## Jaynes, Reference Measures, and Blondel's Soft Value

Fix a prompt sequence $\mathbf{x}$. Let $\mathbf{u} = (u_1,\dots,u_T)$ denote a complete continuation ending in $\mathrm{EOS}$, and let the token-level state be the prefix
$$
s_t := \mathbf{x} \oplus \mathbf{u}_{<t}.
$$
All sums below are over admissible finite continuations ending in $\mathrm{EOS}$.

Let $p_0(\mathbf{u}\mid \mathbf{x})$ be a reference autoregressive model. If $R(\mathbf{x},\mathbf{u})$ is a verifier reward or sequence score, then the KL-regularized maximum-entropy solution is the reference-measure Gibbs law
$$
p_{\alpha}(\mathbf{u}\mid \mathbf{x})
=
\frac{1}{Z_{\alpha}(\mathbf{x})}
p_0(\mathbf{u}\mid \mathbf{x})
\exp\!\left(\frac{1}{\alpha}R(\mathbf{x},\mathbf{u})\right),
$$
with partition function
$$
Z_{\alpha}(\mathbf{x})
=
\sum_{\mathbf{u}}
p_0(\mathbf{u}\mid \mathbf{x})
\exp\!\left(\frac{1}{\alpha}R(\mathbf{x},\mathbf{u})\right).
$$

This is Jaynes' maximum-entropy construction with a nonuniform reference measure {% cite levine2018reinforcement %}. It is often convenient to absorb the reference model into a total sequence score
$$
S(\mathbf{x},\mathbf{u})
:=
R(\mathbf{x},\mathbf{u}) + \alpha \log p_0(\mathbf{u}\mid \mathbf{x}),
$$
so that
$$
p_{\alpha}(\mathbf{u}\mid \mathbf{x})
=
\frac{\exp\!\left(S(\mathbf{x},\mathbf{u})/\alpha\right)}
{\sum_{\mathbf{u}'}\exp\!\left(S(\mathbf{x},\mathbf{u}')/\alpha\right)}.
$$

When $S$ decomposes additively along the emitted sequence,
$$
S(\mathbf{x},\mathbf{u})
=
\sum_{t=1}^{T} r_{\mathrm{tot}}(s_t,u_t),
$$
Blondel et al. show that the corresponding autoregressive logits satisfy an exact soft Bellman recursion {% cite blondel2025autoregressive %}:
$$
q^\star(s_t,u_t)
=
\frac{1}{\alpha}r_{\mathrm{tot}}(s_t,u_t) + V_q(s_t \oplus u_t),
$$
where
$$
V_q(s)
=
\log \sum_{v \in \mathcal{V}\cup\{\mathrm{EOS}\}} \exp\!\big(q^\star(s,v)\big).
$$

The important point is not the notation but the meaning. The quantity $V_q(s)$ is the log-partition of all suffixes reachable from the prefix $s$, hence $-\alpha V_q(s)$ is a continuation free energy. The next-token logit is therefore not a purely local score. It is an immediate score corrected by the free energy of all futures that become available after appending that token. This is the precise sense in which next-token prediction already looks ahead.

## Reasoning Traces as Ordered Latent Variables

To talk about chain-of-thought, split the continuation $\mathbf{u}$ into an ordered reasoning trace $\mathbf{z}$ and a final answer $\mathbf{y}$:
$$
\mathbf{u} = \mathbf{z} \oplus \mathbf{y},
\qquad
\mathbf{z}=(z_1,\dots,z_N),
\qquad
\mathbf{y}=(y_1,\dots,y_M).
$$
Here $N=|\mathbf{z}|$ is the number of reasoning tokens, while $\mathbf{y}$ contains the final answer and its terminal $\mathrm{EOS}$ token. The order of the reasoning tokens matters. In particular, the reference model factorizes autoregressively as
$$
p_0(\mathbf{z},\mathbf{y}\mid \mathbf{x})
=
\left(\prod_{i=1}^{N} p_0(z_i \mid \mathbf{x},\mathbf{z}_{<i})\right)
\left(\prod_{j=1}^{M} p_0(y_j \mid \mathbf{x},\mathbf{z},\mathbf{y}_{<j})\right).
$$

This is why chain-of-thought should not be described as an unordered latent state. It is an ordered latent process.

The grand-canonical extension appears because $N$ is not fixed. A model may emit zero reasoning tokens, a short trace, or a long trace before answering. Introduce a chemical potential $\mu$ penalizing each reasoning token, and the associated fugacity
$$
\zeta := \exp(-\mu/\alpha).
$$
Then the grand partition over all traces and answers is
$$
\Xi_{\alpha,\mu}(\mathbf{x})
=
\sum_{\mathbf{y}}
\sum_{N=0}^{\infty}
\sum_{\mathbf{z}\in \mathcal{V}^{N}}
p_0(\mathbf{z},\mathbf{y}\mid \mathbf{x})
\exp\!\left(\frac{R(\mathbf{x},\mathbf{z},\mathbf{y})-\mu N}{\alpha}\right).
$$

Equivalently,
$$
\Xi_{\alpha,\mu}(\mathbf{x})
=
\sum_{N=0}^{\infty} \zeta^N Z_N(\mathbf{x}),
$$
with
$$
Z_N(\mathbf{x})
:=
\sum_{\mathbf{y}}
\sum_{\mathbf{z}\in \mathcal{V}^{N}}
p_0(\mathbf{z},\mathbf{y}\mid \mathbf{x})
\exp\!\left(\frac{R(\mathbf{x},\mathbf{z},\mathbf{y})}{\alpha}\right).
$$

The induced grand-canonical law is
$$
p_{\alpha,\mu}(\mathbf{z},\mathbf{y}\mid \mathbf{x})
=
\frac{1}{\Xi_{\alpha,\mu}(\mathbf{x})}
p_0(\mathbf{z},\mathbf{y}\mid \mathbf{x})
\exp\!\left(\frac{R(\mathbf{x},\mathbf{z},\mathbf{y})-\mu N}{\alpha}\right).
$$

The conjugate observable to fugacity is the reasoning length. In particular,
$$
\mathbb{E}[N \mid \mathbf{x}]
=
\zeta \frac{\partial}{\partial \zeta} \log \Xi_{\alpha,\mu}(\mathbf{x}).
$$
So fugacity is not itself "reasoning effort." Rather, it is the control parameter that governs the expected reasoning effort.

For this grand-canonical picture to be well defined, the partition function must be finite. A sufficient condition is that for each fixed $\mathbf{x}$ there exist constants $C_{\mathbf{x}}>0$ and $\rho_{\mathbf{x}}>0$ such that $Z_N(\mathbf{x}) \le C_{\mathbf{x}}\rho_{\mathbf{x}}^N$ for all $N$, with $\zeta \rho_{\mathbf{x}} < 1$. If that fails, the formalism predicts a runaway long-trace phase rather than a proper normalized law. In language-model terms, that is the regime of uncontrolled looping.

## The Variational Statement That Is Actually True

The global grand partition admits the standard Gibbs variational form
$$
-\alpha \log \Xi_{\alpha,\mu}(\mathbf{x})
=
\min_{q}
\left\{
\mathbb{E}_{q}\!\left[-R(\mathbf{x},\mathbf{z},\mathbf{y})+\mu N\right]
+
\alpha\,\mathrm{KL}\!\left(q(\mathbf{z},\mathbf{y}) \| p_0(\mathbf{z},\mathbf{y}\mid \mathbf{x})\right)
\right\},
$$
where the minimum is over all distributions $q(\mathbf{z},\mathbf{y})$ whose support is contained in that of $p_0$.

This identity immediately gives the rigorous version of the claim that more latent states can reach lower free-energy minima.

**Proposition 1.** Let $\mathcal{Q}_{0}$ be the family of distributions supported on $N=0$ almost surely, and let $\mathcal{Q}_{\mathrm{gc}}$ be the family of all variable-length distributions over $(\mathbf{z},\mathbf{y})$. Then
$$
\min_{q \in \mathcal{Q}_{\mathrm{gc}}} \mathcal{F}_{\alpha,\mu}(q)
\le
\min_{q \in \mathcal{Q}_{0}} \mathcal{F}_{\alpha,\mu}(q),
$$
where
$$
\mathcal{F}_{\alpha,\mu}(q)
:=
\mathbb{E}_{q}\!\left[-R(\mathbf{x},\mathbf{z},\mathbf{y})+\mu N\right]
+
\alpha\,\mathrm{KL}\!\left(q(\mathbf{z},\mathbf{y}) \| p_0(\mathbf{z},\mathbf{y}\mid \mathbf{x})\right).
$$

**Proof.** The family $\mathcal{Q}_{0}$ is a subset of $\mathcal{Q}_{\mathrm{gc}}$. Therefore the infimum of the same functional over the larger family cannot exceed the infimum over the smaller family. By the Gibbs variational identity, these two infima are precisely the zero-shot and grand-canonical free energies. This proves the claim.

This is the clean mathematical core. Enlarging the latent family can only improve the best achievable free energy. What it does *not* say is that every finite decoding heuristic will find that better minimum, or that every extra reasoning token is beneficial. Those are separate algorithmic and modeling questions.

## Answer-Specific Grand Potentials and Marginal MAP

For answer selection we need a slightly finer object. Define the answer-specific grand partition
$$
\Xi_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x})
=
\sum_{N=0}^{\infty}
\sum_{\mathbf{z}\in \mathcal{V}^{N}}
p_0(\mathbf{z},\mathbf{y}\mid \mathbf{x})
\exp\!\left(\frac{R(\mathbf{x},\mathbf{z},\mathbf{y})-\mu N}{\alpha}\right),
$$
and the corresponding answer-specific grand potential
$$
\Omega_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x})
:=
-\alpha \log \Xi_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x}).
$$

The answer marginal is then
$$
p_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x})
=
\frac{\Xi_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x})}
{\sum_{\mathbf{y}'} \Xi_{\alpha,\mu}(\mathbf{y}'\mid \mathbf{x})}
=
\frac{\exp\!\left(-\Omega_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x})/\alpha\right)}
{\sum_{\mathbf{y}'} \exp\!\left(-\Omega_{\alpha,\mu}(\mathbf{y}'\mid \mathbf{x})/\alpha\right)}.
$$

The zero-shot model is the constrained slice $N=0$, namely
$$
\Xi_{\alpha,\mu}^{(0)}(\mathbf{y}\mid \mathbf{x})
=
p_0(\emptyset,\mathbf{y}\mid \mathbf{x})
\exp\!\left(\frac{R(\mathbf{x},\emptyset,\mathbf{y})}{\alpha}\right),
\qquad
\Omega_{\alpha,\mu}^{(0)}(\mathbf{y}\mid \mathbf{x})
=
-\alpha \log \Xi_{\alpha,\mu}^{(0)}(\mathbf{y}\mid \mathbf{x}).
$$

Within this abstraction, zero-shot decoding targets the constrained MAP answer
$$
\mathbf{y}^{\star}_{\mathrm{zs}}
\in
\arg\max_{\mathbf{y}} \Xi_{\alpha,\mu}^{(0)}(\mathbf{y}\mid \mathbf{x}),
$$
whereas chain-of-thought targets the marginal MAP answer
$$
\mathbf{y}^{\star}_{\mathrm{cot}}
\in
\arg\max_{\mathbf{y}} \Xi_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x}).
$$
The distinction is important. Zero-shot compares answers directly. Chain-of-thought first sums over all ordered latent traces leading to an answer and only then compares answers. A single decoded rationale is one sample, or one dominant path, inside that latent model. The mathematically clean target is the marginal over traces.

Now the answer-specific free-energy comparison can be written exactly.

**Proposition 2.** Assume $\Xi_{\alpha,\mu}^{(0)}(\mathbf{y}\mid \mathbf{x})>0$. Then
$$
\Omega_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x})
\le
\Omega_{\alpha,\mu}^{(0)}(\mathbf{y}\mid \mathbf{x}),
$$
with strict inequality if and only if there exists at least one reasoning trace of length $N\ge 1$ with positive base weight and finite Boltzmann weight.

**Proof.** Split the answer-specific grand partition into the zero-shot term and the positive-length terms:
$$
\Xi_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x})
=
\Xi_{\alpha,\mu}^{(0)}(\mathbf{y}\mid \mathbf{x})
+
\Xi_{\alpha,\mu}^{(>0)}(\mathbf{y}\mid \mathbf{x}),
$$
where $\Xi_{\alpha,\mu}^{(>0)}(\mathbf{y}\mid \mathbf{x}) \ge 0$. Therefore
$$
\Omega_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x})
=
-\alpha \log \Xi_{\alpha,\mu}^{(0)}(\mathbf{y}\mid \mathbf{x})
-
\alpha \log\!\left(
1 + \frac{\Xi_{\alpha,\mu}^{(>0)}(\mathbf{y}\mid \mathbf{x})}
{\Xi_{\alpha,\mu}^{(0)}(\mathbf{y}\mid \mathbf{x})}
\right).
$$
The second term is nonpositive, which proves the inequality. It is strictly negative exactly when $\Xi_{\alpha,\mu}^{(>0)}(\mathbf{y}\mid \mathbf{x})>0$. This proves the claim.

This proposition is the rigorous content behind the intuition that extra latent reasoning states enlarge phase space and lower free energy. However, it lowers the grand potential of *each candidate answer separately*. Therefore improved accuracy depends on relative gaps, not on absolute lowering.

Indeed, for any two candidate answers $\mathbf{y}_1$ and $\mathbf{y}_2$,
$$
\log \frac{p_{\alpha,\mu}(\mathbf{y}_1\mid \mathbf{x})}
{p_{\alpha,\mu}(\mathbf{y}_2\mid \mathbf{x})}
=
-\frac{1}{\alpha}
\left(
\Omega_{\alpha,\mu}(\mathbf{y}_1\mid \mathbf{x})
-
\Omega_{\alpha,\mu}(\mathbf{y}_2\mid \mathbf{x})
\right).
$$
So chain-of-thought helps only when it lowers the grand potential of the correct answer more than it lowers the grand potential of its competitors.

## What "Think Step by Step" Can and Cannot Mean

A prompt such as "think step by step" is not a theorem of the partition function. It is a perturbation of the reference model. If $\widetilde{\mathbf{x}}$ denotes the prompt obtained by appending such an instruction to $\mathbf{x}$, then the relevant question is whether the new reference law $p_0(\mathbf{z},\mathbf{y}\mid \widetilde{\mathbf{x}})$ reallocates more mass toward high net-reward traces for the correct answer than for incorrect ones.

The clean odds criterion is
$$
\frac{p_{\alpha,\mu}(\mathbf{y}^\star\mid \widetilde{\mathbf{x}})}
{p_{\alpha,\mu}(\mathbf{y}\mid \widetilde{\mathbf{x}})}
>
\frac{p_{\alpha,\mu}^{(0)}(\mathbf{y}^\star\mid \mathbf{x})}
{p_{\alpha,\mu}^{(0)}(\mathbf{y}\mid \mathbf{x})}
\quad
\Longleftrightarrow
\quad
\frac{\Xi_{\alpha,\mu}(\mathbf{y}^\star\mid \widetilde{\mathbf{x}})}
{\Xi_{\alpha,\mu}(\mathbf{y}\mid \widetilde{\mathbf{x}})}
>
\frac{\Xi_{\alpha,\mu}^{(0)}(\mathbf{y}^\star\mid \mathbf{x})}
{\Xi_{\alpha,\mu}^{(0)}(\mathbf{y}\mid \mathbf{x})}.
$$

This is the correct place to state the prompting hypothesis. A chain-of-thought prompt is useful when it changes the pretrained prior so that the correct answer gains more grand-partition mass than its competitors. That can happen because the prompt pushes the model toward more structured intermediate traces. It can also fail: the prompt may inflate the partition function of elegant but wrong traces, or it may drive the model into a long-trace regime where the chemical potential no longer stabilizes the sum. The formalism allows both outcomes.

## Self-Consistency Is Monte Carlo Marginalization

Once the answer law is written as a latent marginal, the role of self-consistency becomes transparent. In the idealized case where one can sample i.i.d. pairs
$$
(\mathbf{Z}^{(k)},\mathbf{Y}^{(k)}) \sim p_{\alpha,\mu}(\mathbf{z},\mathbf{y}\mid \mathbf{x}),
\qquad k=1,\dots,K,
$$
the empirical answer frequencies
$$
\widehat p_K(\mathbf{y}\mid \mathbf{x})
=
\frac{1}{K}\sum_{k=1}^{K}\mathbf{1}\{\mathbf{Y}^{(k)}=\mathbf{y}\}
$$
satisfy
$$
\mathbb{E}\big[\widehat p_K(\mathbf{y}\mid \mathbf{x})\big]
=
p_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x}),
\qquad
\mathrm{Var}\big[\widehat p_K(\mathbf{y}\mid \mathbf{x})\big]
=
\frac{p_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x})\big(1-p_{\alpha,\mu}(\mathbf{y}\mid \mathbf{x})\big)}{K}.
$$

So self-consistency is a Monte Carlo estimator of the marginal answer law, with the usual $1/K$ variance decay {% cite wang2022self %}. This is the precise numerical-analysis analogy. It is not a statement about ODE integration. In practice, deployed language models do not sample exactly from the ideal reweighted grand-canonical law, but the interpretation remains useful: multi-sample chain-of-thought is trying to approximate a latent marginal, not merely to produce longer prose.

## How the Grand-Canonical Picture Sits on Top of Blondel's Result

Blondel's theorem already tells us that local next-token logits contain a soft value term summarizing future continuation mass {% cite blondel2025autoregressive %}. The grand-canonical extension does not replace that statement. It adds a second layer on top of it.

For each fixed reasoning length $N$, the joint law over $\mathbf{u}=\mathbf{z}\oplus \mathbf{y}$ is still a canonical reference-measure EBM, and Blondel's soft Bellman recursion applies token by token along that sequence. The grand-canonical model then sums these canonical slices over all admissible values of $N$ with weight $\zeta^N$. In other words, Blondel explains how future mass is compressed into local logits *within* a fixed continuation, while the grand-canonical extension explains how explicit reasoning introduces an *outer* marginalization over how much latent computation the model is allowed to externalize.

This resolves an apparent tension. If next-token logits already look ahead, why can chain-of-thought still help? The answer is not that zero-shot decoding is purely myopic. The answer is that the model must approximate its continuation free energies with finite capacity. Hard problems can demand a sharper estimate of suffix mass than a single internal look-ahead pass can provide. Emitting intermediate reasoning tokens turns hidden future integration into an explicit sequence of state updates. Each emitted token moves the prefix from $s_t$ to $s_{t+1}$, and the model reevaluates a new local soft value on a refined state. Chain-of-thought therefore spends extra inference-time compute to sequentially refine the approximation of the same free-energy object that Blondel identifies inside the logits.

That is also why the strongest defensible statement is modest but useful. Chain-of-thought does not magically create a new objective. It enlarges the latent phase space over which the model can represent and marginalize structured futures. When the pretrained prior and the verifier reward are aligned with the task, that larger phase space can lower the relevant grand-potential gaps and improve answer selection. When they are not aligned, longer reasoning can simply generate longer mistakes.

## Conclusion

The mathematically clean picture is therefore the following. Jaynes' maximum-entropy principle gives a reference-measure Gibbs law over complete continuations. Blondel et al. show that, in function space, the corresponding autoregressive logits satisfy a soft Bellman recursion, so local next-token scores already contain a continuation free energy {% cite blondel2025autoregressive levine2018reinforcement %}. Chain-of-thought then adds an ordered latent trace whose length is itself variable. That makes the correct thermodynamic object a grand partition over reasoning traces and answers, with chemical potential penalizing extra reasoning tokens and fugacity controlling expected reasoning effort.

From this viewpoint, zero-shot decoding is the $N=0$ constrained model and chain-of-thought is marginal MAP over ordered latent traces. The rigorous theorem is that enlarging the latent family cannot worsen the optimal grand free energy, and the answer-specific theorem is that marginalizing over reasoning traces cannot increase the grand potential of a fixed answer. What remains empirical is whether a given prompt shifts enough mass toward the right traces to improve the *relative* grand-potential gap of the correct answer.

That seems to me to be the most precise version of the intuition that "thinking step by step" helps language models. It is not an ODE story. It is a grand-canonical marginalization story built on top of the soft Bellman geometry already present in autoregressive logits.

---

## References

{% bibliography --cited %}
