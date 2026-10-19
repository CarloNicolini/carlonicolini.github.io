---
layout: post
title: First-order OCO as a portfolio estimator
description: "How the universal_portfolio branch implements COMID, EG/OGD, follow-the-loser PA, BCRP as a MeanRisk comparator, and which pieces belong in a first skfolio 1.0 PR."
date: 2026-09-02
published: true
permalink: "/sections/science/2026/09/02/first-order-oco-and-olps-in-skfolio.html"
categories:
  - science
  - finance
  - math
---
*Post 5 of 6. Previous: [Incremental moments, full solves]({% link _posts/2026-09-01-streaming-meanrisk-is-not-oco.md %}). I assume the 2025 post [Introducing skfolio new online convex optimization module]({% link _posts/2025-10-03-Introducing-skfolio-online-convex-optimization.md %}) for mirror-map intuition. Next: [What a research PR to skfolio 1.0.0 actually contains]({% link _posts/2026-09-03-landing-olps-on-skfolio-1.md %}).*

The branch at `~/workspace/skfolio` on `universal_portfolio` is an Online Convex Optimization engine for portfolio selection {% cite hazan2016introduction orabona2019modern li2014online %}, wired through `BaseOptimization`. It is not Cover's mixture over CRPs {% cite cover1991universal %}; that module was deleted. Public imports today:

```python
from skfolio.optimization.online import (
    FollowTheWinner, FollowTheLoser, BCRP, UCRP, CRP, BestStock, regret, RegretType,
)
```

`optimization/__init__.py` still does not re-export them. `FirstOrderOCO`, mirror maps, and projectors are internal. That split is the one I would keep for 1.0.

## The engine

`FirstOrderOCO` in `_foco.py` is a COMID step {% cite duchi2010composite mcmahan2011follow xiao2010dual %}. Given a mirror map $$\psi$$, a projector onto $$K$$, a step-size schedule $$\eta_t$$, optional gradient predictor, and a mode:

OMD

$$
x_{t+1}
=
\arg\min_{x\in K}
\bigl\{
\eta_t\langle g_t, x\rangle + D_\psi(x, x_t)
\bigr\}.
$$

FTRL (as implemented: $$\eta$$ on the linear term)

$$
x_{t+1}
=
\arg\min_{x\in K}
\bigl\{
\eta_t\sum_{s=1}^t \langle g_s, x\rangle + \psi(x)
\bigr\}.
$$

The helper `_composite_update` solves the dual form $$z=-\eta g + \nabla\psi(x_{\mathrm{center}})$$ (centre absent in FTRL), then $$x=\nabla\psi^*(z)$$, then `project_geom`, then the external `projector`. Dynamic maps (AdaGrad diagonal) use `grad_psi_after` / `grad_psi_star_after` so the metric $$H_{t+1}$$ is the one Orabona's notes want. Burg/PROD bypasses $$\nabla\psi^*$$ and solves a scalar dual for the simplex constraint (`constrained_inverse`).

Optimistic updates follow the Rakhlin–Sridharan effective gradient $$g_{\mathrm{eff}}=g_t-\tilde g_t+\tilde g_{t+1}$$. In OMD the full $$g_{\mathrm{eff}}$$ enters the proximal step. In FTRL the prediction is added to the cumulative sum. `discount` implements $$G_t=\gamma G_{t-1}+g_t$$. `SwordMeta` is exponential weights over expert engines; it is research code and should not be public in the first PR.

Default log-wealth loss on net returns $$r_t$$, relatives $$x_t=\max(1+r_t,10^{-12})$$:

$$
\ell_t(w)=-\log(w^\top x_t)=-\log(1+w^\top r_t),
\qquad
\nabla\ell_t(w)=\frac{-r_t}{1+w^\top r_t}.
$$

The analytic gradient lives in `_autograd_objectives.py`. `use_autograd=True` is a debug switch. Shipping `autograd>=1.6` as a hard 1.0 dependency for a path the default does not use is how you pick a fight with the PR template.

## Geometries the first PR can defend

| `strategy` | $$\psi$$ | Default mode | Closed form |
|---|---|---|---|
| `eg` | $$\sum w_i\log w_i$$ | FTRL | softmax / multiplicative {% cite helmbold1998line %} |
| `ogd` | $$\tfrac12\|w\|_2^2$$ | FTRL | Euclidean step + project |
| `prod` | $$-\sum\log w_i$$ | Burg path | Soft-Bayes {% cite orseau2017soft %} |

