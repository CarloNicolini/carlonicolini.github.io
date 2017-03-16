---
layout: post
title: Information theory fundamentals
categories: science
published: false
date: 2017-01-19
---

<blockquote>
    "Studying the most important concepts in information theory with examples and exercises done."
</blockquote>

Some concepts are fundamental in information theory and here I write down a short summary with the most important definitions and results. These are my notes while studying the book from Cover and Thomas "Elements of Information theory". Together with notes about information theory I'll integrate some concepts of probability, for those who are not too familiar (me included) with them.

# Random variable

Usually called $$X$$ it's a function from the set of possible outcomes of a set $$\mathcal{X}$$. Usually a random variable is denoted in uppercase. As an example a discrete random variable can be interpreted as the outcome of a dice roll. In that case the random variable $$X$$ is defined over an alphabet of $$\mathcal{X}=\{1,2,3,4,5,6 \}$$ possible events. In the case of a coin flip, the random variable is valued head or tail. A coin-toss (or Bernoulli trial) is the experiment where a random variable has only two possible outcomes.  Examples of Bernoulli trials include:
  * Flipping a coin. In this context, obverse ("heads") conventionally denotes success and reverse ("tails") denotes failure. A fair coin has the probability of success 0.5 by definition. In this case there are exactly two outcomes.
  * Rolling a die, where a six is "success" and everything else a "failure". In this case there are six outcomes, and the event is a six; the complementary event "not a six" corresponds to the other five outcomes.
  * In conducting a political opinion poll, choosing a voter at random to ascertain whether that voter will vote "yes" in an upcoming referendum.


# Entropy (Shannon)

If $$X$$ is a random variable with a finite alphabet $$\mathcal{X}$$ and $$XX$$ is distributed according to a probability distribution $$p(x)$$ then the entropy of $$X$$ is defined as:

$$H(X) = - \sum_{x \in \mathcal{X}} p(x)\log p(x)$$

When measuring the logarithms in base 2, entropy is measured in bits. Nats or Hartleys are used in case logarithm have natural or 10 base respectively.
The entropy is a measure of the average uncertainty in the random variable $$X$$. It is the number of bits in average that are required to describe the random variable.

- One can see the entropy as the expected value of the log-probability of $$X$$, indeed a connection with the thermodynamical entropy is evident if one rewrites $$H(X)$$ as:

  $$ H(X) = - E_p \log( p(x)) = E_p \log \frac{1}{p(x)}.$$

