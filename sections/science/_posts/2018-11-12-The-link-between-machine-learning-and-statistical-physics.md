---
layout: post
title: The link between machine learning and statistical physics
categories: science
published: false
use_math: true
date: 2018-11-12
---

Reading the paper by Max Tegmark ["Why does deep and cheap learning work so well"](https://arxiv.org/pdf/1608.08225.pdf) is illuminating.


The abstract:

We show how the success of deep learning could depend not only on mathematics but also on physics: although well-known mathematical theorems guarantee that neural networks can approxi-mate arbitrary functions well, the class of functions of practical interest can frequently be approximated through *cheap learning* with exponentially fewer parameters than generic ones. 
We explore how properties frequently encountered in physics such as symmetry, locality, compositionality, and polynomial log-probability translate into exceptionally simple neural networks.
We further argue that when the statistical process generating the data is of a certain hierarchical form prevalent in physics and machine-learning, a deep neural network can be more efficient than a shallow one.
We formalize these claims using information theory and discuss the relation to the renormalizationgroup. 
We prove various *no-flattening theorems* showing when efficient linear deep networks cannot be accurately approximated by shallow ones without efficiency loss; for example, we show that $n$ variables cannot be multiplied using fewer than 2 neurons in a single hidden layer.

[![deep networks encode hierarchical data generation](https://i.ytimg.com/an_webp/5MdSE-N0bxs/mqdefault_6s.webp?du=3000&sqp=CN-gpd8F&rs=AOn4CLBQHDHpJnmjp8OTGEyGL3QWe7CjYQ)](https://www.youtube.com/watch?v=5MdSE-N0bxs)


| Physics                   | ML                                |
|---------------------------|:---------------------------------:|
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
