---
layout: post
title: Thoughts
categories: science
published: false
date: 2018-06-24
---

This is a Python code to compute the spectral density of a random matrix ensemble via the average resolvent

    def spectral_density_laplacian_er(n,p,x,reps,eps=1E-1):
        def resolvent_trace(x,lambdai):
            return np.sum([1.0/(xi+1j*eps-x) for xi in lambdai])
        def average_resolvent_trace(x):
            return np.mean([resolvent_trace(x, eigvalsh(LER(n,p)) ) for r in range(0,reps)])
        return [-1/(np.pi*n)*np.imag(average_resolvent_trace(z)) for z in x]

The $\eps$ parameter is the one present in the limit. While analytically a limit procedure should be computed, but to perform the thing numerically, it corresponds to the bin size of an histogram, so if it is not too big (in the order 0.1) the noise of the expectations is averaged out.
The spectral density is computed as:

$$
\rho(x) = -\frac{1}{\pi n} \lim \limits_{\epsilon \to 0^+}\Im \left \langle \right \sum \limits_{i=1}^n \frac{1}{\lambda_i + j\epsilon - x} \rangle
$$

You can test it in this way:

    n=200
    p=0.25
    x=np.linspace(350,650,50)
    reps=10
    rho = spectral_density_laplacian_er(n,p,x,reps)
    plt.plot(x,rho)

and compare with this result:

    plt.hist(np.array([eigvalsh(LER(n,p)) for r in range(0,10)]).flatten(),200,normed='freq')
    plt.show()


