---
layout: post
title: How to list all tensorflow devices
categories: tech
date: 2018-07-10
---

This is how you do:

{% highlight python %}
from tensorflow.python.client import device_lib

def get_available_devices():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU' or x.device_type=='CPU']
get_available_devices()
{% endhighlight %}
