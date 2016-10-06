---
layout: post
title: How to upgrade R to the latest version on Ubuntu 14.04
categories: tech
date: 2016-06-10
---

Follow this instruction:

[https://www.digitalocean.com/community/tutorials/how-to-set-up-r-on-ubuntu-14-04](https://www.digitalocean.com/community/tutorials/how-to-set-up-r-on-ubuntu-14-04)

but first you need to add the key to the Ubuntu keyserver:

    sudo gpg --keyserver-options http-proxy=http://YOURPROXYSERVER --keyserver keyserver.ubuntu.com --recv-key E084DAB9

where `YOURPROXYSERVER` is the address of your proxy server.


 