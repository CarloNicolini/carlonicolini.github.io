---
layout: post
title: Introducing skfolio new online convex optimization module
date: 2025-10-03
published: true
categories: science
---

## Bridging online convex optimization into skfolio

For a long time, something about portfolio optimization just didn't sit right with me.

When I started building `skfolio`, I was primarily focused on bringing classical, batch optimization methods—like Markowitz mean-variance and Black-Litterman—into the familiar `scikit-learn` ecosystem. And don't get me wrong, those tools are incredibly powerful. But for months, I found myself increasingly frustrated by a fundamental mismatch between the math and reality.

In the batch paradigm, we take a historical window of returns, estimate expected returns and covariance matrices, and optimize our weights as if the market were a static dataset. Sometimes we even throw in assumptions about Gaussian returns for good measure. But anyone who has traded knows that financial markets are fundamentally sequential. Prices arrive day by day, tick by tick. We are forced to make allocation decisions on the fly, without knowing the future, and certainly without knowing whether the underlying distribution will behave the way our historical window suggests.

I wanted to find a framework that actually respected the sequential nature of the market.

## Descending a (convex) rabbit hole

This frustration sent me down a deep rabbit hole into the literature of online portfolio selection (OLPS). I started by reading the classic Li and Hoi survey {% cite li2014online %}, and the financial intuition immediately resonated with me.

Algorithms like PAMR (passive aggressive mean reversion), CWMR (confidence weighted mean reversion), and OLMAR (online moving average reversion) made intuitive sense.

> If a stock drops, maybe it's mean-reverting and we should buy more; if the portfolio drifts too far from a moving average, rebalance it.

But as I tried to implement them, I hit a wall. While the financial logic was brilliant, mathematically, the algorithms felt like a disjointed collection of isolated heuristics. Every paper seemed to invent a bespoke optimization problem and a custom solver just for that specific strategy. There was no unifying thread. How was I supposed to build a cohesive, extensible software module out of a dozen different bespoke rules?

## Engineering math for the best API

I was stuck on this architectural problem for weeks.
Then, I stumbled upon two foundational texts that completely rewired my thinking: Elad Hazan's *Introduction to Online Convex Optimization* {% cite hazan2016introduction %} and Francesco Orabona's notes on *A Modern Introduction to Online Learning* {% cite orabona2019modern %}.

I realized I didn't need to model the market probabilistically at all. What if we abandoned the assumptions about expected risk and return, and instead framed the problem as a repeated game against an *adversary*?

In this mindset, at each time step $t$, we choose a portfolio $\mathbf{w}_t$ from the probability simplex $\Delta_d$. The market (the adversary) then reveals the relative price vector $\mathbf{x}_t$, and we suffer a loss:

$$
f_t(\mathbf{w}_t) = -\log(\mathbf{w}_t^\top \mathbf{x}_t)
$$

Instead of maximizing an expected return, our goal is simply to minimize **regret**—the difference between our accumulated loss and the loss we would have suffered had we just picked the single best fixed portfolio in hindsight:

$$
\text{Regret}_T = \sum_{t=1}^T f_t(\mathbf{w}_t) - \textrm{min}_{\mathbf{w} \in \Delta_d} \sum_{t=1}^T f_t(\mathbf{w})
$$

Suddenly, the Li and Hoi survey made sense in a completely new way. All those heuristic strategies were actually just first-order optimization algorithms trying to guarantee sub-linear regret.

### The challenge

Understanding the math was one thing, but translating this beautiful, rigorous framework into the `skfolio` and `scikit-learn` ecosystem was a massive engineering challenge.

`scikit-learn` estimators are generally built for batch learning: you call `.fit(X)` and you're done. But online convex optimization (OCO) is intensely dynamic. Weights update continuously as new data streams in. How do you design an API that captures this dynamism without breaking the familiar compositional patterns that make `skfolio` so nice to use?

I spent a long time tearing apart the old algorithms, trying to find their structural seams.
I also wanted a solution that let the user not only optimize based on the Kelly's maximum log-wealth criterion, but to support *any* possible portfolio risk metric, like minimizing portfolio variance or CVaR.
It turned out that to do that I needed to compute the gradients of various risk functions against the asset weights.
Naturally this could be done via the nice `autograd` package: the result was for sure correct but it required me to remap any pre-existing skfolio portfolio metric into the *autograd* package. Moreover it was slow and heavy to compute.
Hence I derived the gradients with respect to *any* existing risk measure manually, and verified that the results are numerically correct.

Here is a summary of some of the analytical gradients I implemented to make the online optimization extremely fast and exact:

