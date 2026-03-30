---
layout: post
title: PLP is inference-time approximation of free energy
date: 2026-03-03
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
That logarithm is the free energy, up to the usual sign convention from physics.
Any prompting technique is trying to approximate it.

This is the core conceptual jump between post-training alignment and inference-time compute.
When we deploy a scaffold, we are not invoking a mysterious faculty of "reasoning" or treating the model as an anthropomorphic oracle.
We are approximating, at inference time, a log-partition over future traces that the raw autoregressive policy cannot cheaply marginalize in one forward pass.

![inference_time_reweighting](/static/postfigures/inference_time_reweighting.svg)
**Figure 1: Inference-Time Trace Reweighting.**
**(Left)** The raw autoregressive policy induces a broad, unconstrained proposal distribution over reasoning traces $q(\tau \mid x)$ branching from an initial prompt $x$.
**(Center)** A verifier, judge, or heuristic defines a non-negative potential field $\Phi(\tau, x)$ (orange), smoothly warping the energy landscape of available paths and highlighting promising basins.
**(Right)** The normalized semantic target distribution $p(\tau \mid x)$. By applying the inference-time scaffold, probability mass (represented by line thickness and color intensity) is shifted away from dead ends and concentrated onto a smaller subset of high-value continuations.

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
Then define the continuation value

$$
V(s) := \log Z(s).
$$

This is the exact prefix free energy.

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

![Local score plus continuation free energy](/static/postfigures/arm_ebm_soft_value_function.png)

*Figure 2. A local decision only becomes meaningful once it is augmented by the free energy of its downstream subtree. The practical role of runtime scaffolds is to estimate that future mass better than plain next-token decoding can.*

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
Population methods such as importance weighting, sequential Monte Carlo, or twisted SMC {% cite zhao2024probabilistic %} can then be read as procedures that move mass through a sequence of tempered targets {% cite tokdar2010importance %} {% cite loula2025syntactic %} {% cite zhao2024probabilistic %}.

This also gives a principled language for iterative answer refinement.
Progressive-Hint Prompting and later work on refined answer distributions can be read as sequential procedures that repeatedly sharpen an empirical answer law rather than trusting a single first-pass sample {% cite zheng2023progressive %} {% cite pal2024refining %}.

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

![Single versus multiple reasoning basins](/static/postfigures/replica_trick_plp.svg)

*Figure 3. A single verbalized path may give the illusion of diversity while remaining trapped in one hidden basin. Finite-replica thinking asks a deeper question: how many distinct high-mass continuation families are actually contributing downstream of a prefix?*

This connects beautifully to the dependence analysis already present in PLP.
The pairwise correlation $\rho$ and the effective sample size $K_{\mathrm{eff}}$ measure output-level dependence.
Replica overlap suggests a more geometric, prefix-level version of the same story.

That is the fourth low-hanging fruit:
use replicated reasoning traces not only to improve answers, but also to **measure the ruggedness of the continuation landscape itself**.

If two or more replicas keep collapsing to the same basin, the problem is not a lack of samples.
It is a lack of inferential diversity.
That is a completely different failure mode, and it calls for different interventions: different decompositions, different retrieved evidence, different latent strategies, or different verifier placements.

## What this says about prompting

Once seen through this lens, many prompting techniques become much easier to classify.

Chain-of-thought does not magically add "reasoning" as an ontologically new faculty.
It introduces a latent sequential state, allowing the model to externalize part of the free-energy computation into the token stream.
That interpretation is now explicit in work that treats rationales as latent variables and optimizes answer likelihood by marginalizing over them {% cite phan2023training %}, and in work that casts CoT adaptation more broadly as amortized inference over intractable posteriors {% cite hu2024amortizing %}.

Self-consistency does not magically uncover truth by social consensus.
It samples multiple reasoning paths and marginalizes them at the answer level {% cite wang2022self %}.
Later variants such as Progressive-Hint Prompting and refined answer distributions can be read as more deliberate ways of refining that sampled answer distribution over multiple rounds {% cite zheng2023progressive %} {% cite pal2024refining %}.

Tree-of-Thoughts and related tree-search methods do not create intelligence from branching alone.
They allocate compute across prefixes, attach heuristic or uncertainty estimates to partial states, and search over the resulting frontier {% cite yao2023tree %} {% cite mo2023uncertain %} {% cite zhou2024lats %}.
In older approximate-inference language, this is closer to Monte Carlo tree search with value guidance than to a new cognitive primitive {% cite buesing2020approximate %}.

Reflexion and self-backtracking do not merely add self-awareness.
They repeatedly revise the proposal so that more mass moves toward regions with better downstream verifier-weighted continuation mass {% cite shinn2023reflexion %} {% cite yang2025selfbacktracking %}.

Finally, SMC-style steering methods make the probabilistic interpretation explicit.
They treat LM control as sampling from an unnormalized target distribution and use learned twist or future-value estimates to guide particles toward high-mass regions {% cite zhao2024probabilistic %} {% cite loula2025syntactic %}.

In short:

> Prompting techniques are numerical methods for approximating free energy under finite compute.

That is a much less romantic sentence than the usual discourse around agents and reasoning.
It is also, I think, much closer to the truth {% cite meyerson2025position %}.


## The big picture

The sharpest version of the story is now the following.

Autoregressive models can behave as if they plan ahead only when their local decisions already contain a compressed summary of the future partition over continuations.
When that summary is imperfect, inference-time scaffolds step in: the feedback loop they inject intelligence helps to numerically approximate the missing free-energy terms by spending more runtime compute.

This is why the right question is not "do agents reason?" or even "does chain-of-thought work?"
The right question is:

> Which inference-time procedure best approximates the verifier-weighted free energy of future traces under a finite compute budget?

That, to me, is the real systems interpretation of PLP.
And it is also why the next generation of scaffolds should probably be evaluated less like personalities and more like numerical schemes.

---

## References

{% bibliography --cited %}
