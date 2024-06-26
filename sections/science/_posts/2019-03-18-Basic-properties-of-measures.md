---
layout: post
title: Short introduction to measure theory
categories: science
date: 2019-03-18
published: false
use_math: true
---

In these notes, we'll take a look at the **bare essentials** of modern probability theory.
We'll describe the basic ideas, but we will skip Lebesgue integration, at the moment.
To do this, we need to introduce some **measure theory** first, to see how things emerge naturally and beatifully.

### [Introduction to Banach-Tarski paradox](https://www.youtube.com/watch?v=Tk4ubu7BlSk)

Any proper introduction to probability theory has to deal with **measure theory**.

To motivate why we need measure theory, suppose we have a solid ball, filled in 3D space.
A couple of clever guys in 1980, showed that you can cut this ball into small pieces, and by performing only rigid transformations, we can rearrange the pieces of the ball, into two solid balls of both the same surface and volume of the original ball.
This is called the Banach-Tarski paradox.

Stefan Banach and Albert Tarski proved this strange paradox, only using the Zermelo-Frank axioms of mathematics, which are some of the basic fundamentas in math.
Apparently, something must be wrong.
There are two ways to handle this apparent paradox:

1. Reject the axiom of choice. It is very hard to reject, as it is a very simple axiom.
2. Accept the possibility of non-measurable sets. This is a simpler to accept thing.

Apparently, the path to resolve the paradox is to assume that ball is not measurable, hence it makes no sense to say that the measure of the set of tiny objects that make the ball, is not measurable.
The set cannot be assigned a measure in any meaningful way.

Hence, there is a concept underlying what is a measurable set that we need to better specify.
So, in the next lines we need to define what is a *measurable set* and what is a *measure*.

### Measure theory

**Definition 1**: The power-set of the set $\Omega$ is the set of all subsets of $\Omega$, and is indicated as $2^\Omega$.

**Definition 2**: Given a set $\Omega$, a $\sigma$-algebra on $\Omega$ is a collection $A \subset 2^{\Omega}$ such that, $A$ is non empty, and  the following conditions hold:
1. $A$ is closed under complements: this means that if $E\in A$ then $E^c  \in A$.
2. $A$ is closed under countable unions: this means that  the  union of all subsets in $E\in A$, still is a set in $A$.

*Remark 1* The set $\Omega$ itself is always a member of every $\sigma$-algebra on $\Omega$. This happens since $R \in A$ then $E^c \in A$, hence $E \bigcup E^c \in A$ (by property 1.) and this union is simpliy $\Omega$ itself, by property 2.

*Remark 2* The empty set is always in the $\sigma$-algebra $A$.


*Remark 3* Any $\sigma$-algebra $A$ is closed under countable intersections. Remember that conditions 2 tells us that $\Omega$ is closed under countable unions. By this property we also have closeness under countable intersections.
We can say this because any set is equal to the complement of its complement, and by De Morgan's law, the interesection of the complements, equals the complement of the unions:

$$
\bigcap (E_i^c)^c = \bigcup (E_i^c)^c \in A
$$
and this proves that $A$ is closed under countable interesections.


### [Measure theory: basic properties of measures](https://www.youtube.com/watch?v=ILXe_NsvQ6Q&index=5&list=PL17567A1A3F5DB5E4)

**Definition 3** Given a set $C \in 2^\Omega$, the $\sigma$-algebra generated by $C$, indicated by $\sigma(C)$, is the smalles $\sigma$-algebera containing $C$.
That is, $\sigma(C) = \limits_{A \supset C}\bigcap A$.

We can prove that $\sigma(C)$ exists because:
1. $2^\Omega$ is a $\sigma$ algebra
2. Any intersection of $\sigma$ algebras is a $\sigma$-algebra. 

### Examples of $\sigma$-algebras

These are $\sigma$-algebras:
1. The trivial $\sigma$-algebra is the empty set $A=\{ \emptyset, \Omega \}$
2. $A=\{ \emptyset, E,E^c,\Omega \}$
3. If $\Omega = \mathbb{R}$, the Borel $\sigma$ algebra $\mathbb{B}(\tau)$ is the $\sigma$ algebra generated by the set of all the open sets in $\mathbb{R}$, denoted by $\tau$.

**Definition 4** A measure $\mu$ on $\Omega$ with $\sigma$-algebra $A$ is a function $\mu$ from $A$ to numbers from $0$ to $\infty$ such that two conditions holds:
1. The measure evaluated on the empty set must be zero $\mu(\emptyset)=0$
2. The measure evaluated on the union of the sets, must be the sum of the measure evaluated on each set

