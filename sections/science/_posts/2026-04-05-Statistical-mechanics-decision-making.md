---
layout: post
title: Statistical mechanics of decision making
description: "From Jaynes and the soft Bellman equation to a grand-canonical reading of chain-of-thought, with fugacity as reasoning effort."
date: 2026-04-05
published: true
categories:
  - science
  - deep-learning
---

A recurring question about language models is deceptively simple to state. When does asking a model to "think step by step" actually help it decide, and when does it just produce longer text? I want to give that question a precise answer, and the cleanest language I know for it comes from statistical mechanics. The plan is to start from how a maximum-entropy agent makes decisions, show that next-token prediction is already such an agent, and then read chain-of-thought as a specific thermodynamic operation: marginal inference over an ordered latent trace whose length is itself a fluctuating quantity.

The thread that holds everything together is one object, the free energy, and one recent result. Blondel et al. proved that autoregressive models and energy-based models coincide in function space, so that a model's next-token logits contain a soft Bellman look-ahead term {% cite blondel2025autoregressive %}. Everything below is an attempt to take that result seriously and follow where it leads.

## Decisions as a maximum-entropy ensemble

Jaynes' principle says that, given some constraints on a system, the least committal distribution consistent with them is the one of maximum entropy. Cast sequential decision-making in that mould. An agent moves through states $$s_t$$ by taking actions $$a_t$$, the environment evolves under a transition kernel $$p(s_{t+1}\mid s_t,a_t)$$, and a trajectory is $$\tau=(s_0,a_0,s_1,\dots)$$. Without any goal the agent follows a reference dynamics $$\bar p(\tau)$$, fixed by the initial distribution and an uninformative policy.

Now impose one constraint: the expected return $$R(\tau)=\sum_t \gamma^t r(s_t,a_t)$$ must hit a target value. Minimising the relative entropy to $$\bar p$$ subject to that constraint gives, through a single Lagrange multiplier $$\beta=1/\alpha$$, an exponential tilt of the reference measure,
$$
p^\star(\tau)=\frac{1}{Z}\,\bar p(\tau)\,\exp\!\Big(\tfrac{1}{\alpha}R(\tau)\Big),
\qquad
Z=\int \bar p(\tau)\exp\!\Big(\tfrac{1}{\alpha}R(\tau)\Big)\,d\tau .
$$
For a physicist the dictionary is exact. The return is a negative energy, $$E(\tau)=-R(\tau)$$; the multiplier $$\alpha$$ is a temperature; and $$F=-\alpha\log Z$$ is a free energy. At $$\alpha\to 0$$ the distribution freezes onto the single best trajectory, the ground state. At $$\alpha\to\infty$$ it forgets the reward and relaxes to $$\bar p$$. This is the maximum-entropy view of control, and it is the same construction that underlies reinforcement learning as inference {% cite levine2018reinforcement %}.

To turn $$p^\star(\tau)$$ into something an agent can execute step by step, write it through a soft value function. Define the soft state value as a log-sum-exp backup,
$$
V(s_t)=\alpha\log\sum_{a}\exp\!\Big(\tfrac{1}{\alpha}\,Q(s_t,a)\Big),
\qquad
Q(s_t,a)=r(s_t,a)+\gamma\,\mathbb{E}_{s_{t+1}}\big[V(s_{t+1})\big],
$$
with optimal policy $$\pi^\star(a\mid s_t)\propto\exp\big(Q(s_t,a)/\alpha\big)$$. This is the soft Bellman equation. The hard $$\max$$ of classical dynamic programming has been smoothed into $$\log\sum\exp$$, and the smoothing has a thermodynamic meaning: $$V(s)=-\alpha\log Z(s)$$ is the local free energy of every future reachable from $$s$$, propagated backward through time. A maximum-entropy agent is a bounded-rational one. It trades reward against the entropy of its own choices, and the temperature sets the exchange rate.

## Next-token prediction already looks ahead

A language model fits this picture with almost no friction. The state $$s_t=\mathbf{x}\oplus\mathbf{u}_{<t}$$ is the context generated so far, the action is the next token, and the dynamics are degenerate because appending a token is deterministic. The reference measure is not uniform; it is the pretrained model itself.

