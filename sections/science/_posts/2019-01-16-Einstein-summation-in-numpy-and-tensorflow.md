---
layout: post
title: Einstein summation in Numpy and tensorflow
date: 2019-01-16
published: false
---


Einstein summation is a convention in tensor algebra where repeated indices are implicitly summed.
For example, imagine we have a matrix (a tensor of rank 2) $A_{i,j}$. To compute the trace, i.e. the sum of diagonal elements one has to compute

\begin{equation}
\textrm{Tr}(A) = \sum_{i=j}^n A_{ij}
\end{equation}

In the Einstein summation convention, the $\sum$ symbol is skipped and the trace of the matrix is indicated as $A_{ii}$.
You can extend this thing to very complex kind of computations with tensors of higher rank.
For example, you may want to compute the trace over the last two dimensions of a tensor of rank 4 $B_{i,j,k,l}$. This is equivalent to:

\begin{equation}
\tilde{B}_{ij} = \sum_{k=l}^n B_{i,j,k,l}
\end{equation}

The result is a tensor of rank 2, as we have summed over two indices.
This is done in numpy with the `np.einsum` function.

{% highlight python %}
import numpy as np
dim1 = 4
dim2 = 3
dim3 = 5
dim4 = 2
A = np.random.random([dim1,dim2,dim3,dim4])
np.einsum('ijkl->ij',A)
{% endhighlight %}

Here the sum is done over the missing indices `k,l`. The input array is indicated with `'ijkl'` while the output array as `'ij'`.

Batched outer products
----------------------

Suppose we have a tensor with shape `[batch_size, N]` where the first dimension `batch_size` is the number of $N$ arrays of which we want to compute the outer products with themselves.
The result should be a tensor of shape `[batch_size,N,N]` where every element along the two last dimensions is the outer product of the `N` size vector at row `batch_size`.
This is equivalent to computing the summation of the outer products:


\begin{align}
x  \in \mathbb{R}^{b \times n} \\\\
X  \in \mathbb{R}^{b \times n \times n} \\\\
X  = \sum_{j,k}^n x_{ij} x_{jk}
\end{align}


{% highlight python %}
import numpy as np
batch_size = 2
N = 5
x = np.random.random([batch_size,N])
np.einsum('ij,ik->ijk',x, x)
{% endhighlight %}



