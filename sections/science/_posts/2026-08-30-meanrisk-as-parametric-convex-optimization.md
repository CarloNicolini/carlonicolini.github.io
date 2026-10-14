---
layout: post
title: MeanRisk as a parametric convex program
description: "What skfolio 1.0 MeanRisk actually solves, why every fit rebuilds a CVXPY graph, and why WalkForward is a trajectory through θ rather than T unrelated estimators."
date: 2026-08-30
published: true
categories:
  - science
  - machine-learning
---

*Post 2 of 6 in [From solving convex programs to tracking them]({% link sections/science/_posts/2026-08-29-from-solving-to-tracking-convex-programs.md %}). Next: [Binding cross-validation to solver structure]({% link sections/science/_posts/2026-08-31-skfolio-accelerate-compiled-trajectories.md %}).*

MeanRisk is easy to describe badly. "It does mean-variance." It does, as a special case. The class is a factory for convex programs whose data $$\theta$$ come from a prior estimator and whose feasible set $$K$$ is assembled from a long list of optional constraints. If you want to track $$w^\star(\theta)$$ later, or replace the solve by an online step, you need the actual program. This post is that program, as 1.0.0 implements it in `src/skfolio/optimization/convex/_mean_risk.py` and `_base.py`.

## The parameter $$\theta$$

`fit(X)` does not see prices. $$X$$ is net returns, shape $$(T,n)$$. A `prior_estimator` (default `EmpiricalPrior()`) produces a frozen `ReturnDistribution`:

$$
\theta = (\mu,\; \Sigma,\; R)
$$

with $$\mu\in\mathbb{R}^n$$, $$\Sigma\in\mathbb{R}^{n\times n}$$, and $$R\in\mathbb{R}^{T\times n}$$ the scenario matrix used by path-dependent risks (CVaR, drawdowns, EVaR). Optional sample weights and a factor model ride along; they do not change the picture.

You can swap the prior without touching the solver: Ledoit–Wolf, Black–Litterman, entropy pooling, a vine-copula synthetic sample. Compact acceleration in the next post only fires when that prior is the default empirical one. That is a software fact with a mathematical reading: the compact engines know how to form $$(\mu,\Sigma)$$ from a Gram matrix. They do not know how to form a Black–Litterman posterior.

Assets with non-finite $$\mu_i$$ or $$\Sigma_{ii}$$ are dropped (`investable_mask`). The program is then posed in the remaining coordinates.

## Four objectives

Let $$\mu_{\mathrm{net}}(w)$$ be expected return after costs and fees, defined below. Let $$\mathrm{risk}_i(w)$$ be one of the convex risk measures MeanRisk knows. Four `ObjectiveFunction` values:

Minimize risk

$$
\min_{w\in K} \;\mathrm{risk}_i(w)
\quad\text{s.t.}\quad
\mu_{\mathrm{net}}(w)\ge \texttt{min\_return}.
$$

Maximize return

$$
\max_{w\in K} \;\mu_{\mathrm{net}}(w)
\quad\text{s.t.}\quad
\mathrm{risk}_i(w)\le \texttt{max\_risk}_i.
$$

Maximize utility

$$
\max_{w\in K} \;\mu_{\mathrm{net}}(w) - \lambda\,\mathrm{risk}_i(w).
$$

Maximize ratio. The fractional program $$( \mu_{\mathrm{net}}(w)-r_f)/\mathrm{risk}_i(w)$$ is homogenized (Charnes–Cooper / Schaible) {% cite charnes1962programming %}: a scale factor $$t>0$$, a constraint that the net-return numerator equals one after scaling, minimize risk in the scaled variable. Variance is not 1-homogeneous; skfolio converts to standard deviation internally and warns.{% fn %} Compact engines in accelerate refuse `MAXIMIZE_RATIO` for this reason. The ratio path is a different compiled shape.

Default constructor: long-only, `budget=1`, minimize variance. That is Markowitz on the simplex {% cite markowitz1952portfolio %}, plus whatever extra constraints you turned on.

## Risk measures as convex atoms

`ConvexOptimization` looks up `_{risk_measure}_risk`. Variance is the square of an SOC on a square-root factor of $$\Sigma$$:

$$
\mathrm{stdev}(w) = \|\Sigma^{1/2} w\|_2,
\qquad
\mathrm{variance}(w)=\mathrm{stdev}(w)^2.
$$

