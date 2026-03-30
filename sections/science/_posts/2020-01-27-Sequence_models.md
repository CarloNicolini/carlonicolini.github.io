---
layout: post
title: Sequence models and recurrent networks
date: 2020-01-27
published: false
categories: science
---

## At the core of modern NLP

Many prediction problems are naturally **sequential**: speech, text, sensor traces, or any ordered data where the $t$-th observation may depend on earlier ones. This note fixes notation for such models and sketches the simplest recurrent neural network (RNN) and how it is trained.

## Notation

We write $x^{\langle t \rangle}$ for the input at time $t$ and $y^{\langle t \rangle}$ for the corresponding target (when there is one). Training examples need not share the same length: for example $i$, we denote the input length by $T_x^{(i)}$.

### Example: named entity recognition

In **named entity recognition (NER)**, each token in a sentence gets a label (person, location, organization, other, …). For a sentence of length $T$, you have inputs $x^{\langle 1 \rangle},\ldots,x^{\langle T \rangle}$ and labels $y^{\langle 1 \rangle},\ldots,y^{\langle T \rangle}$. The model must use context: the same surface form can be an entity or not depending on neighbors.

## Discrete tokens: vocabulary and one-hot vectors

To feed text into a network, we first choose a **vocabulary** (a fixed list of tokens—often words or subwords). Each token is mapped to an index in $\{1,\ldots,|V|\}$. A common encoding is the **one-hot** vector in $\mathbb{R}^{|V|}$: all zeros except a single one at the token’s index. For instance, with a small vocabulary the sentence

> Harry Potter and Hermione Granger invented a new spell

might be represented as indices $(x^{\langle 1 \rangle},\ldots,x^{\langle T \rangle})$, each then expanded to a one-hot vector.

Vocabularies are often large (on the order of $10^4$ tokens or more), so in practice the first trainable layer is usually an **embedding** matrix that maps each index to a dense vector of moderate dimension, rather than feeding raw one-hot vectors through a huge first-layer weight matrix.

## Why a plain feedforward stack is awkward

Two issues show up immediately. **Variable length:** a sentence with $T=7$ and one with $T=20$ are not the same tensor shape unless you pad or segment. **High-dimensional discrete inputs:** one-hot vectors over $|V|$ categories call for a structured first stage (embeddings or a factored input layer), analogous to how convolutional networks exploit structure in images.

## Recurrent neural networks

A simple strategy is to read the sequence **left to right** (or right to left, or both in bidirectional models) and maintain a **hidden state** that summarizes the past.

Initialize $a^{\langle 0 \rangle} = 0$. For $t = 1,2,\ldots,T$, update

$$
a^{\langle t \rangle} = g\left( W_{aa}\, a^{\langle t-1 \rangle} + W_{ax}\, x^{\langle t \rangle} + b_a \right),
$$

and predict at each step

$$
\hat{y}^{\langle t \rangle} = h\left( W_{ya}\, a^{\langle t \rangle} + b_y \right).
$$

Here $g$ is typically $\tanh$ or ReLU for the hidden recurrence; $h$ is chosen for the task (e.g. softmax over labels for per-token classification, sigmoid for binary outputs). The same parameters $(W_{aa}, W_{ax}, W_{ya}, b_a, b_y)$ are shared across $t$: the network is **weight-tied** over time.

For a compact form, one can stack $W_{aa}$ and $W_{ax}$ into a single matrix multiplying the concatenation $[a^{\langle t-1 \rangle}; x^{\langle t \rangle}]$; the mathematics is unchanged.

### Forward pass (summary)

The two defining equations are exactly the pair above: a recurrence for $a^{\langle t \rangle}$ and a readout for $\hat{y}^{\langle t \rangle}$. Unrolling over time draws the familiar chain of cells, each receiving $x^{\langle t \rangle}$ and the previous $a^{\langle t-1 \rangle}$.

## Loss and backpropagation through time

For supervised training, one defines a loss at each time step where a label exists, e.g.

$$
\mathcal{L} = \sum_{t \in \mathcal{T}} \ell\bigl( \hat{y}^{\langle t \rangle}, y^{\langle t \rangle} \bigr),
$$

and sums or averages over the batch. **Backpropagation through time (BPTT)** applies the chain rule along the unrolled graph: gradients flow backward from later losses into earlier hidden states and shared weights. In long sequences, implementations often **truncate** the unrolling (TBPTT) so that memory and compute stay bounded; that trades off exact long-range credit assignment for feasibility.

## Conclusion

The vanilla RNN is the minimal nonlinear dynamical system that shares parameters across time and can, in principle, summarize arbitrarily long prefixes in $a^{\langle t \rangle}$. In practice, deep or long unrollings make **vanishing and exploding gradients** common; **LSTMs**, **GRUs**, and other gated architectures were introduced largely to stabilize memory over many steps. For very long contexts and parallel training, **attention** and **transformer** models replace or augment recurrence with mechanisms that route information more directly. The recurrence above remains the standard starting point: it makes explicit what “using the past” means in a differentiable model and why training requires unfolding the same weights across the sequence.
