---
layout: post
title: Variational inference in the spectral entropies framework
categories: science
published: false
date: 2018-05-21
use_math: true
---

# Variational inference

This code does wonderful things thanks to the Tensorflow automatic differentiation capabilities.

{% highlight python %}
from __future__ import with_statement

tf_logdir = '/tmp/'


import tensorflow as tf
import networkx as nx

import numpy as np

import seaborn as sns

import matplotlib.pyplot as plt
import pandas as pd

from scipy.linalg import expm

def graph_laplacian(A):
    return np.diag(A.sum(axis=0))-A

def vonneumann_density(L,beta):
    rho = expm(-L*beta)
    return rho/np.trace(rho)
tf.reset_default_graph()
g = tf.Graph()
with g.as_default(), tf.device('/device:CPU:0'):
    # Define the observed matrix (using the karate club)
    N = 50
    beta = 1*1E-2
    #G = nx.erdos_renyi_graph(N,pstar)
    #G = nx.karate_club_graph()
    #G = nx.planted_partition_graph(4,10,0.8,0.2)
    G = nx.barabasi_albert_graph(100,15)
    avgnn = np.array(list(nx.neighbor_degree.average_neighbor_degree(G)))
    N = len(G.nodes())
    A = nx.to_numpy_array(G)
    shape=[N, N]
    m = A.sum()
    L=np.diag(A.sum(axis=0))-A
    rho = vonneumann_density(L=L,beta=beta)
    
    # Convert stuff to tensorflow to create nodes in the computational graph
    beta=tf.convert_to_tensor(beta,name='beta',dtype=tf.float64)
    rho = tf.convert_to_tensor(rho,name='rho',dtype=tf.float64)
    Lobs = tf.convert_to_tensor(L,name='Lobs',dtype=tf.float64)
    
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
    train = tf.train.AdamOptimizer(learning_rate=0.01).minimize(rel_entropy)
    # Initialize the global variables
    init = tf.global_variables_initializer()

    # Run the computational graph
    with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as session:
        # op to write logs to Tensorboard
        writer = tf.summary.FileWriter(tf_logdir, session.graph)
        session.run(init)
        all_loss,alldeltaL = [], []
        epochs = 200
        ##### Start the training
        for step in range(epochs):
            ########## Tensorflow logging ##########
            session.run(train)
            
            ####### Matplotlib logging #######
            all_loss.append(session.run(rel_entropy))
            alldeltaL.append(session.run(deltaL))
            # Write logs at every iteration
            print('\r beta:',session.run(beta), 'step', step,  'density:',session.run(model_density), 'deltam:', session.run(deltaL) ,'loss:', all_loss[-1],end='')

        fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(20,9))
        ax[0].plot(all_loss)
        ax[0].set_title('Relative entropy')
        ax[0].set_xlabel('iteration')
        ax[1].plot(A.sum(axis=0),'r-')
        ax[1].set_title('Degree')
        ax[1].set_xlabel('node')
        ax[1].set_ylabel('degree')
        ax[1].plot(session.run(Amodel).sum(axis=0),'b.')
        ax[2].plot(alldeltaL)
        ax[2].set_title('$\Delta m$')
        
        plt.tight_layout()

{% endhighlight %}