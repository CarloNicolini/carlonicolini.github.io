---
layout: post
title: What a research PR to skfolio 1.0.0 actually contains
description: "A maintainer-facing cut: rebase universal_portfolio onto v1.0.0, the in-list and out-list, tests, gallery, naming, and the follow-up issues that must not ride along."
date: 2026-09-03
published: true
categories:
  - science
  - machine-learning
---

*Post 6 of 6. Previous: [First-order OCO as a portfolio estimator]({% link sections/science/_posts/2026-09-02-first-order-oco-and-olps-in-skfolio.md %}). Series start: [From solving convex programs to tracking them]({% link sections/science/_posts/2026-08-29-from-solving-to-tracking-convex-programs.md %}).*

This is the merge plan. The mathematics lived in posts 1–5. Here I write down what I would put in a GitHub issue, what I would rebase, what I would delete, and what I would ask a reviewer to run. skfolio 1.0.0 is tagged (2026-08-23). `CONTRIBUTING.md` asks for an issue before a substantial change, a branch named `feature/no-ref/online-portfolio-selection` until the issue exists, conventional commits `feat(optimization): …`, and a PR title prefixed `[ENH]`.{% fn %} The library itself is described in {% cite nicolini2025skfolio %}.

The working tree I have is `universal_portfolio` at about 35 commits ahead of a v0.15.5 merge-base, 0 behind *that* main, and **not** rebased onto 1.0. Local HEAD has a dummy message. There is one unpublished commit. None of this is reviewable until it sits on `v1.0.0`.

## Rebase, then cut

1. Open the issue. Problem statement: skfolio 1.0 can stream *moments* and re-solve MeanRisk (`online_predict`); it cannot run Helmbold/Li–Hoi OLPS as `BaseOptimization` estimators. Link the four-regime glossary (post 1) so "online" is not a fight in the first comment.
2. Branch from `v1.0.0`: `feature/issue-N/online-portfolio-selection`.
3. Rebase `universal_portfolio` onto that. Expect collisions in `optimization/__init__.py`, `docs/api.rst`, `pyproject.toml` (`autograd`), `model_selection/` (1.0 already has `_online/`), and the user guide. 1.0 renamed `expend_train` → `expand_train`, `FactorModel` the estimator → `TimeSeriesFactorModel`, `EWMu.alpha` → `half_life`. The branch will not apply cleanly; that is the work.
4. Delete from the rebased tree everything in the out-list below *before* opening the PR. A 19k-line dump with SWORD and Cover leftovers is not a research PR. It is a hostage situation.

Commit hygiene after the rebase: one commit for the engine and estimators, one for tests, one for docs/gallery, or a single well-messaged `feat(optimization): add online portfolio selection estimators` if the history is otherwise noise. Do not ship the 35-commit diary (`...` messages included). Squash onto 1.0, then optionally split the squash by area so a reviewer can read `git log origin/main..HEAD --stat`.

`skfolio.optimization` on 1.0 must still look like 1.0 plus a new subpackage. MeanRisk, `_fit`, compact accelerate, and `online_learning.rst` stay untouched.

## Issue body (paste-ready outline)

- **Problem.** Cannot run EG/OLMAR as sklearn estimators; 1.0 `online_*` is streaming MeanRisk.
- **Glossary.** Four regimes (link post 1). `partial_fit` on MeanRisk vs on `FollowTheWinner`.
- **Scope.** In-list / out-list below.
- **Integration invariant.** After `partial_fit`, `weights_` is the next traded book; `predict(X_test)` applies that book to a *future* window; `fit_predict` is the sequential in-sample path.
- **Non-goals.** No MeanRisk `_fit` change, no accelerate import, no C solver, no `autograd` core dep.
- **Docs.** Gallery under `examples/online_learning/`, new `olps.rst`, see-also on `online_learning.rst`.

## In the first PR

**Package.** `src/skfolio/optimization/online/` with public:

