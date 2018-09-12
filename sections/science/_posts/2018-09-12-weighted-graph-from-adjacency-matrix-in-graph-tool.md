---
layout: post
title: Weighted graphs from adjacency matrix in graph-tool
categories: science
published: true
use_math: true
date: 2018-09-12

---

{% highlight python %}
def to_graph_tool(adj):
    g = gt.Graph(directed=False)
    eprop = g.new_edge_property('double')
    g.edge_properties['weight'] = eprop
    nnz = np.nonzero(adj)
    g.add_edge_list(np.hstack([np.transpose(nnz),adj[nnz[0]]]),eprops=eprop)
    return g
{% endhighlight %}
