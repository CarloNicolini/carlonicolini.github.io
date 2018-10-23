---
layout: post
title: Install latest igraph 0.7.1 for Python3 on Ubuntu
categories: tech
date: 2018-07-10
---

If you choose to use the igraph library with Python 2, it’s a cakewalk to get it running on a fresh install of Ubuntu 16.04:

    sudo apt install python-igraph

However, a python3-igraph package is not available in the same repo and you have to take a little detour. We’ll use pip3 to do the deed which we first have to install:

    sudo apt install python3-pip

On Ubuntu 16.04, packages build-essential and python-dev should already be installed, but some other packages are missing, lxml2 and lz. Install them like so:

    sudo apt install libxml2-dev libz-dev

That should be all. We can now install igraph for Python 3:

    sudo pip3 install python-igraph