<table style="font-size:0.75em; width:100%; border-collapse: collapse;">
  <caption>
    <strong>Notation:</strong> $\mathbf{w}$ = portfolio weights, $\mathbf{r}_t$ = asset returns at time $t$, $T$ = number of periods, $\Sigma$ = covariance matrix, $\mu$ = target/mean return, $\pi$ = permutation sorting portfolio returns $\mathbf{w}^\top\mathbf{r}_t$ in ascending order, $\omega_k$ = OWA weights, $k = (1-\beta)T$ with $\beta$ = confidence level, $\theta$ = temperature parameter, $p_t$ = entropic probabilities.
  </caption>
  <thead>
    <tr style="border-top: 2px solid #444; border-bottom: 2px solid #444;">
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px; text-align: left;">Risk Measure</th>
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px; text-align: left;">Formula</th>
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px; text-align: left;">Gradient $\nabla_{\mathbf{w}}$</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-top:1px solid #ddd; border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;"><strong>Log-Wealth</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$-\log(1 + \mathbf{w}^\top \mathbf{r}_t)$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$\frac{-\mathbf{r}_t}{1 + \mathbf{w}^\top \mathbf{r}_t}$</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;"><strong>Variance</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$\mathbf{w}^\top \Sigma \mathbf{w}$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$2\Sigma \mathbf{w}$</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;"><strong>Semi-Variance</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$\frac{1}{T-1} \sum_{\mathbf{r}_t^\top \mathbf{w} < \mu} (\mu - \mathbf{r}_t^\top \mathbf{w})^2$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$\frac{2}{T-1} \sum_{\mathbf{r}_t^\top \mathbf{w} < \mu} (\mathbf{r}_t^\top \mathbf{w} - \mu)$<br>$\times (\mathbf{r}_t - \nabla\mu)$</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;"><strong>Mean Absolute Deviation</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$\frac{1}{T} \sum_{t=1}^T |\mathbf{r}_t^\top \mathbf{w} - \mu|$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$\frac{1}{T} \sum_{t=1}^T \text{sign}(\mathbf{r}_t^\top \mathbf{w} - \mu)$<br>$\times (\mathbf{r}_t - \nabla\mu)$</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;"><strong>Worst Realization</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$-\min_t (\mathbf{r}_t^\top \mathbf{w})$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$-\mathbf{r}_{\text{worst}}$</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;"><strong>Gini Mean Difference</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$\sum_{t=1}^T \omega_{\pi(t)} (\mathbf{r}_t^\top \mathbf{w})$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$\sum_{t=1}^T \omega_{\pi(t)} \mathbf{r}_t$ <br><small>(where $\pi$ is sort permutation, $\omega_k$ are OWA weights)</small></td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;"><strong>CVaR (Conditional Value at Risk)</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$-\frac{1}{k}\sum_{t=1}^{\lfloor k \rfloor} \mathbf{w}^\top\mathbf{r}_{\pi(t)}$<br>$+ \mathbf{w}^\top\mathbf{r}_{\pi(\lceil k \rceil)}\big(\frac{\lceil k \rceil}{k} - 1\big)$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$-\frac{1}{k}\sum_{t=1}^{\lfloor k \rfloor} \mathbf{r}_{\pi(t)}$<br>$+ \mathbf{r}_{\pi(\lceil k \rceil)}\big(\frac{\lceil k \rceil}{k} - 1\big)$</td>
    </tr>
    <tr style="border-bottom:2px solid #444;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;"><strong>EVaR (Entropic Value at Risk)</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$\inf_{\theta > 0} \Big\{ \theta \log \Big( \frac{1}{(1-\beta)T}$<br>$\times \sum_{t=1}^T \exp\big(\frac{-\mathbf{r}_t^\top \mathbf{w}}{\theta}\big) \Big) \Big\}$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 4px;">$-\sum_{t=1}^T p_t \mathbf{r}_t$ <br><small>(where $p_t \propto \exp(-\theta^* \mathbf{r}_t^\top \mathbf{w})$)</small></td>
    </tr>
  </tbody>
</table>

<div>
<img src="/static/postfigures/skfolio_online_basic.svg" alt="skfolio_batch_vs_online">
<caption>
Batch learning vs. online convex optimization for portfolio selection in <code>skfolio</code>. In batch approaches, portfolio weights are updated after observing the entire dataset, whereas online learning adjusts weights sequentially after each observed return, enabling more adaptive and responsive strategies.
</caption>
</div>

## The solution: decoupling the architecture