`learning_rate="auto"` for EG is $$\eta_t=\sqrt{\log n/(t+1)}$$ (`theory`; `moderate` and `empirical` multiply by constants). OGD uses a diameter/gradient-bound schedule. These are the identities tests should lock: EG on the simplex is multiplicative, OGD is a projected gradient step, FTRL with entropy reproduces EG.

McMahan's FTRL–OMD equivalence {% cite mcmahan2011follow %} is the reason one engine can expose `mode="omd"` and `mode="ftrl"`. The tests on the branch already check that entropy FTRL matches EG's multiplicative form on a short synthetic path. That test is the reviewable heart of `_foco.py`. If it fails after the rebase onto 1.0, the PR is not ready, no matter how pretty the gallery looks.

AdaGrad, SWORD, Ada-BARRONS are implemented. They are also the part of the 2025 post that a maintainer cannot review without a paper. Out of the first diff. Tsallis maps exist and are not wired to any `FTWStrategy`. Deprecated `AdaptiveLogBarrierMap` should stay unpublished.

## Chronology, or why costs are not `previous_weights`

`OnlinePortfolioSelection.partial_fit` accepts one row. The user-guide chronology is the economic state machine:

1. Start period $$t$$ with drifted holdings $$\tilde w_{t-1}$$.
2. Rebalance into the already-chosen traded book $$w_t$$.
3. Charge costs on $$\|w_t-\tilde w_{t-1}\|_1$$.
4. Observe relatives $$x_t$$.
5. Update wealth $$W_{t+1}=W_t\cdot(w_t^\top x_t^{\mathrm{net}}-c^\top|w_t-\tilde w_{t-1}|)$$.
6. Drift $$\tilde w_t \propto w_t\odot x_t$$.
7. OCO (or PA) produces $$w_{t+1}$$.

`all_weights_[t]` stores the **traded** $$w_t$$. `max_turnover` constrains $$\|w_{t+1}-w_t\|_1$$ against the last trade. Costs use the drifted book. MeanRisk's `previous_weights` (post 2) is a third object: a parameter on a batch program, defaulting to zeros if unset, so the first buy is costed from cash. OLPS, if `previous_weights` is omitted, treats the first trade as a starting book and does not invent an entry cost.{% fn %}

I would keep both conventions and write them in the user guide with the numerical example already in `docs/user_guide/online.rst` ($$w=(0.5,0.5)$$, $$x=(1.1,1.0)$$, drift to $$(0.5238,0.4762)$$). Reviewers who have only used MeanRisk will otherwise "fix" OLPS to cost from zero.

`fit` is a row loop of `partial_fit`. `warm_start=False` calls `_reset_state_for_fit`. `predict` is inherited from `BaseOptimization` and applies **final** `weights_` to whatever `X` you pass: lookahead if that $$X$$ is the training stream. `fit_predict` is overridden and returns a `MultiPeriodPortfolio` of one-row `Portfolio`s using `all_weights_[t]`. `predict_online` deep-copies, keeps `warm_start`, and `fit_predict`s. Gallery code must call `fit_predict`, not `predict`. I already made that mistake in an early draft of the 2025 post's mental model; the code is the spec.

## Follow-the-loser is a different proximal problem

