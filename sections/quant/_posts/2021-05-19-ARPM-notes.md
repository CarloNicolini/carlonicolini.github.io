---
layout: post
date: 2021-05-19
published: false
title: ARPM notes
---

Credit risk is the risk of default of loan-type instruments.
We use the term default to differentiate from credit spread risk.

## Definitions
Variable $D$ is the time of default:

\begin{equation}
D \equiv \inf \left \lbrack t \, \textrm{such that} V_{t}^{assets} \leq V_t^{liab} \right\rbrack
\end{equation}

Is the first time when the value of assets is lower than the value of liabilities, or in alternative, when the entity is not able to maintain the promise he makes.
$D$ can be considered a stochastic variable $\textrm{Bernoulli}$ with the only parameter the probability of default and that is the only crucial parameter to model credit risk.
Indeed we have that 

\begin{equation}
1_{D \in [t, t+1)} \sim \textrm{Bernoulli}(p_t)
\end{equation}
where $p_t$ is the probability of default.

The other ingredient is the **exposure at default**, how much one has at stake.

$$
\textrm{EAD}_t = \max \{0, V_{t-} | D = t \}
$$

Finally the  **loss given default**, is obtained as $1-\textrm{recovery rate}$ where the recovery rate is the percentage of things you may get back.
Importantly is to note that given that default events are final, we must model things conditionally.

Credit agencies and NLP methods find a way to bucket credit risky entities into credit ratings.
Ratings generalize the concept of default into buckets AAA,AA,A til D: AAA is good, then AA, A...
We indicate ratings with categorical variable $C$.

Default must be described by exogenous variables 

$$\mathbf{X}_t \equiv (X_{1,t}, \ldots, X_{k,t})'$$

Ratings are categorical distributions based on how close they are to a possible default.
Still the simple version 0/1 is informative.

## Conditioning risk divers
Default is once in a lifetime event, hence one should study the conditional distribution of next period condition of default conditioned on the set of some parameters. Hence one needs to look at exogenous factors $ \mathbf{x}_t $ to model default state.
More in general we need to model conditional transition rates of ratings:

$$
C_{t+1}  \mathbf{x}_t \sim \left ( c, p_{\theta}(c | \mathbf{x}_t)\right )_{c=0}^{\bar{c}} 
$$

where $\theta$ are parameters to be estimated.

The **loss given default** has a distribution with values in the interval $[0,1]$ such at the beta distribution. Similar to the event of default, we aim
at modeling the parameters of the beta distribution **conditional** on the realization of a set of obligor specific risk-drivers

$$
Lgd_{t | \{ D=t, \mathbf{X}_t = \mathbf{x}_t \}} \sim \textrm{Beta}(\alpha_{\theta}(x_t), \gamma_\theta(\mathbf{x}_t))
$$

where $\boldsymbol \theta$ is a vector of parameters to be estimated.

Importantly we do not need to worry about the risk drivers of exposure at default, because the value $V_t$ of a financial instrument at any time is determined by a set of instrument specific risk-drivers. Thereore to model EAD, we need to model specific risk drivers of the value $V_t$.
Here we discuss the key exogenous risk drivers $\mathbf{X}_t$ behind credit risk, which can be divided into four broad categories:

$$
\textrm{credit conditioning risk drivers:} \mathbf{X}_t \supset \left \lbrack \mathbf{X}_{t}^{struct}, \mathbf{X}_t^{macro}, \mathbf{X}_t^{mkt}, \mathbf{X}_t^{proc}\right \rbrack
$$

### Structural risk drivers $\mathbf{X}_t^{\textrm{struct}}$

It is natural to include leverage in the natural risk-drivers:

$$
L_t \subset \mathbf{X}_t^{\textrm{struct}}
$$

One can define **log-leverage**: when "log-leverage" is positive, then one is in default. Log-leverage is defined as:

$$
L = \log \left( \frac{V_t^{liab}}{V_t^{assets}}\right)
$$

