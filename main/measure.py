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
    density_list = []
    S = [G.subgraph(c).copy() for c in C]
    for s in S:
        U, V = nx.bipartite.sets(s)
        E = s.number_of_edges()
        density_list.append(E/(len(U)*len(V))**(1/2))
    density = sum(density_list) / len(density_list)
    return density

def get_edge_density(G, C):
    density_list = []
    S = [G.subgraph(c).copy() for c in C]
    for s in S:
        U, V = nx.bipartite.sets(s)
        E = s.number_of_edges()
        density_list.append(E/(len(U)+len(V)))
    density = sum(density_list) / len(density_list)
    return density
def get_graph_density(G, C):
    density_list = []
    S = [G.subgraph(c).copy() for c in C]
    for s in S:
        U, V = nx.bipartite.sets(s)
        E = s.number_of_edges()
        density_list.append(E/(len(U)*len(V)))
    density = sum(density_list) / len(density_list)
    return density

def get_barbers_modularity(G, C):
    modularity_list = []
    n = G.number_of_nodes()
    m = G.number_of_edges()
    S = [G.subgraph(c).copy() for c in C]
    for s in S:
        U, V = nx.bipartite.sets(s)
        R_c = len(U)
        B_C = len(V)
        m_c = s.number_of_edges()
        modularity_list.append((m_c/m) - (R_c * B_C)/(m**2))
    modularity = sum(modularity_list) / len(modularity_list)
    return modularity