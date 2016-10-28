---
layout: post
title: Computing hypergeometric probability efficiently in C++
categories: science
published: true
date: 2016-10-28
---

Computing hypergeometric function is a slow and difficult process, often affected by overflow errors as evaluating binomial coefficient may return extremely large numbers.
Fortunately, thanks to some hypergeometric identities, is possible to evaluate the hypergeometric probability quickly.

I've implemented and tested the **HyperQuick** algorithm, from;

**Aleš Berkopec**, *HyperQuick algorithm for discrete hypergeometric distribution*, Journal of Discrete Algorithms 5 (2007) 341–347

that evaluates the value of hypergeometric cumulative distribution of the form:

$$
C(n,x,N,M) = \sum \limits_{j=0}^x \frac{\binom{M}{j}\binom{N-M}{n-j}}{\binom{N}{n}}
$$

The demonstration is based on the binomial identity

$$
\sum \limits_{k=0}^x \binom{M}{k}\binom{N-M}{n-k} =
\sum \limits_{m=M}^{N-n+x} \binom{m}{x}\binom{N-1-m}{N-m-n+x}
$$

As shown by the author, for any accuracy $$\epsilon \geq 0$$ the required number of computational cycles is less then $$N-n$$, where $$N$$ is the size of the population and $$n$$ is the size of the sample.
Here I provide the straight C++ implementation of the pseudocode the author provides in its paper, for real-wolrd uses.
Please let me know if you find any bug.

    {% highlight cpp %}
    #include <cstdio>
    const double TOL=1E-9;
    double InvJm(int n, int x, int N, int m)
    {
        return (1.0-double(x)/(double(m)+1.0))/(1.0-(double(n)-1.0-double(x))/(double(N)-1.0-double(m)));
    }

    double hyperquick(int n, int x, int N, int M)
    {
        double s=1.0;
        for (int k=x; k<=M-2; ++k)
        {
            s = s*InvJm(n,x,N,k)+1.0;
        }
        double ak=s;
        double bk=s;
        double k=M-2;
        double epsk = 2*TOL;
        while ((k<(N-(n-x)-1)) && epsk>TOL )
        {
            double ck = ak/bk;
            k = k+1;
            double jjm = InvJm(n,x,N,k);
            bk = bk*jjm + 1.0;
            ak = ak*jjm;
            epsk = (N-(n-x)-1-k)*(ck-ak/bk);
        }
        return 1-(ak/bk-epsk/2);
    }

    int main(int argc, char *argv[])
    {
        int n=atoi(argv[1]);
        int x=atoi(argv[2]);
        int N=atoi(argv[3]);
        int M=atoi(argv[4]);

        printf("Hypergeometric probability(%d,%d,%d,%d)=%f\n", n,x,N,M, hyperquick(n,x,N,M));
    }
    {% endhighlight %}

I think the code is self-explanatory and any porting in languages like Python is straightforward.
