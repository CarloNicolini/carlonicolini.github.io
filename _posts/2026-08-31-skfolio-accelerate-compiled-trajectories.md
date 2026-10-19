---
layout: post
title: Binding cross-validation to solver structure
description: "How skfolio-accelerate compiles a CV plan once, slides empirical Grams, and reuses OSQP/Clarabel topology without changing the MeanRisk investment problem."
date: 2026-08-31
published: true
permalink: "/sections/science/2026/08/31/skfolio-accelerate-compiled-trajectories.html"
categories:
  - science
  - finance
  - math
  - engineering
---
*Post 3 of 6. Previous: [MeanRisk as a parametric convex program]({% link _posts/2026-08-30-meanrisk-as-parametric-convex-optimization.md %}). Next: [Incremental moments, full solves]({% link _posts/2026-09-01-streaming-meanrisk-is-not-oco.md %}).*

Post 2 left MeanRisk as $$w^\star(\theta)=\arg\min_{w\in K}f(w;\theta)$$, with 1.0 reconstructing $$f$$ from scratch on every WalkForward fold. `skfolio-accelerate` is a drop-in for `skfolio.model_selection.cross_val_predict` that keeps that same $$w^\star$$ and attacks the reconstruction. It is not an online estimator. If you remember one architectural sentence: reuse is local to one call, and anything that would change the investment problem is refused.

I care about this tree in a series on OLPS because it is the existence proof that consecutive MeanRisk programs are a trajectory. The 60× numbers are for variance. They are also a warning: the gain is QP structure plus overlapping windows, not a general theory of "online solvers."

## The call, classified

`cross_val_predict(estimator, X, cv)` in `src/skfolio_accelerate/predict.py` starts with `classify_call`. Four backends, plus native sklearn as an escape:

1. `osqp` — boxed mean-variance QP (`MinVarianceOSQP`)
2. `clarabel` — scenario LP / QP / SOC / exponential cone
3. `closed-form` — default `EqualWeighted`, `Random`, `InverseVolatility`
4. `fit-assemble` — clone, native `fit`, assemble test portfolios from `weights_`
5. `sklearn` — unmodified skfolio `cross_val_predict`

`backend="auto"` walks that list. `backend="compact"` raises if the estimator is ineligible instead of falling through.

The gates are boring on purpose. Compact MeanRisk needs the default empirical prior, `MINIMIZE_RISK` or `MAXIMIZE_UTILITY`, an equality budget, scalar or array bounds (not dicts), $$\ell_1=0$$, `raise_on_failure=True`, `save_problem=False`. Variance may use OSQP or Clarabel; scenario risks must be Clarabel. Risk limits, groups, MIP, uncertainty sets, `MAXIMIZE_RATIO`, custom `solver_params`, pipelines, `n_jobs ∉ \{None,1\}`, shuffled splitters, `efficient_frontier_size`: compact blocked. Some of those still get `fit-assemble` (native solve, skip joblib and `predict()` construction). Sequential `previous_weights` (costs, turnover, previous-weight fallback) go all the way to `sklearn`, because folds are then economically coupled.

That last gate is the economic/numerical split from post 1, enforced in code. I will come back to it after the three amortizations.

## Amortization 1: the CV plan

`compile_cv_plan(cv, X)` is the only place that iterates `splitter.split`. It returns an immutable `CVPlan`: kind, a list of `FoldSpec`, optional CPCV fold-blocks, a `path_batches()` iterator.

| `plan.kind` | Splitter | Paths | How moments move |
|---|---|---|---|
| `walk_forward` | `WalkForward` | 1 | contiguous sliding Gram |
| `kfold` | `KFold` / `TimeSeriesSplit` / int | 1 | indexed add/remove if windows overlap |
| `cpcv` | `CombinatorialPurgedCV` | many | precomputed fold-block Grams, purge/embargo subtracted |
| `mrc` | `MultipleRandomizedCV` | many | per-path session; columns sliced once |

`FoldSpec` carries `train_idx`, `test_idx`, `test_segments`, `path_ids`, optional `asset_idx`. Mutable RNGs inside a splitter are consumed once. Native fallback keeps a `deepcopy(cv)` taken *before* compilation, so a retry does not see a spent `RandomState`.

This is already a change of abstraction. 1.0 WalkForward *is* a Python generator of index pairs, each pair spawning `fit`. Accelerate *names* the trajectory and then walks it with a session object. Combinatorial purged CV {% cite lopezdeprado2018advances %} is the annoying case that makes the plan worth having: training sets are unions of fold blocks minus purge/embargo, so you want $$n_{\mathrm{folds}}$$ block Grams, not $$n_{\mathrm{splits}}$$ full $$X^\top X$$.

