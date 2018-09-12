---
layout: post
title: Weighted graphs from adjacency matrix in graph-tool
categories: science
published: true
use_math: true
date: 2018-09-12

---

{% highlight python %}
import graph_tool.all as gt
def to_graph_tool(adj):
    g = gt.Graph(directed=False)
    eprop = g.new_edge_property('double')
    g.edge_properties['weight'] = eprop
    nnz = np.nonzero(np.triu(adj))
    g.add_edge_list(np.hstack([np.transpose(nnz),adj[nnz[0]]]),eprops=[eprop])
    return g
{% endhighlight %}

and to plot the result:

{% highlight python %}
g = to_graph_tool(bct.binarize(bct.threshold_absolute(A[0:50,0:50],0.55)))
print(g.num_vertices(),g.num_edges())
state = gt.minimize_blockmodel_dl(g,state_args=dict(recs=[g.ep.weight],rec_types=["real-exponential"]))
print('Done')
state.draw()
{% endhighlight %}
