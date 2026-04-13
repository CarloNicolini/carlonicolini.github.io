---
layout: post
title: Random rooted trees, continuation free energy, and the Diligent Learner
description: "A unified theory of delayed commitment, decomposition tax, and tool building in scaffolded inference."
date: 2026-04-04
published: true
categories:
  - science
  - language-physics
---

## Why these two theories should meet

In the last few posts I have argued that inference-time compute is best described at the scaffold level. A scaffold induces a finite random rooted tree over traces. Its local branching law depends on continuation free energy, delayed commitment, and the tax paid when a task is split into smaller parts. In parallel, the Diligent Learner program studies reasoning as validator-guided search and isolates a single bottleneck: the probability mass $\gamma$ that the model assigns to good next steps {% cite shalevshwartz2025reasoning koplow2026toolbuilding %}. The two traditions use different language, but they point to the same local object.

This post makes that connection explicit. Under a Boltzmann-style local control law, a finite-budget scaffold can be written as a maximum-entropy control process on prefixes. In that setting, the local choice between answering, abstaining, and decomposing is governed by continuation free energy in the sense suggested by Blondel et al. {% cite blondel2025autoregressive %} and by the probabilistic-control literature {% cite levine2018reinforcement kappen2005linear kappen2005path %}. The Diligent Learner parameter $\gamma$ then becomes a derived quantity rather than a primitive one: it is the probability mass of the good continuation basin under the local free-energy law.

The payoff is partly conceptual and partly algebraic. First, the scaffold's local branching probabilities admit a closed-form soft-control law. Second, under the specialization used below, the Diligent Learner parameter $\gamma$ is a logistic transform of a free-energy gap between good and bad continuation basins. Third, delayed commitment acquires an explicit entropic value when several continuation basins remain competitive. Fourth, tool building can be modeled as a reduction in effective decomposition tax or, equivalently, as an additive bonus on good-basin free energy. This shifts the log-odds of $\gamma$ by a predictable amount.

These results do not show that real systems already estimate the relevant values accurately. They do, however, explain why tool use can stabilize long-horizon reasoning in principle. Tools help when they reshape the local free-energy landscape so that good continuations retain non-negligible mass at depth.

## Setup and notation

I will work inside the PLP viewpoint introduced in [Probabilistic Language Programming]({% link sections/science/_posts/2026-03-01-Probabilistic-Language-Programming.md %}) and expanded in [Scaffolding is all you need]({% link sections/science/_posts/2026-03-02-Scaffolding-is-all-you-need.md %}), [PLP is inference-time approximation of free energy]({% link sections/science/_posts/2026-03-31-PLP-is-inference-time-approximation-of-free-energy.md %}), and [Soft values, symmetry breaking, and random rooted trees]({% link sections/science/_posts/2026-04-02-Soft-values-symmetry-breaking-and-random-rooted-trees.md %}).

Let $x$ denote the root task, $\tau$ a complete execution trace, and $s$ a trace prefix. A deployed scaffold $\mathcal{D}$ induces a proposal law $\pi_{\mathcal{D}}(\tau \mid s)$ over completions extending $s$. Let $\Phi(\tau, x) \ge 0$ be a verifier potential. For inverse temperature $\beta > 0$, define the tempered continuation partition

$$
Z_\beta(s)
:=
\sum_{\tau \succ s}
\pi_{\mathcal{D}}(\tau \mid s)\,
\Phi(\tau, x)^\beta.
$$

The corresponding soft continuation value is

$$
V_\beta(s)
:=
\frac{1}{\beta}\log Z_\beta(s),
$$

and the continuation free energy is

$$
F_\beta(s):=-V_\beta(s).
$$

Maximizing $V_\beta$ is therefore the same as minimizing continuation free energy. This is the natural control objective in maximum-entropy RL {% cite levine2018reinforcement %}, and it is also the object that Blondel et al. identify inside next-token prediction as a cached lookahead term {% cite blondel2025autoregressive %}. In the rest of the post I treat $V_\beta$ as available. How well a deployed system can estimate it is a separate empirical question.