- Entropy is always greater or equal than zero $$H(X) \geq 0$$.
- Entropy is a convex function. This means that [Jensen Inequality](#JensenInequality) is valid.
- Entropy of an isolated system never decreases (second law of thermodynamics). This rules out possibilities for perpetual motion machines.
- Such definition of entropy also arises as the answer to questions like: "what is the average length of the shortest description of the random variable?"
- The binary entropy is the entropy of the simplest random variable taking values 0 or 1 with probability $$p$$:

  $$H(p) := -p \log(p) - (1-p) \log(1-p)$$

  ![Binary entropy](http://www.pmean.com/12/images/SpermM1.gif)

__________
## Examples

**1. Entropy of a uniform distribution**

A random variable has an uniform distribution over 32 outcomes. Thus a 5-bit string would suffice to describe the outcome of the random variable. Indeed its entropy is computed as: 

$$H(X)= -\sum_{i=1}^{32} p(i)\log(p(i))= -\sum_{i=1}^{32} 1/32\log(1/32)=\log_2(32) = 5$$ bits.

**2. Entropy of coin flip experiment (geometric distribution)**

Let $$XX$$ be the random variable encoding the number of required coin tosses before head occurs. Such random variable is distributed according to the geometric distribution. Indeed the geometric distribution is the probability distribution of the number of Bernoulli trials needed to get one success. 
The geometric distribution is an appropriate model if the following assumptions are true.
The phenomenon being modeled is a sequence of independent trials.
There are only two possible outcomes for each trial, often designated success or failure. The probability of success, p, is the same for every trial.

The geometric distribution of a fair coin toss is encoded by the success probability $$p=1/2$$, therefore according to the geometric distribution the p.d.f of the random variable $$x$$ is 

$$P(X=n) = p(1-p)^{n-1}$$

Applying the definition of entropy and remembering that in this case the alphabet $$\mathcal{X}$$ has infinite elements (number of coin tosses), we obtain:

$$\begin{align}
H(X) &= - \sum_{n=1}^{\infty} p(1-p)^{n-1} \log\left(p(1-p)^{n-1}\right) = - \left[ \sum_{n=0}^{\infty} p(1-p)^n \log\left(p(1-p)^n\right)\right] \\
& =-\frac{p \log p}{1-p} - \frac{p (1-p) \log (1-p)}{p^2} = \frac{(-p \log p - (1-p)\log(1-p))}{p} \\ &= \frac{H(p)}{p}= 2 \textrm{ bits}.
\end{align}
$$

where we have used the following identities about the geometric series:

$$\sum_{n=0}^{\infty} r^n = \frac{1}{1-r} \qquad \sum_{n=0}^{\infty}n r^n = \frac{r}{(1-r)^2}$$

**3. Entropy of functions**


Let $$X$$ be a random variable taking on a finite number of values. What is the general inequality relationship of $$H(X)$$ and $$H(Y)$$ if:

a. $$Y=2^X$$
b. $$Y=\cos(X)$$?

This problem can be analyzed understanding that a one-to-one map of a random variable should not change its information content while instead any processing on $$X$$ should decrease its entropy. Therefore the data processing inequality tells us that the information content of a signal cannot be increased via a local operation, in this case a mapping. In the case of the mapping $$Y=2^X$$ the mapping is one-to-one therefore we can prove that $$H(X)=H(Y)$$. Conversely, the second mapping $$Y=\cos(X)$$ is not one-to-one (at least not in the entire domain of $$X$$, therefore information)

A possible solution to the problem is to consider $$y=g(x)$$, then $$p(y) = \sum_{x: y=g(x)} p(x)$$.

__________

# Joint entropy
The joint entropy of a pair of discrete random variables $$X$$ and $$Y$$ with a joint probability distribution $$p(x,y)$$ is defined as:

$$
H(X,Y) = - \sum_{x \in \mathcal{X}}\sum_{y \in \mathcal{Y}} p(x,y) \log(p(x,y))
$$

and can be expressed as $$H(X,Y) = -E \log(p(X,Y))$$.

## Conditional entropy

If $$(X,Y) \sim p(x,y)$$ the conditional entropy, also called equivocation, $$ H(Y\vert X) $$ is defined as:

$$H(Y|X) = \sum_{x \in \mathcal{X}} p(x) H(Y| X=x)= - E \log p(Y|X)$$

For the conditional entropy the chain rule holds that says:

$$
H(X,Y)=H(X)+H(Y|X)
$$

## Venn Diagram for Information
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Entropy-mutual-information-relative-entropy-relation-diagram.svg/744px-Entropy-mutual-information-relative-entropy-relation-diagram.svg.png" >

##  Jensen Inequality <a id="JensenInequality"></a>

## Relative entropy


## Fisher information
The Fisher information matrix is the Hessian of the relative entropy:

Let $$\theta \in \mathbb{R}^k$$ be the parameter indexing a set $$\mathcal{M}$$ of statistical models with densities $$p_\theta$$. Then the Fisher information matrix is 

$$
I_{ij}(\theta) = \mathbf{E}_{v_\theta} \left[ \left( \frac{\partial \log p_\theta}{d \theta_i } \right) \left( \frac{\partial \log p_\theta}{d \theta_j} \right) \right]
$$

As a corollary:

$$ I_{ij}(\theta) = \frac{\partial^2 }{\partial \theta_i \partial \theta_j} D_{KL}(\mu_{\theta0} \| \mu_\theta)$$

Proof: it is a classical result that $$ I_{ij}(\theta) = \mathbf{E}_{v_\theta} \left[ \left( \frac{\partial \log p_\theta}{d \theta_i } \right) \left( \frac{\partial \log p_\theta}{d \theta_j} \right) \right] $$. The present results follows from this and the fact that the entropy of $$\mu_{\theta0}$$ is independent of $$\theta$$.

Interestingly the mutual information between two random variables can also be seen as the divergence of the product of their marginal distributions from their actual joint distribution:

$$I[X;Y] = D_{KL}(\mathcal{L}(X,Y) \| \mathcal{L}(X) \times \mathcal{L}(Y))$$