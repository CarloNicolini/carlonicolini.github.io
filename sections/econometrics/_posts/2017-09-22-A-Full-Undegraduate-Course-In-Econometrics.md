---
layout: post
title: A Full Undergraduate Course in Econometrics
categories: science
published: false
use_math: true
date: 2017-09-22
---

<blockquote>
	"Introduction to econometrics with statistics and probability theory notes."
</blockquote>

# [Populations and samples in econometrics](https://www.youtube.com/watch?v=M9s91hSoNtk&index=5&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

Econometrics is concerned with how do we come up with estimates of population parameters given a sample.

# [Estimators - the basics](https://www.youtube.com/watch?v=qvR7sSGphQ4&index=6&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

For example on average what is the effect of one year of education on wages? We only have a sample from the population, say 1000 individuals.
We want to study the linear relation between wages and education using the sample data, for example in the form:

$$wages = \alpha + \beta \textrm{education}$$

Sample estimators are indicated with an hat for example $$\hat{\beta}$$. The idea is to feed the sample data and it outputs the estimate of the population parameter.
There is difference between the estimator $$\hat{\beta}$$ (a function) and the population estimate $$\beta^\star$$ (just a point).

# [Estimators properties](https://www.youtube.com/watch?v=UxbY85Cm9SQ&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU&index=7)

What does it mean to be a good estimator?
The sample estimator aren't going to be exactly as the population parameters. In the frequency plot we hope that on average our estimator outputs the population parameters.
We should have the maximum in the frequency plot at the population parameter.
This property is called **unbiased**.

The second property is that increasing the sample size, the estimator are closer and closer to the true population parameter.
Eventually the distribution should become a delta centered in $$\beta^\star$$.
We call this property **consistency** of the estimator.
If I arbitrarily increase my sample size $$n\rightarrow +\infty$$ I get a value which is closer and closer to the population parameter.

# [Unbiasedness and consistency](https://www.youtube.com/watch?v=21lXGc02XwM&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU&index=8)

Often unbiasedness and consistency are mixed up but they are not the same.
Unbiasedness indicates that $$E[\hat{\beta}] = \beta^{population}$$.

Consistency means that if I increase the sample size the values I get to the estimator are closer and closer to the population value.
It is possible though to have an estimator that is **biased** but consistent.
Increasing the sample size the estimator gets closer to the population parameter and the estimator gets **consistent**.

It's pretty usual to have an estimator consistent but unbiased, as we don't often have the luxury of having the two properties together.

# [Unbiasedness vs consistency of estimators - an example](https://www.youtube.com/watch?v=6i7mqDJICzQ&index=9&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

As an example let's take a population with mean $\mu$ that we want to estimate with just a sample from the population.
Use some statistic tool to make some guess about the parameters.

Let's say that
$$
\tilde{x} = \frac{1}{N-1} \sum \limits_{i=1}^N x_i
$$
is this an unbiased estimator?
Given that we know the population process we can apply the expectation operator, then
$$
E[\tilde{x}] = \frac{1}{N-1} \sum \limits_{i=1}^N E[x_i] = \frac{1}{N-1} N \mu = \frac{N \mu}{N-1}
$$
so in general this does not equal $$\mu$$, so we should use the sample mean to estimate the sample mean.
Is this estimator consistent? Yes because in the case $N \rightarrow +\infty$$ the expected value of $$E[\tilde{x}] \rightarrow \mu$$.

So for example the biased estimator $$\tilde{x}$$ is biased but consistent.

# [Efficiency of estimators](https://www.youtube.com/watch?v=6i7mqDJICzQ&index=9&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

What is the efficiency of an estimator?
Suppose to have an unbiased estimator $$\hat{\beta}$$ and another estimator $$\tilde{\beta}$$ which outputs a range of $$\beta$$ closer to the parameter.
In this case the $$\tilde{\beta}$$ is more **efficient** than $$\hat{\beta}$$ and has to be preferred.

Although in real-world situations it's often the case that with a more efficient estimator has some degree of bias.

# [Good estimator properties summary](https://www.youtube.com/watch?v=uh4zUdKvxPA&index=11&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