On the compact OSQP path this is written as the quadratic $$w^\top\Sigma w$$ with $$P=2\Sigma+2\ell_2 I$$. Same number when $$\Sigma$$ is PD.

CVaR is Rockafellar–Uryasev {% cite rockafellar2000optimization %}:

$$
\mathrm{CVaR}_\beta(w)
=
\alpha + \frac{1}{T(1-\beta)}\sum_{t=1}^T u_t,
\qquad
R w + \alpha\mathbf{1} + u \ge 0,\; u\ge 0.
$$

Scenario returns in that inequality are *net of* transaction costs and management fees along the path. Drawdown measures introduce an auxiliary process $$v_0=0$$, $$v_t\ge v_{t-1}-(Rw)_t$$, $$v_t\ge 0$$, then apply LP or exponential-cone risk to $$v$$. EVaR uses exponential cones. None of this is optional colour. It is why a "MeanRisk solver" that only does QP is incomplete, and why accelerate has a Clarabel engine at all.

Regularizers $$\ell_1\|w\|_1+\ell_2\|w\|_2^2$$ sit on the objective. Compact OSQP accepts $$\ell_2$$; $$\ell_1\ne 0$$ is blocked because it changes the QP pattern (and, with costs, starts to look like a second L1 term on $$w$$).

## Costs, turnover, previous weights

Net expected return in the CVXPY tree is

$$
\mu_{\mathrm{net}}(w)
=
\mu^\top w
- c^\top |w - w_{\mathrm{prev}}|
- f^\top w
- \mathcal{U}_\mu(w),
$$

where $$c$$ is per-asset transaction cost, $$f$$ management fees, $$\mathcal{U}_\mu$$ an optional mu-uncertainty penalty. If `previous_weights is None`, `_clean_previous_weights` fills **zeros**. The first rebalance is then costed as if you bought the whole book from cash. That is a modelling choice. The OLPS base class in the branch does the opposite by default: no `previous_weights` means the first trade is a starting book, not an entry from zero. Mixing the two conventions in one backtest will manufacture a fake first-period cost. Post 5 comes back to this.

`max_turnover` is **elementwise**:

$$
|w_i - w_{\mathrm{prev},i}| \le \texttt{max\_turnover}.
$$
{% fn %}
It is not $$\tfrac12\|w-w_{\mathrm{prev}}\|_1$$. People coming from turnover-budget papers trip on this constantly. The OLPS projector, when `max_turnover` is set, uses an L1 budget against the *last traded* $$w_t$$, while costs are charged against *drifted* holdings. Three different geometries, one parameter name. The 1.0 PR has to document that or reviewers will think it is a bug.

`needs_previous_weights` is true if any transaction cost, `max_turnover`, or a `"previous_weights"` fallback is set. Then `cross_val_predict` disables `n_jobs` and runs `_run_path`: clone per fold, `set_params(previous_weights=prev)`, `prev` taken from the last predicted portfolio. Folds are no longer independent. Accelerate's compact path refuses this entire family. Native skfolio is the reference implementation of the sequential *economic* problem.

## The feasible set $$K$$

`_get_weight_constraints` piles on: box bounds (scalar, array, or dict), equality `budget` or box `min_budget`/`max_budget`, `max_long`/`max_short`, group and linear inequalities $$Aw\ge b$$, optional MIP cardinality (SCIP/MOSEK/GUROBI/CPLEX). Tracking error against a benchmark in $$y$$ is another convex constraint. Uncertainty sets on $$\mu$$ and $$\Sigma$$ wrap the objective.

I am listing this because it is the reason MeanRisk cannot be "the OCO estimator with extra flags". Cardinality is mixed-integer. Ratio homogenization changes the variable. Efficient frontiers loop the same program over a grid of risk levels (`efficient_frontier_size`) and return a `Population`. An OCO `partial_fit` that reuses this `_fit` would inherit all of that by accident. 1.0 already has a `partial_fit` on MeanRisk; it still calls `_fit` after updating the prior. Post 4 is that path. It is batch MVO with a streaming $$\theta$$, which is a legitimate product feature and a different paper from Helmbold.

## Every `fit` allocates a new problem

This is the sentence accelerate exists to contradict, so it has to be stated as code, not as an insult.