The breakthrough finally came when I started the `universal_portfolios` branch. I realized that if I decoupled the moving parts, everything snapped into place.

I broke the problem down into three independent, composable pieces:

1. **Predictors**: the things that extract signals from the sequence of prices (like tracking a moving average or a trend). In modern OCO, this can also take the form of *optimism*, where we try to guess the next gradient before taking a step {% cite lekeufack2024optimistic %} and also {% cite orabona2019modern %} chapter 12.
2. **Objectives**: the instantaneous loss function we want to minimize (like log-wealth, or a hinge loss that penalizes margin violations).
3. **Engines**: the core mathematical update rules that actually move the portfolio weights.

By isolating the engines, I could implement a unified `FirstOrderOCO` estimator that handles the heavy lifting.
To satisfy the strict long-only, fully-invested constraints of the portfolio simplex, I implemented mirror descent and Follow-The-Regularized-Leader (FTRL) using different **mirror maps**.

Instead of writing a custom solver for every strategy, the update rule became a generalized FTRL expression:

$$
\mathbf{w}_{t+1} = \textrm{argmin}_{\mathbf{w} \in \Delta_d}  \left\{ \eta_t \sum_{s=1}^t \langle \mathbf{g}_s, \mathbf{w} \rangle + \psi(\mathbf{w}) \right\}
$$

Where $\mathbf{g}_s$ is the gradient of our instantaneous objective, and $\psi(\mathbf{w})$ is a strictly convex regularizer that defines our mirror map geometry.

If I wanted to change how the weights were updated, I didn't need to rewrite the trading logic. I just needed to swap out the regularizer $\psi$.

### The interplay of mirror maps

This modularity allowed me to experiment with how different geometries affect portfolio learning. The choice of the mirror map fundamentally changes the algorithm's behavior on the simplex.

For instance, using a standard Euclidean mirror map ($\psi(\mathbf{w}) = \frac{1}{2}\|\mathbf{w}\|_2^2$) gives us online gradient descent (OGD). But on the portfolio simplex, Euclidean geometry can be overly aggressive and often unsuited, as it doesn't naturally respect the multiplicative nature of wealth.

Swap that for an entropic mirror map (the negative entropy function $\psi(\mathbf{w}) = \sum_i w_i \log w_i$), and the `FirstOrderOCO` engine instantly becomes the famous exponentiated gradient (EG) algorithm {% cite helmbold1998line %}.
The updates become elegantly multiplicative, naturally avoiding negative weights so that with a learning rate $\eta_t$ and the current gradients $\mathbf{g}_t$, one has the update rule:

$$
w_{t+1,i} \propto \exp\!\left(-\eta_t \sum_{s=1}^t g_{s,i}\right)
$$

Even more fascinating was implementing the Burg entropy mirror map (used in the PROD or Soft-Bayes algorithm {% cite orseau2017soft %}).
Because its regularizer acts as a log-barrier ($\psi(\mathbf{w}) = -\sum_i \log w_i$), it naturally prevents any single asset's weight from collapsing to zero. In my empirical tests, this made the algorithm uniquely robust to large learning rates without suffering from catastrophic over-concentration.

<div>
<img src="/static/postfigures/skfolio_online_mirror_maps.svg" alt="online_mirror_maps">
<caption>
Comparison of mirror maps and regularizers used in online convex optimization for portfolio learning. Each map induces a different update geometry on the portfolio simplex, enabling a flexible plug-and-play framework for new algorithms in <code>skfolio</code>.
</caption>
</div>

In this table I present some of the most important mirror maps $\psi$ that I've developed in the [`skfolio.optimization.online._mirror_maps`]():
<table style="font-size:0.90em; width:100%; border-collapse: collapse;">
  <caption style="caption-side: bottom; padding-top: 8px; font-size:0.95em; color:#444;">
    <strong>Table:</strong> Key mirror maps and their associated regularizers used in online convex optimization algorithms for portfolio selection in <code>skfolio</code>. Each row summarizes a representative algorithm, its mirror map and induced geometric structure.
  </caption>
  <thead>
    <tr style="border-top: 2px solid #444; border-bottom: 2px solid #444;">
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Algorithm</th>
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Regularizer $\psi(w)$</th>
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Mirror Map</th>
      <th style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-top:1px solid #ddd; border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>EG</strong> (Exponentiated Gradient)</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">$\sum_i w_i \log w_i$ (neg-entropy)</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Softmax</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Multiplicative</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>OGD</strong> (Online Gradient Descent)</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">$\frac{1}{2}w_2^2$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Identity</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Euclidean</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>PROD</strong> (Soft-Bayes)</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">$-\sum_i \log w_i$<br> (Burg entropy)</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">$w_i \mapsto -1/w_i$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Log-barrier</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>AdaGrad</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">$\frac{1}{2} w^\top H_t w$, $H_t = \text{diag}(\sqrt{\sum_s g_s^2})$</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Adaptive diagonal</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Data-dependent</td>
    </tr>
    <tr style="border-bottom:1px solid #ddd;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>SWORD</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Variation-adaptive meta-learning</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Meta-aggregation</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Composite</td>
    </tr>
    <tr style="border-bottom:2px solid #444;">
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;"><strong>Ada-BARRONS</strong></td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Composite barrier + adaptive quadratic</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Barrier + Mahalanobis</td>
      <td style="border-right:1px solid #bbb; border-left: 1px solid #bbb; padding: 6px;">Second-order</td>
    </tr>
  </tbody>