## Amortization 2: sufficient statistics

`OverlapMomentCache` stores

$$
n,\quad
s=\sum_{t\in\mathrm{train}} r_t,\quad
G=\sum_{t\in\mathrm{train}} r_t r_t^\top
$$

and forms

$$
\mu = s/n,
\qquad
\Sigma = \bigl(G - s s^\top / n\bigr) / (n-1)
$$

when a solver asks. That is `numpy.cov(..., ddof=1)` and skfolio's empirical covariance *before* nearest-PD projection. The compact path skips the projection. Tests treat this as a contract: it matches native when the sample $$\Sigma$$ is already PD, which is the intended regime $$T>n$$.{% fn %}

A WalkForward slide of $$k$$ rows is exact rank-$$k$$:

$$
G \leftarrow G - R_{\mathrm{drop}}^\top R_{\mathrm{drop}} + R_{\mathrm{add}}^\top R_{\mathrm{add}},
\qquad
s \leftarrow s - R_{\mathrm{drop}}^\top\mathbf{1} + R_{\mathrm{add}}^\top\mathbf{1}.
$$

Updates are applied to *copies* of $$(s,G)$$. After many slides, cancellation can nibble positive-definiteness; OSQP then retries with $$10^{-10}$$ diagonal jitter. No extra shrinkage is introduced. Tests lock WalkForward to 1 cold Gram + $$(n_{\mathrm{splits}}-1)$$ updates, and purged CPCV to $$n_{\mathrm{folds}}$$ block Grams + $$n_{\mathrm{splits}}$$ updates.

Scenario risks set `keep_returns=True` and keep the training window (a view when rows are contiguous). CVaR still needs $$R$$, not just $$(\mu,\Sigma)$$. The moment cache cannot make a cone smaller; it can only avoid rebuilding $$R^\top R$$ when you did not need it.

`is_default_empirical` is the kill switch: `assume_centered`, `ddof\neq 1`, `window_size`, log-normal, investment horizon, `max_history`, or a non-empirical mu/covariance estimator → compact blocked. Incremental *statistics* are not a different estimator. If you wanted EW covariance in this loop you would be in post 4, and you would still be solving a full program.

## Amortization 3: frozen topology

Module comment in `compact.py`: topology (cone types and sparsity) is reused while $$(n_{\mathrm{assets}}, T)$$ stay constant. Numeric returns and covariance are the fold-varying data. Solver objects die with the `cross_val_predict` call. There is an `@lru_cache` only for CSC index patterns of a dense upper triangle, never for numeric matrices.

**Variance / `MinVarianceOSQP`.** `setup()` once with a dummy dense-upper $$P$$ so the nnz pattern is frozen. Each fold:

$$
P \leftarrow 2\cdot\mathrm{scale}\cdot\Sigma + 2\ell_2 I,
\qquad
q \leftarrow \text{linear term from utility, if any}.
$$

Then `prob.update(Px=..., q=...)`. If `warm` and a previous iterate exists, `warm_start(x, y)` and increment `n_warm_starts`. If `warm=False` but an iterate exists, it **zeros** $$x,y$$, because OSQP would otherwise carry them across `update` {% cite stellato2020osqp %}. Failed solve: jitter the diagonal and retry.

The first fold of a path is always cold. MRC paths share one OSQP topology across asset subsets for variance, but *disable* the first warm start of each path on purpose. Clarabel workspaces are never shared across MRC paths: there is no supported cold-start reset, so a leftover interior point can leak between subsets. That comment in `predict.py` is worth more than a page of ADMM theory. Numerical state is reusable only when you can prove the next problem is the same cone with new data.

**CVaR / `CVaRClarabel`.** Fixed CSC pattern for $$\alpha+\sum u/(T(1-\beta))$$ and $$Rw+\alpha+u\ge 0$$. Each fold writes $$-R$$ into precomputed column slices and tries `solver.update(A=...)`.

**Other scenario risks / `ScenarioClarabel`.** Weaker. Every `solve` rebuilds sparse $$P,q,A,b$$ and cones from Python lists, then `_clarabel_try_update`. If Clarabel refuses the update, a new `DefaultSolver`. Presolve, chordal decomposition, and dropzeros are disabled so updates stay legal. `n_warm_starts` here counts successful *data* updates, not OSQP-style primal/dual iterates.

`EngineCache` keys on $$(n_{\mathrm{assets}}, T)$$ and rebuilds when either changes. For WalkForward with a fixed window length that key is constant. For expanding windows it is not; you pay a new factorization when $$T$$ grows. Nobody should advertise a single speedup factor.

