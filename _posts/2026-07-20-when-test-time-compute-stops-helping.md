---
layout: post
title: "When test-time compute stops helping: common-mode error, verifier limits, and selective reliability"
description: "A reliability theory for adaptive inference when samples are dependent, verification is imperfect, and abstention is allowed."
date: 2026-07-20
published: false
permalink: "/sections/science/2026/07/20/when-test-time-compute-stops-helping.html"
categories:
  - science
  - ai
  - math
---
## Abstract

Test-time compute can improve a language-model system by generating alternatives, searching a reasoning tree, checking intermediate states, or revising an answer. None of these operations makes reliability monotone in compute without further assumptions. This paper develops a small theory for identifying the assumptions that are actually doing the work. It distinguishes a fixed finite tree from an adaptively generated random tree, charges nonreturn explicitly, and gives a drift bound for an adaptive frontier whose promising branches can be pruned. It then separates verifier soundness from probabilistic completeness, derives saturation under latent common-mode error, gives an exact beta-mixture example, and shows the ceiling induced by a binary verifier with false positives. Fréchet bounds state what remains identifiable when only marginal candidate accuracies are known. A held-out protocol estimates distributional risk and calibration without reusing development tasks, while selective abstention exposes the trade-off between coverage and conditional error. Finally, no-free-lunch and undecidability results delimit universal claims without ruling out strong domain-specific systems. The empirical component is deliberately divided into deterministic simulations and a single-request live OpenAI engineering smoke test. Neither has been executed for this manuscript version, so generated values are marked as pending and only analytical predictions are reported.

## From scaffolding to stopping

The earlier essay [Scaffolding is all you need]({% link _posts/2026-03-02-Scaffolding-is-all-you-need.md %}) described an answer-or-decompose policy that induces a random rooted tree. Its central distinction was semantic: OR-like branching creates alternatives, whereas AND-like decomposition creates additional essential obligations. The present paper begins after that distinction. It asks when another sample, branch, verification pass, or revision ceases to buy reliability.

This question is not answered by counting calls. Self-consistency samples several reasoning paths and aggregates their answers {% cite wang2023selfconsistency %}; Tree of Thoughts searches over evaluated intermediate states {% cite yao2023tree %}; least-to-most and decomposed prompting change the interfaces among subproblems {% cite zhou2023least khot2023decomposed %}; and compute-optimal inference allocates different budgets to prompts of different difficulty {% cite snell2025scaling %}. These procedures spend compute in different places and expose themselves to different failure modes. More calls can even produce non-monotone aggregate accuracy when a task distribution mixes easy and hard queries {% cite chen2024morecalls %}, while intrinsic self-correction can degrade reasoning in the absence of external feedback {% cite huang2024selfcorrect %}. A useful theory must therefore name the filtration, the stopping rule, the dependence structure, the verifier errors, and the target risk.

The thesis is narrow. Additional test-time compute is reliable only to the extent that it creates conditionally useful diversity, preserves promising frontier mass, and applies evidence whose false-positive behavior is controlled on the deployment distribution. When those conditions fail, compute may saturate, merely reshuffle error, or make the result worse. Abstention can still improve the reliability of returned answers, but only by reducing coverage; it does not erase failure.

## Formal setting and estimands

Let a task-label pair $$(X,Y^\star)$$ be drawn from a deployment distribution $$\mathcal D$$. The ground-truth predicate $$C(x,y)\in\{0,1\}$$ says whether candidate answer $$y$$ is correct for $$x$$. A scaffold receives $$X=x$$, builds a history $$H_t$$, and at each step may sample a candidate, expand or prune a frontier, query a verifier, stop with an answer, or abstain. The histories generate a filtration $$(\mathcal F_t)_{t\geq 0}$$. The stopping time $$\tau$$ may be infinite unless a hard budget forces termination.

The returned value is $$\widehat Y\in\mathcal Y\cup\{\bot\}$$, where $$\bot$$ denotes abstention or operational nonreturn. We keep three quantities separate:

$$
\kappa = \mathbb P(\widehat Y\neq\bot),\qquad
r_{\mathrm{sel}} = \mathbb P(C(X,\widehat Y)=0\mid \widehat Y\neq\bot),\qquad
r_{\mathrm{total}} = \mathbb P(C(X,\widehat Y)=0\ \text{or}\ \widehat Y=\bot).
$$

Coverage $$\kappa$$ and selective risk $$r_{\mathrm{sel}}$$ describe the answers a system is willing to return. Total risk treats abstention as failure and equals $$1-\mathbb P(C(X,\widehat Y)=1)$$. Applications may instead assign abstention a cost $$0<\lambda<1$$, but that cost must be stated; reporting selective accuracy alone can make a system that answers almost nothing look arbitrarily reliable.

