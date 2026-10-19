---
layout: post
title: From solving convex programs to tracking them
description: "A four-regime map from batch MeanRisk through skfolio-accelerate and 1.0 streaming MVO to true OLPS, written as study notes for a skfolio 1.0 PR."
date: 2026-08-29
published: true
permalink: "/sections/science/2026/08/29/from-solving-to-tracking-convex-programs.html"
categories:
  - science
  - finance
  - math
---
*Post 1 of 6. I already told the OLPS origin story in [Introducing skfolio new online convex optimization module]({% link _posts/2025-10-03-Introducing-skfolio-online-convex-optimization.md %}). This series sits next to that post. It is study material for landing a research PR on skfolio 1.0.0, not a second introduction to exponentiated gradient. Next: [MeanRisk as a parametric convex program]({% link _posts/2026-08-30-meanrisk-as-parametric-convex-optimization.md %}).*

skfolio 1.0.0 shipped in August 2026 {% cite nicolini2025skfolio %}. On my disk I now have three trees that look, if you read their READMEs in isolation, like they are arguing with each other. Mainline `MeanRisk` still builds a CVXPY problem {% cite diamond2016cvxpy %} from a training window and throws it at Clarabel. `skfolio-accelerate` claims that a WalkForward of those problems is mostly one compiled quadratic with sliding moments. The `universal_portfolio` branch treats the same simplex as an online convex optimization game {% cite hazan2016introduction orabona2019modern %} and never forms $$(\mu,\Sigma)$$ at all.

I wrote two internal notes after staring at that pile.{% fn %} One said: accelerate already exploits the overlap that online convex optimization exploits, only at a different semantic level. The other said: do not bury a C online solver inside accelerate; make a sequential convex runtime and let OLPS be one policy on top. Both notes are mostly right about the mathematics. Both overreach as a merge plan. The rest of this post is the map I wish I had before those notes, plus the cuts I now think a 1.0 PR can survive.

## A running example

Take twenty liquid equities, daily net returns $$r_t\in\mathbb{R}^n$$, long-only, fully invested:

$$
K = \{ w\in\mathbb{R}^n : w\ge 0,\; \mathbf{1}^\top w = 1 \}.
$$

At a rebalance date $$t$$ you may do either of two things that look similar in a backtest plot and are different programs.

The batch MeanRisk decision (minimum variance, default empirical prior) is

$$
w_t = \arg\min_{w\in K} \; w^\top \hat\Sigma_t w,
\qquad
\hat\Sigma_t = \mathrm{Cov}(r_{t-N:t-1}).
$$

The exponentiated-gradient decision {% cite helmbold1998line %} is

$$
w_{t+1,i} \propto w_{t,i}\,\exp(-\eta g_{t,i}),
\qquad
g_t = \nabla_w\bigl(-\log(1+w_t^\top r_t)\bigr) = \frac{-r_t}{1+w_t^\top r_t},
$$

with $$w_{t+1}$$ projected back onto $$K$$. You choose $$w_t$$ *before* $$r_t$$ is revealed. There is no $$\hat\Sigma_t$$.

If you evaluate both with `predict(X_test)` after a single `fit(X_train)`, you have already smashed the distinction. The first method is supposed to freeze $$w_t$$ on a held-out window. The second is supposed to rewrite $$w$$ every row. sklearn's `fit`/`predict` pair does not know which one you meant. That is the whole software problem, and it is why this series exists.

## Four regimes, not three

The notes drew a line

$$
\text{batch CVXPY}
\;\longrightarrow\;
\texttt{skfolio-accelerate}
\;\longrightarrow\;
\text{true OCO}.
$$

skfolio 1.0 already occupies a fourth slot they underweighted: `MeanRisk.partial_fit` together with `online_predict`. Incremental exponentially weighted moments, then a **full** convex rebuild. Streaming batch Markowitz {% cite markowitz1952portfolio %}, not online learning in the Hazan–Orabona sense.

<figure>
<img src="/assets/media/postfigures/skfolio_batch_to_olps_spectrum.svg" alt="Four regimes from batch MeanRisk to OLPS" style="width:100%; display:block; margin: 0 auto; margin-bottom: 0.5em;">
<figcaption>
The same long-only simplex, four decision rules. Accelerate changes how $$w^\star(\theta)$$ is computed along a trajectory of $$\theta$$. Streaming MeanRisk changes how $$\theta$$ is estimated. OLPS throws $$\theta$$ away.
</figcaption>
</figure>

Write $$\theta$$ for the statistical payload a convex estimator consumes: expected returns, covariance, scenario matrix, sample weights. Write $$P(\theta)$$ for the canonical convex program MeanRisk would send to a solver. Then the four rules are:

| Regime | Decision | State that actually persists | Evaluation in 1.0 |
|---|---|---|---|
| Batch MeanRisk | $$w_t=\arg\min P(\hat\theta(X_{\mathrm{train}}))$$ | none (clone per fold) | `cross_val_predict` + `WalkForward` |
| Compiled trajectory | the same $$w_t$$, cheaper $$\theta$$ and a frozen $$P$$ | Gram $$(n,s,G)$$, OSQP $$(x,y)$$ | same `MultiPeriodPortfolio` |
| Streaming MeanRisk | $$\theta_t\leftarrow\mathcal U(\theta_{t-1},r_t)$$, then $$\arg\min P(\theta_t)$$ | moments only; new `cp.Problem` | `online_predict` |
| OLPS | $$w_{t+1}=\mathcal A(w_t,\nabla\ell_t)$$ | weights, dual sums, drifted holdings | `fit_predict` / static regret |

The notes' boxed slogan is still the right first cut:

$$
\text{MeanRisk/WF}:\quad D_t \to P_t \to w_t
\qquad\text{versus}\qquad
\text{OCO}:\quad (w_t, \nabla\ell_t)\to w_{t+1}.
$$

Streaming MeanRisk is the hybrid they skipped: $$D_t$$ becomes incremental, $$P_t$$ is still a global empirical program.

## What the notes get right

Three layers of temporal structure, not one speedup trick.

**Data.** Consecutive WalkForward windows share almost every row. The sufficient statistics

$$
n=\#\{t\},\quad
s=\sum_t r_t,\quad
G=\sum_t r_t r_t^\top
$$

slide with a rank-$$k$$ add/drop. Accelerate already does this in `OverlapMomentCache`.{% fn %} That is the cheap map $$\theta_t\to\theta_{t+1}$$.

**Problem.** For boxed mean-variance the cone (here: a QP) has a fixed sparsity pattern while $$(n_{\mathrm{assets}}, T_{\mathrm{window}})$$ stay put. You can compile once and write new $$P,q$$. OSQP {% cite stellato2020osqp %} is built for that; Clarabel {% cite goulart2024clarabel %} is less so, which is why variance WalkForward is sixty times faster and CVaR is three.

**Solution.** The next optimiser often sits near the last one, because $$\theta$$ moved a little. Warm-starting the primal-dual iterate is continuation in disguise. It is *not* yet an online algorithm. The notes were careful here: an OCO step

$$
w_{t+1}
=
\arg\min_{w\in K}
\Bigl\{
\langle g_t, w\rangle
+
\tfrac1{\eta} D_\psi(w,w_t)
\Bigr\}
$$

intentionally *restricts* the move. Warm-started batch still tries to hit $$w^\star(\theta_{t+1})$$ exactly, using $$w^\star(\theta_t)$$ as a guess.

Two kinds of state, and they must not be fused. Economic state is the holdings you actually carry: `previous_weights`, L1 transaction costs, turnover, the drifted portfolio $$\tilde w_t \propto w_t\odot x_t$$ after relatives $$x_t=1+r_t$$. Numerical state is $$x,y$$, factorizations, active sets, Clarabel's interior point. If you reuse numerical state into a problem whose economic data changed (costs, a different asset subset, a leftover dual on a dead constraint), you have silently solved a different investment problem. Accelerate refuses that mix: nonzero `transaction_costs`, `max_turnover`, or `needs_previous_weights` fall through to native skfolio. That refusal is a design document, not a missing feature.

WalkForward as a trajectory. Let $$P(\theta)=\arg\min_w f(w;\theta)$$. A rolling backtest samples

$$
w^\star(\theta_1),\; w^\star(\theta_2),\;\ldots,\; w^\star(\theta_T)
$$

with $$\theta_{t+1}-\theta_t$$ small. The theoretical excuse for an accelerator is that you can *track* that path. The theoretical excuse for OLPS is that you may not want $$w^\star(\theta_t)$$ at all.

CVXPY as a frontend, solvers as consumers of canonical data. A C kernel should see $$(Q,p,A,b)$$ or a cone triple, never a `MeanRisk` object. Forcing `cp.OnlineSolver(MeanRisk(...))` inverts the dependency. I still believe that.

Do not pretend sequential semantics fit in `problem.solve()`. CVXPY's custom solver hook is one-shot: canonical data in, primal/dual out. A session API (`update_parameters`, `step`, persistent `state`) is a different object. The notes were right to keep those apart.

## Where they overreach

**Same state machine, different policy.** It is a pleasant slogan that continuation and FTRL are two policies over `step(P_t, S_t) → (x_t, S_{t+1})`. The sklearn contracts are not the same. Continuation must match `MeanRisk.fit` weights to numerical tolerance, because the investment problem is defined to be that convex program. FTRL must match a multiplicative update and a regret bound; matching MeanRisk weights would be a *bug*. Tests, information sets, and failure modes diverge immediately. Unifying them in one C ABI is a multi-year solver project. It is not the merge vehicle for 1.0.