To keep the runtime finite, assume the scaffold has a depth or budget cap. Then each run produces a finite random rooted tree $T_\beta(x)$. Every internal node corresponds to a prefix $s$. At that node the scaffold may do one of three things. It may answer directly, it may abstain and gather extra information before deciding, or it may decompose the task into child prefixes.

Let $\mathcal{Y}(s)$ be the set of terminal answer actions, $\mathcal{W}(s)$ the set of abstention or probing actions, and $\mathfrak{D}(s)$ the set of admissible decompositions. Let $q_{\mathrm{ans}}$, $q_{\mathrm{abs}}$, and $q_{\mathrm{dec}}$ be the proposal kernels over these action classes.

For a direct answer $y \in \mathcal{Y}(s)$, let $r(y,s)$ denote its terminal reward or log-potential contribution. For a probing action $w \in \mathcal{W}(s)$, let $p(o \mid s,w)$ be the distribution of revealed observations and let $\lambda_{\mathrm{abs}}(s,w) \ge 0$ be its tax. For a decomposition $D=(s_1,\dots,s_k)\in\mathfrak{D}(s)$, let $\lambda_{\mathrm{dec}}(s,D) \ge 0$ be its decomposition tax. This tax summarizes compute, latency, interface mismatch, dependence between children, and composition fragility.

Under the usual conditional-independence approximation between child subtrees given $D$, the three local partition terms are

$$
Z_{\beta}^{\mathrm{ans}}(s)
:=
\sum_{y\in\mathcal{Y}(s)}
q_{\mathrm{ans}}(y\mid s)\,
\exp\!\bigl(\beta r(y,s)\bigr),
$$

$$
Z_{\beta}^{\mathrm{abs}}(s)
:=
\sum_{w\in\mathcal{W}(s)}
q_{\mathrm{abs}}(w\mid s)\,
\exp\!\bigl(-\beta\lambda_{\mathrm{abs}}(s,w)\bigr)
\sum_{o} p(o\mid s,w)\,
\exp\!\bigl(\beta V_\beta(s\oplus o)\bigr),
$$

and

$$
Z_{\beta}^{\mathrm{dec}}(s)
:=
\sum_{D=(s_1,\dots,s_k)\in\mathfrak{D}(s)}
q_{\mathrm{dec}}(D\mid s)\,
\exp\!\Bigl(
\beta\sum_{i=1}^k V_\beta(s_i)
-\beta\lambda_{\mathrm{dec}}(s,D)
\Bigr).
$$

The local soft value decomposes as

$$
Z_\beta(s)
=
Z_{\beta}^{\mathrm{ans}}(s)
+
Z_{\beta}^{\mathrm{abs}}(s)
+
Z_{\beta}^{\mathrm{dec}}(s),
\qquad
V_\beta(s)=\frac{1}{\beta}\log Z_\beta(s).
$$

## A three-way local control law

The first result is immediate once the partition is written in this way, but it is the structural statement on which the rest of the post depends.

**Proposition 1.** The local control policy over the three modes $m \in \{\mathrm{ans},\mathrm{abs},\mathrm{dec}\}$ is

$$
\pi_\beta(m\mid s)
=
\frac{Z_{\beta}^{m}(s)}{Z_\beta(s)}
=
\exp\!\Bigl(\beta\bigl(V_\beta^{m}(s)-V_\beta(s)\bigr)\Bigr),
$$

where $V_\beta^{m}(s):=\beta^{-1}\log Z_\beta^{m}(s)$. Conditioned on choosing decomposition, the law of a particular skeleton $D$ is

