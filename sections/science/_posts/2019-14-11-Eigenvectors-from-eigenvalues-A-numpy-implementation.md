---
layout: post
title: Eigenvectors from eigenvalues a numpy implementation
categories: science
published: true
date: 2019-11-14
---

Recently a very nice article appeared on [QuantaMagazine](https://www.quantamagazine.org/neutrinos-lead-to-unexpected-discovery-in-basic-math-20191113/), that relates the eigenvalues of a matrix with its eigenvectors.
The paper is explained in detail in the following arxiv paper

[https://arxiv.org/pdf/1908.03795.pdf](https://arxiv.org/pdf/1908.03795.pdf)

Here I provided a very simple and initial numpy implementation of this method, that is able to return the squared norm of the eigenvectors of any hermitian matrix

{% highlight python%}
import numpy as np
def minor(A_,i):
	"""
	Returns the j-th minor of a matrix A by removing its j-th column and row

	Args:
		A_: the input square matrix
		j:  the row and column to remove
	"""
    n = A_.shape[0]
    ix = list(set(list(range(n))) - set([i]))
    return A_[np.ix_(ix,ix)]

def norm_squared_eig(A : np.array):
	"""
	Returns the element-wise squared norm of the elements of the eigenvectors
	of an hermitian matrix
	Args:
		A_: the input square matrix
	Returns:
		|V(i,j)|^2 where V is the eigenvector matrix of A
	"""
    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        return ValueError('Only applies to square hermitian matrices')
    lambdA = np.linalg.eigvals(A)
    V2 = np.zeros([n,n])
    lambdaM = [np.linalg.eigvals(minor(A,j)) for j in range(n)]
    for i in range(n):
        lhs =  np.prod([lambdA[i] - lambdA[k] for k in np.arange(0,n) if k!=i])
        for j in range(n):
            lambdaMj = lambdaM[j]
            rhs = np.prod([lambdA[i] - lambdaMj[k] for k in range(0,n-1)])
            V2[i,j] = rhs/lhs
    return V2
{% endhighlight %}

You can test this wonderful computational trick against the result of the eigenvectors from numpy

{% highlight python %}
import numpy as np

# Creates an hermitian matrix
X = np.random.random([10,10])
X = X+X.T
# compute its correct eigenpairs
lambdX, Vx = np.linalg.eig(X)
# Compute the absolute difference of the elements from the 
# function norm_squared_eig
np.abs(norm_squared_eig(X) - Vx.T**2).sum()
{% endhighlight %}

You can check that the result is pretty good, with a nice numerical precision.


I want to extend this function to the application of the numpy.linalg.eigvalsh function, the order of the eigenpairs has to be considered though in this case.
It's not simply replacing `np.linalg.eig` with `np.linalg.eigh` because while `eigh` returns the eigenpairs sorted by the magnitude of the eigenvalues, `eig` does not.


A simple illustration that shows the meaning of matrix minors and eigenvalues, as in our case:

<img src='https://d2r55xnwy6nx47.cloudfront.net/uploads/2019/11/Valuevector_LRI-1087x1720.jpg' class='center' width='100%'>