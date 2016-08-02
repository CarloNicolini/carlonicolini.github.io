---
layout: default
title: How to reset unity in Ubuntu 14.04
date: 2015-10-05
---

For those who struggle with frequent freezes of Unity, this is a short guide on how to reset Unity to default settings in Ubuntu 14.04.

1. Open a terminal window (from Launcher or `CTRL+ALT+T`)
2. Type the following

	{% highlight sh linenos %}
    sudo apt-get install dconf-tools
    {% endhighlight %}

3. Reset unity:

	{% highlight sh linenos %}
    dconf reset -f /org/compiz
    setsid unity
    unity --reset-icons
    {% endhighlight %}