</table>

### Adaptive learning rates: AdaGrad

While mirror maps control the geometry of our updates, what about the speed? In standard online gradient descent, finding the right learning rate is notoriously difficult. If we step too far, we overshoot; if we step too little, we never learn.

This is where algorithms like **AdaGrad** (adaptive gradient) {% cite orabona2019modern %} or SWORD {% cite zhao2020dynamic %} come into play.
Instead of using a single, fixed learning rate, AdaGrad adapts its step size on the fly for *each individual asset*. It does this by keeping a running sum of the squared gradients observed so far:

$$
\eta_{t,i} = \frac{D_i}{\sqrt{\sum_{s=1}^t g_{s,i}^2}}
$$

Assets that experience large, volatile price swings automatically get their learning rates dampened, while stable assets maintain larger step sizes. In the `skfolio` OCO engine, you can effortlessly switch to the AdaGrad strategy to benefit from this automatic, coordinate-wise scaling. It beautifully removes the need to manually tune step sizes, adapting intrinsically to the market's volatility.

### Optimism as a predictor

Another beautiful consequence of this architecture is how easily we can implement **optimistic mirror descent** (or more generally, Optimistic FTRL). 
In adversarial markets, reacting to the last observed gradient is always one step too late.
But what if we could *predict* the next gradient instead?

We start by letting $$ \mathbf{m}_{t+1} $$ be our prediction of the next gradient $$ \mathbf{g}_{t+1} $$.
By feeding this optimistic predictor into the `FirstOrderOCO` engine, the main FTRL update rule gets an additional lookahead term:

$$
\mathbf{w}_{t+1} = \textrm{argmin}_{\mathbf{w} \in \Delta_d}  \left\{ \eta_t \left( \sum_{s=1}^t \mathbf{g}_s + \mathbf{m}_{t+1} \right)^\top \mathbf{w} + \psi(\mathbf{w}) \right\}
$$

We take a *lookahead* step based on our prediction $$ \mathbf{m}_{t+1} $$, and then correct it at the next step once the true market prices and the actual gradient $$ \mathbf{g}_{t+1} $$ are revealed.

In financial terms, this translates beautifully to momentum tracking. For example, our predictor could simply be the moving average of the past gradients:

$$
\mathbf{m}_{t+1} = \frac{1}{K} \sum_{k=0}^{K-1} \mathbf{g}_{t-k}
$$

Instead of chasing daily noise, setting $K$ to average the last $60$ to $120$ days of gradients acts as a momentum lookback, which turns out to be one of the few first-order enhancements that genuinely improves follow-the-winner strategies.

### Hedging our bets: SWORD and meta-experts

Even with adaptive learning rates and optimism, there is a fundamental uncertainty we can't escape: the market's non-stationarity.
We don't know in advance how much the optimal portfolio will drift over time (what the literature calls the *path-length*), nor do we know the exact variation of the gradients.

To solve this, I implemented the **SWORD** (Smoothness-aware Online Learning with Dynamic Regret) family of algorithms based on the ideas laid out by {% cite zhao2020dynamic %}.
Instead of relying on a single learning rate, SWORD uses a meta-expert framework.
It spins up multiple *expert* algorithms simultaneously, each running with a different step size from a predefined pool.

Then, a meta-algorithm (specifically, an optimistic variant of the Hedge algorithm) continuously evaluates these experts and shifts our actual portfolio weight towards the most successful ones.
The result is a strategy that achieves the "best of both worlds" as it automatically balances the tradeoff between learning quickly in turbulent markets and staying steady in calm ones, guaranteeing optimal dynamic regret without needing a crystal ball.