On 1.0 main, `_fit` validates $$X$$, fits or `partial_fit`s the prior, then creates **new** `w = cp.Variable(n_assets)` (and a homogenizing `factor` for ratios), rebuilds expected return, regularization, tracking error, turnover, weight constraints, every active `_{risk}_risk` atom, then `cp.Problem(objective, constraints)` and `_solve_problem`. `_cvx_cache` only deduplicates expressions *inside* one solve. There is no `cp.Parameter` for $$\Sigma$$. There is no `warm_start` of Clarabel/OSQP iterates across `fit` calls. `save_problem=True` keeps the last `problem_` for inspection; it is not a compiled session.

Solver selection is a string, default `"CLARABEL"`, with tighter gap tolerances stuffed into `solver_params` for Clarabel and SCIP. MIP constraints refuse a non-MI solver. That is the whole policy.

WalkForward (`src/skfolio/model_selection/_walk_forward.py`) is a sklearn `BaseCrossValidator` parameterized by `train_size` and `test_size`, optional calendar `freq`, `expand_train`, purge. It never shuffles. `cross_val_predict` clones the estimator per fold, `fit`s, `predict`s the test slice into a `Portfolio`, concatenates to a `MultiPeriodPortfolio` (or a `Population` of paths for combinatorial / randomized CV). Each clone starts with empty numerical state. Overlapping windows are a statistical fact the solver never hears about.

So the parametric view

$$
w^\star(\theta) = \arg\min_{w\in K} f(w;\theta)
$$

is already how the *mathematics* of MeanRisk works. The *implementation* samples $$w^\star(\theta_t)$$ by constructing $$f(\,\cdot\,;\theta_t)$$ from scratch. Continuity of $$w^\star$$ in $$\theta$$ (when $$K$$ is fixed and $$f$$ is strongly convex, say variance plus $$\ell_2$$) is why a warm start ought to help. 1.0 does not use it. Accelerate does, for a subset of $$f$$.

## sklearn contract, which a PR must not break

`BaseOptimization` is a `BaseEstimator`. Constructor stores parameters only. `fit` is wrapped in `__init_subclass__` with a fallback chain (`fallback=[...]`, including the string `"previous_weights"`). `predict(X)` builds a `Portfolio` (or `Population`) and copies `transaction_costs`, `management_fees`, `previous_weights`, `risk_free_rate` onto it. `score` is Sharpe of that portfolio. `weights_` is the public learned attribute.

`partial_fit` on MeanRisk is **not** wrapped by that fallback decorator. Failures are handled inside `_fit`. `efficient_frontier_size` is forbidden on `partial_fit`. Fallback estimators other than `"previous_weights"` are forbidden, because a second estimator would not have seen the same stream.

`clone()` must remain valid. Learned state lives in trailing-underscore attributes. If an OCO estimator stuffed a live OSQP workspace into a constructor argument, GridSearch and `cross_val_predict` would share mutable solver state across folds. Accelerate's engines are local to one `cross_val_predict` call for the same reason.

## Implication for the 1.0 PR

Do not replace `_fit` with an OCO loop. MeanRisk's batch contract *is* "solve this convex program on the training window." Reviewers will diff `_mean_risk.py` and reject a behavioural change to CVaR, MIP, or ratio. OLPS subclasses `BaseOptimization` beside MeanRisk, same `fit`/`predict` verbs, different `_fit`. `BCRP` on the branch already inherits MeanRisk and overwrites the return with cumulative log-wealth when asked; that is the one place the two regimes should touch.

The parametric language $$w^\star(\theta_t)$$ is the hand-off to post 3. If $$\theta_t$$ is empirical and $$K$$ is a box plus a budget, the sequence of programs has a frozen topology. That is a compiled trajectory, still batch semantics.

{% footnotes %}
{% fnbody %}Homogenization for ratio objectives is the reason MAXIMIZE_RATIO with VARIANCE is rewritten through standard deviation. A compact QP that stored $$P = 2\Sigma$$ could not represent that fractional program without a second compiled shape.{% endfnbody %}
{% fnbody %}Elementwise turnover is in `_turnover` / `max_turnover` on ConvexOptimization. I am not claiming it is the unique sensible constraint, only that OLPS must not silently reinterpret it as an L1 budget without a distinct parameter.{% endfnbody %}
{% endfootnotes %}

---

# References

{% bibliography --cited %}
