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
def to_graph_tool_slow(adj):
    g = gt.Graph(directed=False)
    edge_weights = g.new_edge_property('double')
    g.edge_properties['weight'] = edge_weights
    num_vertices = len(adj)
    for i in range(0,num_vertices):
        for j in range(i+1,num_vertices):
            if adj[i,j]!=0:
                e = g.add_edge(i,j)
                edge_weights[e] = adj[i,j]
    return g
{% endhighlight %}

Unfortunately here, speaking about performances, the doubly nested for loop is not a great idea.
Moreover,  it is clear here that one is trying to add links with their specific weight by considering them in a double nested for loop, which can be expensive to evaluate.
Unfortunately at the moment the following the indication from [stackoverflow](https://stackoverflow.com/questions/23288661/create-a-weighted-graph-from-an-adjacency-matrix-in-graph-tool-python-interface) does not seem to work correctly.

However I worked out a correct implementation for **undirected, weighted** networks, that works pretty well.
The implementation is the following: it is using the *add_edge_list* method, exploiting `numpy.nonzero` method.

{% highlight python %}
def to_graph_tool(adj):
    g = gt.Graph(directed=False)
    edge_weights = g.new_edge_property('double')
    g.edge_properties['weight'] = edge_weights
    nnz = np.nonzero(np.triu(adj,1))
    nedges = len(nnz[0])
    g.add_edge_list(np.hstack([np.transpose(nnz),np.reshape(adj[nnz],(nedges,1))]),eprops=[edge_weights])
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