$$
\pi_\beta(D\mid s,\mathrm{dec})
\propto
q_{\mathrm{dec}}(D\mid s)\,
\exp\!\Bigl(
\beta\sum_{i=1}^{|D|}V_\beta(s_i)
-\beta\lambda_{\mathrm{dec}}(s,D)
\Bigr).
$$

*Proof.* The first identity follows by partitioning $Z_\beta(s)$ into the three disjoint mode contributions and normalizing. The second identity is the same normalization restricted to the decomposition term. $\square$

Under this parameterization, a scaffold is a locally normalized soft controller over macro-actions. Direct answers, abstentions, and decompositions all compete through the same currency: continuation free energy corrected by local taxes. The random rooted tree is thus the sample path of a finite maximum-entropy control process on prefixes.

## The Diligent Learner as a free-energy statement

To recover the Diligent Learner, I now specialize the scaffold. Remove abstention for the moment. Let each local move be a one-step semantic extension $a$ that produces a single child prefix $s\oplus a$. Let $\mathcal{G}(s)$ denote the set of good extensions, meaning those that still admit a validator-accepted completion, and let $\mathcal{B}(s)$ denote the bad ones. Define the good and bad partition terms

$$
Z_{\beta}^{G}(s)
:=
\sum_{a\in\mathcal{G}(s)}
q(a\mid s)\,
\exp\!\bigl(\beta V_\beta(s\oplus a)\bigr),
$$

$$
Z_{\beta}^{B}(s)
:=
\sum_{a\in\mathcal{B}(s)}
q(a\mid s)\,
\exp\!\bigl(\beta V_\beta(s\oplus a)\bigr).
$$

Let

$$
V_\beta^{G}(s):=\frac{1}{\beta}\log Z_{\beta}^{G}(s),
\qquad
V_\beta^{B}(s):=\frac{1}{\beta}\log Z_{\beta}^{B}(s).
$$

Under this specialization, the Diligent Learner step-success parameter is an immediate consequence of the local partition.

**Theorem 2.** The probability mass that the local policy assigns to good next steps is

$$
\gamma_\beta(s)
:=
\sum_{a\in\mathcal{G}(s)} \pi_\beta(a\mid s)
=
\frac{Z_\beta^{G}(s)}{Z_\beta^{G}(s)+Z_\beta^{B}(s)}
=
\sigma\!\Bigl(\beta\bigl(V_\beta^{G}(s)-V_\beta^{B}(s)\bigr)\Bigr),
$$

where $\sigma(z)=1/(1+e^{-z})$ is the logistic function.

*Proof.* The first equality is the definition of good-basin mass. The second follows from normalization. The third follows by dividing numerator and denominator by $Z_\beta^{B}(s)$. $\square$

The bridge between the two theories is now explicit. In the Diligent Learner language, one assumes that $\gamma$ does not collapse with depth. In the random-rooted-tree language, the same condition becomes a statement about the free-energy gap between the good and bad continuation basins along correct prefixes.

The theorem also gives an immediate sampling consequence.

**Corollary 2.1.** If the scaffold can draw $B$ conditionally independent proposals from the same prefix $s$, the probability of seeing at least one good extension is

$$
1-(1-\gamma_\beta(s))^B.
$$

If $\gamma_\beta(s)\ge \underline{\gamma}>0$ along a depth-$T$ correct trajectory and the proposal batches are conditionally independent across depths, then

$$
\mathbb{P}(\text{reach depth }T)
\ge
\prod_{t=0}^{T-1}\Bigl(1-(1-\underline{\gamma})^{B_t}\Bigr).
$$

*Proof.* The first statement is the complement of failing $B$ times in a row. The second multiplies these lower bounds along the depth-indexed path. $\square$

This corollary is weaker than the full search analysis in the Diligent Learner papers {% cite shalevshwartz2025reasoning koplow2026toolbuilding %}. It also relies on an idealized conditional-independence assumption. Even so, it makes the core mechanism transparent. Global success depends on keeping a positive free-energy gap between good and bad basins. Search only exposes that mass; it does not create it.

