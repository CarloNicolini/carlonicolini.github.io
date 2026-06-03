---
layout: post
title: Better Jupyterlab with git and Darcula theme
description: 'Better Jupyterlab with git and Darcula theme.'
date: 2020-07-21
published: false
categories:
  - tech
---

A way to produce a better Jupyterlab notebook:

```bash
    pip install --upgrade jupyterlab-git
    jupyter lab build
    jupyter labextension install @telamonian/theme-darcula
```