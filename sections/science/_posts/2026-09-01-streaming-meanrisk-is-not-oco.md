---
layout: post
title: Incremental moments, full solves
description: "skfolio 1.0 online_predict and MeanRisk.partial_fit carry exponentially weighted moments and still rebuild the convex program. That is streaming Markowitz, not online convex optimization."
date: 2026-09-01
published: true
categories:
  - science
  - machine-learning
---

*Post 4 of 6. Previous: [Binding cross-validation to solver structure]({% link sections/science/_posts/2026-08-31-skfolio-accelerate-compiled-trajectories.md %}). Next: [First-order OCO as a portfolio estimator]({% link sections/science/_posts/2026-09-02-first-order-oco-and-olps-in-skfolio.md %}).*

1.0 added a page titled "Online Learning" (`docs/user_guide/online_learning.rst`) and four public names: `online_predict`, `online_score`, `OnlineGridSearch`, `OnlineRandomizedSearch`. The changelog lists `partial_fit` on `EWMu`, `EWCovariance`, `EmpiricalPrior`, `CharacteristicsFactorModel`, and `MeanRisk`. If you arrive from the OLPS literature {% cite hazan2016introduction li2014online %} those names will mislead you for a week. This post is the corrective: what 1.0 actually incrementally updates, what it still solves from scratch, and why an OLPS PR should *hook* this evaluation API rather than invent a parallel one.

## The stateful walk

All four utilities share a loop.

1. `clone` the estimator once, unfitted.
2. `partial_fit` on the first `warmup_size` rows.
3. Evaluate on the next test window, with an optional purge gap between data the estimator has seen and the window you score.
4. `partial_fit` the newly observed rows into the *same* instance.
5. Repeat until the sample ends.

Standard `cross_val_predict` clones and refits from scratch at every fold. Here the estimator is a single object that ages. For portfolio optimizers, scores are not an average of per-fold Sharpes. Short test windows make a per-fold Sharpe undefined (one observation, no variance). `online_predict` concatenates out-of-sample `Portfolio` pieces into one `MultiPeriodPortfolio` and computes the measure on that path. That scoring choice is the good part of the 1.0 design, and it is one OLPS wants: wealth is a path functional.

`online_score` also accepts non-predictor estimators (covariance, priors). Those are scored per test window by a callable `scorer(estimator, X_test)`, typically `make_scorer(..., response_method=None)`, then averaged. `online_covariance_forecast_evaluation` is a third cousin: Mahalanobis calibration, diagonal calibration, portfolio QLIKE against realized returns. None of this is Helmbold.

Pipelines are unsupported. Pre-selection and imputation in a `Pipeline` have no `partial_fit` protocol in this workflow. NaN-aware moment estimators are the intended way to handle a changing universe. An OLPS estimator that wants the same evaluation should be a single `BaseOptimization` step, not a pipeline.

A WalkForward with `train_size=252`, `test_size=21` and streaming `online_predict(..., warmup_size=252, test_size=21)` can look identical in a calendar plot and still differ in $$\theta$$. WalkForward refits empirical $$(\mu,\Sigma)$$ on each rolling window (or, with `expand_train=True`, on a growing prefix) from a *clone*. `online_predict` never clones after the first construction: EW moments at date $$t$$ are a function of the entire warmup-plus-observed path, with exponential decay, and the convex program is the MeanRisk instance that has been living since day 0. If you need "the same estimator the desk would have had at date $$t$$ given only data $$\le t$$", both can be causal. They are still different filters of the past.

## What MeanRisk.partial_fit does

Default `MeanRisk()` cannot `partial_fit`.{% fn %} `EmpiricalMu` and `EmpiricalCovariance` have no incremental API. The documented pattern is

```python
from skfolio.moments import EWMu, EWCovariance
from skfolio.optimization import MeanRisk
from skfolio.prior import EmpiricalPrior

model = MeanRisk(
    prior_estimator=EmpiricalPrior(
        mu_estimator=EWMu(half_life=40),
        covariance_estimator=EWCovariance(half_life=40),
    )
)
```

`half_life` replaced `alpha` in 1.0; migration notes matter when rebasing the branch.

On each `partial_fit` call MeanRisk:

- does **not** reset the estimator (`fit` does);
- requires the prior (and uncertainty sets, if any) to implement `partial_fit`;
- forbids `efficient_frontier_size`;
- allows fallback `"previous_weights"` only, not a list of other estimators;
- calls the prior's `partial_fit`, then runs the same `_fit` path as batch: new `cp.Variable`, new `cp.Problem`, full Clarabel/OSQP solve.

In the notation of post 1:

$$
\theta_{t+1} = \mathcal U(\theta_t, r_{t+1}),
\qquad
w_{t+1} = \arg\min_{w\in K} f(w;\theta_{t+1}).
$$

$$\mathcal U$$ is an EW update of $$\mu$$ and $$\Sigma$$ (and whatever else the prior owns). The second line is still a global empirical program. There is no proximal restriction toward $$w_t$$. There is no regret. If the solver fails and `raise_on_failure=False`, `online_predict` records a `FailedPortfolio` and continues; with `fallback="previous_weights"` the last valid allocation is the next reference. Other fallback estimators are banned because they would not have been trained on the same stream.

