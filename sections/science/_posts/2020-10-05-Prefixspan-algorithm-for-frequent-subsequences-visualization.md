---
title: Prefixspan algorithm for frequent subsequences visualization
date: 2020-10-05
layout: post
categories: science
published: false
---

# Prefixspan and subsequences

    {%highlight python %}
    from typing import List, Tuple
    import networkx as nx
    import json
    import ast

    class PatternVisualization(object):

        def __init__(self, patterns: List[Tuple]):
            self.patterns = patterns

        def to_json_tree(self):

            def dfs_rename(json_tree):
                """
                This function performs a depth first search, replacing the key id
                with the key name and only keeping the last element in the list.
                It also keep the last element for the 'parent' key.
                :param json_tree:
                :return:
                """
                id_key = ast.literal_eval(json_tree['id'])
                if not id_key:
                    json_tree['name'] = '[]'
                else:
                    json_tree['name'] = str(id_key[-1])
                if json_tree['parent'] != 'null':
                    if ast.literal_eval(json_tree['parent']):
                        json_tree['parent'] = str(ast.literal_eval(json_tree['parent'])[-1])
                json_tree.pop('id', None)  # removes the key id
                if 'children' not in json_tree:
                    return None
                for c in json_tree['children']:
                    result = dfs_rename(c) # recursive solution
                    if result is not None:
                        return result
                return None

            tree = self._create_tree()
            json_tree_data = nx.tree_data(tree, root='[]')

            dfs_rename(json_tree_data)
            return json_tree_data

        def _create_tree(self):
            tree = nx.DiGraph()
            edges = []
            all_samples = []
            maxfreq = -1
            tree.add_node('[]', parent='null')
            for freq, sample in self.patterns:
                maxfreq = max(freq, maxfreq)
            for freq, sample in self.patterns:
                for j in range(len(sample)):
                    src = f'{sample[:j]}'
                    dst = f'{sample[:j+1]}'
                    all_samples.append(sample)
                    if (src, src) not in tree.edges() and (src, dst) not in edges and sample in all_samples:
                        if dst == str(sample): # it's a terminal node
                            tree.add_node(dst, parent=src, size=freq)
                        else: # has children
                            tree.add_node(dst, parent=src)
                        tree.add_edge(src, dst)

            return tree

        def dump_json_tree_data(self, filename):
            json.dump(self.to_json_tree(), open(filename, 'w'))



    if __name__ == '__main__':

        patterns = [(6, [10, 10, 4]),
                    (6, [6, 5, 5, 6, 6]),
                    (7, [375, 374, 374, 375]),
                    (7, [5, 6, 6, 5]),
                    (7, [5, 6, 5, 5]),
                    (8, [10, 6, 5, 6]),
                    (8, [6, 5, 5, 6]),
                    (9, [5, 5, 4]),
                    (11, [375, 374, 374]),
                    (12, [10, 6, 5]),
                    (13, [10, 5, 6]),
                    (13, [6, 5, 6, 6]),
                    (13, [6, 6, 5, 5]),
                    (15, [5, 6, 5]),
                    (15, [5, 5, 6, 6]),
                    (17, [119, 119, 195]),
                    (20, [6, 5, 5]),
                    (25, [5, 5, 6]),
                    (26, [6, 6, 5]),
                    (28, [5, 6, 6]),
                    (36, [6, 5, 6]),
                    (44, [10, 10, 6, 6]),
                    (47, [374, 374, 375]),
                    (49, [374, 375, 374]),
                    (50, [375, 374, 375]),
                    (103, [10, 10, 6]),
                    (114, [10, 6, 6])]

        PatternVisualization(patterns).dump_json_tree_data('tree/tree2.json')
    {% endhighlight %}
