---
date: 2021-05-18
---

If you have problems with empty plotly output in jupyterlab remember that you need these packages:


    pip install jupyterlab "ipywidgets>=7.5"
    jupyter labextension install jupyterlab-plotly
    # OPTIONAL
    jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget@4.14.3


