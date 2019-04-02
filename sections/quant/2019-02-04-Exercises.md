---
layout: post
title: Exercises for quantitative interviews
date: 2019-02-04
published: false
categories: quant
---

### Exercise 1
One morning in Springfield, it started snowing at heavy but constant rate. Homer Simpson had just started his own snowplow business. His snowplot started out at 08:00 AM and at 09:00 AM it had gone 2 miles. By 10:00 AM it had gone 3 miles.
Assuming that the snowplow removes a constant volume of snow per hour, determine the time at which it started snowing.

### Solution
The amount of snow in millimiters is the variable $y(t)$. Since the rate of snow is constant, then the growth of snow is linear, hence $y(t)=c t$ where $c$ denotes the constant rate, and time is measured in hours.
Homer Simpsons starts at $t=0$, and at $t=1$ he traveled $x(t=1)=2$ miles.
However at $t=2$ he only traveled $3$ miles, because its speed depends on the amount of snow.

The amount of snow on the ground in front of the snowplow is $h(t) = c t - c_s t$