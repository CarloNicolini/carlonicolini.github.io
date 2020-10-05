---
layout: post
title: Sequence models
date: 2020-01-27
published: false
---

Temporal sequences are indexed with $x^{\langle 1 \rangle}$. The label of the i-th element of the sequence is denoted as $y^{\langle 1 \rangle}$.
So for example in Name Entity Recognition one has 

Every training example has a different length, we denote with $T_x^{(i)}$ the length of the sequence of the training example $i$.

To represent a word in a sentence one must define a vocabulary. For example the sentence

    Harry Potter and Hermione Granger invented a new spell
    x^<1>  x^<2> .... x^<T>

can be defined as an array of integers representing the word in the vocabulary.
This representation is called **One-hot** representation.

We want to learn sequence models with a neural network, with some input layer, some hidden layer etc.
It does not work simply like this, as every example may have different lenght.
Similarly as for convolutional neural networks we need a previous layer to deal with the very large vocabulary (which could be as large as 10,000 elements).

## Recurrent neural networks
Reading the sentence from left to right.

Initialize parameters of layer 0 to 0, as follows $a^{\langle 0 \rangle}=0$.
Then parameters of layer 1 are set as 

$$a^{\langle 1 \rangle} = g(w_{aa} a^{\langle 0 \rangle} + w_{ax}x^{\langle 1 \rangle} + b_a)$$

The activation function $g$ can be either $\tanh$, a $ReLu$ function but also activation.

The predicted value is hence found as

$$\hat{y}^{\langle 1 \rangle} = g(w_{ya} a^{\langle 1 \rangle} + b_y)$$

and so on the so forth for the following words.

### Forward step of a basic RNN
The two main equations for a recurrent neural networks are then used to update weights and biases for each layer:

\begin{equation}
a^{\langle t \rangle} = g\left( W_{aa} a^{\langle t-1 \rangle} + W_{ax} x^{\langle t \rangle} + b_a \right)
\end{equation}
and for the predicted values
\begin{equation}
\hat{y}^{\langle t \rangle} = g\left( W_{ya} a^{\langle t \rangle} + b_y \right)
\end{equation}	

## Back
