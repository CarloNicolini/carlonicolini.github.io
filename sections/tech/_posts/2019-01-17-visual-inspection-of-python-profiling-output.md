---
layout: post
title: Visual inspection of python profiler output with gprof2dot
date: 2019-01-17
published: true
categories: tech
---

Ever wondered how to make a beatiful and powerful call graph from your python profiler?
I have found that there is no need to install heavyweight tools like KCachegrind or even worse, buying expensive IDEs.
The solution is simple.

Wrap the part of code you want to inspect (here a bogus function with name `my_super_slow_function()`) with the following call:

{% highlight python %}
def my_super_slow_function():
    return 1

import cProfile
pr = cProfile.Profile()
pr.enable()

my_super_slow_function()

pr.disable()
pr.dump_stats(file='profile.pstat')
{% endhighlight %}

Then run your Python code as always. This result in a `"profile.stat"` file that you can analyze using graphviz and the wonderful tool `gprof2dot`.
First install graphviz (on Ubuntu a simple thing):

{% highlight bash %}
sudo apt-get install graphviz
{% endhighlight %}

then install `gprof2dot` from the PyPi repositories:

{% highlight bash %}
sudo pip3 install gprof2dot
{% endhighlight %}

Finally you can convert the `profile.stat` file into a beatiful call graph.

{% highlight bash %}
gprof2dot -f pstats profile.pstat | dot -Tpdf -o profile.pdf
{% endhighlight %}

Take a look at the output file. Isn't it great?

<img src="https://raw.githubusercontent.com/jrfonseca/gprof2dot/733b59379592c39d9f595de7323260d397b8d3b9/sample.png" >
