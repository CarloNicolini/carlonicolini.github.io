---
layout: post
title: Vasicek model in Python
description: 'Vasicek model in Python.'
published: false
permalink: "/sections/science/2019/07/05/Vasicek-model.html"
categories:
  - science
  - finance
  - math
---
The Vasicek model is a special Ornstein-Uhlenbeck process that implements mean-reverting behaviour
Its formulation in terms of SDE is

$$
dr_t = k \left( \theta - r_t \right) dt + \sigma dW_t \quad r(0)=r_0
$$

