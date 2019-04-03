---
layout: post
title: Einstein summation in Numpy
categories: science
date: 2019-01-16
published: true
use_math: true
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
B^\star_{ij} = \sum_{k=l}^n B_{i,j,k,l}
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

Batched matrix operations via `np.einsum`
-----------------------------------------

My greatest interest in the usage of numpy einstein summation is when doing operations on batched squares matrices. By *batched* matrix, here I mean an array of square matrices, hence an
array with three indices. 

# Batched outer products
To start, suppose we have a tensor with shape `[batch_size, N]` where the first dimension `batch_size` is the number of $N$ arrays of which we want to compute the outer products with themselves.
The result should be a tensor of shape `[batch_size,N,N]` where every element along the two last dimensions is the outer product of the `N` size vector at row `batch_size`.
This is equivalent to computing the summation of the outer products:

\begin{align}
x  \in \mathbb{R}^{b \times n}
\end{align}

\begin{align}
X  \in \mathbb{R}^{b \times n \times n}
\end{align}

\begin{align}
X  = \sum_{j,k}^n x_{ij} x_{jk}
\end{align}

where $b$ is the `batch_size` and $n=$`N`.
This operation can be done via the appropriate `np.einsum` call as follows in this example:

{% highlight python %}
import numpy as np
batch_size = 2
N = 5
x = np.random.random([batch_size,N])
X = np.einsum('ij,ik->ijk',x, x)
{% endhighlight %}


# Batched graph matrices

Similarly to the discussed above, complex operations on graph-related matrices can be done. Here I propose batched graph laplacians, modularity matrix.
Here are some example functions that I wrote for `networkqit`

{% highlight python %}
def graph_laplacian(A):
    """
    Get the graph Laplacian from the adjacency matrix
    :math:`\\mathbf{L} = \\mathbf{D} - \\mathbf{A}`
    If a batched adjacency matrix of shape [batch_size, N, N] is
    given, the batched laplacian is returned.
    """
    if len(A.shape)==3:
        N = A.shape[-1] # last dimension is number of nodes
        D = np.eye(N) * np.transpose(np.zeros([1, 1, N]) + np.einsum('ijk->ik', A), [1, 0, 2])
        return D - A
    else:
        return np.diag(A.sum(axis=0)) - A


def normalized_graph_laplacian(A):
    """
    Get the normalized graph laplacian 
    :math:`\\mathcal{L}=I - D^{-1/2} A D^{-1/2}`
    If a batched adjacency matrix of shape [batch_size, N, N] is
    given, the batched laplacian is returned.
    """
    if len(A.shape)==3:
        N = A.shape[-1]
        invSqrtD = np.eye(N) * np.transpose(np.zeros([1, 1, N]) + 1/np.sqrt(np.einsum('ijk->ik', A)), [1, 0, 2])
        return  np.eye(N) - invSqrtD @ A @ invSqrtD
    else:
        invSqrtT = np.diag(1.0 / np.sqrt(A.sum(axis=0)))
        return np.eye(A.shape[0]) - invSqrtT @ A @ invSqrtT


def modularity_matrix(A):
    """
    Returns the modularity matrix
    :math:`\\mathbf{B} = \\mathbf{A} - \\frac{\\mathbf{k} \\mathbf{k}^T}{2m}`
    """
    if len(A.shape)==3:
        N = A.shape[-1]
        b  = A.shape[0]
        k = np.einsum('ijk->ik', A)
        kikj = np.einsum('ij,ik->ijk', k, k)
        m = np.sum(np.sum(A,axis=1), axis=1, keepdims=True)
        B = A - (kikj/np.broadcast_to(np.expand_dims(m,axis=2),A.shape))    # batched kikj/2m
        return  B
    else:
        k = A.sum(axis=0)
        return A - np.outer(k, k) / k.sum()

def signed_laplacian(A):
    """
    Returns the signed Laplacian as defined in https://arxiv.org/pdf/1701.01394.pdf
    :math:`\\mathbf{\\bar{L}} = \\mathbf{\\bar{D}} - \\mathbf{A}
    where the diagonal matrix D is made of the absolute value of the row-sum of A.
    """
    if len(A.shape)==3:
        N = A.shape[-1] # last dimension is number of nodes
        D = np.eye(N) * np.transpose(np.zeros([1, 1, N]) + np.einsum('ijk->ik', A), [1, 0, 2])
        return np.abs(D) - A
    else:
        return np.diag(np.abs(A.sum(axis=0))) - A
{% endhighlight %}