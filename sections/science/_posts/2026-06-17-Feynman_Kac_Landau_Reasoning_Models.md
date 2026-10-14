---
layout: post
title: "Feynman-Kac theory of reasoning models"
description: "A research programme for measuring commitment transitions, gauge-invariant observables, and universality in the free-energy landscape of autoregressive generation."
date: 2026-06-17
published: true
categories:
  - science
  - deep-learning
---

## Motivation: what is the free energy of a language model?

When a language model generates text, it narrows down an enormous space of possible continuations into a single sequence. At the start, many futures are plausible. By the end, only one has survived. This progressive narrowing looks like a physical process: a system relaxing from a high-entropy state into a low-entropy committed state, dissipating information along the way. The question is whether that analogy is just a metaphor or whether it can be made quantitative, predictive, and falsifiable.

Two recent developments make the question urgent. The first is Blondel et al.'s proof that autoregressive models and energy-based models are bijectively related in function space, so that next-token logits already encode a soft Bellman look-ahead term {% cite blondel2025autoregressive %}. The second is the explosion of post-training techniques---RLHF, DPO, GRPO, and their descendants---that are all, at different levels of approximation, solving the same maximum-entropy RL problem whose optimal solution is an energy-based model {% cite ouyang2022training rafailov2024direct shao2024deepseekmath guo2025deepseek kumar2025llm %}.

The programme I describe in this note tries to answer four questions. First, is there a genuine *arrow of time* in autoregressive generation, measurable from the model's own probability distributions? Second, does the model undergo a *commitment transition*---a sharp collapse from many plausible futures to one---and can that transition be described by a Landau free energy? Third, is the transition *universal*, with the same critical exponent across model scales and architectures? Fourth, can we *bridge* the free-energy picture between base (pretraining-only) models and aligned (RLHF/DPO-tuned) models, placing them on a single common axis?

The central methodological decision is to move from instruction-tuned models to *base* models. The reason is that several of the interesting signatures we previously chased in instruction-tuned models turned out to be artifacts of alignment, decoding templates, and the gauge ambiguity of the log-partition function. Base models remove those confounders and let us isolate the intrinsic physics of autoregressive generation.

## Theory I: the bijection between ARMs and EBMs

### Energy-based models as the optimal policy

An energy-based model assigns to each response $\mathbf{y}$ given prompt $\mathbf{x}$ the Gibbs distribution

$$
p_R^{\mathrm{ebm}}(\mathbf{y}\mid\mathbf{x}) = \frac{\exp(R(\mathbf{x},\mathbf{y}))}{\sum_{\mathbf{y}'} \exp(R(\mathbf{x},\mathbf{y}'))},
$$

where $R:\mathcal{X}\times\mathcal{Y}\to\mathbb{R}$ is a reward (or negative energy). The log-partition

$$
A_R^{\mathrm{ebm}}(\mathbf{x}) = \log \sum_{\mathbf{y}} \exp(R(\mathbf{x},\mathbf{y}))
$$

is intractable, costing $O(V^T)$ for vocabulary size $V$ and maximum length $T$.

Crucially, the EBM is the *analytical solution* of the KL-regularized RL objective

$$
\max_{p} \;\mathbb{E}_{Y\sim p}[R(X,Y)] - \mathrm{KL}(p(\cdot|X)\,\|\,p_{\mathrm{ref}}(\cdot|X)),
$$

whose optimum is