The budget $$b$$ can count calls, generated tokens, wall-clock time, or money. Results indexed by $$b$$ are not automatically comparable if increasing the budget also changes the model, prompt, verifier, or stopping rule. Throughout the theory, a “more compute” comparison holds the task distribution and all non-budget design choices fixed unless a proposition says otherwise.

## Theory I: local failures on fixed and random trees

### A fixed-tree union bound

Consider first a deterministic finite rooted tree $$T$$ fixed before any model output is observed. Let $$E\subseteq T$$ be a fixed set of essential nodes, and let $$G_u$$ be the event that the local obligation at node $$u\in E$$ is met. The exact assumptions are that the run terminates, that it returns one answer, and that simultaneous satisfaction of all essential obligations is sufficient for root correctness:

$$
\bigcap_{u\in E}G_u\ \subseteq\ \{C(X,\widehat Y)=1\}.
$$

Then no independence assumption is needed. Taking the contrapositive inclusion and applying Boole's inequality gives

$$
\mathbb P(C(X,\widehat Y)=0)
\leq
\mathbb P\left(\bigcup_{u\in E}G_u^c\right)
\leq
\sum_{u\in E}\mathbb P(G_u^c).
$$

If every essential obligation fails with probability at most $$\varepsilon$$, the familiar bound is $$|E|\varepsilon$$. The proof is only the set inclusion followed by a union bound. Its value is that it reveals exactly what must be fixed: the tree, the essential set, and guaranteed return.

The result is sufficient rather than necessary and can be loose by a factor as large as $$|E|$$ when failures are perfectly correlated. It can also be vacuous when the sum exceeds one. A simple counterexample to careless use is an adaptive procedure that keeps adding a new essential check after every passed check. There is no deterministic $$|E|$$ to insert. Another counterexample is a procedure that never returns on a positive-probability event; a bound over local wrong-answer events says nothing about that missing mass. A fixed-tree union bound should therefore not be presented as a theorem about an adaptive agent.

### An adaptive random-tree bound with nonreturn

Adaptive scaffolds generate random trees, a setting naturally related to branching-process models {% cite harris1963branching %}. Let $$\mathcal U$$ be a countable set of potential node addresses, such as finite strings of child indices. Let $$A_u$$ be the event that address $$u$$ is visited, and let $$F_u$$ be failure of the local obligation defined for that address. Let $$N=\{\tau=\infty\}$$ be nonreturn and $$W$$ be the event that the scaffold returns an incorrect answer.

The structural assumption is now pathwise: every returned wrong answer has at least one failed local obligation on its realized tree,

$$
W\subseteq\bigcup_{u\in\mathcal U}(A_u\cap F_u).
$$

Consequently,

$$
\mathbb P(W\cup N)
\leq
\mathbb P(N)+\sum_{u\in\mathcal U}\mathbb P(A_u\cap F_u).
$$

Suppose that immediately before visiting $$u$$ the available history is $$\mathcal H_u$$ and that a predictable bound $$\varepsilon_u(\mathcal H_u)$$ satisfies

$$
\mathbb P(F_u\mid \mathcal H_u,A_u)\leq \varepsilon_u(\mathcal H_u).
$$

Tonelli's theorem for nonnegative terms then yields the adaptive form

$$
\mathbb P(W\cup N)
\leq
q_{\mathrm{nr}}
+
\mathbb E\left[
\sum_{u\in T_{\mathrm{vis}}}
\varepsilon_u(\mathcal H_u)
\right],
\qquad
q_{\mathrm{nr}}=\mathbb P(N).
$$

Under a uniform conditional bound $$\varepsilon_u\leq\varepsilon$$ and finite expected visited-node count $$\mathbb E|T_{\mathrm{vis}}|$$, this becomes

$$
\mathbb P(W\cup N)
\leq
q_{\mathrm{nr}}+\varepsilon\,\mathbb E|T_{\mathrm{vis}}|.
$$

The proof does not require independent node failures. Adaptivity is absorbed by conditioning each local hazard on the history that caused the node to be visited. The price is that an unconditional statement such as “every node has error at most $$\varepsilon$$” is insufficient: selection can preferentially visit nodes on which the conditional error is much larger. For a minimal counterexample to omitting nonreturn, let every visited local obligation pass but let the controller enter an infinite loop with probability $$q>0$$. The local-failure sum is zero while total risk is at least $$q$$.

Three limitations matter. First, the pathwise witness assumption may fail when composition introduces a root error despite every declared local obligation passing. Such composition errors need their own essential event. Second, finite expected tree size is stronger than almost-sure finiteness; a tree can terminate almost surely yet have infinite expected size. Third, a hard budget turns nonreturn into an explicit timeout or abstention but does not make it disappear from total risk. The event has merely acquired a label.