1. Unbiased: $$E[\hat{\beta}] = \beta^{population}$$
2. Consistency: as $$n \rightarrow \infty$$ it must be $$\hat{\beta} \rightarrow \beta^{population}$$.
3. Efficiency
4. Linearity in parameters: $$\hat{\beta}$$ must be linear in parameters of the sample.

# [Lines of best fit in econometrics](https://www.youtube.com/watch?v=KIQbe-FJoa8&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU&index=12)
Fitting is a way to estimate population parameters. Suppose there is some relation between education years and wages. We hypothesize there is some positive correlation between the two.
How does education affects the average wage of an individual?
Doing that is like drawing a line through the points in the 2D space x-y. The line tells us how much increase of education is needed to have an y increase in wage.
The slope of the line is the $$\beta^{pop}$$.
This is a relation of the form $$y= \alpha + \beta x$$.

Now given a sample of the population, can I draw a line, i.e. draw an estimate of the population parameter (slope of the line).

# [The mathematics behind drawing a line of best fit](https://www.youtube.com/watch?v=YL-NNb4gojA&index=13&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

One idea is to fit a line to minimize the sum of distances between the line and the points.
Use $$x_i$$ to predict $$y_i$$.
For example 

$$ S = \sum \limits_{i=1}^N \|(y_i - \hat{y}_i)\| $$.

This allows us to get $$\hat{\alpha}$$ and $$\hat{\beta}$$. The sum has to have modulus here.
This is one way: the problem of the modulus function is that is hard to differentiate.
It's better using a square sum:

$$ S = \sum \limits_{i=1}^N (y_i - \hat{y}_i)^2 $$.

In minimizing the sum of the square I don't care about small deviations from the line as from big deviations from the line, so outliers counts a lot and anomalous points move the fitted line close to them because of the square contribution.
Perhaps we can generalize for example to the fourth-power

$$ S = \sum \limits_{i=1}^N (y_i - \hat{y}_i)^4 $$

This would count big deviations a lot more. There are many different ways to fit a straight line to data, but actually the default is the sum of squares minimization.

# [Least squares estimators as BLUE](https://www.youtube.com/watch?v=vOBtEiij-fA&index=14&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

What does it mean to **least squares** estimators to be good?
This means that I have built some sort of population and an underlying process in the population that connects wages with the average wage. The problem in econometrics is that we don't have the entire population but only a sample.
We use some mathematical functions to make inferences to have estimates of $$\alpha^{pop}$$ and $$\beta^{pop}$$.

For an estimator to be good it must be **unbiased**, **consistent** and **efficient**.
The condition for an estimator to be good are called **BLUE**.

BLUE stands for **B**est **L**inear **U**nbiased **E**stimator.
These assumptions are called the Gauss-Markov assumptions.
The least-square estimator is a BLUE estimator. There are no other linear estimator that give us good unbiased estimate of the parameters.

# [Deriving least squares estimators - part 1](https://www.youtube.com/watch?v=Hi5EJnBHFB4&index=15&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

The Least Squares estimator is defined as

$$ S = \sum \limits_{i=1}^N (y_i - \hat{y}_i)^2$$

Here the $$\hat{y}_i = \hat{\alpha} + \hat{\beta} x_i$$ while $$y=\mu x + c$$. This is equivalent to 

$$ S = \sum \limits_{i=1}^N (y_i - \hat{\alpha} \hat{\beta} x_i)^2$$

To mimimize $$S$$ we need to differentiate with respect to $$\hat{\alpha}$$ and $$\hat{\beta}$$. In other words we have to set:

$$
\frac{\partial S}{\partial \hat{\alpha}}=0, \frac{\partial S}{\partial \hat{\beta}}=0
$$

The derivative with respect to $$\hat{\alpha}$$ results:

$$
\begin{equation}
\frac{\partial S}{\partial \hat{\alpha}}= -2 \sum \limits_{i=1}^N(y_i - \hat{\alpha} - \hat{\beta} x_i) = 0 \tag{I}\label{eq:partiallsalpha}
\end{equation}
$$

the one with respect to $$\hat{\beta}$$ is:

