---
layout: post
title: Variational inference in Tensorflow in the spectral entropies framework
categories: science
published: false
date: 2019-07-20
---

# Code

The ideas collected in the previous sections are collected in this code, which has then been developed in the package **networkqit**.

{% highlight python %}
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

import sys
sys.path.append('..')

import tensorflow as tf
import networkx as nx

import numpy as np
import networkqit as nq
import networkx as nx
import seaborn as sns
plt.style.use('ggplot')
from networkqit import graph_laplacian as GL
import matplotlib.pyplot as plt

tf.reset_default_graph()

# Imperative part
G = nx.barabasi_albert_graph(50,15)
N = len(G.nodes())
shape=[N, N]
A = nx.to_numpy_array(G)
m = A.sum()
L= np.diag(A.sum(axis=0)) - A

# Deferred part
with tf.device('/device:CPU:0'):
    Lobs = tf.placeholder(dtype=tf.float64)
    beta = tf.placeholder(dtype=tf.float64)
    rho = tf.linalg.expm(Lobs)
    rho = rho/tf.trace(rho)

    # Define the tensorflow optimization variable x
    xi = tf.Variable(tf.random_uniform(shape=[N,],dtype=tf.float64), name='xi',dtype=tf.float64)
    # sampling phase, create the sampled matrix Amodel
    rij = tf.random_uniform(shape,minval=0.0, maxval=1.0,dtype=tf.float64)
    rij = (tf.transpose(rij)+rij) / 2.0
    rij = tf.multiply(rij,tf.constant([1.0],dtype=tf.float64)-tf.eye(N,dtype=tf.float64))

    xij = tf.einsum('i,j->ij', xi, xi) # outer product
    pij = xij / (1.0 + xij)
    Amodel = 1.0 / (1.0 + tf.exp(50*rij-50*pij)) # this is like setting < to 0 and > to 1
    Amodel = tf.multiply(Amodel,tf.constant([1.0],dtype=tf.float64)-tf.eye(shape[0],dtype=tf.float64)) # set diagonal to zero
    # Compute the model density
    model_density = tf.reduce_sum(Amodel)/(N * (N-1))
    # Compute the model Laplacian    
    Lmodel = tf.diag(tf.reduce_sum(Amodel,axis=0)) - Amodel

    # Monitor the difference in number of links between model and data
    deltaL = m - tf.reduce_sum(Amodel)

    # Model energy
    Em = tf.reduce_sum(tf.multiply(Lmodel,rho,name='Lmrho'),name='TrLmrho')
    # Observation energy
    Eo = tf.reduce_sum(tf.multiply(Lobs,rho,name='Lobsrho'),name='TrL_orho')
    # Model laplacian eigenvalues
    lm = tf.linalg.eigvalsh(Lmodel,name='lambda_model')
    # Observation laplacian eigenvalues
    lo = tf.linalg.eigvalsh(Lobs,name='lambda_obs')
    # Model free energy
    Fm = -tf.reduce_logsumexp(-beta*lm,name='Fm') / beta
    # Observation free energy
    Fo = -tf.reduce_logsumexp(-beta*lo,name='Fo') / beta

    loglike = beta*(-Fm + Em)
    entropy = beta*(-Fo + Eo)
    rel_entropy = tf.abs(loglike - entropy)
    grad = tf.gradients(rel_entropy,xi)

    # Define the optimizer
    learning_rate = tf.placeholder(dtype=tf.float64)
    train = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(rel_entropy)
    # Initialize the global variables
    init = tf.global_variables_initializer()


with tf.Session() as sess:
    sess.run(init)
    all_loss = []
    all_deltaM = []
    beta_range = np.logspace(2,-3,20)
    nepochs = 10000
    all_steps = 0
    for b in beta_range:
        for epoch in range(0,nepochs):
            feed_dict = {Lobs:L, beta:b , learning_rate: 0.001}
            sess.run(train, feed_dict = feed_dict)
            res = sess.run([beta,rel_entropy,deltaL,model_density,learning_rate],feed_dict = feed_dict)
            #sol = sess.run(xi,feed_dict = feed_dict)
            all_loss.append(res[1])
            all_deltaM.append(res[2])
            all_steps += 1
            # Logging
            print('\rDone:%.1f%% \tStep:%d\tbeta: %.2g\tLoss: %.2g\tDeltaM: %.2g\tDensity: %.2f\tlearning_rate:%.2g' % (100*all_steps/(len(beta_range)*nepochs),epoch,res[0],res[1],res[2],res[3],res[4]), end='')
            
    # Plotting part
    fig,ax = plt.subplots(ncols=2,nrows=1,figsize=(24,8))
    for i,b in enumerate(beta_range):
        ax[0].plot(np.linspace(i*nepochs,(i+1)*nepochs,nepochs),all_loss[i*nepochs:(i+1)*nepochs])
    ax[0].set_title('Relative entropy')
    ax[0].set_xlabel('Iteration')
    for i,b in enumerate(beta_range):
        ax[1].plot(np.linspace(i*nepochs,(i+1)*nepochs,nepochs),all_deltaM[i*nepochs:(i+1)*nepochs])
    ax[1].set_title('$\\Delta m$')
    ax[1].set_xlabel('Iteration')
    
{% endhighlight %}