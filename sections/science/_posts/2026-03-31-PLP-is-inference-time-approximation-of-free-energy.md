---
layout: post
title: PLP is inference-time approximation of free energy
description: "PLP as inference-time free energy / log-partition over traces."
date: 2026-03-31
published: true
categories:
  - science
  - language-physics
---

## Approximate sampling and inference in LLMs

In the previous note on [Probabilistic Language Programming]({% link sections/science/_posts/2026-03-01-Probabilistic-Language-Programming.md %}) and energy-based models, I argued that there is a deep analogy between LLM scaffolds and verifier-reweighted distributions.
The sharper statement is simple and useful:

> PLP is inference-time approximation of the free energy.

The central object of [PLP is the fundamental equation]({% link sections/science/_posts/2026-03-01-Probabilistic-Language-Programming.md %}) that we reproduce via a programmatic scaffold building a trace $\tau$, arriving at the relation:

\begin{equation}
p_{\mathcal{D}}(\tau \mid x) \propto \pi_{\mathcal{D}}(\tau \mid x)\,\Phi(\tau,x).
\end{equation}

A scaffold is a way to first sample traces from a proposal distribution $\pi_{\mathcal{D}}(\cdot \mid x)$ induced by the deployed model, and then reshape that mass with potentials supplied by verifiers, judges, or heuristics.

To make the rest precise, let us start from the basic PLP objects.
Fix a deployment setup $\mathcal{D}$ (model, decoding hyperparameters etc.), an input prompt $x$, and a complete execution trace $\tau$.
In PLP, the forward execution of the workflow induces a proposal distribution $\pi_{\mathcal{D}}(\tau \mid x)$ and the verifier, judge, or preference specification induces a nonnegative potential $\Phi(\tau,x)$.
When the prompt $x$ is fixed, I will often write $\Phi(\tau)$ instead of $\Phi(\tau,x)$ to shorten formulas.

The semantic target is hence modeled as the product of two competing *forces*: the proposal force $\pi_{\mathcal{D}}(\tau \mid x)$ pushing the exploration of different trajectories in the semantic space, and the *verifier force* $\Phi(\tau,x)$ keeping the proposal on track with a warp signal:

\begin{equation}
p_{\mathcal{D}}(\tau \mid x) = \frac{\pi_{\mathcal{D}}(\tau \mid x)\Phi(\tau,x)}{Z_{\mathcal{D}}(x)} \quad Z_{\mathcal{D}}(x)=\sum_{\tau} \pi_{\mathcal{D}}(\tau \mid x)\Phi(\tau,x) \label{eq:fundamental}\tag{1}.
\end{equation}

The normalization factor $Z_{\mathcal{D}}(x)$ is the partition function, namely the total verifier-weighted mass over all traces at fixed input and deployment state.

If we stick to the soft reinforcement learning literature we could now define the reference distribution (proposal) and the *global reward* $R$ as:

\begin{equation}
p_{\mathrm{ref}}(\tau \mid x) := \pi_{\mathcal{D}}(\tau \mid x), \qquad R(\tau,x) := \log \Phi(\tau,x),
\end{equation}

with the usual convention $R(\tau,x)=-\infty$ when $\Phi(\tau,x)=0$.

The same semantic target becomes a softargmax distribution over the reward weighted proposals, a convention that is already well defined in many soft reinforcement learning studies {% cite levine2018reinforcement blondel2025autoregressive %}:

