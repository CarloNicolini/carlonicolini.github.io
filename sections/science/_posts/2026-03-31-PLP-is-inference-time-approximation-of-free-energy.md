---
layout: post
title: PLP is inference-time approximation of free energy
date: 2026-03-31
published: true
categories: science
---

## Approximate sampling and inference in LLMs

In the previous note on Probabilistic Language Programming and energy-based models, I argued that there is a deep analogy between LLM scaffolds and verifier-reweighted distributions {% cite blondel2025autoregressive %}.
After sitting on that connection for a few more days, I think the sharper statement is stronger, cleaner, and much more useful:

> PLP is inference-time approximation of free energy.

The central object of [PLP is the fundamental equation]({% link sections/science/_posts/2026-03-01-Probabilistic-Language-Programming.md %}):

\begin{equation}
p_{\mathcal{D}} \propto q_{\mathcal{D}}(\tau) \Phi(\tau)
\end{equation}

What does this mean in practice?
A scaffold does not answer from a single monolithic law.
It first samples traces from a proposal distribution induced by the deployed model, and then reshapes that mass with potentials supplied by verifiers, judges, or heuristics.

To make the rest precise, let us start from the basic PLP objects.
Fix a deployment setup $\mathcal{D}$ (model, decoding hyperparameters etc.), an input prompt $x$, and a complete execution trace $\tau$.
In PLP, the forward execution of the workflow induces a proposal distribution $q_{\mathcal{D}}(\tau \mid x)$ and the verifier, judge, or preference specification induces a nonnegative potential $\Phi(\tau,x)$.
The semantic target is

\begin{equation}
p_{\mathcal{D}}(\tau \mid x) = \frac{q_{\mathcal{D}}(\tau \mid x)\Phi(\tau,x)}{Z_{\mathcal{D}}(x)}, \qquad Z_{\mathcal{D}}(x)=\sum_{\tau} q_{\mathcal{D}}(\tau \mid x)\Phi(\tau,x).
\end{equation}

where $Z_{\mathcal{D}}(x)$ is the partition function, namely the total verifier-weighted mass over all traces at fixed input and deployment state.

Now we define:

\begin{equation}
p_{\mathrm{ref}}(\tau \mid x) := q_{\mathcal{D}}(\tau \mid x), \qquad R(\tau,x) := \log \Phi(\tau,x),
\end{equation}

with the usual convention $R(\tau,x)=-\infty$ when $\Phi(\tau,x)=0$.

Then the same target becomes