### Adaptive frontier drift

A union bound charges realized failures but does not describe a search policy that silently prunes its only good branch. To model that loss, let $$M_t\in[0,1]$$ be a history-measurable *certified promise* of the current frontier. It can be a lower bound on the probability that the residual policy will eventually return a correct answer, or a calibrated mass assigned to frontier states that retain a valid continuation. The interpretation must be fixed before evaluation.

For a stopping time $$\tau$$ and finite horizon $$B$$, assume that while the process is active,

$$
\mathbb E[M_{t+1}\mid\mathcal F_t]\geq M_t-\delta_t
\quad\text{for }t<\tau\wedge B,
$$

where each $$\delta_t\geq0$$ is predictable. Assume also that on a stopped history, conversion from promise to correctness loses at most $$\eta_\tau$$:

$$
\mathbb E[C(X,\widehat Y)\mid\mathcal F_\tau]\geq M_\tau-\eta_\tau.
$$

Telescoping conditional expectations, and pessimistically charging one unit on histories not stopped by $$B$$, gives

$$
\mathbb P(C(X,\widehat Y)=1,\tau\leq B)
\geq
\mathbb E[M_0]
-
\mathbb E\left[\sum_{t<\tau\wedge B}\delta_t\right]
-
\mathbb E[\eta_\tau\mathbf 1\{\tau\leq B\}]
-
\mathbb P(\tau>B).
$$

The proof sketch defines the stopped process $$M_{t\wedge\tau}$$, sums the one-step drift inequalities through $$B$$, applies the terminal conversion bound on $$\{\tau\leq B\}$$, and uses $$0\leq M_B\leq1$$ to bound the unresolved tail. If $$B\to\infty$$ and the sums are integrable, the last term converges to the nonreturn probability.

This proposition makes frontier preservation a first-class assumption. A counterexample shows why. Begin with exactly one valid branch. At each deliberation round, a noisy self-evaluator independently deletes that branch with probability $$\delta>0$$; expansion creates no replacement. After $$d$$ rounds, success is $$(1-\delta)^d$$. Every extra round spends compute while strictly reducing reliability. Tree search and self-evaluation are useful when they preserve or improve frontier promise, not merely because they make the tree larger. Tree-based deliberation can produce large benchmark gains {% cite yao2023tree %}, but those gains do not establish a universal nonnegative drift condition.

## Theory II: verifiers, dependence, and ceilings

### Sound verification and probabilistic completeness

Verifier-guided search has shown substantial empirical value in mathematical reasoning {% cite cobbe2021verifiers lightman2024verify %}. The reliability theorem, however, needs two distinct properties. Let candidate $$i$$ have correctness bit $$C_i$$ and binary verifier decision $$V_i$$. A verifier is sound on the proposal distribution if

$$
\mathbb P(V_i=1,C_i=0\mid\mathcal F_{i-1})=0.
$$

Soundness says that accepted candidates are correct. It does not say that any candidate will be accepted. Define the conditional acceptance hazard, given no earlier acceptance, by

$$
\gamma_i=
\mathbb P(V_i=1,C_i=1\mid\mathcal F_{i-1},V_1=\cdots=V_{i-1}=0).
$$

If $$\gamma_i$$ is bounded below by a predictable deterministic value with the same symbol, then a scaffold that returns the first accepted candidate obeys

$$
\mathbb P(\text{no correct return by }n)
\leq
\prod_{i=1}^{n}(1-\gamma_i).
$$

In particular, if $$\gamma_i\geq\gamma>0$$, success by call $$n$$ is at least $$1-(1-\gamma)^n$$. More generally, if $$\sum_i\gamma_i=\infty$$, the product tends to zero and the method is probabilistically complete: with probability one it eventually returns a correct answer. The proof repeatedly conditions on survival without acceptance. Independence is unnecessary because the lower bound is conditional on the full preceding history.

The counterexample is a verifier that rejects every candidate. It is perfectly sound but has $$\gamma_i=0$$ and never returns. A second counterexample is a sound verifier paired with a generator that assigns zero probability to every verifiable correct answer. These examples are why soundness and completeness cannot be merged into a single informal claim that a verifier is “good.”

### Common-mode saturation through a latent difficulty

Repeated calls are rarely independent in the unconditional sense. They share the task, specification, model family, training data, prompt, and often the same mistaken premise. Correlated errors have long been recognized as a limit on redundant software: independently developed versions can still fail on the same inputs {% cite eckhardt1985multiversion knight1986independence %}. A minimal probabilistic model introduces a latent task-specific success propensity $$\Theta\in[0,1]$$ and assumes conditional, rather than marginal, independence:

$$
C_i\mid\Theta\overset{\mathrm{iid}}{\sim}\operatorname{Bernoulli}(\Theta).
$$

This is an exchangeable mixture representation in the spirit of de Finetti {% cite definetti1937prevision %}. For OR-style search with an oracle selector, the probability that at least one of $$n$$ candidates is correct is

$$
R_n^{\mathrm{OR}}
=
1-\mathbb E[(1-\Theta)^n].
$$

Dominated convergence gives the exact limit

$$
\lim_{n\to\infty}R_n^{\mathrm{OR}}
=
1-\mathbb P(\Theta=0).
$$

Thus a common-mode atom at $$\Theta=0$$ creates a hard ceiling. It represents tasks for which the entire candidate family has zero chance of entering the correct basin. No number of samples from that same family crosses the ceiling.

The beta mixture is analytically useful. If $$\Theta\sim\operatorname{Beta}(a,b)$$ with $$a,b>0$$, then

$$
R_n^{\mathrm{OR}}
=
1-\frac{B(a,b+n)}{B(a,b)}
=
1-\frac{(b)_n}{(a+b)_n},
$$

and

$$
1-R_n^{\mathrm{OR}}
\sim
\frac{\Gamma(a+b)}{\Gamma(b)}n^{-a}.
$$

The induced pairwise correlation is

$$
\operatorname{Corr}(C_i,C_j)=\frac{1}{a+b+1},\qquad i\neq j.
$$

This example has an important limitation: a beta distribution with positive parameters has no atom at zero, so its OR reliability tends to one. It illustrates polynomially diminishing returns, not a strict asymptotic ceiling. A zero-inflated beta model with probability $$q$$ at zero and probability $$1-q$$ on $$\operatorname{Beta}(a,b)$$ has

$$
R_n^{\mathrm{OR}}
=
(1-q)\left[1-\frac{(b)_n}{(a+b)_n}\right]
\longrightarrow 1-q.
$$

For odd $$n$$, suppose the task is binary, so that answer-level majority voting is equivalent to taking the majority of the correctness bits. Under this additional assumption, majority voting in the beta mixture has the exact beta-binomial reliability

$$
R_n^{\mathrm{maj}}
=
\sum_{k=(n+1)/2}^{n}
{n\choose k}
\frac{B(a+k,b+n-k)}{B(a,b)},
$$

which converges to $$\mathbb P(\Theta>1/2)$$ when there is no mass at $$1/2$$. This limit can be far below one even though OR recall approaches one, because majority vote cannot identify a rare correct minority on systematically hard tasks. Heterogeneous task difficulty can therefore make the optimal call count finite, consistent with observed non-monotone scaling in compound inference {% cite chen2024morecalls %}.

### The imperfect-verifier ceiling

Now replace the oracle selector with a binary verifier. Assume candidates are iid with $$\mathbb P(C_i=1)=p$$, and verifier decisions are conditionally iid across candidates with true-positive rate $$\alpha=\mathbb P(V_i=1\mid C_i=1)$$ and false-positive rate $$\beta=\mathbb P(V_i=1\mid C_i=0)$$. Assume the scaffold returns the first accepted candidate and otherwise does not return after $$n$$ calls. The per-call acceptance probability is

$$
a=\alpha p+\beta(1-p).
$$

For $$a>0$$, direct summation of the geometric stopping law gives

$$
\mathbb P(\text{correct return by }n)
=
\frac{\alpha p}{a}\left[1-(1-a)^n\right],
$$

$$
\mathbb P(\text{nonreturn by }n)=(1-a)^n,
$$

and, whenever a candidate is returned,

$$
\mathbb P(C=1\mid V=1)=
\frac{\alpha p}{\alpha p+\beta(1-p)}.
$$

If $$a=0$$, the verifier accepts nothing and nonreturn has probability one. If $$a>0$$, $$\beta>0$$, and $$p<1$$, more samples drive nonreturn toward zero but leave conditional correctness at a ceiling strictly below one. This is the same posterior precision calculation that explains why filtering improves a raw candidate only when $$\alpha>\beta$$. It also shows why a verifier with a small false-positive rate can become the limiting component of a large search.

The formula depends on binary acceptance, stationary rates, iid proposals, and first-accept selection. A maximum-score selector can behave differently because its extreme-value tails matter. Distribution shift can also change $$\alpha$$ and $$\beta$$ precisely where the generator produces unusual candidates. Process reward models and outcome verifiers remain empirical classifiers, even when their training signal is more granular {% cite lightman2024verify %}; their reported in-distribution performance is not a proof of soundness.

### Fréchet bounds when dependence is unknown