## Delayed commitment and the value of symmetry

The previous section handled the answer-versus-search split. The next step is to understand abstention. This is where Kappen's symmetry-breaking picture becomes directly useful {% cite kappen2005path %}.

Suppose the node is not yet ready to commit because several continuation basins remain viable. If the scaffold abstains, it gathers one more piece of information and only then commits. Let the resulting post-reveal branch scores be $U_1,\dots,U_m$. I absorb any local observation probabilities or proposal weights into these scores so that each $U_i$ is already a full continuation value. Let the abstention tax be $\lambda_{\mathrm{abs}}$.

**Theorem 3.** The abstention branch has value

$$
V_\beta^{\mathrm{abs}}
=
-\lambda_{\mathrm{abs}}
+
\frac{1}{\beta}\log\!\Bigl(\sum_{i=1}^{m}\exp(\beta U_i)\Bigr).
$$

If $U_{\max}=\max_i U_i$ is the best immediate commitment value, then the gain from abstention is

$$
\Delta_{\mathrm{abs}}
:=
V_\beta^{\mathrm{abs}}-U_{\max}
=
-\lambda_{\mathrm{abs}}
+
\frac{1}{\beta}\log\!\Bigl(\sum_{i=1}^{m}\exp\bigl(\beta(U_i-U_{\max})\bigr)\Bigr).
$$

Therefore abstention is optimal if and only if

$$
\lambda_{\mathrm{abs}}
<
\frac{1}{\beta}\log\!\Bigl(\sum_{i=1}^{m}\exp\bigl(\beta(U_i-U_{\max})\bigr)\Bigr).
$$

In the symmetric case $U_1=\cdots=U_m=U$, this becomes

$$
V_\beta^{\mathrm{abs}}=U-\lambda_{\mathrm{abs}}+\frac{1}{\beta}\log m,
\qquad
\Delta_{\mathrm{abs}}=-\lambda_{\mathrm{abs}}+\frac{1}{\beta}\log m.
$$

*Proof.* Insert the $m$ abstention continuations into the local partition and take $\beta^{-1}\log$. The comparison with immediate commitment is obtained by subtracting $U_{\max}$. $\square$

This result makes the value of delayed commitment precise. The term $\beta^{-1}\log m$ is an entropic symmetry bonus. It measures the value of keeping $m$ live basins available for one more step. In Kappen's language, delayed choice appears when several continuations remain competitive {% cite kappen2005path %}. In scaffolded inference the same effect appears as a local free-energy bonus for not collapsing the tree too early.

The theorem also gives a practical rule. If the abstention tax exceeds the symmetry bonus, waiting is wasteful. If the symmetry bonus exceeds the tax, immediate commitment is premature. This formalizes the intuitive distinction between a useful probe and a decorative hesitation.

## Free-energy minimization under decomposition tax

We now turn to decomposition itself. In the previous notes I argued that decomposition should never be treated as free. Here the dependence on tax can be made exact.

Assume the decomposition tax takes the separable form

$$
\lambda_{\mathrm{dec}}(s,D;\lambda)=\lambda\,c(s,D),
\qquad c(s,D)\ge 0,
$$

where $\lambda$ is a global trade-off parameter and $c(s,D)$ is the structural cost of skeleton $D$. Then

$$
V_{\beta}^{\mathrm{dec}}(s;\lambda)
=
\frac{1}{\beta}
\log\!\Biggl(
\sum_{D\in\mathfrak{D}(s)}
q_{\mathrm{dec}}(D\mid s)\,
\exp\!\Bigl(
\beta\sum_{i=1}^{|D|}V_\beta(s_i)
-\beta\lambda c(s,D)
\Bigr)
\Biggr).
$$