$$
p_{\mathcal{D}}(\tau \mid x)
=
\frac{p_{\mathrm{ref}}(\tau \mid x)\exp(R(\tau,x))}
{\sum_{\tau'} p_{\mathrm{ref}}(\tau' \mid x)\exp(R(\tau',x))}.
$$

This is exactly the reference-measure energy-based form that appears in KL-regularized maximum-entropy reinforcement learning and in the recent ARM/EBM equivalence of Blondel et al. {% cite blondel2025autoregressive %}.

So the PLP proposal is not merely "similar" to the reference model.
It is the reference measure.
And the PLP potential is not merely "like" a reward.
Its logarithm is the additive energy correction.

The central intractable object that any prompt engineer is implicitly working with is the partition function:

$$
Z_{\mathcal{D}}(x)=\sum_{\tau} q_{\mathcal{D}}(\tau \mid x)\Phi(\tau,x),
$$

or, more precisely, its logarithm.
Depending on convention, this object can be read as a log-evidence, a soft value, or as minus a free-energy objective.
I will keep the $\log Z$ sign convention throughout, because it is the natural one for search and reweighting.
Any prompting technique is trying to approximate it.

This is the core conceptual jump between post-training alignment and inference-time compute.
When we deploy a scaffold, we are not invoking a mysterious faculty of "reasoning" or treating the model as an anthropomorphic oracle.
We are approximating, at inference time, a log-partition over future traces that the raw autoregressive policy cannot cheaply marginalize in one forward pass.

<figure>
<img src="/static/postfigures/inference_time_reweighting.svg" alt="inference_time_reweighting">
<figcaption>
<strong>Figure 1: Inference-Time Trace Reweighting.</strong>
<strong>(Left)</strong> The raw autoregressive policy induces a broad, unconstrained proposal distribution over reasoning traces $q(\tau \mid x)$ branching from an initial prompt $x$.
<strong>(Center)</strong> A verifier, judge, or heuristic defines a non-negative potential field $\Phi(\tau, x)$ (orange), smoothly warping the energy landscape of available paths and highlighting promising basins.
<strong>(Right)</strong> The normalized semantic target distribution $p(\tau \mid x)$. By applying the inference-time scaffold, probability mass (represented by line thickness and color intensity) is shifted away from dead ends and concentrated onto a smaller subset of high-value continuations.
</figcaption>
</figure>

## The proposal is the reference measure

This exact rewriting clarifies the relation between post-training and inference-time engineering.

At training time, one tries to distill the verifier-reweighted target directly into the model weights.
At inference time, PLP keeps the proposal fixed and approximates the same reweighted target procedurally by sampling, branching, judging, filtering, and resampling.

The two views are therefore not competing stories.
They are two computational routes toward the same normalized distribution.

One route is:

$$
\text{change the weights so that } q_{\theta} \approx p_{\mathcal{D}}.
$$

The other is:

$$
\text{keep } q_{\mathcal{D}} \text{ as the proposal and approximate } p_{\mathcal{D}} \text{ at runtime}.
$$

This makes the scope of PLP much clearer.
It is the semantics-first theory of what to do when the target is known only through a potential and the proposal is accessible mainly through a sampling oracle.
In other words, PLP is the runtime side of the same mathematics that post-training methods try to absorb into parameters.

There is also an important caveat here.
If the potential $\Phi$ is produced by an imperfect LLM judge, then the resulting free-energy landscape is judge-relative, not necessarily truth-relative {% cite lee2025judge %}.
The geometry is still real, but it is the geometry of the deployed verifier.
This matters a lot.
An imperfect judge does not merely add noise to selection.
It warps the energy landscape itself.

## A cautious bridge to Friston and active inference

At this point it is tempting to import Friston's free energy principle wholesale.
I think a narrower claim is both clearer and more defensible.
In the active-inference literature, variational free energy is introduced as a bound on surprise, or equivalently on negative log evidence, under an explicit generative model together with an approximate posterior over hidden states {% cite friston2010free friston2012active %}.
In PLP, by contrast, the object

$$
Z(s)=\sum_{\tau \succ s} q_{\mathcal{D}}(\tau \mid s)\Phi(\tau),
\qquad
V(s)=\log Z(s),
$$

is an exact continuation log-partition under a verifier-reweighted trace law.

So I do not want to claim that PLP literally instantiates the full biological program of the free energy principle.
The weaker statement is the useful one:
the same variational geometry reappears in a runtime systems setting.
A scaffold has a proposal, receives evidence through potentials, and tries to estimate how much good mass remains downstream of a prefix.

<figure>
<table style="font-size:0.88em; width:100%; border-collapse: collapse;">
  <caption style="caption-side: bottom; padding-top: 8px; font-size:0.95em; color:#444;">
    <strong>Table 1.</strong> The same formal structure viewed from three literatures. The PLP and ARM/EBM columns are direct correspondences. The Friston column is an analogy, with the usual sign-convention caveat: Friston minimizes free energy, whereas here I work with the corresponding log-evidence or soft-value quantity to be maximized.
  </caption>
  <thead>
    <tr style="border-top: 2px solid #444; border-bottom: 2px solid #444;">
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px; text-align: left;">view</th>
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px; text-align: left;">base law</th>
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px; text-align: left;">correction or evidence term</th>
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px; text-align: left;">state scalar</th>
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px; text-align: left;">operational meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-top:1px solid #ddd; border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>PLP</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">proposal $q_{\mathcal{D}}(\tau \mid s)$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">potential $\Phi(\tau)$ or energy correction $R=\log \Phi$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">$V(s)=\log \sum_{\tau \succ s} q_{\mathcal{D}}(\tau \mid s)\Phi(\tau)$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">future verifier-weighted continuation mass</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>ARM/EBM</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">reference measure or local policy</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">sequence reward / energy</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">soft value $V_q(s)$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">future summary that makes local logits look ahead {% cite blondel2025autoregressive %}</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>active inference</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">prior or generative model</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">likelihood / sensory evidence</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">$-F$ or log evidence, depending on sign convention</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">quantity whose optimization reduces surprise {% cite friston2010free friston2012active %}</td>
    </tr>
  </tbody>
</table>
</figure>

Read this way, a scaffold that branches, calls tools, or asks a verifier for intermediate feedback is not merely producing more text.
It is also gathering additional evidence about which futures deserve mass.
That is close in spirit to active inference, where action and perception both participate in free-energy reduction {% cite friston2012active %}.
Still, the sensible claim is the algorithmic one:
runtime scaffolds can be interpreted as engineered active-inference-like loops over traces, not as evidence that current LLM systems realize the full neuroscientific theory.

<figure>
<table style="font-size:0.88em; width:100%; border-collapse: collapse;">
  <caption style="caption-side: bottom; padding-top: 8px; font-size:0.95em; color:#444;">
    <strong>Table 2.</strong> A reviewer-style version of the claim. The most useful connection is mathematical and algorithmic, not anthropomorphic.
  </caption>
  <thead>
    <tr style="border-top: 2px solid #444; border-bottom: 2px solid #444;">
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px; text-align: left;">claim</th>
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px; text-align: left;">status</th>
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px; text-align: left;">why</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-top:1px solid #ddd; border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">PLP continuation values and ARM soft values are the same sort of log-partition object.</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>solid</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Both are future log-sums over continuations under a reweighted trace law.</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">$V(s)$ is usefully comparable to evidence or minus free energy in Friston's sense.</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>plausible</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">The comparison is structurally right, but the interpretation depends on sign conventions and on how explicit the generative model is.</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Search, tool use, and verifier queries can be read as engineered active-inference steps.</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>useful interpretation</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">They gather additional evidence and reallocate mass over futures instead of trusting one open-loop rollout.</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Current LLM scaffolds therefore validate the full free energy principle as a theory of cognition.</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>too strong</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">The formal analogy is real, but the biological and philosophical commitments of the full theory go well beyond the runtime mechanics discussed here.</td>
    </tr>
  </tbody>
</table>
</figure>

## What the `factor` primitive is really estimating

The new paper by Blondel et al. shows that local autoregressive logits must absorb a future-looking soft value term {% cite blondel2025autoregressive %}.
To avoid colliding with the PLP proposal notation $q_{\mathcal{D}}$, let me call that local quantity $Q(s,y)$ instead of $q(s,y)$.

For a trace prefix or state $s$, define the future continuation partition

$$
Z(s)
:=
\sum_{\tau \succ s} q_{\mathcal{D}}(\tau \mid s)\Phi(\tau),
$$

where the sum runs over all complete future continuations extending the current prefix.
Then define the continuation value:

$$
V(s) := \log Z(s).
$$

which is the exact prefix free energy.

Now the meaning of the PLP `factor` primitive becomes much sharper.
Whenever we score a partial chain of thought, a partial program, a partial proof sketch, or an intermediate plan, we are not really trying to estimate "local goodness" in isolation.
We are trying to estimate how much **future verifier-weighted mass** remains reachable from that prefix.

That is why simple local fluency is often useless for hard tasks.
A prefix can look elegant and still lead into a dead end.
Conversely, a clumsy-looking prefix can be extremely valuable if it opens a broad basin of correct continuations.

In this sense, `factor` is best understood as a runtime surrogate for continuation free energy.
Tree-of-Thoughts, self-consistency, Reflexion, self-backtracking, and many other scaffolds {% cite wang2022self %} {% cite yao2023tree %} {% cite shinn2023reflexion %} {% cite yang2025selfbacktracking %} are all different numerical schemes for approximating the same intractable object:

$$
V(s)=\log \sum_{\tau \succ s} q_{\mathcal{D}}(\tau \mid s)\Phi(\tau).
$$

<figure>
  <img src="/static/postfigures/local_decision.svg" alt="Local score plus continuation free energy" style="width:70%; display:block; margin: 0 auto; margin-bottom: 0.5em;"/>
  <figcaption>
    <strong>Figure 2.</strong> A local decision only becomes meaningful once it is augmented by the free energy of its downstream subtree. The practical role of runtime scaffolds is to estimate that future mass better than plain next-token decoding can.
  </figcaption>
</figure>

This is, I think, one of the first real low-hanging fruits.
It suggests that we should stop describing intermediate heuristics as vague "critics" and instead ask a very concrete question:

> How good is this heuristic as an estimator of continuation free energy?

That framing immediately gives us something measurable, comparable, and optimizable.

## Why we should not `factor` by raw free energy at every step

In the previous post I asked, half provocatively, why we do not simply `factor` all samples by the future value term.
The answer is subtle and useful.

If we repeatedly add the raw continuation value $V(s_t)$ at many intermediate steps, we generally **double count** future mass.
A long trace would then accumulate multiple copies of essentially the same downstream partition.
That changes the target in an uncontrolled way.

The right object is not raw future value, but a **telescoping shaping term**.
Let $\Psi(s)$ be a heuristic potential on prefixes.
Then the semantics-preserving way to inject it is

$$
r'(s_t,y_t)
=
r(s_t,y_t) + \Psi(s_{t+1}) - \Psi(s_t),
$$

so that along a full trace

$$
\sum_t r'(s_t,y_t)
=
\sum_t r(s_t,y_t) + \Psi(s_T)-\Psi(s_0).
$$

The extra terms telescope.

This matters because it tells us how to guide search without repeatedly rewarding the same future basin over and over again.
In reinforcement learning this is the logic of potential-based shaping.
In PLP it gives a principled answer to how one should place soft factors on intermediate states.

This is the second low-hanging fruit.
PLP should probably distinguish between two different uses of `factor`:

1. **Target-defining factors**, which really modify the semantic target.
2. **Shaping factors**, which are introduced only to improve inference and should telescope or otherwise preserve the intended target up to controllable boundary terms.

That distinction is mathematically clean and practically important.

## A Bellman-style support gap

In the PLP paper, the support gap is defined at the level of completed outputs.
That is already useful.
But the ARM/EBM connection suggests a sharper diagnostic at the level of prefixes.

The most important failures of greedy decoding often happen *before* the final answer is out of reach.
They happen when the model underestimates the future value of a promising prefix and therefore never enters the right basin.

This suggests defining a prefix-level discrepancy such as

$$
\Delta_V(s) := V^\star(s) - \widehat{V}(s),
$$

where $V^\star(s)$ is the ideal continuation free energy under the semantic target and $\widehat{V}(s)$ is the value implicitly assigned by the deployed heuristic, judge, or local policy.

This is not the full Friston free-energy functional, because I have not specified an explicit variational family over hidden states.
But it is the right local error in the same geometry:
the deployed system underestimates the amount of evidence still reachable downstream of the prefix {% cite friston2010free %}.

Large positive $\Delta_V(s)$ means something very specific:
the prefix sits above a rich region of good continuations, but the deployed system does not see it.

This is not merely an output-level support problem.
It is a **Bellman support gap**.
The scaffold fails because it discards a promising prefix too early, before the good mass can be unfolded.

That gives a third low-hanging fruit.
Instead of measuring only whether the correct answer appears in samples, we should also measure whether good prefixes are being undervalued.
This would tell us much more directly when beam search, tree search, or verifier-guided branching are worth the extra compute.

## Tempered targets and annealing schedules

Another immediate consequence is that PLP admits a very natural temperature family.
Given the same proposal $q_{\mathcal{D}}$ and potential $\Phi$, define

$$
p_\beta(\tau \mid x)
\propto
q_{\mathcal{D}}(\tau \mid x)\Phi(\tau,x)^\beta,
\qquad
0 \le \beta \le 1.
$$

At $\beta=0$ we recover the raw proposal.
At $\beta=1$ we recover the semantic target.
Intermediate $\beta$ values define softened bridges between exploration and strict verification.

This gives a clean interpretation of annealed search, progressive filtering, verifier ramp-up, and soft-to-hard planning schedules.
Population methods such as importance weighting, sequential Monte Carlo, or twisted SMC {% cite zhao2024probabilistic %} can then be read as procedures that move mass through a sequence of tempered targets {% cite tokdar2010importance loula2025syntactic zhao2024probabilistic %}.

This also gives a principled language for iterative answer refinement.
Progressive-Hint Prompting and later work on refined answer distributions can be read as sequential procedures that repeatedly sharpen an empirical answer law rather than trusting a single first-pass sample {% cite zheng2023progressive pal2024refining %}.

In practice, this may be one of the most useful low-hanging fruits of all.
Many tree-search and multi-sample workflows fail because they apply an overly sharp verifier too early.
The result is weight collapse.
A small number of trajectories dominate before the system has explored enough of the space.

The free-energy perspective suggests a principled fix:
start from a high-entropy, low-$\beta$ regime and only gradually sharpen the potential.
That turns "temperature schedules" from ad hoc prompting folklore into a legitimate family of intermediate distributions.

## Replica thinking and the geometry of reasoning paths

The most speculative, but also the most exciting, consequence comes from the replica trick perspective, a nice theoretical trick that statistical physicists use very often to perform calculations.

For a prefix tokens sequence $\mathbf{s}$, let's write the log partition function as:

\begin{equation}
V(s)=\log Z(s).
\end{equation}

It turns out that formally, one can rewrite it with the replica trick as

\begin{equation}
V(s) = \lim_{n\to 0}\frac{Z(s)^n-1}{n}.
\end{equation}

For integer $n$, the quantity $Z(s)^n$ is a sum over $n$ replicated future continuations.
In PLP language, this looks almost natural: it is a `plate(n)` over future reasoning traces conditioned on the same prefix.

Of course, the formal limit $n\to 0$ is not yet a practical inference algorithm. But finite replicas are already illuminating.

Suppose we draw two independent continuations from the normalized continuation law downstream of $s$. The probability that the two draws land in the same future branch is:

\begin{equation}
C_2(s) := \sum_{\tau \succ s} p(\tau \mid s)^2.
\end{equation}

and its inverse law

\begin{equation}
N_{\mathrm{basins}}(s):=\frac{1}{C_2(s)}
\end{equation}

can be read as an effective number of continuation basins.

This quantity has an immediate interpretation.
If $N_{\mathrm{basins}}(s)\approx 1$, then most samples are collapsing into the same hidden plan.
Self-consistency will produce many surface variations of the same mistake, since after-all the internal model force field described by the continuation function is very similar!
Instead when $N_{\mathrm{basins}}(s)$ is large, then multiple qualitatively distinct reasoning paths contribute to the same high-value region, and extra sampling can genuinely buy new evidence.

<figure>
<img src="/static/postfigures/replica_trick_plp.svg" alt="Single versus multiple reasoning basins">
<figcaption>
<strong>Figure 3.</strong> A single verbalized path may give the illusion of diversity while remaining trapped in one hidden basin. Finite-replica thinking asks a deeper question: how many distinct high-mass continuation families are actually contributing downstream of a prefix?
</figcaption>
</figure>

This connects beautifully to the dependence analysis already present in PLP.
The pairwise correlation $\rho$ and the effective sample size $K_{\mathrm{eff}}$ measure output-level dependence.
Replica overlap suggests a more geometric, prefix-level version of the same story.

That is the fourth low-hanging fruit:
use replicated reasoning traces not only to improve answers, but also to **measure the ruggedness of the continuation landscape itself**.

If two or more replicas keep collapsing to the same basin, the problem is not a lack of samples.
It is a lack of inferential diversity.
That is a completely different failure mode, and it calls for different interventions: different decompositions, different retrieved evidence, different latent strategies, or different verifier placements.

### Estimating $C_2(s)$ in practice

At this point a natural practical question appears:

> How does one actually estimate $C_2(s)$ for a prefix $s$?

The answer becomes simple once we expand the normalized continuation law explicitly.
Downstream of a prefix $s$, PLP defines

$$
p(\tau \mid s)
=
\frac{q_{\mathcal{D}}(\tau \mid s)\Phi(\tau)}{Z(s)},
\qquad
Z(s)=\sum_{\tau \succ s} q_{\mathcal{D}}(\tau \mid s)\Phi(\tau).
$$

Therefore

$$
C_2(s)
=
\sum_{\tau \succ s} p(\tau \mid s)^2
=
\frac{\sum_{\tau \succ s} q_{\mathcal{D}}(\tau \mid s)^2 \Phi(\tau)^2}{Z(s)^2}.
$$

So $C_2(s)$ is the second moment of the normalized continuation law.
Equivalently, it is the probability that two independent replicas drawn from the target downstream of $s$ land on the same continuation.
In statistical-physics language it is an inverse participation ratio, and in information-theoretic language it is the order-2 collision probability:

$$
H_2(s):=-\log C_2(s),
\qquad
N_{\mathrm{basins}}(s)=e^{H_2(s)}=\frac{1}{C_2(s)}.
$$

This identity is useful because it immediately suggests several estimators, depending on what one can sample and what one can evaluate.

1. **Exact enumeration on tiny continuation trees.**

If the continuation space below $s$ is small enough, one can compute $p(\tau \mid s)$ exactly and then sum the squares directly:

$$
C_2^{\mathrm{exact}}(s)
=
\sum_{\tau \succ s} p(\tau \mid s)^2.
$$

This is mostly a toy-regime diagnostic, but it is conceptually important because it gives the quantity we are trying to approximate in larger systems.

1. **Replica collision estimator when we can sample approximately from the target.**

Suppose the scaffold already produces approximate samples from the target continuation law $p(\cdot \mid s)$, for instance through rejection, resampling, tree search, or an SMC-style procedure.
If we draw $M$ independent replicas $\tau^{(1)},\ldots,\tau^{(M)} \sim p(\cdot \mid s)$, then a natural estimator is the empirical collision rate

$$
\widehat{C}_2^{\mathrm{coll}}(s)
:=
\frac{1}{M(M-1)}
\sum_{i \neq j}
\mathbf{1}\!\left\{\tau^{(i)}=\tau^{(j)}\right\}.
$$

This estimator is directly aligned with the definition of $C_2$ as a two-replica overlap probability.
In practice, for long text traces, exact full-trace collisions are often too rare to be informative, so one usually coarse-grains to a more semantic notion of sameness.

1. **Importance-weighted estimation when we only sample from the proposal.**

Often we do not have direct samples from $p(\cdot \mid s)$; we only know how to sample $\tau^{(i)} \sim q_{\mathcal{D}}(\cdot \mid s)$ and score them with $\Phi$.
Let

$$
w_i := \Phi(\tau^{(i)}),
\qquad
\widehat{Z}(s):=\frac{1}{N}\sum_{i=1}^N w_i.
$$

Then, using the identity above, a natural Monte Carlo estimator is

$$
\widehat{C}_2^{\mathrm{IS}}(s)
:=
\frac{\frac{1}{N}\sum_{i=1}^N q_{\mathcal{D}}(\tau^{(i)} \mid s)\,w_i^2}
{\widehat{Z}(s)^2}.
$$

The presence of the extra factor $q_{\mathcal{D}}(\tau^{(i)} \mid s)$ is not a typo: it comes from the fact that the numerator is an expectation under the proposal of $q_{\mathcal{D}}(\tau \mid s)\Phi(\tau)^2$.
This form is therefore most useful when the scaffold can evaluate its own trace probability, for example as a product of token probabilities and routing decisions along the trace.

1. **Particle or resampling estimator from weighted continuations.**

In many practical systems one already has a weighted cloud of continuations, for instance from beam search with scores, self-consistency with verifier weights, or SMC particles.
If we define normalized weights

$$
\bar{w}_i := \frac{w_i}{\sum_j w_j},
$$

and optionally assign each trace to a basin label $b(\tau_i)$, then the empirical basin mass is

$$
\widehat{p}_b(s)
:=
\sum_{i:\,b(\tau_i)=b}\bar{w}_i,
$$

which yields the plug-in estimator

$$
\widehat{C}_2^{\mathrm{basin}}(s)
:=
\sum_b \widehat{p}_b(s)^2,
\qquad
\widehat{N}_{\mathrm{basins}}(s)
:=
\frac{1}{\widehat{C}_2^{\mathrm{basin}}(s)}.
$$

If every particle is treated as its own basin, this becomes

$$
\widehat{C}_2(s)=\sum_i \bar{w}_i^2,
\qquad
\widehat{N}_{\mathrm{basins}}(s)=\frac{1}{\sum_i \bar{w}_i^2},
$$

which is exactly the familiar inverse-weight concentration statistic used to define effective sample size in particle methods.
Seen this way, the replica-overlap picture and the particle-inference picture are not different ideas at all.
They are the same second-moment geometry viewed from two angles.

There is, however, an important subtlety.
The formula

$$
C_2(s)=\sum_{\tau \succ s} p(\tau \mid s)^2
$$

is defined over complete future traces $\tau$.
For language models, that can be too fine-grained.
Two traces may differ in wording while still instantiating the same hidden plan, the same proof strategy, the same decomposition skeleton, or the same tool-use pattern.
If our real concern is "how many qualitatively distinct reasoning families exist downstream of $s$?", then we should first define a basin map $b(\tau)$ and estimate instead

$$
C_2^{\mathrm{basin}}(s)
:=
\sum_b \mathbb{P}(b(\tau)=b \mid s)^2.
$$

This is usually the quantity that matches the geometric language of reasoning basins.
In practice, the basin map could be defined by final answer equivalence, by latent plan templates, by retrieved-evidence sets, by decomposition trees, or even by clustering rationales in an embedding space.

That caveat matters because exact trace overlap and basin overlap answer different questions.
Exact overlap asks whether the system literally repeats the same trajectory.
Basin overlap asks whether the system keeps revisiting the same region of reasoning space.
For diagnosing lack of inferential diversity, the second question is often the one we actually care about.

Finally, one should remember that $C_2(s)$ is always defined relative to the deployed target distribution.
If the potential $\Phi$ comes from an imperfect judge, then the measured basins are judge-relative basins, not necessarily truth-relative ones.
But that is not a defect of the formalism.
It is the correct statement of what the deployed scaffold believes the future landscape looks like.

## What this says about prompting

Once seen through this lens, many prompting techniques become much easier to classify.

**Chain-of-thought** does not magically add "reasoning" as an ontologically new faculty.
It introduces a latent sequential state, allowing the model to externalize part of the free-energy computation into the token stream.
That interpretation is now explicit in work that treats rationales as latent variables and optimizes answer likelihood by marginalizing over them {% cite phan2023training %}, and in work that casts CoT adaptation more broadly as amortized inference over intractable posteriors {% cite hu2024amortizing %}.
This also puts a clear bound on what one should expect from pure chain-of-thought at inference time:
externalizing rationales can help the model access structure that was already latent in its training distribution, but it does not manufacture arbitrary new competence.
The method is strongest when training has already shaped a useful high-reward landscape over latent traces, and correspondingly weaker as a route to robustly out-of-distribution reasoning.

**Self-consistency** does not magically uncover truth by social consensus.
It samples multiple reasoning paths and marginalizes them at the answer level {% cite wang2022self %}.
Later variants such as Progressive-Hint Prompting and refined answer distributions can be read as more deliberate ways of refining that sampled answer distribution over multiple rounds {% cite zheng2023progressive %} {% cite pal2024refining %}.

**Tree-of-Thoughts** and related tree-search methods do not create intelligence from branching alone.
They allocate compute across prefixes, attach heuristic or uncertainty estimates to partial states, and search over the resulting frontier {% cite yao2023tree %} {% cite mo2023uncertain %} {% cite zhou2024lats %}.
In older approximate-inference language, this is closer to Monte Carlo tree search with value guidance than to a new cognitive primitive {% cite buesing2020approximate %}.

**Reflexion and self-backtracking** do not merely add self-awareness.
They repeatedly revise the proposal so that more mass moves toward regions with better downstream verifier-weighted continuation mass {% cite shinn2023reflexion %} {% cite yang2025selfbacktracking %}.

Finally, SMC-style steering methods make the probabilistic interpretation explicit.
They treat LM control as sampling from an unnormalized target distribution and use learned twist or future-value estimates to guide particles toward high-mass regions {% cite zhao2024probabilistic %} {% cite loula2025syntactic %}.

In short:

> Prompting techniques are numerical methods for approximating continuation free energy under finite compute.

That is a much less romantic sentence than the usual discourse around agents and reasoning.
It is also, I think, much closer to the truth.
And it is the level at which the connection to Friston seems justified:
a statement about approximate inference over hidden future traces, not a grand theory of cognition {% cite friston2010free friston2012active meyerson2025position %}.

## The big picture

The sharpest version of the story is now the following.

Autoregressive models can behave as if they plan ahead only when their local decisions already contain a compressed summary of the future partition over continuations.
When that summary is imperfect, inference-time scaffolds step in:
they numerically approximate the missing continuation values by spending additional runtime compute and by incorporating extra evidence from search, tools, and verification.
That is the limited but useful sense in which they resemble active inference.

This is why the right question is not "do agents reason?" or even "does chain-of-thought work?"
The right question is:

> Which inference-time procedure best approximates the verifier-weighted free energy of future traces under a finite compute budget?

That, to me, is the real systems interpretation of PLP.
And it is also why the next generation of scaffolds should probably be evaluated less like personalities and more like numerical schemes.

---

## References

{% bibliography --cited %}
