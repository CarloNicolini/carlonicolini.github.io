---
layout: post
title: Exercises for quantitative interviews
date: 2019-02-04
categories: quant
published: false
---

Exercise 1
----------

One morning in Springfield, it started snowing at heavy but constant rate. Homer Simpson had just started his own snowplow business. His snowplot started out at 08:00 AM and at 09:00 AM it had gone 2 miles. By 10:00 AM it had gone 3 miles.
Assuming that the snowplow removes a constant volume of snow per hour, determine the time at which it started snowing.

#### Solution


Exercise 2
----------
$a$ and $b$ are randomly chosen real numbers in the interval $[0,1]$,
that is both $a$ and $b$ are standard uniform random variables.
Find the probability that the quadratic equation $x^2+ax+b= 0$ has real solutions.

### Solution
The equation $x^2 + ax + b=0$ has real solutions if its determinant is positive or zero.
The determinant of a second order equation $ax^2 + bx + c=0$ is found as $\Delta = b^2 - 4ac$.
So in our case we have $\Delta = a^2 - 4b$.
We know that both $a$ and $b$ are $\sim U[0,1]$.
Here then we must compute the probability that $a^2-4b \geq 0$, i.e. $P(a^2-4b \geq 0)$, where $a$ and $b$ are uniformly distributed.

The cdf of $a$ is $x$ over the support $[0,1]$.
The cdf of $b$ is $x$ over the support $[0,1]$. 

The cdf of $a^2$ is obtained from the cdf of $a$.
On the support $[0,1]$ the function $g(x)=x^2$ is strictly increasing and has inverse $g^{-1}(y)=\sqrt{y}$.
The derivative of the inverse $\frac{dg^{-1}(y)}{dy}=\frac{1}{2\sqrt{y}}$.
Hence the pdf of $a^2$ is $f_X(g^{-1}(y))\frac{dg^{-1}(y)}{dy}$.


#### Exercise 3
Solve the equation:

\begin{equation}
\sqrt{x+\sqrt{x+{\sqrt{x+\sqrt{x+\sqrt{x...}}}}}} =x
\end{equation}

### Solution
Take the squares we get:
\begin{equation}
{x+\sqrt{x+{\sqrt{x+\sqrt{x+\sqrt{x...}}}}}} =x^2
\end{equation}
and the infinite square appears in the left hand side. However we know that it evaluates to $x$, hence we get $x+x=x^2$, and the solutions are $x_1=0$ and $x_2=2$.

#### Exercise 4
Solve the infinite tetration
\begin{equation}
x^{x^{x^{x^{x^{...}}}}} = 2
\end{equation}

#### Solution
The solution is simple to obtain.
Since the tetration is infinite, we have that the left exponent $(\cdot)^{x^{x^{x^{...}}}}$ is equal to 2. Hence $x^2=2$, and the solution is $x=\sqrt{2}$.