Li–Hoi FTL methods {% cite li2012pamr li2015olmar li2013cwmr %} are default **passive-aggressive**, `update_mode="pa"`, not `FirstOrderOCO`. OLMAR wants a predicted relative $$\phi$$ (SMA or EWMA) to satisfy $$\phi^\top w\ge\varepsilon$$. PAMR wants $$w^\top x\le\varepsilon$$ (penalize yesterday's winners). RMR is OLMAR with an L1-median predictor. CWMR puts a Gaussian around $$w$$ and enforces a probability margin.

The PA step is

$$
w_{t+1}
=
\arg\min_{w\in K}
\tfrac12\|w-w_t\|_2^2
\quad\text{s.t. a linear margin on }w,
$$

which collapses to a closed-form step along a centred direction plus a projection. `update_mode="md"` routes FTL through FOCO with hinge / squared-hinge / softplus. The CWMR docstring calls the MD path experimental. First PR: PA only.

FTL is outside the $$O(\sqrt{T\log n})$$ log-loss guarantee. It is in the Li–Hoi survey as a family that *works* on daily equity mean reversion. That is a product reason to ship it, and a documentation reason not to claim sublinear regret for PAMR.

## BCRP is the code bridge

`BCRP` subclasses `MeanRisk`. With `objective_measure=LOG_WEALTH` it overwrites expected return with $$\sum_t\log((1+r_t)^\top w)$$ and solves a convex program: Kelly / Cover CRP in hindsight. Constraints, solver, `prior_estimator` are the convex stack from post 2. `UCRP` is $$1/n$$. `CRP` is user weights. `BestStock` is one-hot on the best log-wealth asset.

Static regret {% cite cover1991universal hazan2016introduction %}

$$
R_t = \sum_{s\le t}\bigl(\ell_s(w_s)-\ell_s(u)\bigr),
\qquad
\ell=-\log(w^\top x),
$$

with $$u$$ the BCRP (or a user comparator). The solver inside `_regret._solve_bcrp_constant` is Cover-style multiplicative weights on prefixes, not the Dirichlet integral. `RegretType.DYNAMIC_UNIVERSAL` builds a $$T\times n$$ CVXPY program with a path-length budget; fine for a notebook, not for a live loop, out of the first PR.

This is the only place OLPS should call MeanRisk: as a *hindsight* comparator, with an information set no causal strategy is allowed. Tests can check $$R_T\ge 0$$ on log-wealth (up to numerics) and that EG's average regret shrinks on a synthetic multiplicative-weights-friendly sequence. They should not check that EG Sharpe matches minimum-variance MeanRisk.

## Projection

`AutoProjector`: box plus budget, optional L1 turnover, via bisection (`project_box_and_sum`, `project_with_turnover`). The bisection is on a Lagrange multiplier for the sum constraint with clipping to $$[\ell_i,u_i]$$; it is the same algorithm you write on a whiteboard for "simplex with bounds". Groups, linear inequalities, tracking error, variance bounds fall through to a CVXPY `project_convex`. First PR can ship box+budget (+ turnover) with tests against a simplex projection identity, and leave the cvxpy projector as follow-up issue A. Shipping the full MeanRisk constraint language on day one duplicates `_get_weight_constraints` badly. A single random feasible point of MeanRisk, projected by OLPS, is a good future test; it is not a reason to block EG.

## Empirical caution, not a PR claim

The draft study in `paper/follow_the_winner_vs_follow_the_loser.md` found that at *daily* frequency, FTW methods sit next to UCRP, while FTL closes a large fraction of the BCRP–UCRP log-wealth gap; at *monthly* rebalancing the roles reverse, with a $$\sqrt{\Delta}$$ scaling of the EG weight deviation.{% fn %} I wrote about that in 2025. It is a reason to ship both families and to put rebalancing frequency in the gallery. It is not a theorem the PR must prove, and it is not a license to dump fourteen strategies into `optimization/__init__.py`.

## Export cut (repeated in post 6)

In: `FollowTheWinner(strategy="eg"|"ogd")`, `FollowTheLoser(..., update_mode="pa")` for `olmar`/`pamr`/`rmr`/`cwmr`, `UCRP`/`CRP`/`BCRP`/`BestStock`, `regret(..., STATIC)`, `fit` / `partial_fit` / `fit_predict` / `predict_online`, analytic log-wealth gradient, box+budget projector.

Internal: `FirstOrderOCO`, mirror maps, predictors, `SwordMeta`.

Out: SWORD, Ada-BARRONS, Tsallis, FTL MD, `objective=` path-risk on $$T=1$$, `DYNAMIC_UNIVERSAL`, Cover UP, CORN, `autograd` as required, public `online_walk_forward_predict`.

`prod` is a close call: small, tested, Burg is a genuine third geometry. I would still leave it to a second PR unless tests already make it free. Reviewers can only digest so many mirror maps.

{% footnotes %}
{% fnbody %}If you do pass previous_weights into an OLPS estimator, it is interpreted as the book already held before the first rebalance, so first-period costs and turnover are measured against it. That matches a live handoff from a previous strategy.{% endfnbody %}
{% fnbody %}The draft is not a submission. Use it as a caution about daily EG versus UCRP, and as a reason the gallery should show more than one rebalancing frequency. Cross-sectional gradient demeaning on the simplex is a no-op for entropy and Euclidean geometries; do not advertise it as a feature.{% endfnbody %}
{% endfootnotes %}

---

# References

{% bibliography --cited %}