If only marginal candidate accuracies $$p_i=\mathbb P(C_i=1)$$ are known, independence-based scaling curves are not identified. The Fréchet inequalities provide sharp dependence-robust bounds {% cite mikusinski1992frechet %}. For OR success,

$$
\max_i p_i
\leq
\mathbb P\left(\bigcup_{i=1}^{n}\{C_i=1\}\right)
\leq
\min\left(1,\sum_{i=1}^{n}p_i\right).
$$

For conjunctive success,

$$
\max\left(0,\sum_{i=1}^{n}p_i-(n-1)\right)
\leq
\mathbb P\left(\bigcap_{i=1}^{n}\{C_i=1\}\right)
\leq
\min_i p_i.
$$

The proof is elementary. The union contains every individual success event and is at most the sum of their probabilities. The intersection is contained in every individual event, while applying the union bound to the complementary failures gives its lower bound. Nested events attain one set of extremes, and appropriately disjoint event segments attain the other whenever the marginal masses permit it. The bounds are therefore not merely conservative confidence intervals; without additional joint information, no universally tighter bounds exist.

Marginals do not identify majority reliability either. With three candidates and marginal correctness $$2/3$$ for each, a distribution supported uniformly on the three states having exactly two correct candidates makes majority correctness equal to one. Perfectly correlated candidates, all correct with probability $$2/3$$ and all wrong otherwise, have the same marginals but majority correctness $$2/3$$. Reporting only pass-at-one accuracy and a call count is consequently insufficient for predicting aggregation gains. At minimum, evaluations should estimate task-level joint behavior, not infer it from a binomial curve.

## Theory III: distributional risk, calibration, and abstention

### Held-out distributional risk

Reliability is a property of a scaffold and a task distribution, not of a few illustrative prompts. Split tasks into development, calibration, and final test sets sampled iid from the target distribution. All prompts, search policies, budgets, verifier thresholds, bins, and stopping rules must be frozen before the final test set is inspected. If bounded loss $$\ell\in[0,1]$$ charges wrong answers and abstentions according to a prespecified policy, define

$$
R_{\mathcal D}=\mathbb E_{\mathcal D}[\ell(X,Y^\star;\mathcal A)]
$$

for the frozen scaffold $$\mathcal A$$. On an independent test set of size $$m$$,

$$
\widehat R_m=\frac{1}{m}\sum_{j=1}^{m}\ell_j.
$$

Hoeffding's inequality gives the finite-sample upper bound

$$
R_{\mathcal D}
\leq
\widehat R_m+
\sqrt{\frac{\log(1/\delta)}{2m}}
$$

with probability at least $$1-\delta$$. This statement assumes iid bounded test losses and one prespecified analysis. Repeatedly selecting the best scaffold on the same “test” set destroys the guarantee. For budget comparisons on identical tasks, paired loss differences are preferable because task difficulty cancels, but their interval must still account for every budget inspected during selection.

Distributional validity is the larger limitation. An iid guarantee for $$\mathcal D$$ does not transfer to a shifted deployment distribution. Semantic uncertainty can help identify some confabulations in free-form generation {% cite farquhar2024semantic %}, but uncertainty scores require their own held-out validation and do not detect every systematic falsehood.

### Fixed-bin calibration

Let $$S\in[0,1]$$ be a frozen score intended to estimate the probability that a returned answer is correct, and let $$C\in\{0,1\}$$ be observed correctness. Choose bins $$I_1,\ldots,I_K$$ using development or calibration data, then freeze them. In test bin $$j$$, with count $$n_j>0$$, estimate the signed calibration gap by

$$
\widehat g_j
=
\frac{1}{n_j}\sum_{i:S_i\in I_j}(C_i-S_i).
$$

Conditional on the bin count, $$C_i-S_i\in[-1,1]$$. A union bound over fixed bins and Hoeffding's inequality imply that, with probability at least $$1-\delta$$, all populated-bin target gaps $$g_j=\mathbb E[C-S\mid S\in I_j]$$ satisfy

$$
|\widehat g_j-g_j|
\leq
\sqrt{\frac{2\log(2K/\delta)}{n_j}}.
$$

The commonly reported binned expected calibration error,

$$
\widehat{\operatorname{ECE}}
=
\sum_{j=1}^{K}\frac{n_j}{m}|\widehat g_j|,
$$

is descriptive rather than an unbiased estimator, because absolute values turn sampling noise into a positive contribution. Empty and small bins must remain visible. Choosing bin edges, temperatures, or thresholds after seeing test labels invalidates the simultaneous statement. Modern neural classifiers can be substantially miscalibrated, and even effective post-hoc methods such as temperature scaling must be fit on held-out data {% cite guo2017calibration %}.

### Selective abstention

