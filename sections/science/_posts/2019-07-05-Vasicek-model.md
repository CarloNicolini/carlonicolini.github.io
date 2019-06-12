---
layout: post
title: Vasicek model in Python
published: false
---

The Vasicek model is a special Ornstein-Uhlenbeck process that implements mean-reverting behaviour
Its formulation in terms of SDE is

\begin{equation}
dr_t = k \left( \theta - r_t \right) dt + \sigma dW_t \quad r(0)=r_0
\end{equation}

We use the integrating factor