Log-leverage is a natural scoring for ratings, not only for 0/1 events but more in general for ratings (multiclass classification problems).
More generally we can associate higher and higher ratings $C_t$ with more and more negative values for falling into sub-intervals of the real-line.

\begin{equation}
C_t = c \iff L_t \in ( l^{(c-1)}, l^{(c)} )
\end{equation}

### Dimension reduction

If the number $\bar{d}$ of risk drivers is too large then we need to do dimension reduction via linear factor models.

### Aggregate risk divers

The obligor level models provide the distribution of the credit variables, namely default event, rating migration, exposure at default and loss given default, **conditional** on the credit risk drivers.
Alternativel we can attempt model directly a credit variable of interest for a specific obligor $\bar{n}$ as a risk driver $X_{\bar{n},t}$ under the assumption that such variable behaves as the cross-sectional average of the same variable across a given set of comparable obligors $\mathcal{M}$, as follows

\begin{equation}
X_{\bar{n},t} \approx \frac{\sum_{n\in \mathcal{M} X_{n,t}}}{\sum_{n \in \mathcal{M}} 1_{n,t}}
\end{equation}

Then the risk divers that we want to model econometrically become the cross-sectional sums on the right hand side of the above equation. The most notable such approach is used to model the ratings.

More precisely, let us denote by $C_{n,t}$ the rating of obligor $n$ at time $t$. To study the migration, we record the number of obligors in each rating $c\in \{ 0, \ldots, \bar{c}\}$ at time $t$ which we denote by $N_{c,t}$:

\begin{equation}
N_{c,t} \equiv \sum_n 1_{C_{n,t}=c}
\end{equation}

Additionally, we record the **cumulative number of migrations** from a generic bucket $c$ to a different bucket $\tilde{c}$ up to time $t$, which we denote by $N_{c \to \bar{c},t}$

\begin{equation}
N_{c \to \tilde{c},t} = \sum_{s \leq t, n} 1_{(C_{n,s-1}=c, C_{n,s}=\tilde{c})}, \, c \neq \tilde{c}
\end{equation}

The aggregate cohort numbers $N_{c,t}$ and $N_{c \to \tilde{c},t}$ are essential to define and estimate the transition matrix that eventually models the migration from a given rating to another.
Then the aggregate credit risk driver read:

\begin{equation}
\textrm{aggregate risk driver } \mathbf{X}_t \supset \left( \{ N_{c,t}, N_{c\to \tilde{c},t} \}_{c, \tilde{c}=0,\ldots,\bar{c}} \right)
\end{equation}

The aggregate transition from one rating class to another one. Similarly to how we look at log-prices per stock we look at the cumulative number of transitions.
The most relevant item for credit is that we need to move from absolute estimation to conditional estimation.

# Pricing at the horizon: credit

Here we show the overlay effect of credit risk to simple market risk or actual market risk.
The final outcome is the aggregat market and credit P&L $\Pi_{t_{now} \to t_{hor}}^{m\&c}$.
It is not correct to express the market credit P&L as simply the sum of two separate components: the market component and the credit component:

\begin{equation}
\Pi_{t_{now} \to t_{hor}}^{m\&c} \neq \Pi_{t_{now} \to t_{hor}}^{market} + \Pi_{t_{now} \to t_{hor}}^{credit}
\end{equation}

The probability that the obligor defaults over a short horizon, of the order of one day, is neglibile. However for longer investment horizons of the order of months or longer, it becomes important to model the potential default of the obligor.
We need to model the three components of the credit risk framework: the time of default $D$, the exposure at default $Ead_D$ which is determined by the value $V_{D^-}$ right before default and the recovery rate $RecRate_D$ or equivalently its opposite, the loss given default $Lgd_D$.

### Market and credit value
To model the market risk on the value $V_{t_{hor}}$ at any time horizon $t_{hor} > t_{now}$ we could use the available information.
We use $\tilde{\mathbf{X}}^m_{t_{now} \to t_{hor}}$ for the market risk drivers process, to distinguish them from the credit risk drivers process, that drives the default event $1_{D\in (t_{now}, t_{hor})}$.

