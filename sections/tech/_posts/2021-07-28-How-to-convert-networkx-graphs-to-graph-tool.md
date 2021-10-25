---
layout: post
date: 2021-07-28
title: How to convert networkx graphs to graph-tool
---

# How to convert networkx graphs to graph-tool

This small function converts a `networkx` graph to a graph-tool compatible graph, preserving both the edge properties and node properties.

    {%highlight python%}
    def networkx_to_graph_tool(networkx_graph: nx.Graph) -> gt.Graph:
        """
        Converts a networkx graph to a graph-tool graph.
        """
        # Phase 0: Create a directed or undirected graph-tool Graph
        graph_tool_graph = gt.Graph(directed=networkx_graph.is_directed())

        # Add the Graph properties as "internal properties"
        for key, value in list(networkx_graph.graph.items()):
            # Convert the value and key into a type for graph-tool
            tname, value, key = get_prop_type(value, key)

            prop = graph_tool_graph.new_graph_property(tname)  # Create the PropertyMap

            graph_tool_graph.graph_properties[key] = prop  # Set the PropertyMap
            graph_tool_graph.graph_properties[key] = value  # Set the actual value

        # Phase 1: Add the vertex and edge property maps
        # Go through all nodes and edges and add seen properties
        # Add the node properties first
        nprops = set()  # cache keys to only add properties once
        for node, data in networkx_graph.nodes(data=True):

            # Go through all the properties if not seen and add them.
            for key, val in list(data.items()):
                if key in nprops:
                    continue  # Skip properties already added

                # Convert the value and key into a type for graph-tool
                tname, _, key = get_prop_type(val, key)

                prop = graph_tool_graph.new_vertex_property(tname)  # Create the PropertyMap
                graph_tool_graph.vertex_properties[key] = prop  # Set the PropertyMap

                # Add the key to the already seen properties
                nprops.add(key)

        # Also add the node id: in NetworkX a node can be any hashable type, but
        # in graph-tool node are defined as indices. So we capture any strings
        # in a special PropertyMap called 'id' -- modify as needed!
        graph_tool_graph.vertex_properties['id'] = graph_tool_graph.new_vertex_property('string')
        # Add the edge properties second
        eprops = set()  # cache keys to only add properties once
        for src, dst, data in networkx_graph.edges(data=True):
            # Go through all the edge properties if not seen and add them.
            for key, val in list(data.items()):
                if key in eprops: continue  # Skip properties already added
                # Convert the value and key into a type for graph-tool
                tname, _, key = get_prop_type(val, key)
                prop = graph_tool_graph.new_edge_property(tname)  # Create the PropertyMap
                graph_tool_graph.edge_properties[key] = prop  # Set the PropertyMap
                # Add the key to the already seen properties
                eprops.add(key)
        # Phase 2: Actually add all the nodes and vertices with their properties
        # Add the nodes
        vertices = {}  # vertex mapping for tracking edges later
        for node, data in networkx_graph.nodes(data=True):
            # Create the vertex and annotate for our edges later
            v = graph_tool_graph.add_vertex()
            vertices[node] = v
            # Set the vertex properties, not forgetting the id property
            data['id'] = str(node)
            for key, value in list(data.items()):
                graph_tool_graph.vp[key][v] = value  # vp is short for vertex_properties
        # Add the edges
        for src, dst, data in networkx_graph.edges(data=True):
            # Look up the vertex structs from our vertices mapping and add edge.
            e = graph_tool_graph.add_edge(vertices[src], vertices[dst])
            # Add the edge properties
            for key, value in list(data.items()):
                graph_tool_graph.ep[key][e] = value  # ep is short for edge_properties
        # Done, finally!
        return graph_tool_graph    }
    {%endhighlight%}

