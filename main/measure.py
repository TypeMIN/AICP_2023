import networkx as nx

def get_result(G, C):
    return get_average_size(G, C), get_number_of_cc(G, C)

def get_evaluation(G, C):
    return get_vertex_density(G, C), get_edge_density(G, C), get_graph_density(G, C), get_barbers_modularity(G, C)

def get_average_size(G, C):

    nodeCnt = 0
    E = G.number_of_edges()
    V = G.number_of_nodes()
    cnum = len(C)
    csum = 0
    for c in C:
        csum += len(c)
    if cnum == 0:
        return 0
    return csum/cnum

def get_number_of_cc(G, C):
    return len(C)

def get_vertex_density(G, C):
    density = []
    S = [G.subgraph(c).copy() for c in C]
    for s in S:
        U, V = nx.bipartite.sets(s)
        E = s.number_of_edges()
        density.append(E/(len(U)*len(V))**(1/2))
    return density

def get_edge_density(G, C):
    density = []
    S = [G.subgraph(c).copy() for c in C]
    for s in S:
        U, V = nx.bipartite.sets(s)
        E = s.number_of_edges()
        density.append(E/(len(U)+len(V)))
    return density
def get_graph_density(G, C):
    density = []
    S = [G.subgraph(c).copy() for c in C]
    for s in S:
        U, V = nx.bipartite.sets(s)
        E = s.number_of_edges()
        density.append(E/(len(U)*len(V)))
    return density

def get_barbers_modularity(G, C):
    density = 0
    return density