**Proposition 4.** The decomposition value is monotone decreasing and convex in the tax parameter $\lambda$. More precisely, if $\pi_{\beta,\lambda}(D\mid s,\mathrm{dec})$ denotes the tax-weighted decomposition law,

$$
\frac{\partial}{\partial \lambda}V_{\beta}^{\mathrm{dec}}(s;\lambda)
=
-\mathbb{E}_{\pi_{\beta,\lambda}(D\mid s,\mathrm{dec})}[c(s,D)]
\le 0,
$$

and

$$
\frac{\partial^2}{\partial \lambda^2}V_{\beta}^{\mathrm{dec}}(s;\lambda)
=
\beta\,\mathrm{Var}_{\pi_{\beta,\lambda}(D\mid s,\mathrm{dec})}[c(s,D)]
\ge 0.
$$

*Proof.* Differentiate the log-partition once and then again. The standard exponential-family identities yield the mean and variance of $c(s,D)$ under the tax-weighted decomposition law. $\square$

The proposition has two consequences. First, decomposition becomes less attractive as its tax increases. Second, that loss is steepest when the scaffold is still uncertain about which decomposition skeleton it would choose. Variance in $c(s,D)$ measures how much unresolved structural ambiguity remains in the decomposition family.

If every decomposition carries the same unit cost, so that $c(s,D)\equiv 1$, the expression simplifies to

$$
V_{\beta}^{\mathrm{dec}}(s;\lambda)=V_{\beta}^{\mathrm{dec}}(s;0)-\lambda.
$$

In that case there is an explicit phase boundary. Decomposition is locally preferred over direct answering when

$$
\lambda
<
\lambda_c(s)
:=
V_{\beta}^{\mathrm{dec}}(s;0)-V_{\beta}^{\mathrm{ans}}(s),
$$

and similarly against abstention by replacing $V_{\beta}^{\mathrm{ans}}$ with $V_{\beta}^{\mathrm{abs}}$. This is the discrete control-theoretic version of a symmetry-breaking transition. As the tax rises, the random rooted tree contracts from an expansive search object toward a leaf-like direct-answer regime.

## A small arithmetic probe

To check whether this phase-boundary picture has empirical bite, I built a deliberately simple exact-arithmetic benchmark. At each node the scaffold compares three macro-actions:

1. a direct one-shot answer
2. an abstain probe implemented as a step-by-step arithmetic prompt
3. an exact decimal decomposition of the left operand, where all admissible splits are enumerated rather than proposed by the model

This benchmark is intentionally narrow. It is not meant to prove anything about general reasoning. It is meant to isolate the local control law as cleanly as possible. The model only controls the answer and abstain leaves. The decomposition family is exact, finite, and tax-weighted. That makes it a useful probe of Proposition 4.

<figure>
  <img src="/static/postfigures/random_tree_accuracy.svg" alt="Accuracy and control-law observables versus decomposition tax in an exact integer multiplication benchmark." style="width:70%; display:block; margin: 0 auto; margin-bottom: 0.5em;"/>
  <figcaption>
    <strong>Figure 1.</strong> Exact arithmetic probe of decomposition tax and delayed commitment. For two-digit products, direct answering is already strong and decomposition mostly matches it. For three-digit products, exact recursive decomposition beats direct answering at low tax, then collapses sharply as the decomposition tax crosses the mid-20s. The explicit abstain probe, implemented as a step-by-step prompt, does not help in this arithmetic regime: its standalone accuracy stays at zero and its policy mass remains negligible.
  </figcaption>
</figure>

The main qualitative result is the one the proposition predicts. On three-digit multiplication, recursive decomposition is useful only in the low-tax regime. With a small local model, the scaffold reaches about `0.625` accuracy when decomposition is cheap, while the direct-answer baseline stays at `0.0`. As the tax approaches the critical band around `\lambda \approx 25-30`, the decomposition probability and the good-basin mass both collapse, and the scaffold contracts back to a leaf-like regime with near-zero accuracy.

