---
layout: post
title: 'How to flatten multilayer networks in Python'
description: 'How to flatten multilayer networks in Python.'
date: 2019-06-07
published: false
use_math: true
categories:
  - science
  - complex-networks
---

## Dealing with a multilayer network via supra-adjacency matrix

{% highlight python %}
def flatten_multilayer(M):
    if len(M.shape) < 3:
        return M
    elif len(M.shape)==3:
        l,n,m = M.shape
        if n!=m:
           raise
        Mf = np.zeros([l*n,l*n])
        for i in range(l):
            Mf[n*i:n*(i+1),n*i:n*(i+1),] = M[i,:,:]
        return Mf
    elif len(M.shape)==4:
        la,lb,n,m = M.shape
        if n!=m:
            raise
        Mf = np.zeros([la*n,lb*n])
        for i in range(la):
            for j in range(lb):
                Mf[n*i:n*(i+1),n*j:n*(j+1),] = M[i,j,:,:]
        return Mf
{% endhighlight %}