**ADMM continuation as the next kernel.** OSQP *is* ADMM with a cached factorization and a warm start {% cite stellato2020osqp %}. `MinVarianceOSQP` already calls `warm_start(x, y)` on later folds. Writing another ADMM in C to "carry $$(w,z,u)$$" competes with a solver we already wrap. The gap that actually shows up in timings is Clarabel: scenario MeanRisk still rebuilds (or re-canonicalizes) a large cone, so CVaR/MAD/drawdown sit at 2–4× on the 20-year WalkForward and about 1× on a six-solve CPCV. If the research question is "track $$w^\star_t$$ with far fewer iterations", the first experiment is factorization reuse *inside* the engines we have, measured against those numbers. A greenfield ADMM is a later paper.

**Cover's universal portfolios.** The branch is named `universal_portfolio`. Cover's 1991 mixture over the simplex {% cite cover1991universal %} is not implemented as a trading estimator; the old `_universal` module was removed. What the branch actually contains is Helmbold EG, Euclidean OGD, Burg/PROD, Li–Hoi follow-the-loser (OLMAR, PAMR, CWMR, RMR) {% cite li2014online li2012pamr li2015olmar %}, and a `FirstOrderOCO` engine that unifies OMD and FTRL through a composite mirror step {% cite mcmahan2011follow duchi2010composite %}. Static regret's comparator is `BCRP`, which *is* a MeanRisk solve on log-wealth. That is the real code bridge. Promising Cover UP or CORN/BNN in a first PR would be fiction.

**Wrong first artefact.** Maintainers merge sklearn estimators: `fit`, `predict`, `clone`, `get_params`, tests next to `tests/test_optimization/`, a gallery example, an autosummary page. A standalone sequential cone library is a separate repository with a different audience (MPC, online LASSO, resource allocation). The four-box split in the second note is the right *long-term* map:

```
skfolio            portfolio semantics, MeanRisk, WalkForward
universal_portfolio  OLPS policies (this is the first PR)
skfolio-accelerate   portfolio-specific compiled CV
SequentialSolver     general stateful cone engine (not this year)
```

Only the first two boxes belong in a 1.0 pull request. Accelerate stays a research/bench tree until its compact engines are either upstreamed as an optional backend or left alone.

**The word "online" is already taken.** 1.0 documents `online_predict`, `online_score`, `OnlineGridSearch` in `docs/user_guide/online_learning.rst`. Those verbs mean: one stateful estimator, `partial_fit` on expanding observations, Sharpe (or QLIKE) on the concatenated out-of-sample path. The branch adds `skfolio.optimization.online` and a draft `online.rst` that mean Helmbold/Li–Hoi OLPS. A PR that blindly dumps the second user guide on top of the first will be rejected for naming, and it should be. The glossary has to ship in the first paragraph of the new page: two algorithms, one sklearn verb.

## Three execution levels, restated so they stay useful

Independent batch: solve $$P_t$$ from a cold start. This is `MeanRisk.fit` inside `cross_val_predict`.

Warm-started batch: solve $$P_t$$ using numerical state from $$P_{t-1}$$. This is accelerate's OSQP path, and, in a weaker sense, 1.0 `partial_fit` (moments persist, the CVXPY graph does not).

OCO: define $$P_t$$ itself as a local update from $$w_{t-1}$$. This is `FirstOrderOCO.step`.

A future C `step` could implement all three. Shipping all three as one public `OnlineSolver` in CVXPY is how you spend two years without a skfolio merge.

## What I am studying toward

The first PR is an estimator family on 1.0.0: `FollowTheWinner` (`eg`, `ogd`), `FollowTheLoser` in the default passive-aggressive mode, the CRP/UCRP/BCRP/BestStock benchmarks, static `regret`, `partial_fit` / `fit_predict`, box-plus-budget projection. `FirstOrderOCO` stays internal. `autograd` is not a required dependency; log-wealth already has an analytic gradient. SWORD, Ada-BARRONS, Cover UP, and a C sequential solver are follow-up issues with numbers attached, or they are out.

I will not replace `MeanRisk._fit` with an OCO loop. Batch Markowitz with CVaR, cardinality, entropy pooling, and ratio homogenization is the product. OLPS is a second computational regime that happens to share `BaseOptimization` and the simplex.

The remaining posts fill in the code that this map points at. Post 2 is what 1.0 MeanRisk actually solves. Post 3 is how accelerate binds a CV plan to a frozen QP. Post 4 is why `partial_fit` on MeanRisk is still a full solve. Post 5 is the OCO engine on the branch, assuming you have read the 2025 post. Post 6 is the maintainer-facing cut: rebase, in-list, out-list, tests, the `predict()` lookahead trap.

{% footnotes %}
{% fnbody %}The two notes live in the skfolio-accelerate tree as `notes-olps-batch-oco.md` and `approach-to-merge-olps-to-skfolio-accelerate`. They are working documents, not library docs.{% endfnbody %}
{% fnbody %}Default EmpiricalCovariance in skfolio can project to the nearest positive-definite matrix. Accelerate's Gram formula matches numpy.cov(..., ddof=1) before that projection. They agree when the sample covariance is already PD, which is the intended compact regime $$T>n$$.{% endfnbody %}
{% endfootnotes %}

---

# References

{% bibliography --cited %}
