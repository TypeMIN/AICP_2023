import networkx as nx

# Create a random bipartite graph
G = nx.bipartite.random_graph(5, 7, 0.5)

# Give the node color 0 or 1, representing red and blue
color = {node: 0 if node < 5 else 1 for node in G.nodes()}

def LPAb(G, labels):
    # Initialize labels and degree dicts
    degrees = dict(G.degree())

    # Find red and blue nodes
    red_nodes = [n for n in G.nodes() if G.nodes[n]['bipartite'] == 0]
    blue_nodes = [n for n in G.nodes() if G.nodes[n]['bipartite'] == 1]

    # Initialize K and D dicts
    K = {node: 0 for node in labels.values()}
    D = {node: 0 for node in labels.values()}

    # Calculate initial K and D values
    for u in red_nodes:
        K[labels[u]] += degrees[u]
    for v in blue_nodes:
        D[labels[v]] += degrees[v]

    m = G.number_of_edges()

    # Iterate until convergence
    while True:
        QB_before = sum((G.has_edge(u, v) - degrees[u]*degrees[v] / (m))*int(labels[u]==labels[v]) for u, v in G.edges()) / (m)

        # Update labels of blue nodes
        for v in blue_nodes:
            D[labels[v]] -= degrees[v]
            Nvg = {label: sum(int(labels[neighbor] == label) for neighbor in G.neighbors(v)) for label in set(labels.values())}
            labels[v] = max(Nvg.keys(), key=lambda g: Nvg[g] - degrees[v]*K.get(g, 0)/m)
            D[labels[v]] += degrees[v]

        # Update labels of red nodes
        for u in red_nodes:
            K[labels[u]] -= degrees[u]
            Nug = {label: sum(int(labels[neighbor] == label) for neighbor in G.neighbors(u)) for label in set(labels.values())}
            labels[u] = max(Nug.keys(), key=lambda g: Nug[g] - degrees[u]*D.get(g, 0)/m)
            K[labels[u]] += degrees[u]

        QB_after = sum((G.has_edge(u, v) - degrees[u]*degrees[v] / (m))*int(labels[u]==labels[v]) for u, v in G.edges()) / (m)

        if QB_after <= QB_before:
            break

    return labels


def Division(labels):
    # Initialize community sets
    communities = {}

    # Build community sets
    for node, label in labels.items():
        if label in communities:
            communities[label].add(node)
        else:
            communities[label] = {node}

    # Only return non-empty communities
    division = [community for community in communities.values() if community]

    return division

def calculate_delta_QB(G, t1, t2, labels, degrees, m):
    # Calculate the current bipartite modularity before the merge
    QB_before = sum((G.has_edge(u, v) - degrees[u]*degrees[v] / m)*int(labels[u]==labels[v]) for u, v in G.edges()) / m

    # Create a copy of labels and perform a hypothetical merge
    labels_copy = labels.copy()
    for node, label in labels_copy.items():
        if label == t2:
            labels_copy[node] = t1

    # Calculate the new bipartite modularity after the hypothetical merge
    QB_after = sum((G.has_edge(u, v) - degrees[u]*degrees[v] / m)*int(labels_copy[u]==labels_copy[v]) for u, v in G.edges()) / m

    # Calculate and return the change in modularity
    delta_QB = QB_after - QB_before
    return delta_QB

def LPAb_plus(G):
    red_nodes = [n for n in G.nodes() if G.nodes[n]['bipartite'] == 0]
    blue_nodes = [n for n in G.nodes() if G.nodes[n]['bipartite'] == 1]
    labels = {}
    unique_label = 0
    for u in red_nodes:
        labels[u] = unique_label
        unique_label += 1

    for v in blue_nodes:
        labels[v] = None

    degrees = dict(G.degree())
    m = G.number_of_edges()
    labels = LPAb(G, labels)
    # Get community division
    communities = Division(labels)
    while True:
        # Check modularity change for each pair of communities
        for i in range(len(communities) - 1):
            for j in range(i + 1, len(communities)):
                t1 = communities[i]
                t2 = communities[j]
                delta_QB = calculate_delta_QB(G, t1, t2, labels, degrees, m)

                if delta_QB > 0 and not any(
                        calculate_delta_QB(G, t1, t, labels, degrees, m) > delta_QB for t in communities if
                        t != t2) and not any(
                        calculate_delta_QB(G, t2, t, labels, degrees, m) > delta_QB for t in communities if t != t1):
                    # Merge t1 and t2
                    for node in t2:
                        labels[node] = labels[next(iter(t1))]  # Assign the label of an arbitrary node in t1

                    # Go back to phase 1
                    labels = LPAb(G, labels)

        new_communities = Division(labels)

        # Stop if the community division doesn't change
        if communities == new_communities:
            break
    print(labels)
    return new_communities

# Call the function
labels = LPAb_plus(G)

# Print the resulting labels
print("Community labels:", labels)