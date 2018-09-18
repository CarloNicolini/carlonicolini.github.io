---
layout: post
title: Weighted graphs from adjacency matrix in graph-tool
categories: science
published: true
use_math: true
date: 2018-09-12

---
I was playing a bit with networks in Python. In my daily life I typically work with adjacency matrices, rather than other sparse formats for networks.
Adjacency matrix is pretty good for visualization of communities, as well as to give an idea of the distribution of edge weights.
It is exactly in the domain of weighted networks that I need to be able to fit stochastic block models to my observations.
Doing this requires the super-cool library of Tiago Peixoto [graph-tool](https://graph-tool.skewed.de).

The library works with Boost BGL library, hence graphs are stored as adjacency lists or edge lists, typically. 
In order to convert a `numpy.array` representing the adjacency matrix of a graph, hence a function that specifies the edges list together with their associated weights is necessary.

This function, that correctly handles the edge weights, in the variable `weight` is given in the following snippet. 

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

What I find most interesting with weighted networks, is that one can fit stochastic block models to these networks considering the distribution of edge weights.
This is the example of fitting a WSBM with exponentially distributed edge weights, with the results plotted:

{% highlight python %}
g = to_graph_tool(bct.binarize(bct.threshold_absolute(A[0:50,0:50],0.55)))
print(g.num_vertices(),g.num_edges())
state = gt.minimize_blockmodel_dl(g,state_args=dict(recs=[g.ep.weight],rec_types=["real-exponential"]))
print('Done')
state.draw()
{% endhighlight %}

I hope you enjoy this small snippet.
