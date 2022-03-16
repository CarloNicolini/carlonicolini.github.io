---
layout: post
title: Image reconstruction with sklearn regressors
date: 2022-03-02
published: false
---

# How to reconstruct an image using only a small subset of its pixels?

This question can be tackled by means of supervised regression models.
For this we use some of the canned sklearn models and check their results.
This code is taken from

[arogozhnikov.github.io](https://arogozhnikov.github.io/2016/02/09/DrawingPictureWithML.html)

I will anticipate that the results are great, in my humble opinion!

{%highlight python%}
def train_display(regressor, image, train_size=0.02):
    height, width = image.shape
    flat_image = image.reshape(-1)
    xs = numpy.arange(len(flat_image)) % width
    ys = numpy.arange(len(flat_image)) // width    
    data = numpy.array([xs, ys]).T
    target = flat_image
    trainX, testX, trainY, testY = train_test_split(data, target, train_size=train_size, random_state=42)
    mean = trainY.mean()
    regressor.fit(trainX, trainY - mean)
    new_flat_picture = regressor.predict(data) + mean
    plt.figure(figsize=[20, 10])
    plt.subplot(121)
    plt.imshow(image, cmap='gray')
    plt.subplot(122)
    plt.imshow(new_flat_picture.reshape(height, width), cmap='gray')
{%endhighlight%}


    train_display(RandomForestRegressor(n_estimators=100), image)
![]