Fix a prompt $$\mathbf{x}$$ and let $$\mathbf{u}$$ be a complete continuation ending in $$\mathrm{EOS}$$. With a reference autoregressive model $$p_0(\mathbf{u}\mid\mathbf{x})$$ and a verifier reward $$R(\mathbf{x},\mathbf{u})$$, the maximum-entropy solution is again a reference-measure Gibbs law,
$$
p_{\alpha}(\mathbf{u}\mid\mathbf{x})
=\frac{1}{Z_\alpha(\mathbf{x})}\,
p_0(\mathbf{u}\mid\mathbf{x})\exp\!\Big(\tfrac{1}{\alpha}R(\mathbf{x},\mathbf{u})\Big).
$$
Absorb the reference model into a total score $$S(\mathbf{x},\mathbf{u})=R(\mathbf{x},\mathbf{u})+\alpha\log p_0(\mathbf{u}\mid\mathbf{x})$$, and suppose it decomposes additively along the emitted sequence, $$S=\sum_t r_{\mathrm{tot}}(s_t,u_t)$$. Blondel et al. then show that the autoregressive logits satisfy an exact soft Bellman recursion {% cite blondel2025autoregressive %},
$$
q^\star(s_t,u_t)=\tfrac{1}{\alpha}r_{\mathrm{tot}}(s_t,u_t)+V_q(s_t\oplus u_t),
\qquad
V_q(s)=\log\!\!\sum_{v\in\mathcal V\cup\{\mathrm{EOS}\}}\!\!\exp\big(q^\star(s,v)\big).
$$
The notation matters less than what $$V_q(s)$$ is: the log-partition of every suffix reachable from $$s$$, so that $$-\alpha V_q(s)$$ is a continuation free energy. A next-token logit carries an immediate score plus the free energy of all futures that open up after that token. This is the precise sense in which a single forward pass is already doing look-ahead, not greedy guessing. Zero-shot decoding asks the network to compress the entire future partition function into one internal estimate of $$V_q$$.

## Reasoning as an ordered latent process

To talk about chain-of-thought, split the continuation into a reasoning trace and an answer, $$\mathbf{u}=\mathbf{z}\oplus\mathbf{y}$$ with $$\mathbf{z}=(z_1,\dots,z_N)$$. The reference model factorises autoregressively,
$$
p_0(\mathbf{z},\mathbf{y}\mid\mathbf{x})
=\Big(\prod_{i=1}^{N}p_0(z_i\mid\mathbf{x},\mathbf{z}_{<i})\Big)
\Big(\prod_{j=1}^{M}p_0(y_j\mid\mathbf{x},\mathbf{z},\mathbf{y}_{<j})\Big),
$$
which already says something people sometimes forget. A rationale is an *ordered* latent variable. The token $$z_i$$ is conditioned on its predecessors, so a chain-of-thought is a process with a direction, not a bag of intermediate facts {% cite phan2023training %}.

The interesting move is that $$N$$ is not fixed. The model may answer immediately, after a short detour, or after a long argument, and it decides when to stop by emitting $$\mathrm{EOS}$$. A system whose particle number fluctuates is grand canonical, not canonical. So introduce a chemical potential $$\mu$$ that charges each reasoning token, with fugacity $$\zeta:=\exp(-\mu/\alpha)$$, and sum over all trace lengths:
$$
\Xi_{\alpha,\mu}(\mathbf{x})
=\sum_{\mathbf{y}}\sum_{N=0}^{\infty}\sum_{\mathbf{z}\in\mathcal V^{N}}
p_0(\mathbf{z},\mathbf{y}\mid\mathbf{x})\,
\exp\!\Big(\tfrac{R(\mathbf{x},\mathbf{z},\mathbf{y})-\mu N}{\alpha}\Big)
=\sum_{N=0}^{\infty}\zeta^{N}Z_N(\mathbf{x}).
$$
The grand potential is $$\Omega:=-\alpha\log\Xi$$. Fugacity is conjugate to reasoning effort: it governs the expected trace length without being that length. The expected trace length is
$$
\mathbb{E}[N\mid\mathbf{x}]=\zeta\,\frac{\partial}{\partial\zeta}\log\Xi_{\alpha,\mu}(\mathbf{x}),
$$
so lowering $$\mu$$ (raising $$\zeta$$) buys longer expected reasoning. A prompt that elicits more deliberation is, in this language, a prompt that raises the fugacity of the reasoning trace.

There is a stability caveat that the formalism makes explicit. The sum over lengths converges only if the per-step weight stays bounded: it is enough that $$Z_N(\mathbf{x})\le C_{\mathbf{x}}\rho_{\mathbf{x}}^N$$ with $$\zeta\rho_{\mathbf{x}}<1$$. When that fails, $$\Xi$$ diverges and there is no normalised law to speak of. The physics predicts a runaway long-trace phase, which is exactly the uncontrolled-looping failure mode of models pushed to reason without limit.

## What is actually provable

