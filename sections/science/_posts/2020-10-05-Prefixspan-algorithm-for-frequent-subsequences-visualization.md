---
title: Prefixspan algorithm for frequent subsequences visualization
date: 2020-10-05
layout: post
categories: science
published: true
---

## Sequential pattern mining and projections

In the study of discrete sequence data, one of the fundamental tasks is identifying recurrent subsequences. While classical methods rely on candidate generation, the PrefixSpan algorithm (Prefix-projected Sequential pattern mining) introduces a profoundly different, pattern-growth approach.

After working with this algorithm for visualizing frequent sequences, I think the sharpest way to state its advantage is the following:

> PrefixSpan is a recursive approximation of the full pattern space via database projections.

The central object of PrefixSpan is the **projected database**.

What does this mean in practice?
A sequential miner does not answer from a single monolithic law.
It first identifies frequent individual items, uses them as prefixes, and then reshapes the remaining search space by projecting the database relative to each prefix.

To make the rest precise, let us start from the basic sequential objects.
Fix a sequence database $\mathcal{D}$, an alphabet of items $\Sigma$, and a minimum support threshold $\theta$.
A sequence is defined as an ordered list of itemsets $s = \langle e_1, e_2, \ldots, e_n \rangle$, where each $e_i \subseteq \Sigma$.
The semantic target is to find all frequent subsequences $\alpha$, such that

\begin{equation}
\mathrm{supp}(\alpha, \mathcal{D}) = \sum_{s \in \mathcal{D}} \mathbf{1}\{\alpha \sqsubseteq s\} \ge \theta.
\end{equation}

where $\alpha \sqsubseteq s$ denotes that $\alpha$ is a subsequence of $s$.

Now we define the $\alpha$-projected database:

\begin{equation}
\mathcal{D}_\alpha := \{ s' \mid s \in \mathcal{D}, s = \alpha \cdot s' \}.
\end{equation}

Then the recursive step becomes

$$
\mathrm{supp}(\alpha \cdot \beta, \mathcal{D})
=
\mathrm{supp}(\beta, \mathcal{D}_\alpha).
$$

This is exactly the divide-and-conquer form that makes PrefixSpan so efficient.

So the projected database is not merely a "filtered" version of the original database.
It is the exact conditional distribution of suffixes, given the prefix $\alpha$.
And the recursive search is not merely a heuristic.
It is an exhaustive traversal of the suffix space.

The central intractable object that any sequential pattern miner is implicitly working with is the full combinatorial space of all possible subsequences:

$$
\mathcal{S} = \bigcup_{k=1}^\infty \Sigma^k,
$$

or, more precisely, the subset of $\mathcal{S}$ satisfying the support constraint.
Any pattern-growth technique is trying to prune it efficiently.

This is the core conceptual jump from Apriori-style candidate generation to pattern growth.
When we deploy PrefixSpan, we are not invoking a mysterious faculty of combinatorial enumeration.
We are lazily evaluating a prefix tree over future subsequences that the raw database cannot cheaply marginalize in one forward pass.

## The prefix is the reference measure

This exact rewriting clarifies the relation between the sequences and their visualization.

At search time, one tries to distill the frequent sequences directly into a flat list.
At visualization time, we keep the prefix structure fixed and approximate the same generative target procedurally by branching, nesting, and aggregating.

The two views are therefore not competing stories.
They are two computational routes toward the same structured knowledge.

One route is:

$$
\text{scan the database so that we find all } \alpha \text{ where } \mathrm{supp}(\alpha, \mathcal{D}) \ge \theta.
$$

The other is:

$$
\text{keep the prefix } \alpha \text{ as the root and visualize the valid suffixes as children}.
$$

This makes the scope of our visualization much clearer.
It is the structural representation of what happens when the prefix space is known only through a list of frequent sequences.

## Visualizing the Prefix Tree

Whenever we score a partial chain of items, we are not really trying to estimate "local frequency" in isolation.
We are trying to estimate how much **future sequence mass** remains reachable from that prefix.

That is why simple flat lists are often useless for analyzing complex sequence data.
A prefix can look frequent and still lead into a dead end.
Conversely, a specific prefix can be extremely valuable if it opens a broad basin of frequent continuations.

In this sense, mapping PrefixSpan results into a directed graph is best understood as a runtime surrogate for continuation frequency.
The tree data structure provides a clear, hierarchical view of the prefixes and their valid suffixes.

<figure>
  <img src="/static/postfigures/local_decision.svg" alt="Local prefix plus continuation frequency" style="width:70%; display:block; margin: 0 auto; margin-bottom: 0.5em;"/>
  <figcaption>
    <strong>Figure 1.</strong> A local prefix only becomes meaningful once it is augmented by the frequency of its downstream subtree. The practical role of visualization is to estimate that future sequence mass better than a flat list can.
  </figcaption>
</figure>

This suggests that we should ask a very concrete question:

> How good is this data structure as a representation of continuation frequency?

That framing immediately gives us something measurable, comparable, and optimizable. To implement this, we can translate the flat outputs of a PrefixSpan algorithm into a structured JSON tree using `networkx`.

## The code implementation

To transform the frequent patterns into a visualization-ready format, we map the list of tuples `(frequency, sequence)` into a directed graph, and then export it.

{% highlight python %}
import networkx as nx
import json
import ast

class PatternVisualization:

    def __init__(self, patterns: list[tuple]):
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

## The big picture

The sharpest version of the story is now the following.

Algorithms like PrefixSpan can behave as if they explore the entire combinatorial space only because their local projections already contain a compressed summary of the future valid suffixes.
When we wish to visualize this structure, prefix trees step in: the directed hierarchy they inject helps to visually approximate the suffix distributions by explicitly revealing the branching paths.

This is why the right question is not merely "what are the frequent sequences?"
The right question is:

> Which visualization procedure best approximates the conditional frequency of future sequences under a hierarchical prefix structure?

That, to me, is the real systems interpretation of sequential pattern mining visualizations.
