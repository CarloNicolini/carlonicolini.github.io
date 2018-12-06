---
layout: post
title: Expected gradients in the spectral entropies method
categories: science
published: false
date: 2018-06-11
---

We need to compute the gradients with respect to the parameters $$\theta$$ of the quantity

$$
\mathbb{E}\left \lbrack S\left(\rho \|  \sigma(\theta) \right) \right | \theta \rbrack
$$

$$
\nabla_{\theta} \mathbb{E}\left \lbrack S\left(\rho \|  \sigma(\theta) \right) \right | \theta \rbrack
=\beta \nabla_{\theta} \tr \lbrack \rho \mathbb{E}[L(\theta)] \rbrack + \nabla_{\theta} \mathbb{E}\left \lbrack \log \tr \left \lbrack e^{-\beta L(\theta)}\right \rbrack \right \rbrack
$$