- `FollowTheWinner` — `strategy="eg"` and `"ogd"`, `learning_rate="auto"`, default log-wealth, `update_mode` FTRL or OMD if both are tested equal on EG.
- `FollowTheLoser` — `olmar`, `pamr`, `rmr`, `cwmr`, `update_mode="pa"` only.
- `CRP`, `UCRP`, `BestStock`, `BCRP` (MeanRisk, `LOG_WEALTH` default).
- `regret(..., regret_type=STATIC)` and `RegretType.STATIC`.

**API verbs.** `fit` (row loop), `partial_fit` (one row), `fit_predict` → `MultiPeriodPortfolio`, `predict_online` for continuation. Inherited `predict` remains, documented as lookahead if you pass the training stream.

**Constraints.** Box plus budget, optional L1 `max_turnover` against last trade. Transaction costs and management fees against *drifted* holdings, first period free unless `previous_weights` is passed. `clone` / `get_params` / `set_params` must work; learned state in `weights_`, `all_weights_`, `wealth_`, `all_wealth_`.

**Docs.** A gallery example under `examples/online_learning/` (the 1.0 folder), e.g. EG vs UCRP vs BCRP on `load_sp500_dataset` after `prices_to_returns`, evaluated with `fit_predict`. A user-guide page that **links** `online_learning.rst` and spends the first screen on the glossary: streaming MeanRisk vs OLPS. `docs/api.rst` autosummary. `optimization/__init__.py` re-exports the public names.

**Dependency.** Analytic log-wealth gradient. No `autograd` in `pyproject.toml` core deps. The PR template asks.

**Tests** (minimum I would not merge without):

- `clone` / `get_params` / `set_params` round-trip.
- `partial_fit` rejects two rows.
- EG multiplicative identity on a tiny simplex (match `w \odot \exp(-\eta g)` then normalize).
- OGD equals projected gradient for Euclidean $$\psi$$.
- `fit` is sequential: permuting rows changes `all_weights_` (time-series, never shuffle).
- `fit_predict` wealth path vs a manual loop of `partial_fit`.
- UCRP is $$1/n$$ every period.
- Static regret vs BCRP is nonnegative on log-wealth up to a stated atol.
- Costs: drifted-holdings example from the user guide, first period zero cost without `previous_weights`.
- `online_predict` smoke: warmup, `test_size=1`, returns `MultiPeriodPortfolio`, no pipeline.
- `predict(X_train)` after `fit(X_train)` is *not* equal to `fit_predict` (lookahead trap as a documented test, not a failure).

Li–Hoi relatives loaders (`load_nyse_o_relatives_dataset`, …) can ship if they are small and already in `datasets/`. If they bloat the wheel, keep them out of the first PR and use `load_sp500_dataset`.

## Out of the first PR

- SWORD family, Ada-BARRONS, `TsallisMirrorMap`, deprecated log-barrier.
- `FollowTheLoser(update_mode="md")`, CWMR mirror-descent.
- `objective=` CVaR/EVaR/CDaR on a single period (path measures at $$T=1$$ are proxies; autograd factory).
- `RegretType.DYNAMIC_UNIVERSAL`, `DYNAMIC_WORST_CASE` as public API (keep STATIC; prefix-BCRP dynamic can wait).
- Cover Universal Portfolios, CORN/BNN, Anticor, named ONS.
- Public `FirstOrderOCO`, public `online_walk_forward_predict`.
- `autograd` required.
- Any change to `MeanRisk._fit`, any import of `skfolio_accelerate`, any C sequential solver, any ADMM continuation kernel.
- Replacing 1.0 `online_predict` semantics.

`prod` / Burg: second PR unless the rebase makes it free (tests already green, no extra docs). I would still hide it behind the internal engine.

## Naming

| Name in 1.0 | Meaning | Name to add |
|---|---|---|
| `online_predict` | one clone, `partial_fit` stream, path score | keep |
| `docs/user_guide/online_learning.rst` | EW moments + repeated convex solves | keep, add a "see also OLPS" paragraph |
| `skfolio.optimization.online` | OLPS estimators | add |
| `docs/user_guide/olps.rst` (preferred name) | Helmbold / Li–Hoi | add; do not overwrite `online_learning.rst` |