$$
p^\star(\mathbf{y}\mid\mathbf{x}) = \frac{p_{\mathrm{ref}}(\mathbf{y}\mid\mathbf{x})\exp(R(\mathbf{x},\mathbf{y}))}{\sum_{\mathbf{y}'} p_{\mathrm{ref}}(\mathbf{y}'\mid\mathbf{x})\exp(R(\mathbf{x},\mathbf{y}'))}.
$$

This is an EBM with reward $R + R_{\mathrm{ref}}$, where $R_{\mathrm{ref}}(\mathbf{x},\mathbf{y}) := \log p_{\mathrm{ref}}(\mathbf{y}\mid\mathbf{x})$ {% cite blondel2025autoregressive levine2018reinforcement %}. Post-training alignment---whether by PPO, DPO, or GRPO---is at bottom an attempt to find an autoregressive model that approximates this EBM {% cite ouyang2022training rafailov2024direct shao2024deepseekmath kumar2025llm %}.

### The bijection

Blondel et al. establish a bijection between EBMs and ARMs in function space {% cite blondel2025autoregressive %}. Assume the reward decomposes as

$$
R_r(\mathbf{x},\mathbf{y}) = \sum_{t=1}^{|\mathbf{y}|} r(\mathbf{s}_t, y_t),
$$

where $$\mathbf{s}_t = \mathbf{x}\oplus\mathbf{y}_{< t}$$ is the context. 
Define the forward map $$q = \mathcal{M}(r)$$:

$$
q(\mathbf{s}_t, y_t) = \begin{cases} r(\mathbf{s}_t, y_t) & \text{if } y_t = \mathrm{EOS} \\ r(\mathbf{s}_t, y_t) + V_q(\mathbf{s}_t \oplus y_t) & \text{if } y_t \neq \mathrm{EOS} \end{cases}
$$

where

$$
V_q(\mathbf{s}) = \log\sum_{a\in\mathcal{A}} \exp(q(\mathbf{s}, a)).
$$

Then $p_R^{\mathrm{ebm}}(\mathbf{y}\mid\mathbf{x}) = p_q^{\mathrm{arm}}(\mathbf{y}\mid\mathbf{x})$ exactly, and $A_R^{\mathrm{ebm}}(\mathbf{x}) = V_q(\mathbf{x})$.

The inverse map $r = \mathcal{M}^{-1}(q)$ subtracts the future value:

$$
r(\mathbf{s}_t, y_t) = \begin{cases} q(\mathbf{s}_t, y_t) & \text{if } y_t = \mathrm{EOS} \\ q(\mathbf{s}_t, y_t) - V_q(\mathbf{s}_t \oplus y_t) & \text{if } y_t \neq \mathrm{EOS} \end{cases}
$$

This is computable in parallel from any trained model, since it requires only a single forward pass per position. The quantity $q(\mathbf{s}_t, y_t) - V_q(\mathbf{s}_t \oplus y_t)$ is the *advantage* of choosing $y_t$ over the soft-average alternative---a gauge-invariant difference of logits.

### The dual task of the autoregressive model

The bijection says that for the ARM to be equivalent to the EBM, its logits $q$ must simultaneously encode two things: the immediate reward $r(\mathbf{s}_t, y_t)$, and the soft optimal value $V_q(\mathbf{s}_t \oplus y_t)$ of all future continuations. The model is "burdened with a dual task": it must score the next token and implicitly compute a potentially complex future-looking log-partition using only a backward-looking (causal) architecture {% cite blondel2025autoregressive %}.

This is the precise sense in which next-token prediction already does look-ahead. The question is how well, and at what scale.

## Theory II: the gauge problem

### The one-step proxy vs. the lookahead value

There are two objects that are easy to conflate.

The *one-step log-partition* is what you get from a single forward pass:

$$
V_q^{\mathrm{1step}}(\mathbf{s}_t) = \log\sum_{v\in\mathcal{V}} \exp(z_t(v)),
$$

where $z_t$ are the raw logits at position $t$. This is cheap but gauge-dependent.

The *lookahead value* is the true Feynman--Kac object:

$$
\exp V_t(\mathbf{s}_t) = \mathbb{E}_{\mathbf{y}_{>t}\sim\pi}\left[\exp\left(\sum_{s=t}^{T-1} r(\mathbf{s}_s, y_{s+1})\right)\right], \qquad V_T \equiv 0.
$$

This satisfies the discrete soft-Bellman recursion

$$
V_t = \log\mathbb{E}_{y_{t+1}\sim\pi}\left[\exp\left(r(\mathbf{s}_t, y_{t+1}) + V_{t+1}\right)\right].
$$

It looks forward through the entire tree of possible continuations. Blondel's bijection tells us that for an RLHF-trained model, these two objects coincide---the logits have already absorbed the recursion. For a base model, they do not.

### Why the gauge is free for base models

The softmax is invariant under a per-step additive shift $z_t \mapsto z_t + c_t\mathbf{1}$, but

$$
\log\sum_v \exp(z_t(v) + c_t) = V_q^{\mathrm{1step}}(\mathbf{s}_t) + c_t.
$$

So the absolute level of $V_q^{\mathrm{1step}}$ is behaviorally non-identifiable: two models with identical sampling behavior can have different $V_q$ profiles. Cross-entropy pretraining does *not* pin $c_t$. Consequently, anything claimed from raw $V_q$ levels---peak heights, barrier heights---risks being an artifact of an arbitrary normalization.

This is the fundamental reason the free-energy reading of $V_q$ is cleanest in the RLHF/maxent-RL regime (where the construction ties logits to soft $Q$-values) and weakest in base models. The tension is resolved by the bridge construction below.

## Theory III: the Feynman--Kac tilted value and the bridge

### The reference-measure bridge

KL-regularized RL with reference $\pi_{\mathrm{ref}}$ and inverse temperature $\beta = 1/\tau$ has the closed-form optimum

$$
\pi^\star(\mathbf{y}\mid\mathbf{x}) = \frac{1}{Z(\mathbf{x})}\,\pi_{\mathrm{ref}}(\mathbf{y}\mid\mathbf{x})\,\exp(R(\mathbf{x},\mathbf{y})/\tau).
$$

Take the base model as $\pi_{\mathrm{ref}}$. Then any aligned sibling defines an implied reward that is fully gauge-invariant because it is a ratio of two normalized distributions:

$$
\frac{R(\mathbf{x},\mathbf{y})}{\tau} = \log\frac{\pi_{\mathrm{aligned}}(\mathbf{y}\mid\mathbf{x})}{\pi_{\mathrm{base}}(\mathbf{y}\mid\mathbf{x})} + \mathrm{const}(\mathbf{x}).
$$

Per token, this is $\ell_t(v) = \log\pi_t^{\mathrm{aligned}}(v) - \log\pi_t^{\mathrm{base}}(v)$, a *measurable tilt field*. DPO explicitly learns this ratio {% cite rafailov2024direct %}. The tilt field fixes the gauge: the base model is the normalization reference.

### The Feynman--Kac tilt family

Pick a reward $R$---start with a terminal-only reward, such as the indicator that a multiple-choice answer is correct. Define the tilted soft value under the base policy:

$$
V_t^\beta(\mathbf{s}_t) = \frac{1}{\beta}\log\mathbb{E}_{\mathbf{y}_{>t}\sim\pi_{\mathrm{base}}}\left[\exp\left(\beta\sum_{s\geq t} r_s\right)\mid\mathbf{s}_t\right], \qquad V_T^\beta = 0.
$$

This is computed by *Monte Carlo rollouts* under the base model. The family interpolates:

- $\beta \to 0$: $V_t^\beta \to \mathbb{E}[\sum r]$ (risk-neutral value; pure base behavior, no tilt).
- $\beta$ large: $V_t^\beta \to$ free energy dominated by the best futures (the Blondel/EBM regime).

The aligned model corresponds to $V_t^{\beta_{\mathrm{eff}}}$ for some effective $\beta_{\mathrm{eff}}$. The bridge test: does the aligned model's raw $V_q$ profile match $V_t^{\beta_{\mathrm{eff}}}$ computed from the base model?

### What "rollouts" means concretely

At position $t$ in the generation, sample $K$ continuations from the base model, each running to EOS or a maximum length. For each continuation $k$, compute the total reward $R^{(k)}$ (e.g., 1 if the answer is correct, 0 otherwise). The tilted soft value is

$$
V_t^\beta = \frac{1}{\beta}\log\left[\frac{1}{K}\sum_{k=1}^K \exp(\beta\,R^{(k)})\right].
$$

At $\beta \to 0$ this reduces to the fraction of correct rollouts. At $\beta \to \infty$ it reduces to the indicator that *any* rollout is correct. In between, it smoothly interpolates.

The cost is $T \times B \times K$ forward passes per item (sequence length times number of beta values times number of rollouts), compared to $T$ for the one-step proxy. This is why the rollouts are the compute-heavy part of the programme.

### Effective-temperature calibration

Estimate where an aligned model sits on the $\beta$-axis from its divergence from base:

$$
\widehat{\beta_{\mathrm{eff}}} \propto \frac{1}{T}\sum_t D_{\mathrm{KL}}\!\left(\pi_t^{\mathrm{aligned}}\,\|\,\pi_t^{\mathrm{base}}\right),
$$

a monotone proxy calibrated by matching one moment of the tilt field $\ell_t$. This places base ($\beta = 0$) and each aligned model on a single common axis, so "base vs RLHF" becomes "different points on the same tilt family" rather than two incomparable objects.

## Theory IV: the arrow of time

### Gauge-invariant irreversibility

The observables that survive the gauge problem are pure functionals of the $\pi_t = \mathrm{softmax}(z_t)$, not of the raw logits. Define cumulative eviction and creation:

$$
\Sigma_+ = \sum_t D_{\mathrm{KL}}(\pi_{t-1}\,\|\,\pi_t), \qquad \Sigma_- = \sum_t D_{\mathrm{KL}}(\pi_t\,\|\,\pi_{t-1}).
$$

$\Sigma_+$ measures how much the previous distribution is "evicted" by the new one; $\Sigma_-$ measures how much new probability mass is "created." The arrow of time is the claim

$$
\Delta\Sigma = \Sigma_+ - \Sigma_- > 0,
$$

i.e., generation prunes previously-plausible continuations more strongly than it creates new ones. This has been observed robustly in instruction-tuned models; the open question is whether it persists in base models.

The identity

$$
\Delta\Sigma = \underbrace{\big[H(\pi_T) - H(\pi_0)\big]}_{\text{global entropy change}} + \underbrace{\sum_t\big[H(\pi_{t-1},\pi_t) - H(\pi_t,\pi_{t-1})\big]}_{\text{cross-entropy asymmetry}}
$$

makes the cross-entropy asymmetry term the carrier of irreversibility independent of the boundary entropy change {% cite kullback1951information cover2006elements %}. Both terms are gauge-invariant and behaviorally identifiable, so they are valid for base models without any bridge.

## Theory V: the Landau commitment transition

### The order parameter

Define a commitment order parameter $\phi_t \in [0,1]$: $\phi = 0$ means all futures are open (disordered), $\phi = 1$ means the answer is determined (ordered). Candidate gauge-invariant realizations include the negentropy $1 - H(\pi_t)/\log V$, the logit margin $\Delta = z_{\mathrm{correct}} - \max_{\mathrm{wrong}} z$ (for multiple-choice), and the rollout-based $V_t^\beta$.

### The Landau free energy

Posit a Landau free energy along normalized position $x = t/T$:

$$
F(\phi, x) = a(x)\,\phi^2 - b\,\phi^3 + c\,\phi^4 - h(x)\,\phi,
$$

with control parameter $a(x)$ decreasing as context accumulates and external field $h(x)$ accumulating evidence. The toy model with $a(x) = a_0(1-x)$, $h(x) = h_0 x$, $b = c = 1$ produces a peak-then-drop in $-F_{\min}(x)$: a metastable high-$V$ well jumping to a low-$V$ well, a first-order-like "decision" {% cite landau1937theory %}.

### Universality

Near the commitment point, if one exists, the value should scale as

$$
V(x) = V_c - A\,|x - x_c|^\beta + \text{smooth background},
$$

and universality means the exponent $\beta$ (and the collapsed shape) is the same across models and scales, with only $V_c$, $x_c$, $A$, and the width $w$ rescaling. Mean-field Landau predicts $\beta = 1/2$; Ising-like models give $\beta \approx 0.33$. A scale ladder predicts a width law $w \sim N^{-\nu}$ and a temperature-broadening $w \sim T^{1/2}$.

## What did not survive scrutiny

Several claims from earlier work on instruction-tuned models collapsed under examination. The table below records the failures and their root causes, because they motivate every methodological choice in the new programme.

| Claim | Status | Root cause |
|-------|--------|------------|
| Universal interior peak-then-drop in raw $V_q$ vs. $t/T$ | Artifact | Averaging in $t/T$ is flat; per-trajectory argmax-alignment manufactures a cusp even from noise. |
| Diverging susceptibility $\mathrm{Var}(V_q)(x)$ at $x_c$ | Not seen | No interior divergence after gauge normalization. |
| Critical exponent $\beta$ universal in raw $V_q$ | Unsupported | Driven by gauge/scale + alignment, not physics. |
| GSM8K "commitment" at $x \approx 0.99$ | Real but confounded | Template marker "The final answer is ..." forced by instruction tuning, not intrinsic geometry. |

The conclusion is that in instruction-tuned models the $V_q$ shape is dominated by (a) the gauge ambiguity, (b) decoding-template structure, and (c) RLHF KL-regularization. Base models remove (b) and (c) and let us isolate pretraining geometry.

## The base-model strategy

### Why base models

Base models remove the RLHF/maxent-RL term, so there is no injected $\beta\,\mathrm{KL}$ budget and no preference-optimized energy landscape. They remove chat templates and forced markers. And they enable a clean scale ladder with architecture and data held fixed.

### Model roster

The primary ladder is Pythia {% cite biderman2023pythia %}, which fixes architecture and training data (the Pile) while varying only size: 70m, 160m, 410m, 1b, 1.4b, 2.8b, 6.9b (deduped variants). Pythia also ships intermediate training checkpoints, giving a training-time axis to test whether critical structure *emerges* during pretraining.

Secondary ladders provide architecture and tokenizer diversity: Llama-3 base (1B, 3B, 8B) {% cite dubey2024llama %} and GPT-2 (small, medium, large) {% cite radford2019language %}. Each base model should be paired, where possible, with its aligned sibling (e.g., Llama-3.1-8B vs. Llama-3.1-8B-Instruct) so the bridge can be measured directly on a matched pair.

## Datasets and a logits-based correctness protocol

The programme deliberately moves off GSM8K to simple tasks that (a) base models can do without instruction-following, (b) have an unambiguous single-token commitment point, and (c) admit a gauge-invariant correctness signal read directly from logits.

### Multiple-choice datasets

ARC-Easy, ARC-Challenge {% cite clark2018think %}, OpenBookQA {% cite mihaylov2018can %}, MMLU {% cite hendrycks2021measuring %}, SciQ, PIQA, HellaSwag. Start with ARC-Easy and OpenBookQA: easy enough for small Pythia, hard enough to vary confidence.

### Two correctness scorings

1. *Letter-logit method.* Format the prompt as `Question: ... \n A. ... \n B. ... \n C. ... \n D. ... \n Answer:` and read the logits at the answer position, restricted to option-letter tokens. The logit margin $\Delta = z_{\mathrm{correct}} - \max_{\mathrm{wrong}} z$ is gauge-invariant and is the natural commitment order parameter at the decision token.

2. *Option-likelihood method.* Score each full option string by its length-normalized log-probability. Use to confirm the letter-logit method is not a tokenization artifact.

The commitment point is exactly the answer token: no alignment ambiguity, no verbosity confound, no $t/T$ smearing. Correctness, confidence, and the order parameter are all gauge-invariant.

## Central hypotheses

The programme pre-registers six hypotheses with explicit falsifiers.

**H0 (arrow of time).** $\Delta\Sigma > 0$ persists in base models. *Falsifier:* $\approx 0$ or $< 0$ implies the arrow-of-time claim was itself an alignment effect.

**H1 (commitment).** In multiple-choice and cloze tasks with a defined answer, the gauge-invariant order parameter (negentropy, logit margin, or true $V_t^\beta$) shows a reproducible collapse localized at the answer, beyond shift/AR(1)/phase-randomized surrogates. *Falsifier:* indistinguishable from surrogates, or equally strong in open-ended prompts.

**H2 (Landau form).** The approach to commitment is fit by the two-parameter Landau toy $F(\phi, x)$; $(a_0, h_0)$ are stable within a task. *Falsifier:* no stable fit.

**H3 (universality).** Across the Pythia ladder and the checkpoint axis, the collapsed shape and exponent $\beta$ are scale-invariant; width obeys $w \sim N^{-\nu}$ and temperature broadening $w \sim T^{1/2}$. *Falsifier:* $\beta$ scattered in $[0.2, 0.8]$ with no pattern, or $w$ not shrinking with $N$.

**H4 (bridge).** Aligned siblings sit at finite $\beta_{\mathrm{eff}}$ on the base model's tilt family; RLHF *tilts* rather than *reshapes* the base free-energy landscape. *Falsifier:* no $\beta$ matches, implying RLHF reshapes the landscape and raw $V_q$ is not a base-model free energy.

**H5 (mechanism, optional).** Hidden state carries lookahead: transfer entropy $TE(h_t \to V_{t+k})$ and susceptibility $\chi_t$ peak at commitment.

## Experiments

### Session A: foundation and sanity

Build a profiling script that loads one model, computes per-token $\pi_t$-functionals (entropy $H$, $\Sigma_\pm$ summands, Fisher--Rao step {% cite fisher1922mathematical %}, raw $V_q$ flagged as diagnostic-only), and multiple-choice letter-logit correctness. Run on Pythia-410m, Pythia-2.8b, and GPT-2-medium over ARC-Easy and OpenBookQA in bfloat16. Confirm or deny H0. Quantify raw-$V_q$ gauge spread. Prototype negentropy and logit-margin with shift and AR(1) surrogates wired in from the start.

### Session B: Feynman--Kac value done correctly

Build a rollout script that computes $V_t^\beta$ over a $\beta$-grid with terminal correctness reward. Validate against the one-step proxy. Gate question: is there genuine commitment in the *correct* object (not the proxy), beyond surrogates? This is the make-or-break test for the Landau programme.

### Session C: bridge on matched pairs

Build a bridge script for Llama-3.1-8B base vs. Instruct. Measure the tilt field $\ell_t$, estimate $\beta_{\mathrm{eff}}$, and test H4: does the aligned model's raw $V_q$ match $V_t^{\beta_{\mathrm{eff}}}$ from the base model?

### Session D: Landau fit and barrier--confidence link

Fit $F(\phi, x)$; extract $(a_0, h_0)$. Test whether the pre-answer $V_t^\beta$ barrier predicts $p(\mathrm{correct})$ and the margin $\Delta$.

### Session E: universality

Full Pythia ladder plus checkpoint axis. Bootstrap $\beta$. Fit width law $w(N)$ and temperature law $w(T)$. Test task-class separation (multiple-choice vs. cloze).

### Session F: mechanism (optional)

Extract hidden states $h_t$. Compute transfer entropy $TE(h_t \to V_{t+k})$ and susceptibility $\chi_t = \partial V_{t+1}/\partial h_t$.

## Engineering discipline

Every experiment is first a standalone Python script that loads exactly one model, writes results to disk, and exits. Only after the scripts are stable do we assemble a teaching notebook. The rationale is practical: a single process per model is the clean fix for CUDA-OOM, it makes runs independently restartable and cacheable, and it keeps heavy compute out of the notebook.

Each script writes an append-only parquet shard keyed by `(model, dataset, item_id)`, so a crash is recoverable and re-runs are idempotent. A thin shell loop invokes one fresh process per model. The notebook reads only the persisted parquet outputs and is analysis and exposition only: markdown cells stating each hypothesis, the math, the falsifier, then the plot, then a verdict.

## Confounder-control checklist

1. **Gauge/scale of $V_q$**: use gauge-invariant observables or the rollout $V_t^\beta$; never compare raw $V_q$ levels across models.
2. **Alignment artifact**: for any peak or collapse claim, always show shift, AR(1), and phase-randomized surrogates; report the excess over null.
3. **Tokenizer differences**: repeat every alignment in char-fraction as well as $t/T$; verify option letters are single tokens.
4. **Verbosity/variable length**: use answer-anchored alignment $x = (t - t_0)/(T - t_0)$.
5. **Architecture/data vs. size**: Pythia varies size with data and architecture fixed; cross-check with Llama-3 base and GPT-2.
6. **Decoding template**: base models, plain-text prompts, no chat template.
7. **EOS/length handling**: fix `max_new_tokens`, log truncation, separate boundary effects from interior structure.
8. **Temperature**: sweep $T$, report broadening.
9. **Quantization**: bfloat16 default; validate any 8-bit run against bfloat16 on a held-out subset.
10. **Selection bias**: never restrict to correct-only without reporting the full sample.
11. **Multiple comparisons**: bootstrap CIs for $\beta$; pre-register fit windows; correct across models and tasks.

## Criticisms and limitations

The programme has several weak points that should be stated openly.

First, the Landau framework is a *phenomenological* fit, not a derivation. There is no theorem that says autoregressive generation must exhibit a phase transition. The commitment transition might be a smooth crossover, in which case the Landau parameterization is just a convenient curve fit with no physical content. The falsifier for H2 is designed to detect exactly this.

Second, the universality claim (H3) is the highest-risk, highest-gain target. Critical exponents in real physical systems emerge from specific symmetry classes and dimensionality. Language models have no obvious analogue of spatial dimensionality, and the "temperature" in the softmax is not a physical temperature. The exponent $\beta$ might be scale-dependent---which would still be interesting as an emergence signature, but would not be universality in the Landau sense.

Third, the rollout-based $V_t^\beta$ is expensive and noisy. Monte Carlo estimates of log-partition functions have high variance when the reward is sparse (e.g., binary correctness). The effective number of useful rollouts may be small, and importance weighting from the base model to the tilted distribution may be needed to reduce variance. The OREO method {% cite oreo2024 %} trains an explicit value function to avoid this problem; the present programme uses rollouts instead, which is simpler but less efficient.

Fourth, the bridge (H4) assumes that the aligned model is a *tilt* of the base model, i.e., that RLHF preserves the base model's free-energy landscape and only reweights it. This may be false. DPO and GRPO can change the model's behavior in ways that are not captured by a single scalar $\beta_{\mathrm{eff}}$, especially when the reward model itself is imperfect. If the bridge fails, it means RLHF *reshapes* the landscape rather than tilting it---which is still a meaningful result, but not the one the programme hopes for.

Fifth, the base-model strategy removes confounders but also removes signal. Base models do not follow instructions, so the tasks must be simple enough that the model can do them from the prompt alone. This limits the range of reasoning phenomena we can study. The commitment transition might look different in a model that is actually reasoning (chain-of-thought) versus one that is just predicting the next token in a multiple-choice question.

Sixth, Blondel's bijection is in function space. With finite-capacity Transformers, the ARM may not perfectly represent the EBM, especially at small scales. The commitment signal might be *architecture-limited*---a Pythia-70m model that has not learned $V_q$ well will not show a sharp transition, regardless of whether the underlying task has one. The scale ladder is designed to detect this: if commitment sharpens with scale, it is evidence that $V_q$ learning is the bottleneck.

Finally, the arrow-of-time claim ($\Delta\Sigma > 0$) might be generic to *any* next-token-narrowing process, not specific to language models or pretraining. If it holds for a random-walk baseline, it carries no information about the model. The surrogate controls are designed to catch this.

## Connection to the post-training landscape

The survey by Kumar et al. {% cite kumar2025llm %} covers the full post-training pipeline: SFT, reward modeling (Bradley--Terry, Plackett--Luce), policy optimization (PPO {% cite schulman2017proximal %}, DPO {% cite rafailov2024direct %}, GRPO {% cite shao2024deepseekmath %}, ORPO {% cite hong2024orpo %}), and test-time scaling (beam search, best-of-N, chain-of-thought {% cite wei2022chain %}, tree-of-thoughts, MCTS). Several connections to the present programme are worth noting.

OREO {% cite oreo2024 %} explicitly trains a policy and value function by minimizing soft Bellman inconsistency:

$$
V_\phi(\mathbf{s}_t) - V_\phi(\mathbf{s}_{t+1}) = r(\mathbf{s}_t, \mathbf{a}_t) - \beta\log\frac{\pi_\theta(\mathbf{a}_t\mid\mathbf{s}_t)}{\pi_{\mathrm{ref}}(\mathbf{a}_t\mid\mathbf{s}_t)}.
$$

This is exactly the object the rollout-based $V_t^\beta$ approximates. OREO operationalizes it for multi-step reasoning with sparse terminal rewards; the present programme computes it by Monte Carlo instead of learning it.

DPO reparameterizes the reward as a log-ratio $R/\tau = \log(\pi_\theta/\pi_{\mathrm{ref}}) + \mathrm{const}$, which is literally the tilt field $\ell_t$. DPO-trained models (Llama-3, Hermes) implicitly learn $R/\tau$, so their logits *are* tilted soft $Q$-values, and the bridge should work cleanly. GRPO-trained models (DeepSeek) use group-normalized advantages without an explicit value function, so the bridge may be noisier.

GRPO eliminates the value function entirely, using group-normalized rewards. This suggests the commitment signal might be harder to extract from GRPO-trained models than from PPO-trained ones. The distinction between process and outcome reward modeling {% cite kumar2025llm %} maps onto the reward design: terminal-only (outcome) vs. per-step (process). The initial plan uses terminal-only, the simpler case.

The maximum-entropy RL perspective unifies all these methods. The soft Bellman equation {% cite todorov2007linearly haarnoja2018soft fox2016tutorials %} is the fixed-point equation whose solution gives the optimal policy as a softmax over soft $Q$-values. Ziebart's maximum-entropy inverse RL {% cite ziebart2008maximum %} shows that the reward can be recovered from observed behavior, which is what the tilt field does. Jaynes' principle {% cite jaynes1957information %} provides the variational foundation: the least-committal distribution consistent with the expected reward constraint is the Gibbs distribution, and the Lagrange multiplier is the temperature.

## What this programme buys

Even if the Landau transition does not exist or is not universal, the programme produces three things of value.

First, a *gauge-invariant observable suite* for autoregressive generation: the arrow of time $\Delta\Sigma$, the intensive dissipation $\sigma_\pm/T$, the Fisher--Rao speed, the logit margin, and the negentropy. These are well-defined for any model and can be used as diagnostic tools regardless of whether the free-energy interpretation holds.

Second, a *bridge methodology* between base and aligned models, placing them on a single tilt-family axis parameterized by $\beta_{\mathrm{eff}}$. If the bridge works, it means we can compute "the Blondel $V_q$" for base models as $V_t^\beta$ and compare directly with aligned models. If it does not, we learn that RLHF reshapes rather than tilts the landscape, which is itself an important result.

Third, a *scale-resolved picture* of how lookahead capability emerges during pretraining. The Pythia checkpoint axis lets us watch $V_q$ learning emerge with training steps, not just with model size. If the commitment transition sharpens during training, it is evidence that the model is learning to be an energy-based model---in Blondel's language, that the ARM is learning to secretly be an EBM.

The look-ahead was always inside the logits. The question is whether we can measure it, and whether the measurement reveals a phase transition or just a smooth crossover. That is the empirical frontier.

---

## References

{% bibliography --cited %}
