---
layout: default
title: How to install Octave on OSX Yosemite
date: 2015-10-13
---

For those who have problems installing Octave on OSX Yosemite, this is a simple guide.

First of all you need [HomeBrew](www.brew.sh)

1. Open a terminal and install **homebrew** :

	{% highlight sh %}
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{% endhighlight %}


2. Update and check if **homebrew** is working fine.

	{% highlight sh %}
    brew update
    brew doctor{% endhighlight %}

3. Install **XQuartz** which is a **X11** substitute for recent OSX distributions [XQuartz](http://xquartz.macosforge.org/landing/)

4. Install Octave with Homebrew

	{% highlight sh %}
    brew tap homebrew/science
    brew update
    brew install octave --with-x11{% endhighlight %}


Install fltk for Gnuplot (used by Octave for graph visualization)

	{% highlight sh %}
    brew install gnuplot --with-x11
    {% endhighlight %}
