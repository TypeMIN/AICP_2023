import networkx as nx
import random


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
    # Initialize with unique labels
    labels = {i: i for i in G.nodes()}
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

    return labels


# create a random bipartite graph
G = nx.bipartite.random_graph(5, 7, 0.5)

# give the node color 0 or 1, representing red and blue
color = {node: 0 if node < 5 else 1 for node in G.nodes()}
print("Edges of G :", G.edges)

labels = LPAb(G)
print("Community labels:", labels)

modularity = calculate_bipartite_modularity(G, labels)
print("Bipartite Modularity:", modularity)