Compare accelerate (post 3). Accelerate keeps $$\theta$$ as a sliding *empirical* Gram and reuses a compiled $$P$$ to hit the same $$w^\star$$ as batch `fit` on that window. Streaming MeanRisk changes the *definition* of $$\theta$$ (EW, expanding history) and still pays a full compile+solve. They are not nested. You cannot "turn on accelerate" inside `online_predict` without proving that the compact engines know EW moments and that $$T$$ in the cone is either fixed or cheaply updated. Today they do not.

For a 1-homogeneous risk (MAD, CVaR with a fixed scenario length) you could imagine compiling once. EW covariance with a changing effective sample size is already a different $$P$$ every day: the quadratic term moves, and for scenario risks the row count of $$R$$ grows unless you cap history. 1.0 `partial_fit` does not cap. That is why I keep repeating "full solve". It is not an implementation oversight. The shipped semantics *are* "new empirical program on the updated prior."

## Online search is expanding-window model selection

`OnlineGridSearch` / `OnlineRandomizedSearch` walk each candidate along one sequential path with `partial_fit`. Conceptually this is GridSearchCV plus `WalkForward(expand_train=True)`, minus the refit-from-scratch. When `refit=True`, `best_estimator_` is the candidate that already ingested the full sample during evaluation. For covariance estimators the score is often QLIKE; for portfolios it is a `BaseMeasure` on the concatenated path. Multi-metric search needs an explicit `refit=` key.

This is a legitimate way to tune an EW half-life. It is a dangerous way to tune an OLPS learning rate if you forget that `partial_fit` on `FollowTheWinner` *replays* a row as a trading round. Expanding-window `fit` on overlapping train prefixes would show AdaGrad accumulators the same gradient twice.{% fn %} The branch grew a private `online_walk_forward_predict` that warns about this. 1.0's `online_predict` already has the cleaner protocol: warmup once, then one pass over the remainder. The PR should use that and delete the private helper, or keep it unexported.

## Two meanings of `partial_fit`

sklearn's `partial_fit` is overloaded in this library now.

On moment estimators it means: update sufficient statistics, remain a fitted transformer/prior.

On MeanRisk it means: update the prior, then **solve the batch convex program again**.

On `OnlinePortfolioSelection` (the branch) it means: consume **one** return row, charge costs against drifted holdings, take one OCO or PA step, set `weights_` to the allocation you will trade *next*. `fit(X)` is a for-loop of that. The docstring says it explicitly: no gradient aggregation across the matrix, no multi-epoch training.

A user who writes

```python
online_predict(MeanRisk(prior_estimator=ew_prior), X, warmup_size=252, test_size=21)
online_predict(FollowTheWinner(strategy="eg"), X, warmup_size=252, test_size=21)
```

has the same evaluation harness and two algorithms. The first produces, at each rebalance, a Markowitz (or CVaR, …) book from the current EW moments. The second produces a multiplicative-weights book from the cumulative log-loss gradient. Document that in the first paragraph of the OLPS user guide, with a link to `online_learning.rst`, or the issue tracker will fill with "EG does not match MeanRisk.partial_fit."

## What OLPS should reuse

Hook the evaluation, not the solver.

- `partial_fit` as the streaming verb, one row for OLPS, mini-batch allowed only if you define what a mini-batch means (I would not, in the first PR).
- `online_predict` for walk-forward out-of-sample paths without clone-per-fold.
- `FailedPortfolio` / `raise_on_failure` behaviour already specified for optimizers.
- `needs_previous_weights` when costs or turnover are on, so `_run_path` in *batch* `cross_val_predict` stays sequential. OLPS also has internal drifted holdings; those are not the same object (post 5). `set_params(previous_weights=...)` on a clone is how 1.0 threads economic state in CV. An OLPS estimator that ignores `set_params` will look fine in `fit_predict` and break in `_run_path`.

Do not add a public `online_walk_forward_predict`. Do not teach people to score OLPS with `predict(X)` on the same $$X$$ they fitted: that applies the *final* $$w_T$$ to the whole history (lookahead). 1.0 MeanRisk `predict` after `fit` is correct for a frozen batch book. The same method on an online estimator is a trap. `fit_predict` on the branch already returns a `MultiPeriodPortfolio` of per-period books. `predict_online` is a deepcopy plus `warm_start` plus `fit_predict` for a continuation of a fitted instance. Those two names have to be in the gallery, above the fold.

## Implication for the 1.0 PR

Streaming MeanRisk stays. It is a shipped 1.0 feature with examples (`examples/online_learning/plot_3_online_portfolio_optimization_evaluation.py`). The OLPS PR adds a second family of estimators that speak `partial_fit`. The user-guide split:

- `online_learning.rst` — incremental *statistics* and repeated convex solves (existing).
- a new `olps.rst` (or `optimization/online.rst`) — incremental *decisions* with regret (new), opening with a glossary and a link back.

If a later accelerate issue wants to compile the streaming MeanRisk loop, the missing pieces are EW sufficient statistics (not just empirical Grams) and a cone whose $$T$$ is either constant or updated. That work does not belong in the OLPS diff.

{% footnotes %}
{% fnbody %}Default empirical moments on MeanRisk still have no partial_fit in 1.0. Anyone filing "online MeanRisk is broken" after constructing MeanRisk() has hit this gate.{% endfnbody %}
{% fnbody %}AdaGrad / SWORD accumulators are functions of the ordered gradient sequence. Replaying a prefix, then playing it again inside an expanding window, is a different algorithm from a single prequential pass. The private helper on the branch documents this; 1.0 online_predict avoids it by never refitting prefixes.{% endfnbody %}
{% endfootnotes %}

---

# References

{% bibliography --cited %}
