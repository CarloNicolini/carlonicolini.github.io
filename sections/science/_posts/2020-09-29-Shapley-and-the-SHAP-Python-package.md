---
title: Shapley additive explanations and the SHAP Python package
date: 2020-09-29
layout: post
categories: science
published: false
---

# Why interpretability matters?

Currently the ML community is struggling in making sense of its own output.
They are able to produce highly accurate models, but they find hard times in answering "why"?.
Where does the high accuracy of deep neural networks come from, and what are the variables shaping it?

Giving a human-understandable interpretation to machine learning models is turning out to be a more and more difficult, in times of models with hundreds of thousands of parameters.

The best explanation of a simple model is the model itself; it perfectly represents itself and is easy to
understand. For complex models, such as ensemble methods or deep networks, we cannot use the
original model as its own best explanation because it is not easy to understand.

As a matter of example, take the problem of giving an explanation to a bank customer about why his bank has refused him/her a loan.
There are many factors involved in deciding the amount of money to lend and to whom, some of them clearly addressable, some others instead hidden under the complicacies a black-box model.

After the post-2008 crisis, new layers of regulation have, clients should be able to clearly understand all the reason why their loan was refused, as well as 

The process of training some kind of classifier, be it a binary one, a multiclass or a regression classifier 