The grand partition has the standard Gibbs variational form,
$$
-\alpha\log\Xi_{\alpha,\mu}(\mathbf{x})
=\min_{q}\Big\{\mathbb{E}_{q}\big[-R+\mu N\big]
+\alpha\,\mathrm{KL}\!\big(q\,\|\,p_0\big)\Big\},
$$
over distributions $$q(\mathbf{z},\mathbf{y})$$ supported inside $$p_0$$. From this, one clean fact follows immediately.

**Proposition 1.** Let $$\mathcal Q_0$$ be the family of distributions supported on $$N=0$$ and $$\mathcal Q_{\mathrm{gc}}$$ the family of all variable-length distributions. Then $$\min_{q\in\mathcal Q_{\mathrm{gc}}}\mathcal F_{\alpha,\mu}(q)\le\min_{q\in\mathcal Q_0}\mathcal F_{\alpha,\mu}(q)$$, where $$\mathcal F$$ is the bracketed free-energy functional.

The proof is a containment argument: $$\mathcal Q_0\subset\mathcal Q_{\mathrm{gc}}$$, so minimising the same functional over the larger family cannot do worse. Enlarging the latent family can only lower the best achievable free energy. The proposition says nothing about whether a real decoder finds that lower minimum, or whether any particular extra token earns its keep. Those are separate questions, and most disappointments with long reasoning live there.

For answer selection we need a finer object. Define the answer-specific grand partition by summing only over traces that lead to a fixed $$\mathbf{y}$$,
$$
\Xi_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})
=\sum_{N=0}^{\infty}\sum_{\mathbf{z}\in\mathcal V^{N}}
p_0(\mathbf{z},\mathbf{y}\mid\mathbf{x})\,
\exp\!\Big(\tfrac{R(\mathbf{x},\mathbf{z},\mathbf{y})-\mu N}{\alpha}\Big),
\qquad
\Omega_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})=-\alpha\log\Xi_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x}).
$$
The answer marginal is then a softmax over grand potentials, $$p_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})\propto\exp(-\Omega_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})/\alpha)$$. Zero-shot decoding is the constrained slice $$N=0$$ and targets the MAP answer $$\arg\max_{\mathbf{y}}\Xi^{(0)}_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})$$. Chain-of-thought sums over every ordered trace first and only then compares answers, targeting the *marginal* MAP $$\arg\max_{\mathbf{y}}\Xi_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})$$. A single decoded rationale is one sample, or one dominant path, drawn from inside that marginal.

**Proposition 2.** Assume $$\Xi^{(0)}_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})>0$$. Then $$\Omega_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})\le\Omega^{(0)}_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})$$, with strict inequality exactly when some trace of length $$N\ge1$$ has positive base weight.

Split the grand partition into its $$N=0$$ piece and the rest:
$$
\Omega_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})
=\Omega^{(0)}_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})
-\alpha\log\!\Big(1+\frac{\Xi^{(>0)}_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})}{\Xi^{(0)}_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})}\Big).
$$
The correction term is nonpositive, and strictly negative once any positive-length trace contributes. Marginalising over rationales lowers the grand potential of an answer. The algebra then forces a caveat: it lowers the potential of *every* candidate, the wrong ones included. Accuracy is governed by differences, not levels. For two answers,
$$
\log\frac{p_{\alpha,\mu}(\mathbf{y}_1\mid\mathbf{x})}{p_{\alpha,\mu}(\mathbf{y}_2\mid\mathbf{x})}
=-\frac{1}{\alpha}\big(\Omega_{\alpha,\mu}(\mathbf{y}_1\mid\mathbf{x})-\Omega_{\alpha,\mu}(\mathbf{y}_2\mid\mathbf{x})\big),
$$
so reasoning helps only when it drains more free energy from the correct answer than from its competitors.

## What "think step by step" can and cannot mean

This is where the formalism enforces honesty. A prompt is not a theorem about the partition function. It is a perturbation of the reference model. Writing $$\widetilde{\mathbf{x}}$$ for the prompt with the instruction appended, the question is whether the new prior $$p_0(\mathbf{z},\mathbf{y}\mid\widetilde{\mathbf{x}})$$ reallocates mass toward high-reward traces for the correct answer more than for the wrong ones. The clean criterion is an odds comparison,
$$
\frac{\Xi_{\alpha,\mu}(\mathbf{y}^\star\mid\widetilde{\mathbf{x}})}{\Xi_{\alpha,\mu}(\mathbf{y}\mid\widetilde{\mathbf{x}})}
>
\frac{\Xi^{(0)}_{\alpha,\mu}(\mathbf{y}^\star\mid\mathbf{x})}{\Xi^{(0)}_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})}.
$$
When the pretrained prior and the verifier reward are aligned with the task, conditioning on the instruction concentrates $$p_0$$ on structured intermediate traces and this inequality holds. It can also fail. The prompt may inflate the partition function of elegant but wrong arguments, or it may drop $$\zeta\rho_{\mathbf{x}}$$ across the divergence threshold and send the model into the long-trace phase. The grand-canonical picture permits both outcomes, which is its main virtue. It tells you what would have to be true for the prompt to work, instead of promising that it always does.