Suppose a calibrated score $$S=s$$ estimates the probability that the proposed answer is correct. Let a wrong answer cost $$L>0$$, a correct answer cost zero, and abstention cost $$\lambda\in(0,L)$$. Conditional expected answer cost is $$L(1-s)$$, so the Bayes decision returns the answer exactly when

$$
s\geq 1-\frac{\lambda}{L}.
$$

This is the basic reject-option trade-off studied by Chow {% cite chow1970reject %}. For a frozen threshold $$t$$, report coverage and selective risk together:

$$
\kappa(t)=\mathbb P(S\geq t),\qquad
r_{\mathrm{sel}}(t)=\mathbb P(C=0\mid S\geq t).
$$

If $$n_t$$ independent held-out examples are accepted, a one-sided Hoeffding bound gives

$$
r_{\mathrm{sel}}(t)
\leq
\widehat r_{\mathrm{sel}}(t)
+
\sqrt{\frac{\log(1/\delta)}{2n_t}}
$$

with probability at least $$1-\delta$$ for a prespecified threshold. When $$n_t=0$$, selective risk is undefined, not zero. Searching many thresholds on the same test labels requires simultaneous correction or a separate calibration split.

Abstention converts uncertainty into lower coverage; it cannot repair a confident common-mode error. If the score is miscalibrated under shift, the accepted subset may be precisely where the model is overconfident. The operational policy should therefore include a minimum supported bin count, a lower confidence bound on accuracy, and a fallback path for abstained requests. Those engineering choices are part of the estimand, not post-processing details.

## The universal boundary

There are two different reasons not to expect a universally improving scaffold. First, the classical finite no-free-lunch setting fixes finite search and value spaces, gives equal weight to all objective functions from the search space to the value space, compares algorithms under the same observation budget, and uses a performance measure determined by the observed value sequence. Equivalent statements replace the full function class by one closed under permutation. Under those assumptions, every value sequence occurs equally often for each non-revisiting algorithm, so reindexing the sum over objective functions makes the averaged performance independent of the algorithm {% cite wolpert1997nfl %}.

Those assumptions are the theorem, not a description of natural-language workloads. If a deployment distribution concentrates on structured functions, one search policy can dominate another on that distribution without contradiction. Thus no-free-lunch results do not say that all algorithms are equally useful in practice. They say that a universal superiority claim must be purchasing its advantage from assumptions about the task distribution, representation, or admissible function class.

Second, unrestricted semantic verification meets computability limits. Turing proved that no general effective procedure decides every instance of the relevant halting-style questions {% cite turing1937computable %}. Rice's theorem extends the boundary: every nontrivial semantic property of the partial function computed by an arbitrary program is undecidable {% cite rice1953classes %}. If a total verifier could decide whether every arbitrary generated program had a nontrivial semantic property, one could feed it program encodings and decide the corresponding Rice property, a contradiction. A claimed universally sound and complete verifier for arbitrary program behavior therefore cannot exist.

The reduction is a boundary result, not a counsel of despair. Finite-state systems, bounded executions, proof-carrying outputs, decidable logical fragments, unit tests, type systems, and theorem provers with explicit proof kernels can offer strong guarantees in restricted domains. A sound proof checker may be incomplete because the generator never finds a proof. A test suite may be complete for a finite specification but incomplete for arbitrary behavior. The correct engineering conclusion is to narrow the claim until the verifier's semantics and coverage can be stated exactly.

## Methods: three evidence layers that must not be mixed

This paper uses three evidence layers. The first is theory: the propositions above are symbolic consequences of stated assumptions. The second is seeded deterministic simulation: a fixed pseudorandom stream produces reproducible Monte Carlo illustrations and is compared with analytical formulas, but cannot validate an LLM. The third is a live engineering smoke test: one external request checks that an OpenAI request path works and that the returned schema can be recorded. It is not an accuracy experiment. Keeping the layers separate prevents an API success from being narrated as evidence for a reliability theorem.

### Seeded deterministic simulations

The executable suite is `scaffoldlab.experiments`. Its defaults are Python pseudorandom seed $$20{,}260{,}720$$, $$20{,}000$$ trials, and call budgets $$1,2,4,8,16,32$$. “Deterministic” means that the implementation consumes one seeded `random.Random` stream in a fixed order and serializes outputs with stable ordering. The observed proportions are still finite Monte Carlo estimates. Repeating a run with the same source, Python runtime, seed, trial count, and budgets should reproduce its bytes; it does not turn a sampled proportion into an exact probability.

The fixed-tree experiment uses independent local error probabilities $$0.02,0.03,0.04$$. Its analytical root-failure probability is

$$
1-(0.98)(0.97)(0.96)=0.087424,
$$