$$
\mu \left( \bigcup \limits_{i=1}^{\infty} E_i \right) = \sum_{i=1}^{\infty} \mu(E_i)
$$

**Definition 5** A probability measure, is a measure $P$ with the condition that $P(\Omega)=1$. This is called the normalization condition over the universe set.

These last two definitions, are also called the *Kolmogorov* axioms, the mathematician that posed on theoretical roots probability.
Kolmogorov put probability theory on a firm mathematical grounds.

**Example 2** Let us take a finite set $\Omega$ to be the set of numbers from 1 to $n$: $\Omega= \{1,\ldots, n \}$.
Then we define $P(k)=\frac{1}{n}$ $\forall k \in \Omega$. This defines the measure of the set $\Omega$.
This is called the *uniform* distribution on the set $\Omega$. Defining on $\Omega$ makes possible to induce a measure also on the powerset $A=2^\Omega$.

For example by countable additivity, the set $P(\{1,2,4\})$ can be written as the sum $P(\{1 \} \cup \{2\} \cup \{4\})=P(1) + P(2) + P(4)$, and this defines the probability of our set.

**Example 3** Let us consider countably infinite sets. We take the natural numbers $\Omega=\mathbb{N}$ and the $\sigma$ algebra to be the powerset $A=2^\Omega$.
Consider the probability $P(k)$ that it takes $k$ coin-flips to get heads. This can be computed for a fair coin as:

$$
P(k)= \alpha(1-\alpha)^{k-1} = \frac{1}{2}(1-\frac{1}{2})^{k-1}
$$

This is called the geometric distribution, and every set in the $\sigma$-algebra $A$ uniquely defines a probability measure on $A$.

**Example 4** Let us consider an uncountable set $\Omega = [0, \infty )$. The Borel $\sigma$-algebra $\mathbb{B}([0,\infty))$ is the $\sigma$ algebra generated by all open intervals in $[0,\infty)$.
We define a probability measure $P([0,x)) = 1-e^{-x}$ $\forall x >0$.
In fact sets of the form $[0,x)$ and definining a probability measure uniquely induces a probability measure on the whole $\sigma$ algebra. This distribution is called the *exponential* distribution.

For this probability measure, the probability of any single element set is zero $P(\{x\})=0$, because this is a continuous distribution.

**Example 5 Lebesgue measure** On the real line, indiscutably the most important measure.
We take $\Omega = \mathbb{R}$ and $A = \mathbb{B}(\mathbb{R})$.
The measure on the open interval $(a,b)$ is defined as $\mu((a,b)) = b-a$ for any $a,b \in \mathbb{R}$ with $a \leq b$.
This measure is called the *length*. Again this uniquely defines a measure on all the sets.

This is cleary not a probability measure, and in some sense it replaces the $dx$ of calculus, but this is to give a hint of what this measure is useful for.

**Theorem 1** **Basic properties of measures
Let $(\Omega,A,\mu)$ be a measure space, then these properties hold:
1. *Monotonicity*: If $E,F \in A$ and $E \in F$, then $\mu(E) \leq \mu(F)$. This is natural property.
2. *Subadditivity*: If we have some sequence  $E_1, E_2,\ldots \in A$, then $\mu\left( \bigcup \limits_{i=1}^\infty E_i \right) \leq \sum_{i=1}^{\infty} \mu(E_i$)$. This happens because you could double count some sets.
3. *Continuity from below* : If $E_1,E_2 \in A$ and $E_1 \subset E_2 ,\ldots \subset $, then the measure of the union of all the sets $E_i$ tends to the measure of each of them.
$\mu \left( \bigcup \limits_{i=1}^\infty  E_i \right)  = \lim_{i\to \infty} \mu(E_i)$
4. *Continuity from above*: If $E_1,E_2 \in A$ and $E_1 \supset E_2 ,\ldots \supset E_n $, and further, the measure of $E_1$ is finite, then we have $\mu \left( \bigcap \limits_{i=1}^\infty  E_i \right)  = \lim_{i\to \infty} \mu(E_i)$.

In a probability space these two last conditions always hold.
We can see these properties in the case of a probability measure.
If we take the set $E_i=[i,\infty)$ their measure is infinite, but if we take the measure of their interesection, this is clearly $0$, and this comes from these two last properties.

### [More properties of probability measures](https://www.youtube.com/watch?v=t4cwYCVyQLM&list=PL17567A1A3F5DB5E4&index=7)