## Empirical check: daily mean reversion vs. monthly momentum

Building the framework was incredibly satisfying, but the real test was running these algorithms on decades of historical financial data. What I found fundamentally shifted how I view these algorithms.

When I tested follow-the-winner (**FTW**) methods like exponentiated gradient against follow-the-loser (**FTL**) methods like *PAMR* and *OLMAR* at a daily frequency, the results were striking.
The FTW methods were practically indistinguishable from a naïve uniform constant rebalanced portfolio (holding an equal weight of all assets).

The gradients were simply too small—what I call the "vanishing gradient exponent".
Because typical daily equity returns are tiny (often around $\bar{r} \sim 10^{-4}$), I proved that under the regret-optimal learning rate schedule, the maximum weight deviation from a uniform $1/d$ portfolio after $T$ days is:

$$
\max_i |w_{T,i} - 1/d| \approx \frac{\sqrt{T \log d}}{d} \cdot |\bar{r}|_\infty \approx \mathcal{O}(10^{-2})
$$

Any small steps they did take were punished by the market's daily cross-sectional mean reversion. Yesterday's relative winners tend to be today's relative losers.

**Follow-the-Loser** methods, which explicitly exploit this mean reversion, solve a Passive-Aggressive constrained problem at each round:

$$
\mathbf{w}_{t+1} = \arg\min_{\mathbf{w} \in \Delta_d} \frac{1}{2}\|\mathbf{w} - \mathbf{w}_t\|_2^2 \quad \text{s.t.} \quad \text{margin constraint on } \mathbf{w}
$$

This forces the portfolio away from recent winners. At the daily level, FTL methods completely dominated.

But then, I changed the rebalancing frequency to *monthly*. Suddenly, the roles reversed entirely. 
Because returns aggregate multiplicatively, I derived a $\sqrt{\Delta}$ scaling law for the FTW gradient exponent, where $\Delta$ is the rebalancing period in days. At a monthly horizon ($\Delta=21$), the maximum weight deviation grows proportionally:

$$
\max_i |w_{T,i} - 1/d| \propto \sqrt{\Delta}
$$

This meant the FTW methods finally had enough signal and scale to break away from the uniform portfolio and become profitable. At this horizon, short-term mean reversion gives way to the well-documented intermediate-term momentum anomaly, often called the **Jegadeesh-Titman effect**{% cite jegadeesh1993returns %}.
The FTL algorithms that were highly profitable on a daily basis started destroying wealth. Meanwhile, the FTW methods, which are implicit momentum followers, finally shined.

This frequency crossover was a profound realization. The OCO algorithms aren't magic money machines; their effectiveness depends entirely on matching their implicit directional bias—momentum versus mean-reversion—to the specific frequency of the market data.

## The result

After months of sketching, prototyping, running thousands of backtests, and refactoring, watching these components finally compose was incredible.

I didn't want to just release a black-box algorithm, but I also wanted the API to be as effortless as any other `scikit-learn` estimator. Today, in the new `skfolio.optimization.online` module, you can leverage high-level wrappers that cleanly encapsulate all this complexity.

For instance, instantiating a complex strategy like OLMAR on real market data looks like this:

```python
from skfolio.datasets import load_sp500_relatives_dataset
from skfolio.optimization.online import FollowTheLoser, FTLStrategy

# 1. Load sequential price relatives
X = load_sp500_relatives_dataset(net_returns=True)

# 2. Instantiate the online strategy as a scikit-learn estimator
# Under the hood, this configures the predictor, objective, and FirstOrderOCO engine
model = FollowTheLoser(
    strategy=FTLStrategy.OLMAR,
    olmar_predictor='ewma',
    olmar_alpha=0.5,
    epsilon=10.0,
    transaction_costs=0.001 # Realistic 10 bps transaction costs
)

# 3. Process the entire sequence of prices and return the final portfolio
portfolio = model.fit_predict(X)

# 4. Evaluate the performance
print(portfolio.summary())
```

The code block above represents what I wanted to do. You get the simplicity of `.fit_predict(X)`, but underneath, the financial intuition is cleanly handled by the predictors and objectives, while the rigorous math of sub-linear regret is safely executed by the `FirstOrderOCO` engine.

By shifting from static datasets to a dynamic, regret-minimization mindset, we are unlocking a massive literature of robust algorithms for `skfolio`. I'm still exploring the depths of what this framework can do—especially moving toward second-order methods like the online Newton step to better handle correlated market factors—but for the first time, the code actually reflects the sequential, breathing reality of the market.

---

# References

{% bibliography --cited %}