below the union bound $$0.09$$. A conjunctive decomposition experiment compares direct reliability $$0.90$$ with five mandatory children of reliability $$0.97$$ each; the predicted decomposed reliability is $$0.97^5=0.8587340257$$, so decomposition is worse under those assumptions.

The common-mode experiment uses zero mass $$q=0.20$$ and a $$\operatorname{Beta}(2,5)$$ nonzero component. At budget $$n$$ its predicted OR reliability is

$$
0.8\left[1-\frac{B(2,5+n)}{B(2,5)}\right],
$$

with ceiling $$0.8$$. The imperfect-verifier experiment uses $$p=0.20$$, $$\alpha=0.90$$, and $$\beta=0.05$$. Its pass probability is $$0.22$$, predicted coverage at budget $$n$$ is $$1-0.78^n$$, and correctness conditional on acceptance is

$$
\frac{0.20\cdot0.90}{0.20\cdot0.90+0.80\cdot0.05}
=
\frac{9}{11}
\approx0.8181818182.
$$

The frontier-size experiment is a separate branching-process illustration, not the adaptive-pruning experiment from the theorem. It samples offspring count $$K\in\{0,1,2\}$$ with probabilities $$(0.55,0.35,0.10)$$, so $$\mathbb E[K]=0.55$$ and the iid expected total processed population is

$$
\frac{1}{1-\mathbb E[K]}=\frac{20}{9}.
$$

The dependence calculation reports all-success Fréchet bounds for three marginals equal to $$0.8$$: lower bound $$0.4$$, independence value $$0.512$$, and upper bound $$0.8$$. A final held-out-risk illustration draws $$1{,}000$$ Bernoulli losses with configured error $$0.12$$ and computes the one-sided $$\delta=0.05$$ Hoeffding upper bound. The realized sample proportions in every Monte Carlo family remain pending; the numbers in this paragraph are analytical predictions from the frozen parameters.

<!-- GENERATED_ARTIFACT_PENDING: deterministic_simulations; status=not_run; exact_rows=pending; hashes=pending; runtime=pending -->

No `results.json`, `curves.csv`, `reliability_curves.svg`, checksum, runtime, or realized Monte Carlo value is claimed in this version. Those exact generated-artifact values will replace the pending marker only after the suite is run from a clean environment.

### One-request live OpenAI engineering smoke test

The live test is deliberately one request and one task. The command `scaffoldlab live-smoke "What is the sum of all integers from 1 through 100 inclusive?" --max-output-tokens 256` constructs a solve-phase provider request at depth zero. `OpenAIProvider` calls the OpenAI Responses API once through `responses.parse`, with the model named by `OPENAI_MODEL`, a fixed system prompt, the serialized provider request as user input, the strict `Decision` schema as its text format, and a maximum of 256 output tokens. The SDK is initialized with `max_retries=0`. There are no parallel calls, hidden judge calls, or follow-up corrections. The semantic oracle is the closed-form sum $$100\cdot101/2=5050$$.

The command's structured output contains a decision and reported output-token count. The semantic pass condition is an `answer` action whose answer, after surrounding-whitespace removal, is exactly `5050`. A schema-valid `decompose` or `abstain` action passes transport and parsing checks but fails the semantic smoke check. The execution record should contain the UTC start time, configured model name, command exit status, decision kind, redacted structured stdout, output-token count, wall-clock duration, and SHA-256 digests of stdout and stderr. Provider request identifiers, HTTP status, system fingerprints, and raw transport responses are not exposed by the current wrapper and must not be claimed. Credentials and authorization headers are never recorded.

The analytical prediction is that a conforming service returns one parseable response and that a capable model answers 5050. This is not reported as an observed outcome. One easy arithmetic request cannot estimate accuracy, calibration, independence, or common-mode error; its purpose is only to catch request-shape, authentication, routing, parsing, and artifact-capture failures.

<!-- GENERATED_ARTIFACT_PENDING: live_openai_smoke_test; status=not_run; utc_timestamp=pending; configured_model=pending; exit_status=pending; decision_kind=pending; answer=pending; output_tokens=pending; duration_ms=pending; stdout_sha256=pending; stderr_sha256=pending -->

If the one request fails operationally, the failure is retained as the result. The protocol forbids a retry because replacing the first observation would turn a smoke test into an undisclosed selection procedure.

## Reproducibility and analysis discipline

The manuscript freezes the mathematical definitions, simulation defaults, live question, extraction rule, and pass conditions before artifacts are generated. From `scaffolding_reliability`, the reproducible sequence is to synchronize the Python 3.12 environment, activate it with `source .venv/bin/activate`, run `pytest`, and then invoke `python -m scaffoldlab.experiments --seed 20260720 --trials 20000 --output paper/generated`. The deterministic suite requires no network access. The live command is separate and must read credentials only from the environment. Generated records should be immutable, content-addressed, and accompanied by the source revision and environment lock hash.