The abstain result is also informative. I replaced the previous heuristic abstention rule with an explicit probe branch that asks the model to work step by step before committing. In this benchmark that branch does not create a useful symmetry-breaking effect. Its standalone accuracy remains at `0.0`, and if I artificially subsidize it too much it can even poison recursive child solves by replacing easy leaf multiplications with a worse prompt. So at least in this exact arithmetic setting, delayed commitment is not buying an entropic bonus large enough to offset its probing cost.

I do not want to overclaim from this toy system. The benchmark is small, the model is small, and exact multiplication is a bounded domain. Even so, the result is directionally consistent with the theory developed above: decomposition helps when its effective tax is low enough, and a tool-like recursive branch can preserve access to the good basin in a regime where direct answering fails. The same probe also suggests a limitation: an abstain action is not automatically useful just because it adds compute. It still has to reveal evidence that changes which continuation is locally best.

## Tool building as $\gamma$ amplification

We are now ready for the link to tool building. In the Diligent Learner experiments, tool-enabled models preserve a much higher step-success probability across depth {% cite koplow2026toolbuilding %}. Within the present framework, that phenomenon can be interpreted in a precise way.

Suppose a tool does one of two equivalent things at a given prefix $s$. It may reduce the effective tax on each good action by $\delta(s) > 0$, or it may increase the continuation value of each good action by the same amount. Leave the bad actions unchanged. Let $\gamma_\beta(s)$ be the original good-basin mass and let $\gamma_\beta^{\mathrm{tool}}(s)$ be the mass after the tool is available.

**Theorem 5.** Under a uniform bonus $\delta(s)$ on the good basin,

$$
\gamma_\beta^{\mathrm{tool}}(s)
=
\frac{\exp(\beta\delta(s))\,\gamma_\beta(s)}
{1-\gamma_\beta(s)+\exp(\beta\delta(s))\,\gamma_\beta(s)}.
$$

Equivalently, the good-to-bad odds obey

$$
\log\frac{\gamma_\beta^{\mathrm{tool}}(s)}
{1-\gamma_\beta^{\mathrm{tool}}(s)}
=
\log\frac{\gamma_\beta(s)}
{1-\gamma_\beta(s)}
+\beta\delta(s).
$$

*Proof.* The tool multiplies every good-basin Boltzmann weight by $\exp(\beta\delta(s))$ while leaving the bad-basin weights unchanged. Normalize the new partition. Taking log-odds yields the second identity. $\square$

Under this stylized model, tools do not merely add an external branch. They shift the local free-energy gap in favor of good actions. In odds space the effect is additive. Every unit of bonus $\delta$ buys $\beta\delta$ units of log-odds for the good basin.

There is also an immediate depth-stabilization corollary.

**Corollary 5.1.** If the baseline good-basin odds decay with depth as

$$
\log\frac{\gamma_{\beta,t}}{1-\gamma_{\beta,t}}
=
a-\kappa t,
$$

and a tool family provides bonuses $\delta_t=\kappa t/\beta$, then the tool-adjusted odds remain constant across depth:

$$
\log\frac{\gamma_{\beta,t}^{\mathrm{tool}}}{1-\gamma_{\beta,t}^{\mathrm{tool}}}
=
a.
$$

*Proof.* Substitute $\delta_t=\kappa t/\beta$ into the log-odds identity in Theorem 5. $\square$

This corollary states the cleanest mechanism in the post. Tool building acts as a renormalization of the local free-energy geometry. If depth pushes good actions into exponentially worse odds, a suitable tool bonus can offset that decay under the assumptions of Theorem 5.

## What this says about superintelligence through tool building

The search-theoretic claim behind the Diligent Learner program is that long-horizon competence becomes possible when the model keeps assigning enough mass to good next steps {% cite shalevshwartz2025reasoning %}. The present analysis shows how to read that condition inside a scaffold theory.

