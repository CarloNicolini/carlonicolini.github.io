---
layout: post
categories: science
date: 2019-03-21
use_math: true
published: true
---

In these notes I want to introduce Hidden Markov Model, one of the simplest but rich enough models to handle real world applications for modeling sequential models.

In HMM we have random variables $z_1,\ldots z_n \in \{ 1,\ldots,m \}$ which are the **hidden** or **latent** variables, and the random variables $x_1,\ldots x_n \in X$. The hidden variables take discrete values. Instead, the variables in $X$ can be discrete, finite, real or any type, which are the **observed random variables**.
The joint distribution of $\mathbf{z},\mathbf{x}$ respect the graph

<img src="/static/postfigures/hmm.png">

which is called the Trellis diagram, the graphical model for an HMM.
The fact that the joint distribution respects this graphical model, means that the joint distribution factors as

\begin{equation}
p(x_1,\ldots,x_n,z_1,\ldots,z_n) = p(z_1) p(x_1 \vert z_1) \prod \limits_{k=2}^n p(z_k \vert z_{k-1}) p(x_k \vert z_k)
\end{equation}

**Remark 1** One of the applications of HMM is handwriting recognition. In this case, the observed variables are the strokes of the letters, the hidden variables instead are the integer index of the letter.

The parameters of the Hidden Markov Models are the *transition probabilities*,indicated as $T(i,j)$, the *transition matrix*:

\begin{equation}
T(i,j) = P(z_{k+1}=j \vert z_k=i)
\end{equation}

and we have to chose the numbers $T(i,j)$ for all $(i,j)\in \{1,\ldots,m\}$. The transition probability is then a stochastic $n\times m$ matrix.
The second set of parameters are the *emission probabilities* $\epsilon_i(x) = p(x \vert z=i)$, for $i \in \{1,\ldots m\}$ where $p$ is the probability density. In other words $\epsilon_i$ is a probability distribution on the set of observed variables $X$, or $\epsilon_i(x)=P(X_k=x \vert z_k=i)$.
So the joint distribution of the HMM factorizes into the product of transition probabilities and emission probabilities.

Finally, we need to choose an initial distribution, $\pi(i) = P(z_1=i)$: this is a probability mass function, as $z$ are discrete.
Let us rewrite the joint distribution

\begin{equation}
p(x_1,\ldots,x_n, z_1, \ldots z_n) = \pi(i) \epsilon_{z_1}(x_1) \prod \limits_{k=2}^n T(z_{k-1} \vert z_k) \epsilon_{z_k}(x_k)
\end{equation}

**Remark 2** The emission probabilities $\epsilon_i$ are pretty much arbitrary, as they depend on the kind of variables specified by $x$. If $x$ are discrete, the emission probabilities are pmf, they may be Binomial, geometric. If $x$ are real, one can use Gaussian etc.

The main thing that makes HMM work is not the form of the individual distribution, but the most important thing is that the distribution factors in the way specified before. This makes HMM work in the sense that it is possible to do tractable inference.
The inference algorithm is what makes HMM work and is called the *forward-backward* algorithm.

### Example 1
We consider hidden variables $z_k \in \{0,1\}$ and $x$ are real numbers. The $z$ stick to either 1 or 0 with a transition matrix

\begin{equation}
T=\begin{pmatrix}
0.99 & 0.01 \\\
0.02 & 0.98
\end{pmatrix}
\end{equation}
This is a doubly stochastic matrix, in the sense that both rows and columns sum to 1.
Let's say that the $x$ are normally distributed around the $z$s, this means that $x_k$ is conditionally independent on anything else but the $z_k$.
This model would look like the following:

<img src="/static/postfigures/hmm2.png" >

## Forward backward algorithm
The forward-backward algorithm is the tool to make inference on HMM, and is an example of *dynamic programming*, a term used to mean *optimization*.
There are many different methods for making inference, and dynamic programming is one of this kind.
Dynamic programming allows a way to exactly and efficiently compute highly non trivial things, and is due to Richard Bellman, who first used dynamic programming in graph theory.

The forward-backward model assumes that the emission probabilities and transition matrix are known, together with the initial distribution.
The goal of the FB algorithm, is to compute $p(z_k \vert\mathbf{x})$. We denote $x_{i:j}$ as the sequence of $x$ from $x_i$ to $x_j$.
Hence the FB algorithm computes the marginal probability.

In the forward part, the algorithm computes $p(z_k, x_{1:k})$ for all $k=1,\ldots,n$, then the backward part computes $p(x_{k+1:n} \vert z_k)$ for all $k=1,\ldots n$.
How does this algorithm give the result?
We know that

\begin{equation}
p(z_k \vert x) \propto p(z_k,x)=p(x_{k+1:n}\vert x_{1:k}) p(z_k , x_{1:k})
\end{equation}
by the definition of conditioned probability and looking at the graphical model.
The first terms is the backward part, the second term is the forward part.

This makes possible to make arbitrary inference, for example $p(z_k \neq z_{k+1} \vert x)$, a thing known as change detection.
Parameters estimation (like for example mean and variance of gaussian of observed variables) is done via the **Baum-Welch** algorithm, which couples the forward-backward algorithm with **expectation maximization**.

Another thing possible via the forward-backward algorithm is to sample from the posterior, via the Viterbi algorithm.

## Forward algorithm

Most expositions of forward-backward algorithm are very simple, but most expositions are rather tricky. One trick for Markov chains is always used.
The *goal* for the forward algorithm is to compute $p(z_k, x_{1:k})$. Let us start working writing down this distribution:

\begin{align}
p(z_k, x_{1:k}) =& \sum_{z_{k-1}=1}^n p(z_{k}, z_{k-1}, x_{1:k}) = \\\\ & \sum_{z_{k-1}} p(x_k \vert z_k z_{k-1}, x_{1:{k-1}}) p(z_k \vert z_{k-1},x_{1:k-1}) p(z_{k-1} \vert x_{1:{k-1}}) p(x_{1:k-1})
\end{align}

The trick is to take $p(z_k, x_{1:k})$ and marginalize one step back. 


The HMM is a generative probabilistic model, in which a sequence of observable $\mathbf{X}$ variable is generated by a sequence of internal hidden state $\mathbf{Z}$.
The hidden states can not be observed directly.
The transitions between hidden states are assumed to have the form of a (first-order) Markov chain.
They can be specified by the start probability vector $\boldsymbol \pi$ and a transition probability matrix $\mathbf{T}$.
The emission probability of an observable can be any distribution with parameters $\boldsymbol \theta_i$ conditioned on the current hidden state (e.g. multinomial, Gaussian).
The HMM is completely determined by $\boldsymbol \pi, \mathbf{T}$ and $\boldsymbol \theta_i$.

There are three fundamental problems for HMMs:

-    Given the model parameters and observed data, estimate the optimal sequence of hidden states.
-    Given the model parameters and observed data, calculate the likelihood of the data.
-    Given just the observed data, estimate the model parameters.

The first and the second problem can be solved by the dynamic programming algorithms known as the Viterbi algorithm and the Forward-Backward algorithm, respectively. The last one can be solved by an iterative Expectation-Maximization (EM) algorithm, known as the Baum-Welch algorithm.

**  To be continued **
<!-- Continuare da minuto 5:00 di [questo video](https://www.youtube.com/watch?v=M7afek1nEKM) -->