\begin{equation}
p_{\mathcal{D}} (\tau \mid x) = \frac{p_{\mathrm{ref}}(\tau \mid x)\exp(R(\tau,x))} {\sum_{\tau'} p_{\mathrm{ref}}(\tau' \mid x)\exp(R(\tau',x))}.
\end{equation}

This is exactly the reference-measure energy-based form that appears in KL-regularized maximum-entropy reinforcement learning and in the recent ARM/EBM equivalence of Blondel et al. {% cite blondel2025autoregressive %} when instead of simply the answer $\mathbf{y}$, we include the trace $\tau$ that naturally includes the possible scaffold architectures.

So the PLP proposal is the reference model used for proposal exploration in the sequences landscape (as in energy based models) and  the PLP potential is the exponentiated version of the additive energy correction, namely the feedback mechanism that could drive the exploration of better solutions toward the semantic target.

Hence, the central intractable object that any prompt engineer is unknowingly working with is the partition function:

$$
Z_{\mathcal{D}}(x)=\sum_{\tau} \pi_{\mathcal{D}}(\tau \mid x)\Phi(\tau,x) \tag{2},
$$

or, put more precisely, its logarithm hence the free energy!

<figure>
<img src="/static/postfigures/multiple_scaffolds2.svg" alt="scaffold_integration">
<figcaption>
<strong>Figure 1: Integration over traces.</strong> Approximating the continuation partition function
</figcaption>
</figure>

There is a difference in the equation above between integrating over the trace space and integrating over the string space.
The trace space is a richer and vaster environment that one could, at least in theory, optimize over.
Over the last years, people as been involuntarily integrating the trace space in search of better and better approximation of the (finite but very large) sum $\sum_\tau (\cdot)$ above!

Depending on convention, this object can be read as a *log-evidence*, a *soft value*, or as *minus a free-energy* objective.
I will keep the $\log Z_{\mathcal{D}}(x)$ sign convention throughout, because it is the natural one for search and reweighting.
Remember: any prompting technique or programmatic scaffold is just a way to approximate it.

This is the core conceptual jump between post-training alignment and inference-time compute.
When we deploy a scaffold, we are not invoking a mysterious faculty of "reasoning" or treating the model as an anthropomorphic oracle.
We are approximating, at inference time, a log-partition over future traces that the raw autoregressive policy cannot cheaply marginalize in one forward pass.

<figure>
<img src="/static/postfigures/inference_time_reweighting.svg" alt="inference_time_reweighting">
<figcaption>
<strong>Figure 1: Inference-Time Trace Reweighting.</strong>
<strong>(Left)</strong> The raw autoregressive policy induces a broad, unconstrained proposal distribution over reasoning traces. I write this baseline law as $q(\tau \mid x)$ to distinguish it from the deployed scaffold proposal $\pi_{\mathcal{D}}(\tau \mid x)$.
<strong>(Center)</strong> A verifier, judge, or heuristic defines a non-negative potential field $\Phi(\tau, x)$ (orange), smoothly warping the energy landscape of available paths and highlighting promising basins.
<strong>(Right)</strong> The normalized semantic target distribution $p(\tau \mid x)$. By applying the correct inference-time scaffold, probability mass (represented by line thickness and color intensity) is shifted away from dead ends and concentrated onto a smaller subset of high-value continuations.
</figcaption>
</figure>

> When we deploy a scaffold, we are not invoking a mysterious faculty of "reasoning" or treating the model as an anthropomorphic oracle. We are approximating, at inference time, a log-partition over future traces that the raw autoregressive policy cannot cheaply marginalize in one forward pass.

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

Here $q_{\theta}$ denotes a parametric model distribution over traces (or over answers) with parameters $\theta$.

The other is:

$$
\text{keep } \pi_{\mathcal{D}} \text{ as the proposal and approximate } p_{\mathcal{D}} \text{ at runtime}.
$$

This makes the scope of PLP much clearer.
It is the semantics-first theory of what to do when the target is known only through a potential and the proposal is accessible mainly through a sampling oracle.
In other words, PLP is the runtime side of the same mathematics that post-training methods try to absorb into parameters.

There is also an important caveat here.
If the potential $\Phi$ is produced by an imperfect LLM judge, then the resulting free-energy landscape is judge-relative, not necessarily truth-relative {% cite lee2025judge %}: the geometry is still real, but it is the geometry of the deployed verifier.
Simply speaking, an imperfect judge is a process that warps the energy landscape itself.

## The closer bridge is path-integral control

At this point it is tempting to import Friston's free energy principle wholesale {% cite friston2010free %}.
I think there is a closer and cleaner bridge for the present argument: *Kappen's* path-integral view of stochastic optimal control {% cite kappen2005path %}.

For a class of noisy control problems with quadratic control cost, Kappen showed that the nonlinear Hamilton-Jacobi-Bellman equation can be linearized through a log transform of the cost-to-go.
Let $\xi$ denote a physical state and $t$ denote time in his continuous-time setup (this $\xi$ is not the prompt $x$ elsewhere in the note).
Let $\lambda>0$ denote the temperature parameter that appears in Kappen's log transform (it ties control cost to noise strength in his construction {% cite kappen2005path %}).
If $\Psi(\xi,t)$ denotes the forward diffusion partition function in that setting, then the optimal cost-to-go reads

$$
J(\xi,t) = -\lambda \log \Psi(\xi,t),
$$

so the control problem becomes a log-partition over future trajectories.

PLP has the same algebraic structure, but the state is a trace prefix.
Let $s$ denote such a prefix (a string state in the MDP picture).
Define the **continuation partition**

$$
Z(s)=\sum_{\tau \succ s} \pi_{\mathcal{D}}(\tau \mid s)\,\Phi(\tau),
\qquad
V(s)=\log Z(s),
$$

where $\tau \succ s$ means that the complete trace $\tau$ extends $s$, and $\pi_{\mathcal{D}}(\tau \mid s)$ is the conditional proposal law for those completions.

The PLP potential need not be a literal Boltzmann factor.
Earlier we wrote $R(\tau,x)=\log \Phi(\tau,x)$, so always $\Phi(\tau)=\exp(R(\tau))$ in log space.
To align PLP with Kappen's path-cost form, suppose in addition that we can write

$$
R(\tau)=-\frac{S(\tau)}{\lambda}
$$

for some nonnegative **path cost** functional $S(\tau)$ and a **temperature** $\lambda>0$.
Equivalently,

$$
\Phi(\tau)=\exp\!\left(-\frac{S(\tau)}{\lambda}\right).
$$

With that identification, the PLP continuation value $V(s)=\log Z(s)$ matches Kappen's log-partition structure up to sign and scale.
Writing $J_{\mathrm{PLP}}(s)$ for the corresponding cost-to-go under the same sign convention as $J(\xi,t)$,

$$
J_{\mathrm{PLP}}(s)=-\lambda\, V(s).
$$

The parameter $\lambda$ here is the same kind of object as Kappen's temperature: it sets the units that convert log-masses into costs.

This is the closest control-theoretic bridge in this post.
Both formalisms start from a reference law over futures, reweight those futures by an exponential score, and summarize the remaining downstream options in a log-partition.
The comparison to active inference remains useful, but it is a step further away from the runtime mechanics discussed here.

<figure>
<table style="font-size:0.88em; width:100%; border-collapse: collapse;">
  <caption style="caption-side: bottom; padding-top: 8px; font-size:0.95em; color:#444;">
    <strong>Table 1.</strong> The same formal structure viewed from four literatures. The Kappen row is the closest control-theoretic analogue for the present note. The Friston row remains an analogy, not an identity.
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
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">proposal $\pi_{\mathcal{D}}(\tau \mid s)$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">potential $\Phi(\tau)$ or energy correction $R=\log \Phi$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">$V(s)=\log \sum_{\tau \succ s} \pi_{\mathcal{D}}(\tau \mid s)\Phi(\tau)$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">future verifier-weighted continuation mass</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>path-integral control</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">uncontrolled diffusion or reference dynamics</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">path cost $S$ with weight $e^{-S/\lambda}$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">$J(\xi,t)=-\lambda \log \Psi(\xi,t)$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">stochastic cost-to-go under noise {% cite kappen2005path %}</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>ARM/EBM</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">reference measure or local policy</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">sequence reward / energy</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">soft value $V_q(s)$ under local policy $q$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">future summary that makes local logits look ahead {% cite blondel2025autoregressive %}</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>active inference</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">prior or generative model</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">likelihood / sensory evidence</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">$-F$ (variational free energy) or log evidence, depending on sign convention</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">quantity whose optimization reduces surprise {% cite friston2010free friston2012active %}</td>
    </tr>
  </tbody>
</table>
</figure>

Read this way, a scaffold that branches, calls tools, or queries a verifier is not merely producing more text.
It reallocates probability mass across future traces in much the same broad sense that a stochastic controller reallocates mass across future trajectories.
That is the level at which the analogy is strongest.

<!-- <figure>
<table style="font-size:0.88em; width:100%; border-collapse: collapse;">
  <caption style="caption-side: bottom; padding-top: 8px; font-size:0.95em; color:#444;">
    <strong>Table 2.</strong> A reviewer-style version of the claim. The useful connection is mathematical and algorithmic, not anthropomorphic.
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
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">PLP continuation values and Kappen's stochastic cost-to-go encode the same log-partition geometry under $\Phi=e^{-S/\lambda}$.</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>solid</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Both summarize verifier- or cost-weighted futures with a log-sum over continuations.</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
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
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Current LLM scaffolds therefore validate the full free energy principle as a theory of cognition.</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>too strong</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">The formal analogy is real, but the biological and philosophical commitments of the full theory go well beyond the runtime mechanics discussed here.</td>
    </tr>
  </tbody>
</table>
</figure> -->

## What the `factor` primitive is really estimating

The new paper by Blondel et al. shows that local autoregressive logits must absorb a future-looking soft value term {% cite blondel2025autoregressive %}.
To avoid colliding with the PLP proposal notation $\pi_{\mathcal{D}}$, let me call that local quantity $Q(s,y)$ instead of $q(s,y)$.
Here $s$ is again a trace prefix and $y$ is the next token (or decoded action) that extends $s$ by one step.

For a trace prefix or state $s$, the continuation partition is the $Z(s)$ introduced above:

$$
Z(s)
:=
\sum_{\tau \succ s} \pi_{\mathcal{D}}(\tau \mid s)\Phi(\tau),
$$

where the sum runs over all complete future continuations extending the current prefix.
The continuation value is

$$
V(s) := \log Z(s).
$$

This represents the exact prefix free energy at $s$. 
While this raw log-partition produces an extensive quantity that can suffer from length bias across traces of vastly different lengths, it establishes the correct geometric structure of the search problem. In agentic tool-use, this is typically replaced by an intensive operator like MellowMax to ensure scale-free comparisons, as we explore in [a subsequent post]({% link sections/science/_posts/2026-04-03-Mellowmax-doob-and-agentic-tool-use.md %}). 
Moreover, because pre-training acts as a backward dynamic programming pass, the autoregressive model caches this future value directly in its immediate logits. Evaluating the one-step soft value at inference time therefore does not strictly require expensive Monte Carlo rollouts; the forward pass simply reads the internalized global energy.

Now the meaning of the PLP `factor` primitive becomes much sharper.
Whenever we score a partial chain of thought, a partial program, a partial proof sketch, or an intermediate plan, we are not really trying to estimate "local goodness" in isolation.
We are trying to estimate how much **future verifier-weighted mass** remains reachable from that prefix.

That is why simple local fluency is often useless for hard tasks.
A prefix can look elegant and still lead into a dead end.
Conversely, a clumsy-looking prefix can be extremely valuable if it opens a broad basin of correct continuations.

In this sense, `factor` is best understood as a runtime surrogate for continuation free energy.
Tree-of-Thoughts, self-consistency, Reflexion, self-backtracking, and many other scaffolds {% cite wang2022self %} {% cite yao2023tree %} {% cite shinn2023reflexion %} {% cite yang2025selfbacktracking %} are all different numerical schemes for approximating the same intractable object:

$$
V(s)=\log \sum_{\tau \succ s} \pi_{\mathcal{D}}(\tau \mid s)\Phi(\tau).
$$

<figure>
  <img src="/static/postfigures/local_decision.svg" alt="Local score plus continuation free energy" style="width:70%; display:block; margin: 0 auto; margin-bottom: 0.5em;"/>
  <figcaption>
    <strong>Figure 2.</strong> A local decision only becomes meaningful once it is augmented by the free energy of its downstream subtree. The practical role of runtime scaffolds is to estimate that future mass better than plain next-token decoding can.
  </figcaption>
</figure>

This viewpoint turns a vague design question into a measurable one.
Rather than describing intermediate heuristics as vague "critics", we can ask a concrete question:

> How good is this heuristic as an estimator of continuation free energy?

That criterion is concrete enough to compare heuristics, train better surrogates, and evaluate search procedures on common ground.

## Why raw free energy should not be factored at every step

Index the unfolding trace by time steps $t=0,1,\ldots,T$.
Let $s_t$ denote the prefix after $t$ steps, let $y_t$ denote the token (or action) taken at step $t$, and let $r(s_t,y_t)$ denote any additive reward used in a reinforcement-learning view of the same trajectory.

If we repeatedly add the raw continuation value $V(s_t)$ at many intermediate steps, we generally **double count** future mass.
A long trace would then accumulate multiple copies of essentially the same downstream partition, and that would change the target in an uncontrolled way.

The right object is not raw future value, but a **telescoping shaping term**.
Let $G(s)$ be a heuristic **potential** on prefixes (I use $G$ here to avoid clashing with Kappen's partition notation $\Psi(\xi,t)$).
Then the semantics-preserving way to inject it is

$$
r'(s_t,y_t)
=
r(s_t,y_t) + G(s_{t+1}) - G(s_t),
$$

so that along a full trace

$$
\sum_t r'(s_t,y_t)
=
\sum_t r(s_t,y_t) + G(s_T)-G(s_0).
$$

The extra terms telescope.

This matters because it tells us how to guide search without repeatedly rewarding the same future basin over and over again.
In reinforcement learning this is the logic of potential-based shaping.
In PLP it gives a principled answer to how one should place soft factors on intermediate states.

This suggests a clean semantic distinction in PLP.
The `factor` primitive has two roles:

1. **Target-defining factors**, which really modify the semantic target.
2. **Shaping factors**, which are introduced only to improve inference and should telescope or otherwise preserve the intended target up to controllable boundary terms.

The distinction is mathematically clean and practically important.
It separates modeling choices from inference aids and makes it easier to see when a scaffold has changed the task itself.

## A Bellman-style support gap

In the PLP paper, the support gap is defined at the level of completed outputs.
That is useful, but the ARM/EBM connection suggests a sharper diagnostic at the level of prefixes.

Many failures of greedy decoding happen *before* the final answer becomes unreachable.
They begin when the system underestimates the future value of a promising prefix and therefore never enters the right basin.

This suggests the prefix-level discrepancy

$$
\Delta_V(s) := V^\star(s) - \widehat{V}(s),
$$

where $V^\star(s)$ is the ideal continuation free energy under the semantic target and $\widehat{V}(s)$ is the value implicitly assigned by the deployed heuristic, judge, or local policy.

This quantity measures a local value mismatch in the same variational geometry.
It asks whether the deployed system assigns enough mass to the good continuations that remain reachable from $s$.
In that sense, a large positive $\Delta_V(s)$ means that the prefix contains more downstream evidence than the system currently credits it with {% cite friston2010free %}.

That is the **Bellman support gap**.
The prefix lies above a rich continuation basin, but the deployed system fails to see it.
A scaffold can then discard a promising branch too early, before the good mass has time to unfold.

This perspective suggests a more informative diagnostic than answer-level accuracy alone.
Instead of asking only whether the correct answer appears in `sample`s, we should also ask whether promising prefixes are persistently undervalued.
That would tell us more directly when beam search, tree search, or verifier-guided branching are likely to buy useful compute.

## Tempered targets, delayed choice, and symmetry breaking

Another immediate consequence is that PLP admits a natural temperature family.
Given the same proposal $\pi_{\mathcal{D}}$ and potential $\Phi$, define

$$
p_\beta(\tau \mid x) \propto \pi_{\mathcal{D}}(\tau \mid x)\Phi(\tau,x)^\beta, \qquad 0 \le \beta \le 1.
$$

At $\beta=0$ we recover the raw proposal.
At $\beta=1$ we recover the original semantic target from the fundamental equation \eqref{eq:fundamental}.
Intermediate $\beta$ values define softened bridges between exploration and strict verification.

If we write the potential as $\Phi(\tau, x)=e^{R(\tau, x)}$, then

$$
p_\beta(\tau \mid x) \propto \pi_{\mathcal{D}}(\tau \mid x)e^{\beta R(\tau, x)},
$$

so $\beta$ plays the role of an inverse temperature.
Small $\beta$ gives a broad, high-entropy law.
As $\beta$ increases, mass concentrates on higher-reward trajectories.

Kappen's 2005 analysis clarifies the control meaning of this continuation quantity {% cite kappen2005path %}.
In his path-integral treatment, the optimal stochastic policy can change qualitatively as the noise level or the time-to-go changes.
The important example in the paper is a delayed-choice problem with two slits or targets.
When the product of noise level and time-to-go is large, the optimal controller steers toward the middle and postpones the final commitment.
Only later does the symmetry break and one route become preferable.

This lesson transfers directly to scaffold design.
When early reasoning states still support several plausible continuation basins, hard commitment to one branch can be suboptimal even from a rational control viewpoint.
A good scaffold should often keep several futures alive a little longer and let the symmetry break later, once extra evidence, tool outputs, or verifier signals separate the basins more clearly.

This gives a clean interpretation of annealed search, progressive filtering, verifier ramp-up, and soft-to-hard planning schedules.
Population methods such as importance weighting, sequential Monte Carlo, or twisted SMC {% cite zhao2024probabilistic %} can then be read as procedures that move mass through a sequence of tempered targets {% cite tokdar2010importance loula2025syntactic zhao2024probabilistic %}.

This also gives a principled language for iterative answer refinement.
Progressive-Hint Prompting and later work on refined answer distributions can be read as sequential procedures that repeatedly sharpen an empirical answer law rather than trusting a single first-pass sample {% cite zheng2023progressive pal2024refining %}.

Many tree-search and multi-sample workflows fail because they apply an overly sharp verifier too early.
The result is weight collapse.
A small number of trajectories dominate before the system has explored enough of the space.

The free-energy perspective suggests a principled fix:
start from a high-entropy, low-$\beta$ regime and only gradually sharpen the potential.
Temperature schedules then become a controlled way of delaying commitment in a noisy planning problem.

## From free energy to a decomposition policy

The companion note [Scaffolding is all you need]({% link sections/science/_posts/2026-03-02-Scaffolding-is-all-you-need.md %}) made the reliability point.
AND-style decompositions add essential failure points, whereas OR-style search buys alternatives.
Kappen's control picture sharpens that argument.

If a node keeps several alternative solution basins alive, the effective continuation cost has the schematic OR form

$$
J_{\mathrm{OR}}(s)\approx -\lambda \log \sum_{b\in\mathcal{B}(s)} \exp\!\left(-\frac{J_b(s)}{\lambda}\right) + \Delta_{\mathrm{sel}}(s),
$$

where $\mathcal{B}(s)$ indexes disjoint **basins** of future traces (for example, distinct high-level plans), $J_b(s)$ is the cost-to-go if the scaffold commits to basin $b$, and $\Delta_{\mathrm{sel}}$ summarizes selection and verification costs.
The temperature $\lambda$ is the same scale as in $\Phi(\tau)=\exp(-S(\tau)/\lambda)$ whenever that representation is used.
This is the option-value term.
Several basins can coexist, and uncertainty can make delayed commitment rational.

If a node instead commits to mandatory subtasks that all must succeed, the effective continuation cost is closer to

$$
J_{\mathrm{AND}}(s)\approx \sum_{i=1}^K J_i(s) + \Delta_{\mathrm{valid}}(s)+\Delta_{\mathrm{comp}}(s),
$$

where $K$ is the number of subtasks, $J_i(s)$ is the cost-to-go carried by the $i$th child interface after decomposition, and $\Delta_{\mathrm{valid}}$ and $\Delta_{\mathrm{comp}}$ summarize decomposition validity and composition risk.
This is the same essential-node tax that appeared in the reliability note, now written in cost language rather than failure-probability language.

The practical consequence is simple.
A good scaffold should not jump directly from "one-shot answer" to "mandatory decomposition".
It should choose among four control modes:

1. answer directly when direct answer reliability is already high;
2. use OR-style search when several whole-solution basins can be compared by a verifier or selector;
3. delay commitment when the landscape is still multimodal and extra information is cheap;
4. use AND-style decomposition only after symmetry breaks, or when child interfaces are locally verifiable and composition is stable.

Decomposition is therefore not a default formatting choice.
It is a control action whose value depends on uncertainty, horizon, verifier quality, and the geometry of the continuation landscape.

## Replica thinking and the geometry of reasoning paths

Another useful consequence comes from the replica trick, a standard device in statistical physics for analyzing log partition functions.

For a token prefix $s$, the log partition function is again

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

Write the **normalized continuation law** downstream of $s$ as

$$
p(\tau \mid s)
=
\frac{\pi_{\mathcal{D}}(\tau \mid s)\,\Phi(\tau)}{Z(s)}.
$$

Suppose we draw two independent samples from $p(\tau \mid s)$.
The probability that the two draws land on the same complete trace $\tau$ is

\begin{equation}
C_2(s) := \sum_{\tau \succ s} p(\tau \mid s)^2.
\end{equation}

and its inverse law

\begin{equation}
N_{\mathrm{basins}}(s):=\frac{1}{C_2(s)}
\end{equation}

can be read as an effective number of continuation basins.

This quantity has an immediate interpretation.
If $N_{\mathrm{basins}}(s)\approx 1$, then most samples collapse into the same hidden plan.
Self-consistency then produces many surface variations of the same mistake because the continuation landscape remains concentrated in one basin.
If $N_{\mathrm{basins}}(s)$ is large, several qualitatively distinct reasoning paths contribute downstream, and additional samples can provide genuinely new evidence.

<figure>
<img src="/static/postfigures/replica_trick_plp.svg" alt="Single versus multiple reasoning basins">
<figcaption>
<strong>Figure 3.</strong> A single verbalized path may give the illusion of diversity while remaining trapped in one hidden basin. Finite-replica thinking asks a deeper question: how many distinct high-mass continuation families are actually contributing downstream of a prefix?
</figcaption>
</figure>

This connects directly to the dependence analysis already present in PLP.
In [Probabilistic Language Programming]({% link sections/science/_posts/2026-03-01-Probabilistic-Language-Programming.md %}), $\rho$ denotes a pairwise correlation between scaffold outputs and $K_{\mathrm{eff}}$ denotes an effective sample size that adjusts the nominal draw count for dependence.
Replica overlap suggests a more geometric, prefix-level version of the same story.

One practical consequence follows:
replicated reasoning traces can improve answers and can also **measure the ruggedness of the continuation landscape itself**.

If two or more replicas keep collapsing into the same basin, the main bottleneck is inferential diversity rather than sample count.
That points to different interventions: new decompositions, different retrieved evidence, alternative latent strategies, or a different verifier placement.

<!-- ### Estimating $C_2(s)$ in practice

At this point a natural practical question appears:

> How does one actually estimate $C_2(s)$ for a prefix $s$?

The answer becomes simple once we expand the normalized continuation law explicitly.
Downstream of a prefix $s$, PLP defines

$$
p(\tau \mid s)
=
\frac{\pi_{\mathcal{D}}(\tau \mid s)\Phi(\tau)}{Z(s)},
\qquad
Z(s)=\sum_{\tau \succ s} \pi_{\mathcal{D}}(\tau \mid s)\Phi(\tau).
$$

Therefore

$$
C_2(s)
=
\sum_{\tau \succ s} p(\tau \mid s)^2
=
\frac{\sum_{\tau \succ s} \pi_{\mathcal{D}}(\tau \mid s)^2 \Phi(\tau)^2}{Z(s)^2}.
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

Often we do not have direct samples from $p(\cdot \mid s)$; we only know how to sample $\tau^{(i)} \sim \pi_{\mathcal{D}}(\cdot \mid s)$ and score them with $\Phi$.
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
\frac{\frac{1}{N}\sum_{i=1}^N \pi_{\mathcal{D}}(\tau^{(i)} \mid s)\,w_i^2}
{\widehat{Z}(s)^2}.
$$

The presence of the extra factor $\pi_{\mathcal{D}}(\tau^{(i)} \mid s)$ is not a typo: it comes from the fact that the numerator is an expectation under the proposal of $\pi_{\mathcal{D}}(\tau \mid s)\Phi(\tau)^2$.
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
It is the correct statement of what the deployed scaffold believes the future landscape looks like. -->

## Implications for prompting

Once seen through this lens, many prompting techniques become much easier to classify.

**Chain-of-thought** introduces a latent sequential state, allowing the model to externalize part of the free-energy computation into the token stream.
That interpretation is now explicit in work that treats rationales as latent variables and optimizes answer likelihood by marginalizing over them {% cite phan2023training %}, and in work that casts CoT adaptation more broadly as amortized inference over intractable posteriors {% cite hu2024amortizing %}.
This also puts a clear bound on what one should expect from pure chain-of-thought at inference time:
externalizing rationales can help the model access structure that was already latent in its training distribution, but it does not manufacture arbitrary new competence.
The method is strongest when training has already shaped a useful high-reward landscape over latent traces, and correspondingly weaker as a route to robustly out-of-distribution reasoning.

**Self-consistency** samples multiple reasoning paths and marginalizes them at the answer level.
Later variants such as Progressive-Hint Prompting and refined answer distributions can be read as more deliberate ways of refining that sampled answer distribution over multiple rounds {% cite zheng2023progressive pal2024refining wang2022self %}.

**Tree-of-Thoughts** allocates compute across prefixes, attaches heuristic or uncertainty estimates to partial states, and searches over the resulting frontier {% cite yao2023tree mo2023uncertain zhou2024lats %}.
In older approximate-inference language, this is closer to Monte Carlo tree search with value guidance than to a new cognitive primitive {% cite buesing2020approximate %}.

**Reflexion and self-backtracking** repeatedly revise the proposal so that more mass moves toward regions with better downstream verifier-weighted continuation mass {% cite shinn2023reflexion %} {% cite yang2025selfbacktracking %}.

Finally, SMC-style steering methods make the probabilistic interpretation explicit.
They treat LM control as sampling from an unnormalized target distribution and use learned twist or future-value estimates to guide particles toward high-mass regions {% cite zhao2024probabilistic %} {% cite loula2025syntactic %}.

In short:

> Prompting techniques are numerical methods for approximating the right partition function over traces under finite compute.

This perspective places chain-of-thought, search, refinement, and particle methods within the same mathematical frame.

## Conclusions

Autoregressive models can successfully plan ahead only when their local decisions already contain a compressed summary of the future partition over continuations, the soft-continuation value as in {% cite blondel2025autoregressive %}.
When that summary is imperfect, inference-time scaffolds can spend runtime compute, search, tools, and verification to approximate the missing continuation values more accurately.

Kappen's control perspective sharpens the design rule.
Under uncertainty, the right scaffold often delays commitment, keeps several continuation basins alive, and turns search into hard decomposition only once the landscape becomes easier to separate.

The practical question is therefore not only which scaffold is most accurate, but which control policy over answer, search, delay, and decomposition best approximates verifier-weighted free energy under a finite compute budget.

---

## References

{% bibliography --cited %}