## Facts 
Let $(\Omega, A,P)$ be a probability measure space with $E,F,E_i \in A$. Then the following holds:

1. $P(E \cup F) = P(E) * P(F)$ if $E\cap F =\emptyset$
2. $P(E \cup F) = P(E) + P(F) - P(E\cap F)$
3. $P(E) = 1-P(F)$
4. *Inclusion exclusion formula*

$$P\left (\bigcup_{i=1}^n E_i \right) = \sum_i P(E_i) - \sum_{i<j} P(E_i \cap E_j) + \sum_{i<j<k} P(E_i \cap E_j \cap E_k) - \ldots ... + (-1)^{n+1} P(E_1 \cap E_2 \cap \ldots \cap E_n)$$

5. *Subadditivity formula* $P(\bigcup_{i=1}^n E_i) \leq \sum_{i=1}^n P(E_i)$ and $P(\bigcup_{i=1}^\infty E_i) \leq \sum_{i=1}^\infty P(E_i)$

[https://www.youtube.com/watch?v=wV3JuVI2tLM&list=PL17567A1A3F5DB5E4&index=8](https://www.youtube.com/watch?v=wV3JuVI2tLM&list=PL17567A1A3F5DB5E4&index=8)
We specialize on the Borel sigma algebras on th real.
Measures on the space take a very special form.

**Definition 6** A Borel measure on $\mathbb{R}$ is a measure on $\mathbb{R}$ with a Borel $\sigma$-algebra ($\mathbb{R},\mathbb{B}(\mathbb{R})$.

**Definition 7** A cumulative distribution function (c.d.f) is a function on the reals to the reals $F : \mathbb{R} \to \mathbb{R}$ such that 
1. it is non-decreasing ($x \leq y => F(x) \leq F(y) $) 
2. it is *right-continuos* $\lim_{x\to a^-} F(x) = F(a)$
3. $\lim_{x\to \infty} F(x)=1$
4. $\lim_{x\to 0} F(x)=0$

In other words, it can jumps but needs to include points from the right.


**Theorem 2** If $F$ is a cdf, then there is a unique Borel probability measure on $\mathbb{R}$ such that 
1. the measure of the sets is of the form $P(-\infty,x])=F(x)$
2. if $P$ is a Borel probability measure on $\mathbb{R}$ then there is a unique cdf $F$ such that $F(x)=P((-\infty,x])$ , $\forall x \in \mathbb{R}$.

That is, there is an equivalence between cdfs and Borel probability measures.


### [References for Probability and Measure theory](https://www.youtube.com/watch?v=aJjB16jJQEQ&list=PL17567A1A3F5DB5E4&index=9)

Here are some reference books:

Real analysis (undergrad)
1. Rudin's "Principle of math analysis"
Probability:
2. Jacob and Pratter "Probability essentials"
3. Durrent "Probability: theory to examples"
4. Grimmet and Stirzcker: "Probability and random processes"

5. Folland's "Real analysis"
6. Rudin' "Real and complex analysis"

### [Conditional probability and independence](https://www.youtube.com/watch?v=5BWk5qe5EJ8)
In just every application in probability, these two concepts are critical.

*Notation*: we often suppress the mention to the underlying set $\Omega$ and its $\sigma$-algebra $A$. We just specificy $P(E)$, i.e. the probability of the event $E$.
With the word *event* we mean a measurable set in a $\sigma$-algebra.
The set $\Omega$ is also called the *sample space*.

**Definition 10** If the probability $P(B)>0$ then $P(A \vert B) = \frac{P(A\cap B)}{P(B)}$. The probability $P(A\vert B)$ is called the conditional probability of $A$ given $B$.
It can be seen as the fraction of $B$ that is contained in $A$, or the probability that $A$ occurs, given that $B$ occurs.

Let us study a concrete example. We have a pair of dice. Let define $A$ the event that we get two ones on both dices. Let $B$ define the event that both dice have the same face.
The set $\Omega$ is the set with 36 elements,  and label the event $A$ as 1. The probability is $1/36$.
The probability of $B$ is instead $1/36 + 1/36 + 1/36+ 1/36 + 1/36 + 1/36=1/6$, by additivity.
The conditional probability $P(A\vert B)$ is just $B$, because $B$ contains $A$. If we know that we get two dice with the same number, then the probability to have two ones is clearly $1/6$.

**Definition 11** (*independence*) The events $A$ and $B$ are independent, if $P(A \cap B)=P(A)P(B)$.
Intuitively, we can think about independence as if two events are unrelated.

