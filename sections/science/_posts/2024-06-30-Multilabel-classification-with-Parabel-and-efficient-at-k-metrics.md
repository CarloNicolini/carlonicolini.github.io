---
layout: post
title: Multilabel classification with Parabel and efficient at-k metrics
description: "Parabel multilabel classification, scikit-learn API, Precision@k / Recall@k."
date: 2024-06-30
published: true
categories:
  - science
  - statistical-learning
---

## The annoying gap in extreme multilabel classification

For a long time, something about extreme multilabel classification kept bothering me.

Training the model was not really the hard part. There are already very good algorithmic ideas for that, and Parabel is one of the cleanest: build a tree over labels, reduce a gigantic flat prediction problem into a sequence of smaller routing decisions, and keep inference fast enough that the whole setup remains usable.

The irritating part came one step later.

Once the model was trained, I almost always ended up writing the same glue code again and again:

- one layer to make the classifier feel like a normal `scikit-learn` estimator,
- one layer to deal with sparse multilabel matrices without wasting memory,
- and another layer to compute the metrics that actually matter in extreme classification, such as Precision@k or Recall@k.

That repetition is what pushed me to split the problem into two small libraries with very explicit jobs:

- [`scikit-omikuji`](https://github.com/carlonicolini/scikit-omikuji) for training Parabel-style extreme multilabel models behind a familiar estimator API;
- [`skxml`](https://github.com/carlonicolini/scikit-xml) for evaluating top-k predictions efficiently, including scorer objects that plug directly into `scikit-learn`.

This post is really about why that split turned out to be the right abstraction.

## Why ordinary multilabel tooling starts to feel wrong

In ordinary multilabel classification, it is still common to think in terms of full binary outputs:

$$
\hat{Y} \in \{0,1\}^{n \times L},
$$

where $L$ is the number of labels.

But in extreme multilabel settings, $L$ is not ten, or twenty, or even a few hundred.
It can be tens of thousands or hundreds of thousands.

At that point, the actual user-facing question changes.
I usually do not care whether the model got the entire binary vector exactly right.
I care whether the most relevant few labels rose to the top.

That is why metrics such as Precision@k, Recall@k, MAP@k, and NDCG@k are interesting.

If the system recommends five labels and four of them are good, that is often a success even if the complete multilabel indicator vector is still far from exact.

So there are really two separate engineering problems:

1. train a model that can search a huge label space quickly;
2. evaluate its ranked predictions without falling back to slow, awkward post-processing.

`scikit-omikuji` solves the first part.
`skxml` solves the second.

## Why I wanted Parabel behind a scikit-learn interface

Parabel is attractive for a very practical reason: it respects scale.
Rather than treating every label independently, it organizes the label space into a hierarchy and uses tree traversal to prune the search.

That makes the problem feel much less like "predict a gigantic sparse bit vector" and much more like "route efficiently through a label index".

The Rust library `omikuji` already provides that speed-oriented core.
What I wanted was not to reinvent the algorithm, but to make it feel native inside the Python ecosystem I already use for everything else.

So the central object in `scikit-omikuji` is deliberately simple:

{% highlight python %}
from skomikuji import OmikujiClassifier

classifier = OmikujiClassifier(
    n_trees=3,
    max_depth=20,
    beam_size=10,
    linear_c=1.0,
    top_k=5,
)
{% endhighlight %}

That may look trivial, but it is exactly the point.
I wanted Parabel training to feel like instantiating any other estimator, not like entering a special-purpose side universe with custom file formats and one-off scripts.

Under the hood, the wrapper exposes the hyperparameters that matter most for the tree ensemble and the linear node classifiers:

- the number of trees,
- the maximum depth,
- the beam size used during traversal,
- the branching and clustering controls,
- and the loss used by the internal linear models.

The estimator API is conventional on purpose:

{% highlight python %}
classifier.fit(X_train, y_train)
y_score = classifier.predict_proba(X_test)
y_pred = classifier.predict(X_test, proba_threshold=0.5)
{% endhighlight %}

That means the model can participate in the rest of a Python workflow without ceremony.

## The small detail that matters: sparse arrays and dtypes

One of the easiest ways to make extreme multilabel tooling unpleasant is to pretend dense arrays are fine.
They are not.

The whole point of the problem is that both the feature matrix and the label matrix are usually very sparse.
And once a Python wrapper talks to a lower-level implementation, data types suddenly matter much more than people expect.

In `scikit-omikuji`, I chose to make those expectations explicit:

- features should be sparse and `float32`,
- labels should be sparse and `uint32`.

This keeps the memory layout predictable and lets the Python layer pass data into the Rust backend without unnecessary conversions.

The minimal workflow therefore looks like this:

{% highlight python %}
import numpy as np
from sklearn.datasets import make_multilabel_classification
from skomikuji import OmikujiClassifier

X_train, y_train = make_multilabel_classification(
    n_samples=1000,
    n_features=100,
    n_labels=10,
    n_classes=50,
    sparse=True,
    allow_unlabeled=False,
    random_state=42,
)

X_test, y_test = make_multilabel_classification(
    n_samples=200,
    n_features=100,
    n_labels=10,
    n_classes=50,
    sparse=True,
    allow_unlabeled=False,
    random_state=43,
)

X_train = X_train.astype(np.float32)
y_train = y_train.astype(np.uint32)
X_test = X_test.astype(np.float32)
y_test = y_test.astype(np.uint32)

model = OmikujiClassifier(
    n_trees=3,
    max_depth=20,
    linear_c=1.0,
    top_k=10,
)
model.fit(X_train, y_train)
{% endhighlight %}

I like this example because it shows the contract very clearly.
The user does not have to care how the tree is represented internally, but they do need to hand the estimator a sparse representation that matches the backend.

That is a good tradeoff.

## Why prediction should stay ranked

Once a Parabel-like model has been fitted, the most natural output is a ranked shortlist.

This is why `predict_proba` is the central method in the workflow.
In the wrapper, it returns a sparse score matrix with nonzero values only where the model actually surfaced candidate labels.

Conceptually, that is exactly what I want:

- do not pretend every label was equally considered,
- do not spend memory on labels that never entered the beam,
- and keep the result close to the model's own retrieval logic.

Only later, if needed, one can threshold those scores into a binary prediction matrix.
But that thresholded output is already a lossy collapse of the richer ranked result.

In extreme multilabel classification, the ranking usually comes first and the binary cut comes second.

## Why at-k metrics deserve their own library

This is where the second half of the story begins.

Suppose I have a score matrix from `scikit-omikuji`.
What is the right next question?
Not:

> what is the global subset accuracy?

but rather:

> among the top few labels the model surfaced, how many were useful?

That is the logic behind Precision@k and Recall@k.

If $T_i$ is the true label set for sample $i$ and $\hat{T}_i^{(k)}$ is the set of the top-$k$ predicted labels, then:

$$
\mathrm{Precision@}k
=
\frac{1}{n}\sum_{i=1}^n
\frac{|\hat{T}_i^{(k)} \cap T_i|}{k},
$$

and

$$
\mathrm{Recall@}k
=
\frac{1}{n}\sum_{i=1}^n
\frac{|\hat{T}_i^{(k)} \cap T_i|}{|T_i|}.
$$

These metrics are simple, but the implementation details are not always simple when inputs can be dense, sparse, or already partially ranked.

That is why I extracted them into `skxml`.

The public API is intentionally flat:

{% highlight python %}
from skxml import precision_at_k, recall_at_k, map_at_k, ndcg_at_k

p_at_5 = precision_at_k(y_true, y_score, k=5)
r_at_5 = recall_at_k(y_true, y_score, k=5)
map_at_5 = map_at_k(y_true, y_score, k=5)
ndcg_at_5 = ndcg_at_k(y_true, y_score, k=5)
{% endhighlight %}

That is the entire idea.
The model should focus on producing ranked candidates.
The metric layer should focus on evaluating those rankings correctly and quickly.

## The part I particularly wanted: scikit-learn scorers

One of the most annoying frictions in machine learning code is when a metric works in a notebook cell but cannot participate cleanly in model selection.

I wanted these ranking metrics to be usable not only as standalone functions, but also as first-class scorers inside `cross_validate`, `GridSearchCV`, or any other familiar `scikit-learn` evaluation loop.

That is why `skxml` exports scorer factories such as:

{% highlight python %}
from skxml import precision_at_k_scorer
from sklearn.model_selection import cross_validate

scores = cross_validate(
    model,
    X_train,
    y_train,
    scoring={"precision@5": precision_at_k_scorer(k=5)},
)
{% endhighlight %}

This is a small feature, but it changes how the library feels.

Instead of evaluating extreme multilabel models through custom after-the-fact scripts, I can keep the whole experiment inside the normal `scikit-learn` loop.
That makes hyperparameter tuning and benchmarking much less fragile.

## Using the two libraries together

Once both layers exist, the workflow becomes much cleaner.

Train with `scikit-omikuji`:

{% highlight python %}
from skomikuji import OmikujiClassifier

model = OmikujiClassifier(
    n_trees=5,
    max_depth=30,
    beam_size=20,
    cluster_k=4,
    loss_type="log",
    n_jobs=-1,
)
model.fit(X_train, y_train)

y_score = model.predict_proba(X_test)
y_pred = model.predict(X_test, proba_threshold=0.3)
{% endhighlight %}

Then evaluate with `skxml`:

{% highlight python %}
from skxml import compute_metrics

metrics = compute_metrics(
    y_true=y_test,
    y_pred=y_pred,
    y_score=y_score,
    k=5,
    propensity_coeff=(0.5, 0.4),
)

for name, value in metrics.items():
    print(f"{name}: {value:.4f}")
{% endhighlight %}

This separation ended up matching the problem much better than a single monolithic library would have.

`scikit-omikuji` is about search in a huge label space.
`skxml` is about measuring whether that search returned the right things near the top.

## Why propensity-scored metrics matter

Extreme multilabel datasets are often long-tailed.
Some labels appear everywhere, while others are rare but still important.

If I only compute plain Precision@k, I may end up flattering a model that is merely good at predicting popular labels.
That is useful information, but it is not the whole story.

This is why `skxml` also includes propensity-scored variants.
They reweight the contribution of hits so that retrieving rare labels counts more than simply rediscovering the obvious frequent ones.

I do not see these scores as a replacement for the ordinary at-k metrics.
They answer a slightly different question.

- plain Precision@k asks whether the top of the ranking is useful on average;
- propensity-scored Precision@k asks whether the ranking is still useful once label popularity bias is discounted.

When the label distribution is very skewed, looking at both is much more informative than looking at either one alone.

## The architectural point

At first I was tempted to keep everything inside a single package.
But the more I worked on this, the more the boundary clarified itself.

The training side and the evaluation side are connected, but they are not the same concern.

`scikit-omikuji` has to care about:

- sparse feature-label pipelines,
- Rust bindings,
- Parabel hyperparameters,
- beam search,
- and scalable prediction.

`skxml` has to care about:

- efficient top-k extraction,
- ranking-aware metrics,
- propensity weighting,
- and compatibility with `scikit-learn` scorers.

Trying to merge those concerns too early would have made both libraries worse.

Keeping them separate made the API clearer:
one library gives me a fast extreme multilabel estimator, the other gives me the evaluation language that such estimators actually need.

## Final thought

If I had to summarize the design in one sentence, it would be this:

train the large-label model as if it were a normal estimator, but evaluate it as a ranking system.

That is really the philosophy behind these two projects.

`scikit-omikuji` lets Parabel and the Rust `omikuji` backend enter a normal Python workflow without friction.
`skxml` gives that workflow the metrics it was missing, especially when top-k quality matters more than exact dense reconstruction.

I built both because I wanted extreme multilabel classification to feel less like a special-case research script and more like a coherent part of the `scikit-learn` ecosystem.
