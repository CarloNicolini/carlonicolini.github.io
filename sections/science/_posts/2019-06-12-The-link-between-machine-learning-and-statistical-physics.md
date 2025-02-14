---
layout: post
title: The link between machine learning and statistical physics
categories: science
published: true
use_math: true
date: 2019-06-12
---

Reading the paper by Max Tegmark ["Why does deep and cheap learning work so well"](https://arxiv.org/pdf/1608.08225.pdf) is illuminating.


# The abstract:

The abstract of this paper already gives a very good introduction of the ideas presented. The main problem is tackled is why are neural networks working so well in reducing complexity? The answer is that random patterns in the universe are not really *random* but some kind of structures are always present. It is exactly on this phenomenon that neural networks are based.
For example physics is based on a number of conservation laws, symmetries and locality, which are all the essential ingredients that define, even in the presence of non-deterministic noise, how our universe works.

We show how the success of deep learning could depend not only on mathematics but also on physics: although well-known mathematical theorems guarantee that neural networks can approximate arbitrary functions well, the class of functions of practical interest can frequently be approximated through *cheap learning* with exponentially fewer parameters than generic ones. 
We explore how properties frequently encountered in physics such as symmetry, locality, compositionality, and polynomial log-probability translate into exceptionally simple neural networks.
We further argue that when the statistical process generating the data is of a certain hierarchical form prevalent in physics and machine-learning, a deep neural network can be more efficient than a shallow one.
We formalize these claims using information theory and discuss the relation to the renormalization group. 
We prove various *no-flattening theorems* showing when efficient linear deep networks cannot be accurately approximated by shallow ones without efficiency loss; for example, we show that $n$ variables cannot be multiplied using fewer than 2 neurons in a single hidden layer.

<iframe width="560" height="315" src="https://www.youtube.com/embed/5MdSE-N0bxs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

| Physics                   | ML                                |
|:--------------------------|----------------------------------:|
| Hamiltonian $H$           | Surprisal $-\log p$               |
| Simple $H$                | Cheap learning                    |
| Quadratic $H$             | Gaussian $p$                      |
| Locality                  | Sparsity                          |
| Translation symmetric $H$ | Convolutional netw.               |
| Spin                      | Bit                               |
| Free energy difference    | KL-divergence                     |
| Effective theory          | Nearly lossles data distillation  |
| Irrelevant operator       | Noise                             |
| Relevant operator         | Feature                           |


In order to facilitate a comparison between the formalism used in computer science, mathematical probability and statistical physics, here I try to develop a small table where all the terms are translated in the two perspectives.
And we continue with the link between statistical physics and Bayesian theory, here in a small table (we set $k_B=1$)


| Physical perspective                                                        | Statistical perspective                                                                                |
|:----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------:|
| Potential $\phi(\theta)$                                                    | Negative log-joint $\phi( \theta ) = - \log p(y, \theta \| m)$                                         |
| Boltzmann distribution $q(\theta)=\frac{1}{Z} \exp{-\beta \phi(\theta)}$    | Posterior distribution. $q(\theta)=\frac{1}{Z}\exp{-\log p(y,\theta \|m)}=\frac{1}{Z} p(y,\theta\|m)$  |
| Partition function $Z=\int \exp{-\beta \phi(\theta)}$                       | Model evidence $Z=\int p(y,\theta \| m)$                                                               | 
| Internal energy $U=\int q(\theta) \phi(\theta) d\theta$                     | Expected log-joint $U=\int p(\theta \| y,m) \log p(y,\theta \|m) d\theta$                              |
| Entropy $S=-\int q(\theta) \log q(\theta) d\theta $                         | Shannon Entropy $S_{shannon} = -\int q(\theta) \log q(theta) d\theta$                                  |
