import networkx as nx
import random
from collections import Counter




def calculate_bipartite_modularity(G, labels):
    m = G.number_of_edges()
    modularity = 0.0
    for u in G.nodes():
        for v in G.nodes():
            if labels[u] == labels[v]: # Aij and nodes i and j in the same community
                modularity += G.has_edge(u, v) - (2*G.degree(u)*G.degree(v))/(m)
    modularity = modularity/(2*m)
    modularity = modularity*m
    return modularity


def LPAb(G):
    # print(G.nodes)
    for node in G.nodes():
        G.nodes[node]['bipartite'] = 0 if 'u' in node else 1
    red_nodes = [n for n in G.nodes() if G.nodes[n]['bipartite'] == 0]
    blue_nodes = [n for n in G.nodes() if G.nodes[n]['bipartite'] == 1]
    # Initialize with unique labels
    labels = {}
    unique_label = 0
    for u in red_nodes:
        labels[u] = unique_label
        unique_label += 1
    for v in blue_nodes:
        labels[v] = unique_label
        unique_label += 1
    # print(labels)
    nodes = list(G.nodes())
    while True:
        random.shuffle(nodes)
        new_labels = labels.copy()
        for node in nodes:
            best_label = labels[node]
            best_modularity = calculate_bipartite_modularity(G, new_labels)

            for v in G.neighbors(node):
                new_labels[node] = labels[v]
                new_modularity = calculate_bipartite_modularity(G, new_labels)

                if new_modularity > best_modularity:
                    best_label = labels[v]
                    best_modularity = new_modularity

            new_labels[node] = best_label
        if new_labels == labels:
            break

        labels = new_labels
    # print(labels)
    communities = {}
    for node, label in labels.items():
        if label in communities:
            communities[label].add(node)
        else:
            communities[label] = {node}

    # Only return non-empty communities
    communities = [community for community in communities.values() if community]
    return communities


# # create a random bipartite graph
# G = nx.bipartite.random_graph(5, 7, 0.5)
#
# # give the node color 0 or 1, representing red and blue
# color = {node: 0 if node < 5 else 1 for node in G.nodes()}
# print("Edges of G :", G.edges)
#
# labels = LPAb(G)
# print("Community labels:", labels)
#
# modularity = calculate_bipartite_modularity(G, labels)
# print("Bipartite Modularity:", modularity)
