---
layout: post
title: Matlab R2016a crashes on Ubuntu 16.04 with NVidia 361 drivers
date: 2016-08-17
categories: tech
---

For those of you who upgraded Ubuntu from 14.04 to 16.04 and have found that Matlab is crashing with errors in nvidia drivers, you have three options:

1. If you have Matlab R2015 use that.
2. Downgrade your NVidia drivers.
3. Run Matlab R2016a with `-softwareopengl` flag:



https://devtalk.nvidia.com/default/topic/926199/linux/361-28-crashes-matlab-r2016a/