## What the 20-year table actually says

Synthetic $$5040\times 20$$ daily returns, native `n_jobs=1`, median of three isolated-process runs, skfolio 1.0.0:

| Risk | WalkForward (228 solves) | MRC (480) | CPCV (6) |
|---|---:|---:|---:|
| Variance | 60.6× | 76.9× | 11.8× |
| Semi-variance | 2.3× | 3.0× | 0.98× |
| MAD | 2.3× | 3.1× | 1.1× |
| CVaR | 3.3× | 4.1× | 1.1× |
| Max drawdown | 2.2× | 2.6× | 1.1× |

Path Sharpe differences stay in the $$10^{-5}$$–$$10^{-16}$$ range on that table; ranking tests (`precision@k`, Spearman) exist because a 4e-5 Sharpe gap can still reorder a grid.

Read the table as three sentences. Variance wins because QP structure plus OSQP warm start plus Gram slides dominate hundreds of overlapping windows. Scenario MeanRisk is 2–4× because Clarabel still rebuilds a large cone; when you only have six CPCV solves the overhead can exceed the saving. EqualWeighted's 5–13× on tiny problems is the joblib/`predict()` tax, a constant per fold, which is why it looks like a miracle on $$T=120$$ and a rounding error on a cone that already dominates.

Peak RSS matches native on these sizes: importing Python and skfolio is the memory. The interesting remaining question is a 10,000-asset QP with a persistent factorization, which this package does not claim.

## Economic state versus numerical state

Compact engines assume costs, fees, and a nonzero risk-free rate are identically zero. `previous_weights` set → compact blocked. `transaction_costs ≠ 0` or `max_turnover` set → usually `sklearn`, because `needs_previous_weights` makes folds sequential. Management fees alone can still `fit-assemble`: fees are copied onto the `Portfolio` object after a native `fit`.

OSQP's `warm_start` is numerical. `previous_weights` in MeanRisk is economic: it appears inside $$c^\top|w-w_{\mathrm{prev}}|$$. Using yesterday's primal as today's initial point does not insert yesterday's holdings into the objective. Using yesterday's holdings as today's `previous_weights` *does*. The notes insisted on that split; accelerate implements it by refusal rather than by a more clever engine. I think that is the correct 1.0 posture. A compact formulation of $$\lambda\|w-w_{\mathrm{held}}\|_1$$ is a new program, with a new test against native skfolio's sequential `_run_path`. It is not a warm-start flag.

MRC's zero-reset of OSQP when `warm=False` is the same doctrine on the numerical side. A leftover dual from a 15-asset subset is not a hint for a different 15-asset subset. Continuation needs a *reason* the active set is comparable.

## Assembly even when the solver is native

Native `cross_val_predict` clones, `safe_split` copies, wraps `n_jobs=1` in joblib, and constructs a `Portfolio` via `predict()` every fold. `fit-assemble` and closed-form skip that. HRP, standard deviation, Gini, ratio objectives still call `MeanRisk.fit` / `HierarchicalRiskParity.fit` and then assemble. Speedups of 1.05–2.1× are that tax cut. Pipelines stay on sklearn because `predict` is no longer "apply `weights_` to a test slice" in a way the assembler understands.

`grid_search` is a sibling: a compact MeanRisk grid, score from weights (mean OOS Sharpe), construct only the winning `MultiPeriodPortfolio`. General estimators still use sklearn/skfolio search.

## Implication for the 1.0 PR

Accelerate is evidence. It is not the OLPS implementation, and it should not be imported into `skfolio.optimization`. A reviewer who is told "we also wrote a C ADMM so WalkForward can continue duals" will ask for the table above, notice that OSQP already continues duals, and ask why scenario risks are 3×. Those are fair questions for an accelerate issue. They are noise on an OLPS PR.

If something from this tree belongs near skfolio later, it is the *idea* of compiling a CV plan once and the *discipline* of not reusing solver state across unrelated problems. `online_predict` in 1.0 already carries estimator state on purpose; that is a different, documented contract (post 4). OLPS `partial_fit` carries a small primal (and, for FTRL, a gradient sum). None of these should share a cache.

{% footnotes %}
{% fnbody %}When sample $$\Sigma$$ is indefinite, native skfolio may project; compact OSQP may jitter. Parity tests use Sharpe rtol around $$10^{-3}$$ and weight atol from $$5\cdot 10^{-4}$$ (variance) down to $$2\cdot 10^{-5}$$ (most scenario measures).{% endfnbody %}
{% endfootnotes %}

---

# References

{% bibliography --cited %}
