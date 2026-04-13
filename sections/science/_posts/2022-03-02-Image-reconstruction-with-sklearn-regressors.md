---
layout: post
title: Image reconstruction with sklearn regressors
description: 'Image reconstruction with sklearn regressors.'
date: 2022-03-02
published: false
categories:
  - science
  - statistical-learning
---
A grayscale image is just a function $f(x, y)$ on a discrete grid: at each pixel coordinate you read an intensity. If you hide most of the pixels and keep only a small random subset, can you **fill the grid back in**? Framed that way, the task is plain **supervised regression**: train a model on pairs $(x, y) \mapsto \text{intensity}$, then predict intensity at every lattice point.

This note follows the neat experiment by [Alex Rogozhnikov](https://arogozhnikov.github.io/2016/02/09/DrawingPictureWithML.html), implemented with scikit-learn regressors. The results are surprisingly good for such a simple pipeline.

## Setup

1. Flatten the $H \times W$ image to a vector of length $HW$.
2. Build features: for each index $i$, use pixel column $x_i = i \bmod W$ and row $y_i = \lfloor i / W \rfloor$.
3. Subsample a fraction `train_size` of pixels for training; the rest are only used implicitly (they are predicted, not supervised).
4. **Center** the training targets by subtracting their mean, fit the regressor on residuals, then add the mean back after prediction. That keeps the model from wasting capacity on the global brightness level.

Any regressor that accepts two-dimensional inputs works: random forests, gradient boosting, kernel ridge, MLPs, etc. Trees excel at **piecewise constant** or mildly smooth approximations on the plane; smooth kernels or neural nets can interpolate more evenly when the image is gentle and sampling is dense enough.

## Code

```python
import numpy
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


def train_display(regressor, image, train_size=0.02):
    height, width = image.shape
    flat_image = image.reshape(-1)
    xs = numpy.arange(len(flat_image)) % width
    ys = numpy.arange(len(flat_image)) // width
    data = numpy.array([xs, ys]).T
    target = flat_image
    trainX, testX, trainY, testY = train_test_split(
        data, target, train_size=train_size, random_state=42
    )
    mean = trainY.mean()
    regressor.fit(trainX, trainY - mean)
    new_flat_picture = regressor.predict(data) + mean
    plt.figure(figsize=[20, 10])
    plt.subplot(121)
    plt.imshow(image, cmap="gray")
    plt.subplot(122)
    plt.imshow(new_flat_picture.reshape(height, width), cmap="gray")
    plt.show()
```

With only about **2%** of pixels labeled, a random forest often reproduces recognizable structure: large uniform regions collapse to flat patches, edges become staircases aligned with axis splits, and fine texture is lost unless you add many more trees or samples. That behaviour is a direct readout of how the learner **generalizes** from sparse coordinates to the full grid.

## Conclusion

This is not how one would compress or restore real images (no spatial context beyond $(x,y)$, no multiscale prior, no noise model). It *is* a crisp didactic demo: the same API you use for tabular regression suddenly acts like a **learned inpainting** trick, and changing `regressor` or `train_size` makes inductive bias and sample complexity visible in one figure.

For a fair comparison across models, fix `random_state`, sweep `train_size`, and measure error on the held-out pixels (`testX`, `testY`) as well as visual quality on the full grid. Rogozhnikov’s original post explores several learners and pictures; start there if you want richer baselines than a single forest.
