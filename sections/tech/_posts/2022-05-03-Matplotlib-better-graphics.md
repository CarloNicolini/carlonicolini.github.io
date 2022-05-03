---
title: Better graphics with matplotlib and seaborn
layout: post
date: 2022-05-03
---

These lines should never miss at the beginning of your Jupyter notebooks (especially if you are on Mac)
We set the default font to Helvetica (where available), and specify the high resolution for the images.

```python
sns.set_context("notebook") # makes the text in the plots larger, for better visibility
%config InlineBackend.figure_format = 'svg' # makes the plots HD in the notebook
mpl.rcParams["figure.autolayout"] = True # enables tigh layout. Better multiplots


plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Helvetica'
```