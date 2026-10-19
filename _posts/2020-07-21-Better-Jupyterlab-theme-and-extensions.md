---
layout: post
title: Better Jupyterlab with git and Darcula theme
description: 'Better Jupyterlab with git and Darcula theme.'
date: 2020-07-21
published: false
permalink: "/sections/tech/2020/07/21/Better-Jupyterlab-theme-and-extensions.html"
categories:
  - engineering
---
A way to produce a better Jupyterlab notebook:

```bash
    pip install --upgrade jupyterlab-git
    jupyter lab build
    jupyter labextension install @telamonian/theme-darcula
```