The central object is not $\gamma$ alone. It is the local partition over answer, abstention, and decomposition, together with the decomposition and probing taxes that shape that partition. The Diligent Learner parameter $\gamma$ is the projection of this richer object onto a single binary question: how much mass reaches the good next-step basin? That projection is useful, but the underlying geometry matters. A system can lose $\gamma$ because the good basin itself is weak, because decomposition is too expensive, because abstention is unavailable when symmetry is high, or because the interface to tools is too noisy to deliver its bonus.

This point changes how tool building should be interpreted. In a PLP scaffold, a tool is not just an API call. It is a runtime transformation that changes the local control law. A calculator, theorem prover, interpreter, or search engine can reduce execution uncertainty, shrink composition error, and convert a vague internal reasoning burden into an externally verifiable step. In the notation above, that means lowering $\lambda_{\mathrm{dec}}$, raising the good-basin value $V_\beta^{G}$, or both.

Under this reading, "superintelligence through tool building" becomes a concrete claim about local geometry rather than a slogan. The claim is that tool use can help preserve a positive good-basin free-energy gap as depth increases. If tools add latency without changing that gap, they do not help. If they reduce the effective tax or raise the good-basin value enough to slow or stop the collapse of $\gamma$, they extend the horizon over which search remains effective.

The random rooted tree viewpoint adds one more nuance. Not all extra branching is useful. OR-style branching helps when it preserves mass over several validator-checkable continuations. AND-style branching hurts when it creates new essential nodes without compensating gains in local value. The best scaffold is therefore not the widest scaffold. It is the scaffold that spends branching budget exactly where the free-energy gap, the abstention bonus, and the decomposition tax justify it.

## Scope and limitations

The results above are algebraic statements inside a stylized model. They do not by themselves establish that deployed LLM systems estimate $V_\beta$, $\lambda_{\mathrm{abs}}$, or $\lambda_{\mathrm{dec}}$ accurately. They also do not show that real tools provide a uniform additive bonus on the good basin while leaving the bad basin unchanged. Theorem 5 should therefore be read as a mechanism result, not as a full empirical model of tool use.

Several assumptions are strong. The decomposition branch uses a conditional-independence approximation between child subtrees. Corollary 2.1 assumes conditionally independent batches across depths. The abstention result absorbs observation probabilities into post-reveal branch values. Those assumptions are useful because they isolate the control logic cleanly, but they may fail in real scaffolded systems. In practice, hidden dependence between branches, miscalibrated verifiers, and poor estimates of continuation values can all weaken the predicted gains.

The scientific value of the framework lies in what it separates. It separates local value estimation from search, decomposition tax from tool bonus, and entropic delay value from direct-answer preference. That separation does not solve the empirical problem, but it makes the empirical problem testable.

## Conclusion

The bridge between random rooted trees and the Diligent Learner is now straightforward. A scaffolded inference process can be written as a finite random rooted tree generated by a maximum-entropy control law over prefixes. Blondel's continuation value supplies the local score. Kappen's symmetry-breaking picture explains when abstention has value. The Diligent Learner parameter $\gamma$ then appears as the resulting good-basin mass, that is, as a logistic transform of a free-energy difference under the specialized policy used here.

Once that bridge is in place, several qualitative intuitions become quantitative statements. Delayed commitment is valuable when its entropic bonus exceeds its tax. Decomposition becomes less attractive at a rate controlled by the expected structural cost of the chosen skeleton. Tool building shifts the log-odds of good next steps by an additive amount and can, under stylized assumptions, offset depth-induced decay in $\gamma$.

The main conclusion is therefore modest but useful. Search, decomposition, abstention, and tool use are not separate tricks. They are local moves inside the same free-energy-controlled random tree. The empirical challenge is to estimate the relevant values and taxes well enough that the good basin remains accessible as the reasoning horizon grows.

---

## References

{% bibliography --cited %}