All empirical claims must identify their layer. A theorem is checked by proof and, optionally, numerical illustration. A simulation row is a generated calculation under a synthetic model, not evidence about deployment behavior. A live response is an engineering observation, not a distributional estimate. Any later benchmark study should use a preregistered task split, preserve paired task identifiers across budgets, freeze policies before final testing, report timeouts and abstentions, and retain per-task candidate outcomes so that dependence can be estimated.

## Limitations

The local-failure bounds depend on a correct specification of essential obligations. Unknown unknowns, misspecified ground truth, and composition failures omitted from the event set remain outside the bound. Conditional local error bounds may be difficult to estimate under an adaptive visitation policy. The frontier-promise process $$M_t$$ is useful only when it has an operational interpretation and held-out calibration; an arbitrary heuristic score does not acquire theorem status by being named promise.

The latent-$$\Theta$$ model imposes exchangeability and conditional iid behavior. Real candidate sequences can have order effects, context accumulation, self-conditioning, and changing proposal kernels. The beta family is an illustration, not a universal law. Pairwise correlation alone does not determine higher-order joint behavior, and the Fréchet bounds can be too wide for decisions even though they are mathematically sharp.

The binary-verifier ceiling assumes stationary class-conditional rates and first-accept selection. Learned verifiers can have score-dependent and adversarially selected errors. Calibration estimates are finite-sample and distribution-specific. Binned summaries hide within-bin variation, while abstention can move cost to users or downstream systems. The no-free-lunch and undecidability sections concern unrestricted classes; applying them to a bounded benchmark without qualification would be an overreach.

Finally, the deterministic simulations and live request are pending. This version contains no generated empirical outcome. Its numerical examples are evaluations of displayed formulas. A later version must preserve failed checks as well as passed checks and must not backfill predictions as observations.

## Discussion

The theory suggests a diagnostic order for test-time compute. First ask whether extra calls create alternatives or extra mandatory gates. Then ask whether those alternatives differ after conditioning on task difficulty and shared context. Next ask whether adaptive search preserves the mass of valid continuations. Finally ask whether the selector is sound enough, complete enough, and calibrated enough on held-out tasks. The weakest of these components controls the asymptote.

This view reconciles several apparently conflicting observations. Self-consistency can work because multiple paths expose answer-level redundancy {% cite wang2023selfconsistency %}. Decomposition can work because it changes the local task distribution or inserts symbolic modules {% cite zhou2023least khot2023decomposed %}. Verifier-guided search can work because correctness may be easier to recognize than to generate {% cite cobbe2021verifiers %}. Compute-optimal allocation can work because marginal value varies by prompt difficulty {% cite snell2025scaling %}. Yet none of these findings implies that repeated calls from one error family, judged by one fallible verifier, approach certainty.

The practical stopping condition is therefore evidential. Stop expanding when the held-out lower bound on marginal utility falls below its cost, when frontier drift becomes negative, when verifier precision sets the dominant ceiling, or when the system should abstain. “Use more compute” is not a reliability policy. A reliability policy specifies where diversity comes from, what evidence licenses selection, what happens on nonreturn, and which distribution supports the claim.

## Data and code availability

This manuscript introduces no human-subject or proprietary dataset. The executable simulation code is available in `src/scaffoldlab/experiments.py`, the one-call provider in `src/scaffoldlab/openai_client.py`, the command-line entry point in `src/scaffoldlab/cli.py`, and offline tests in `tests/` under `scaffolding_reliability`. At this version, no generated simulation or live-response artifact exists. Any released live record will be redacted and content-hashed and will exclude credentials and transport headers.

## Conflicts of interest

The author declares no conflicts of interest relevant to this manuscript.

## Funding

No external funding was received specifically for this work.

## Author contributions

Carlo Nicolini conceived the study, defined the theoretical framework and empirical separation, and is responsible for validation and final approval of generated artifacts. AI assistance supported literature discovery, formal counterexample checking, drafting, and bibliography consistency checks; responsibility for the claims remains with the human author.

## AI-use disclosure

A generative AI coding and writing assistant was used to search for official bibliographic records, organize the argument, check algebraic edge cases, and draft prose under explicit constraints. No AI-generated empirical value is presented as an observation. The assistant did not execute the pending deterministic suite or the live OpenAI request in this manuscript version. Bibliographic metadata were checked against DOI records, official proceedings, publisher pages, or arXiv records, and citation-key consistency was checked mechanically.

---

## References

{% bibliography --cited %}
