---
layout: post
title: 'Plotly and Jupyterlab issues'
description: 'Plotly-and-JupyterLab issues resolution'
date: 2021-05-18
published: true
categories: 
  - tech
---

# How to install jupyterlab utilities

If you have problems with empty plotly output in jupyterlab remember that you need these packages:

```bash
pip install jupyterlab "ipywidgets>=7.5"
jupyter labextension install jupyterlab-plotly
# OPTIONAL
jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget@4.14.3
```