## Self-consistency is Monte Carlo

Once the answer law is written as a latent marginal, sampling several rationales and taking a majority vote stops looking like a heuristic. If one could draw $$(\mathbf Z^{(k)},\mathbf Y^{(k)})\sim p_{\alpha,\mu}$$ for $$k=1,\dots,K$$, the empirical answer frequencies $$\widehat p_K(\mathbf{y}\mid\mathbf{x})$$ would be unbiased for $$p_{\alpha,\mu}(\mathbf{y}\mid\mathbf{x})$$ with variance $$p(1-p)/K$$. Self-consistency is a Monte Carlo estimator of the marginal answer law, with the usual $$1/K$$ decay {% cite wang2022self %}. Deployed models do not sample exactly from the ideal reweighted law, so this is an idealisation. It is the right one to keep in mind: multi-sample reasoning is approximating an integral over traces, not merely generating more prose.

## Where this leaves the question, and where it could go

Two statements survive scrutiny. Enlarging the latent family cannot raise the optimal free energy, and marginalising over traces cannot raise the grand potential of a fixed answer. What stays empirical is whether a given prompt moves enough mass toward the right traces to widen the *relative* gap of the correct answer. The slogan that "thinking helps" is true in a weak, defensible form and false as a guarantee, and the inequality above marks the exact boundary between the two.

A few directions follow naturally enough to be worth stating, with the warning that they are conjectural to different degrees.

The first is operational. Fugacity sets expected reasoning length through $$\mathbb{E}[N]=\zeta\,\partial_\zeta\log\Xi$$, and the answer marginal is a function of the accumulated free energy. That suggests an adaptive stopping rule: keep emitting reasoning tokens while the marginal grand potential of the leading answer is still falling faster than $$\mu$$ charges per token, and halt when the two balance. A controller that watches the running estimate of $$\Omega(\mathbf{y}^\star\mid\mathbf{x})$$ would, in principle, tune effort to the difficulty of the instance rather than to a fixed token budget.

The second concerns interaction. Self-consistency treats sampled rationales as independent draws. Let them read one another instead, as in debate or multi-agent reasoning, and the single-agent soft Bellman picture generalises to a coupled game. With reward for one path affinely coupled to the trajectories of the others, $$R^i=b^i+\sum_{j}C^{ij}Y^j$$, the sign of the coupling matrix is interpretable: positive entries build consensus, negative entries drive critique. Under a mild concavity condition on $$C+C^\top$$ the coupled system has a unique soft-Bellman equilibrium, which gives a clean target for what multi-path reasoning is supposed to converge to and a knob, the coupling topology, that current schemes set only implicitly.

The third is more speculative and I flag it as such. Because $$\Omega$$ is a genuine free energy, its temperature derivative is a heat capacity, $$\partial^2_\alpha F\propto\mathrm{Var}(R)/\alpha^2$$, and one can ask whether the abrupt onset of reasoning ability with scale is a near-critical phenomenon rather than a smooth one. In the same spirit, an "aha" step in a rationale would show up as a discontinuous drop in $$\mathbb{E}[R\mid\mathbf{z}_{\le t}]$$ along the trace, a barrier crossing rather than a slide downhill. These are framings, not results. The formalism makes them precise enough to test, and that is the most I would claim for them today.

## Closing

The mathematically solid story runs in one line. Jaynes gives a reference-measure Gibbs law over continuations; Blondel et al. show the corresponding autoregressive logits satisfy a soft Bellman recursion, so a single pass already carries a continuation free energy {% cite blondel2025autoregressive levine2018reinforcement %}; and chain-of-thought adds an ordered latent trace of fluctuating length, making the right object a grand partition with chemical potential charging each reasoning token and fugacity setting expected effort. Zero-shot decoding is the $$N=0$$ constrained model, chain-of-thought is marginal MAP over traces, and self-consistency is Monte Carlo over that marginal. The look-ahead was always inside the logits. Reasoning out loud is the model externalising, one token at a time, an integration it would otherwise have to fold into a single forward pass.

---

## References

{% bibliography --cited %}