$$
\begin{equation}
\frac{\partial S}{\partial \hat{\beta}}= -2 \sum \limits_{i=1}^N x_i (y_i - \hat{\alpha} - \hat{\beta} x_i = 0 \tag{II}\label{eq:partiallsbeta}
\end{equation}
$$

These two conditions give us the estimates $$\hat{\alpha}$$ and $$\hat{\beta}$$.

# [Deriving least squares estimators - part 2](https://www.youtube.com/watch?v=hGv9fnmlYaU&index=16&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

We want to derive some useful statistical relationships, they are

$$
\sum \limits_{i=1}^N x_i = N \bar{x} \qquad \sum \limits_{i=1}^N y_i = N \bar{y} 
$$

These corresponds to computing the sample mean of $$x$$ and $$y$$.
This relation instead

$$
\sum \limits_{i=1}^N (x_i - \bar{x})(y_i - \bar{y}) = \sum \limits_{i=1}^N y_i(x_i -\bar{x}) = \sum \limits_{i=1}^N x_i(y_i - \bar{y})
$$

corresponds to computing the covariance between $$x_i$$ and $$y_i$$. It can be rewritten as

$$
\sum \limits_{i=1}^N x_i y_i - \bar{y} \sum \limits_{i=1}^N x_i - \bar{x} \sum \limits_{i=1}^N y_i + \bar{x}\bar{y} \sum \limits_{i=1}^N 1
$$

but the second and term summands correspond to the sample mean times $$N$$, so we obtain:

$$
\sum \limits_{i=1}^N x_i y_i - N \bar{y}\bar{x} - N \bar{y}\bar{x} + N \bar{y}\bar{x} = \sum \limits_{i=1}^N x_i y_i - N \bar{x} \bar{y}
$$

and this leads to the above said relationships.

# [Deriving least squares estimators - part 3](https://www.youtube.com/watch?v=jF3_s2wqPGQ&index=17&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

We can now use the above mentioned relationships and apply the zero derivative conditions to obtain the LS estimators. We rewrite the conditions here:

$$
\frac{\partial S}{\partial \hat{\alpha}}= -2 \sum \limits_{i=1}^N(y_i - \hat{\alpha} - \hat{\beta} x_i) = 0
$$

$$
\frac{\partial S}{\partial \hat{\beta}}= -2 \sum \limits_{i=1}^N x_i (y_i - \hat{\alpha} - \hat{\beta} x_i) = 0
$$

We use the two relationships to obtain:

$$
N \bar{y} = \hat{\alpha}N + \hat{\beta}N \bar{x}
$$

and we obtain:

$$
\bar{y} = \hat{\alpha} + \hat{\beta} \bar{x} \tag{III}
$$

This tells me that the line of best fit goes through $$\bar{y}$$ and $$\bar{x}$$. We use the other conditions to derive the values of $$\hat{\alpha},\hat{\beta}$$.

# [Deriving Least Squares Estimators - part 4](https://www.youtube.com/watch?v=AIjuYfjU9dc&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU&index=18)

$$\hat{\alpha},\hat{\beta}$$ has to be chosen such that the line of best fit goes through the sample mean. We use the derivative w.r.t $$\hat{\beta}$$ to impose the second condition.


$$
\sum \limits_{i=1}^N x_i y_i = \hat{\alpha} N \bar{x} + \hat{\beta} \sum \limits_{i=1}^N x_i^2 = (\bar{y}-\hat{\beta} \bar{x} + \hat{\beta} \sum \limits_{i=1}^N x_i^2
$$

and we finally obtain

$$
\sum \limits_{i=1}^N x_i y_i = N \bar{x}\bar{y} - \hat{\beta}N \bar{x}^2 + \hat{\beta} \sum \limits_{i=1}^N x_i^2
$$

# [Deriving Least Squares Estimators - part 5](https://www.youtube.com/watch?v=JC0Tm9j-k80&index=19&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

These are the least squares estimators $$\hat{\alpha},\hat{\beta}$$. These are BLUE estimators.

$$
\begin{equation}
\hat{\alpha} = \bar{y} - \hat{\beta} \bar{x}
\end{equation}
$$

$$
\begin{equation}
\hat{\beta} = \frac{\textrm{Cov}(x_i,y_i)}{\textrm{Var}(x_i)}
\end{equation}
$$


# [Least Squares Estimators - in summary](https://www.youtube.com/watch?v=y5INeKvfpcQ&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU&index=20)

# [Taking expectations of a random variable](https://www.youtube.com/watch?v=6XqICKT1Kug&index=21&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

The expectation of a random variable is defined in the discrete case as:

$$
E[X] = \sum \limits_{x} P(X=x)X
$$

where $$x$$ is the set of all possible values that the variable $$X$$ can take, or also called the *support* of $$X$$.
In the case of a fair dice with 6 faces, this is obviously computed as $$P(X=1)1 + P(X=2)2 + \ldots + P(X=6)6 = 21/6 = 3.5$$

In the case of continuous random variable we use the integral over the support of the random variable:

$$
E[X] = \int \limits_{-\infty}^{\infty} f_x(X) dx
$$

where $$f_x(X)$$ is called the probability density function of the random variable $$X$$.

# [Moments of a random variable](https://www.youtube.com/watch?v=U2L809GBMcI&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU&index=22)

The higher order moment of a random variable 

$$
E[X^k] = \int \limits_{-\infty}^{+\infty} x^k f_x(X) dx
$$

This is called the $$k$$-th moment of the distribution. For example the $$4$$-th moment is interesting in statistics.

# [Central moments of a random variable](https://www.youtube.com/watch?v=BXN8jgQTjao&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU&index=23)

Suppose a p.d.f of a random variable peaked at 10. The expectation of such delta distributed variable is the integral of a Dirac delta function $$\delta(x-10)$$.
In this case the expectation of $$E[x^2]$$ is 100.
Instead the expectation of $$E[(x-10)^2]=0$$. This is called the second central moment of the distribution, or $$\textrm{Var}(X)$$. It's the spread of the points around the mean.
The variance of $$X$$ is computed as 

$$\mathrm{Var}[X] = E[(X-E[X])^2]$$

Higher order moments tell about the tails of the distribution.
The central moments of a distribution are indicated as: 

$$
\mu_k = E[(X-E[X])^k] = \int \limits_{-\infty}^{\infty}(x-\mu)^k f(x) dx
$$

1. The zeroth central moment $$\mu_0$$ is 1.
2. The first central moment $$\mu_1$$ is 0 (not to be confused with the first (raw) moment itself, the expected value or mean).
3. The second central moment $$\mu_2$$ is called the **variance**, and is usually denoted $$\sigma^2$$, where $$\sigma$$ represents the standard deviation.
4. The third and fourth central moments are used to define the standardized moments which are used to define **skewness** and **kurtosis**, respectively.

# [Kurtosis](https://www.youtube.com/watch?v=Pf7awGwzy4k&index=24&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

Kurtosis is the 4-th central moment of a distribution.
Two variables can have same expected value and variance but if one has a fatter tail it's impossible to say because variance is relative to points near the expected value.

$$\textrm{Kur}[X] = E\left[\left(\frac{(x-\bar{x})}{\sigma}\right)^4\right ] = \frac{\mu_4}{\sigma^4}$$

where $$\mu_4$$ is the fourth central moment and $$\sigma$$ is the standard deviation.
Typically one refers to the measure $$\Gamma$$:

$$\Gamma[X] = \frac{\textrm{Kur[X]}}{\sigma^4} - 3$$

where the $$-3$$ is called the excess kurtosis compared to the kurtosis of the normal distribution.

# [Skewness](https://www.youtube.com/watch?v=z3XaFUP1rAM&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU&index=25)

Skewness is the 3rd central moment of a distribution. Skewness refers to the symmetry of the random	variable around the mean: the distribution has long positive tails.

Skewness is computed as:

$$Skewness[X] = E[(x - \bar{x})^3]$$

# [Expectations and Variance properties](https://www.youtube.com/watch?v=NcJdOXuUdgU&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU&index=26)

We know the definition of the expectation of a random variable $$X$$ computed as 

$$
E[X] = \int \limits_{-\infty}^{\infty} f_x(X) dx
$$

The expectation operator is a **linear** operator. In other words $$E[a X + b Y] = a E[X] + b E[Y]$$.
Instead for the variance this is not true as

$$\textrm{Var}[aX] = E[(aX - a \mu_x )^2] = a^2 \textrm{Var}[X].$$

We can compute also how the variance behaves in the case of linear combination of random variables $$X,Y$$:

$$
\textrm{Var}[aX + bY] = E[(aX + bY - a \mu_x - b\mu_y)^2] = a^2 \textrm{Var}[X] + b^2 \textrm{Var}[Y] + 2ab \textrm{Cov}[X,Y]
$$

# [Covariance and correlation](https://www.youtube.com/watch?v=KDw3hC2YNFc&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU&index=27)

Let's think about if we had two random variance $$X,YY$$ such that if $$X$$ increases also $$Y$$ increases. Mathematically we can say that $$X$$ and $$Y$$ are positively correlated. In mathematical terms we define the covariance as 

$$
\textrm{Cov}[X,Y] = E[(X-\mu_x)(Y-\mu_y)]
$$

We can normalize the covariance using the **correlation** between $$X,Y$$: this is based on the division by the square root of the product of the variance of $$X$$ and $$Y$$ individually:

$$
\textrm{Corr}[X,Y] = \frac{\textrm{Cov}[X,Y]}{\sqrt{\textrm{Var}[X] \textrm{Var}[Y]}} := \rho
$$

the correlation is bounded in  $$[-1,1]$$.

# [Population vs sample quantiles](https://www.youtube.com/watch?v=fOAZQ_U7-qk&index=28&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

# [The Population regression function](https://www.youtube.com/watch?v=oFaoCzj3YUY&index=29&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

# [Gauss-Markov assumptions - part 1](https://www.youtube.com/watch?v=NjTpHS5xLP8&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU&index=31)

The Gauss-Markov theorem states that in a linear regression model in which the errors have expectation zero and are uncorrelated and have equal variances, the best linear unbiased estimator (BLUE) of the coefficients is given by the ordinary least squares (OLS) estimator, provided it exists. The errors do not need to be normal, nor do they need to be independent and identically distributed (only uncorrelated with mean zero and homoskedastic with finite variance). 

We can list the Gauss-Markov assumptions here:

1. The population process must be linear in parameters (for example $$wages = \alpha + \beta education + u_i$$) where $$u_i$$ is an error term.
2. $$\{ x_i, y_i \}$$ are a random sample from the population. Each individual in the population must be equally likely picked. In other words all the data-point must come from the same population process.

3. Zero conditional mean of errors. This means that mathematically the expectation of $$E[u_i \vert educ]=0$$, in other words if I know someone level of education this does not help me to predict wheter he will be above or below the average population line.
If it happens that $$E[u_i \vert x_i]$$ means that the Least Squares estimators are **biased**, in other words the $$E[\hat{\beta} \vert x_i] \neq \beta^{pop}$$.
This is equivalent to say $$\textrm{Cov}[u_i, x_y]=0$, no correlations between noise and independent variables.

# [Gauss-Markov assumptions - part 2](https://www.youtube.com/watch?v=ti9h-Au8LQw&index=32&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

4. **no perfect collinearity** in regression. This means that if I have some model $$y=\alpha + \beta_1 x_1 + \beta a_2 x_2 + u$$ it means that there must not be an exact relationship between $$x_1$$ and $$x_2$$, for example there must **not** be relation of this kind $$x_1 = \delta_0 + \delta_1 x_2$$.

5. **Homoskedastic errrors**. This means that the distribution of errors stays relatively constants, in other words the variance of the errors is constant: $$\textrm{Var}[u_i] = \sigma^2$$ and **does not** vary with $$x_i$$.

6. **No serial correlations**. This means that $$Cov[u_i,u_j]=0$$, knowing one error does not help me predict another error.

# [ Zero conditional mean of errors](https://www.youtube.com/watch?v=msSDI328UPc&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU&index=33)

# [Omitted variable bias](https://en.wikipedia.org/wiki/Omitted-variable_bias)
Omitted-variable bias (OVB) occurs when a model created incorrectly leaves out one or more important factors.
The bias is created when the model compensates for the missing factor by over- or underestimating the effect of one of the other factors.
OVB is the bias that appears in the estimates of parameters in a regression analysis, when the assumed specification is incorrect in that it omits an independent variable that is correlated with both the dependent variable and one or more included independent variables.

1. [Omitted variable bias - example 1](https://www.youtube.com/watch?v=6I1tUM0RB6I&index=34&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)
2. [Omitted variable bias - example 2](https://www.youtube.com/watch?v=_Ka_PAvdDjk&index=35&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)
3. [Omitted variable bias - example 3](https://www.youtube.com/watch?v=CndHm9WDVIE&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU&index=36)
4. [Omitted variable bias - proof part 1](https://www.youtube.com/watch?v=9-lPES4e0n8&index=37&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU)

## Detailed analysis of the OVB

Consider a linear model of the form

$$
y_i = \beta x_i + z_i \delta + u_i
$$

where:

- $$x_i$$ is a $$1 \times p$$ vector of values of $$p$$ independent variables observed at time $$i$$.
- $$\beta$$ is a $$p \times 1$$ column vector of unobservable parameters (the response coefficients) to be estimated.
- $$z_i$$ is a scalar and is the value of another independent variable observed at time $$i$$.
- $$\delta$$ is a scalar and is an unobservable parameter (the response coefficient of $$z_i$$) and has to be estimated.
- $$u_i$$ is the unobservable error term occurring at time $$i$$; it's an unboserved realization of a random variable with $$E[u_i \vert x_i]=0$$ and $$E[u_i \vert z_i]=0$$.
- $$y_i$$ is the observation of the dependent variable at time $$i$$.

We collect the observations of all variables and stack them one below another to obtain the matrix $$X$$ and the vectors $$Y,Z$$ and $$U$$.

If the independent variable $$z$$ **is omitted from the regression**, then the estimated values of the response parameters of the other independent variables will be given by the ordinary least squares (OLS) estimator:

$$
\hat{\beta} = (X^T X)^{-1} X^T Y^T
$$

Substituting for $$Y$$ based on the assumed linear model we get:

$$
{\begin{aligned}{\hat  {\beta }}&=(X'X)^{{-1}}X'(X\beta +Z\delta +U)\\&=(X'X)^{{-1}}X'X\beta +(X'X)^{{-1}}X'Z\delta +(X'X)^{{-1}}X'U\\&=\beta +(X'X)^{{-1}}X'Z\delta +(X'X)^{{-1}}X'U.\end{aligned}}
$$

On taking expectations, the contribution of the final term is zero; this follows from the assumption that $$U$$ is uncorrelated with the regressors $$X$$.
On simplifying the remaining terms:

$$
{\displaystyle {\begin{aligned}E[{\hat {\beta }}|X]&=\beta +(X'X)^{-1}E[X'Z|X]\delta \\&=\beta +{\text{bias}}.\end{aligned}}} 
$$

The second term after the equal sign is the omitted-variable bias in this case, which is non-zero if the omitted variable z is correlated with any of the included variables in the matrix X (that is, if X'Z does not equal a vector of zeroes).
Note that the bias is equal to the weighted portion of $$z_i$$ which is explained by $$x_i$$.

The Gauss–Markov theorem states that regression models which fulfill the classical linear regression model assumptions provide the BLUE estimators.
With respect to ordinary least squares, the relevant assumption of the classical linear regression model **is that the error term is uncorrelated with the regressors**.

The presence of omitted-variable bias violates this particular assumption. 
The violation causes the OLS estimator to be biased and inconsistent. The direction of the bias depends on the estimators as well as the covariance between the regressors and the omitted variables. A positive covariance of the omitted variable with both a regressor and the dependent variable will lead the OLS estimate of the included regressor's coefficient to be greater than the true value of that coefficient. 

# [Reverse causality](https://www.youtube.com/watch?v=yBipwlHXxJc&list=PLwJRxp3blEvZyQBTTOMFRP_TDaSdly3gU&index=39)

It's an other problem occurring from the failed Gauss–Markov of the zero conditional mean of errors. This is called an issue of **endogeneity**, or in other words $$x$$ is an endogenous regressor. For this reason the Gauss–Markov assumption $$E[u_i \vert x_i]=0$$ fails and in general one has $$E[u_i \vert x_i] \neq 0$$. Reverse causality tends to produce **upperly biased** estimate.
How do reverse causality leads to violation of Gauss–Markov assumption of zero conditional mean of errors?

Example: let's say we are interesting in finding out whether the prevalence of a civil war in a country leads to a decrease in the human development index (HDI) in that country. The linear model to describe this problem is the following:


$$
\textrm{HDI} = \alpha + \beta \textrm{CW} + u
$$
If a country has a civil war does this lead to a decreased HDI? So we think $$\beta<0$$. But it is also true that conversely the likely that if a country has a civil war, it also has a lower HDI index. So we write:

$$
\textrm{CW}_i = \delta + \gamma \textrm{HDI} + v_i
$$

Why does this lead to the Gauss–Markov assumption on zero conditional mean of errors failure? We must check that the covariance between $$u_i$$ and $$CW$$ variables. We can write:

$$\textrm{Cov}[u, CW] = \textrm{Cov}[u, \delta + \gamma \textrm{HDI}] + v = \gamma \textrm{Cov}[u,\textrm{HDI}] = \gamma \textrm{Cov}[u, \alpha + \beta \textrm{CW} + u]
$$ (assuming the covariance between the errors $$u$$ and $$v$$ is zero)
This last term contains the covariance of $$u$$ with $$u$$.

"Correlation proves causation," is considered a questionable cause logical fallacy when two events occurring together are taken to have established a cause-and-effect relationship.


# [41 - Measurement error in independent variables]()
Another violation of the Gauss–Markov assumption is $$E[u_i \vert x_i] \neq 0$$. In this case the ordinary least squares estimate of $$\hat{\beta}_{ols}$$ will be biased.

If I don't measure the independent variable $$x_i$$ correctly this leads to a $$x_i + v_i$$ where $$v_i$$ is some form of error. In this case then the expected value of $$E[u_i \vert x_i]$$ becomes in the form of $$E[u_i \vert x_i + v_i]$$ and in general is different than zero.


# [42 - Measurement error in independent variables]()
Suppose a company level of sales is related to advertising by the following relation

$$S_t = \alpha + \beta  A_t + u_t$$

where $$S_t$$ are the sales and $$A_t$$ is the level of advertising. If the level of advertising is measured with some error $$M_t = A_t + v_t$$ then the model becomes:

$$S_t = \alpha + \beta M_t + (u_t-v_t)$$

Then we see that $$\textrm{Cov}[u_t - \beta v_t, M_t ]$$ is not zero, indeed $$\textrm{Cov}[u_t - \beta v_t, M_t ] \approx -\beta  \textrm{Cov}[v_t,A_t + v_t]=-\beta  \textrm{Cov}[v_t, v_t] = -\beta  \sigma^2$$.

# [43 - Functional misspecification]()
It is a normal econometric problem to specify the wrong model and this can lead to violation in the Gauss-Markov assumptions. For example modeling the wage vs age relation with a linear function whereas it is clear that the relation is quadratic.

# [46 - Random sample summary]()
Another Gauss-Markov assumptions is the Random Sampling. Mathematically this means that if I have a collection of random variables $$Y_1, \ldots Y_n$$, if they are independent and come from the same common probability distribution function, that implies that this is a random sample.
Practically this means that one has to same uniformly at random from the population to avoid biases in the samples.

# [48 Serial correlation summary]()
Ways to have serial correlation (in mathematical terms $$\textrm{Cov}[u_i,u_s]\neq 0$$ for $$i \neq s$$)in the model are:

1. Omit important variables
2. Functional misspecification
3. Measurement errors (if I underestimating the variable for example).

This means that the OLS estimates will be no longer unbiased, and not BLUE. Although this means that there may be other estimators which have lower sampling variance and work better than the ordinary least squares.

A sign of serial correlation is when you see long streak of all positive and all negative residuals for example, so locally the mean of the residual (errors) is not zero.

# [52 - Serial correlation biased standard error ]()
It may happen that effects of clustering lead to bias in the estimate.
Consider the model

$$Y_{ig} = \alpha + \beta  CS_{g} +\zeta_{ig}$$

where $$CS$$ is the classroom size, $$g$$ is the group, $$i$ is the individual in the class and the score of the individual is $$Y_{ig}$$. The nature of the error is both due to the size of the group and the skil variability the individual, so one can write $$\zeta_{ig}=v_g + \eta_{i}$$.
We can see that this model has serial correlation since $$\textrm{Cov}(\zeta_{ig},\zeta_{jg}) \neq 0$$ 
Clustering effects on the errors