If the branch's `online.rst` is copied onto `online_learning.rst`, the PR should be closed.

## Reviewer script

From a clean 1.0 venv, after `uv pip install -e ".[dev]"`:

```bash
uv run pytest tests/test_optimization/test_online -q
uv run pytest tests/test_model_selection/test_online -q
uv run ruff check src/skfolio/optimization/online tests/test_optimization/test_online
```

Then the gallery script, manually:

```python
from sklearn.base import clone
from skfolio.datasets import load_sp500_dataset
from skfolio.model_selection import online_predict
from skfolio.optimization.online import FollowTheWinner, UCRP, BCRP, regret
from skfolio.preprocessing import prices_to_returns

X = prices_to_returns(load_sp500_dataset())
eg = FollowTheWinner(strategy="eg")
path = eg.fit_predict(X)
assert path.returns.shape[0] == len(X)

frozen = clone(eg).fit(X).predict(X)  # lookahead on purpose
# frozen.returns is w_T applied to every row; path is not that

ucrp = UCRP().fit_predict(X)
R = regret(FollowTheWinner(strategy="eg").fit(X), X)
assert R[-1] >= -1e-6
```

`online_predict(FollowTheWinner(strategy="eg"), X, warmup_size=60, test_size=1)` should return a `MultiPeriodPortfolio` whose first test date is after warmup. If it applies `predict` internally instead of `predict_online` / per-row weights, that is a bug in the integration, and it is on us to patch the OLPS estimator's `predict` or to teach `online_predict` a `method=` for online estimators. I would prefer the estimator grow a flag or `predict` that uses last-period weights for a *future* test window (causal) while `fit_predict` remains the in-sample sequential path. That design choice has to be explicit in the issue, because 1.0 `online_predict` currently assumes `predict(X_test)` after `partial_fit` is the right out-of-sample map, which is true for MeanRisk (frozen book on the next window) and true for EG only if `weights_` is the book you trade *next*, applied to the test window without refitting inside `predict`. That last sentence is the integration invariant. Write it on the issue.{% fn %}{% fn %}

## Follow-up issues (named, not in the diff)

**A. Richer projections.** Groups, linear inequalities, tracking-error, variance bound via the existing cvxpy `project_convex`. Tests against MeanRisk-feasible random points.

**B. Clarabel in-place updates.** Accelerate's scenario path is 2–4× because cones rebuild. Upstream or in accelerate, not in `optimization/online`.

**C. Solver-state continuation as a benchmark.** Persistent OSQP $$x,y$$ (already there) plus factorization reuse on expanding $$T$$, measured on the 20-year table. Accelerate issue. Success criterion: iteration counts, not a new public class.

**D. SequentialSolver C library.** Only after B and C have numbers. Canonical QP/cones in, state out. No `MeanRisk` in the ABI. Separate repository.

**E. `prod`, AdaGrad, then SWORD.** One strategy family per PR once A is stable.

**F. Pattern matching / Cover UP.** Only with a dataset and a test that is not "it runs."

## What success looks like

A maintainer who knows MeanRisk and has not read Hazan can clone the branch, run the gallery, see EG next to UCRP, read that `predict` lookaheads, and leave `src/skfolio/optimization/convex/` grepless in the diff. The issue uses the word "online" with a glossary. Accelerate is cited as evidence that WalkForward is a trajectory, then left alone. The C solver is a footnote.

That is a research-level PR onto 1.0.0. It is also smaller than the branch I already wrote. The cut is the contribution.

{% footnotes %}
{% fnbody %}PR title tags in the template are [ENH], [MNT], [DOC], [BUG]. New estimators also need the gallery and docs/api.rst or the docs CI fails.{% endfnbody %}
{% fnbody %}MeanRisk after partial_fit: weights_ is the solution of $$P(\theta_t)$$, and predict(X_test) applies that frozen book to the next window. EG after partial_fit: weights_ is $$w_{t+1}$$, the book for the next unobserved relative. Both are valid predict semantics. Mixing them in one paragraph without the glossary is how the review stalls.{% endfnbody %}
{% endfootnotes %}

---

# References

{% bibliography --cited %}
