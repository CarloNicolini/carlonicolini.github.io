---
title: How to make HDBScan an inductive clustering method
categories: tech
layout: post
date: 2021-07-28
---

There is a large difference between inductive and transductive clustering methods.
While the first are more similar to supervised learning, in the sense that once trained on N examples they can generalize to M unseen new samples, transductive method instead need to see all data, but cannot generalize to new samples.

HDBscan is largely a transductive method, and to make it able to generalize to new data we can wrap in a new class the `approximate_predict` method offered by the library.

{% highlight python %}
from hdbscan import HDBSCAN
from hdbscan import approximate_predict

class HDBSCANPredict(HDBSCAN):
    def __init__(self, min_cluster_size=10, alpha=1.0, cluster_selection_epsilon=0.0):
        super().__init__(
            min_cluster_size=min_cluster_size,
            alpha=alpha,
            cluster_selection_epsilon=cluster_selection_epsilon,
            prediction_data=True,
        )

    def predict(self, X, y=None):
        self.generate_prediction_data()
        return approximate_predict(self, X)[0]

    def predict_proba(self, X):
        self.generate_prediction_data()
        return approximate_predict(self, X)[1]

    def fit_transform(self, X, y=None):
        super().fit(X)
        out = approximate_predict(self, X)[0][:, None]
        return out

    def transform(self, X, y=None):
        return approximate_predict(self, X)[0][:, None]

    def fit(self, X, y=None):
        super().fit(X, y)
        self.generate_prediction_data()
        return self
{% endhighlight %}