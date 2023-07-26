import networkx as nx
import itertools

# G is bipartite graph, k is biplex number, t is threshold, X is current node, N_X is extention set, cand_p is candidate of vertices in X, cand_q is vertices already visited
# new_X is X`, new_N_X is extention set of X`, new_cand_p is cand_p(X`), new_cand_q is cand_q(X`)
def iMB_Basic(G, k, t, X, N_X, cand_p, cand_q, total_graph):
    while (len(cand_p) > 0):
        u = cand_p.pop(0)
        new_X = X.copy()
        new_X.append(u)
        new_cand_p = cand_p.copy()

        # make new_N_X
        new_N_X = list()
        for v in N_X:
            count = 0
            for vertex in G.neighbors(v):
                if vertex in new_X:
                    count += 1
            if count >= len(new_X) - k:
                new_N_X.append(v)
        # Apply the early stop strategy


        # Apply the advanced node expansion strategy


        if len(new_X) >= t:
            combo = combinations(new_N_X, t)
            tem_X = list()
            tem_N_X = list()
            maximum_N_X = 0
            for N_X_ in combo:
                # maximum_X = 0
                test = True
                for vertex_u in new_X:
                    count = 0
                    for vertex_v in G.neighbors(vertex_u):
                        if vertex_v in N_X_:
                            count += 1
                    if count < len(N_X_) - k:
                        test = False
                if test:
                    if len(N_X_) > maximum_N_X:
                        maximum_N_X = len(N_X_)
                        tem_X = new_X.copy()
                        tem_N_X = N_X_.copy()
                    # list all MBs

            tem_G = G.copy()
            node_to_remove = list()
            for node in tem_G.nodes():
                if node not in tem_X and node not in tem_N_X:
                    node_to_remove.append(node)

            tem_G.remove_nodes_from(node_to_remove)

            if len(total_graph) == 0:
                total_graph.append(tem_G)
            else:
                test2 = True
                for graph in total_graph:
                    if is_subgraph(graph, tem_G) or is_subgraph(tem_G, graph): #graph가 tem_G의 sub
                        test2 = False
                        if len(graph.nodes) < len(tem_G.nodes):
                            total_graph.remove(graph)
                            total_graph.append(tem_G)
                        break
                if test2:
                    total_graph.append(tem_G)

        if len(new_X) + len(new_cand_p) >= t and len(new_N_X) >= t:
            new_cand_q = cand_q.copy()
            iMB_Basic(G, k, t, new_X, new_N_X, new_cand_p, new_cand_q, total_graph)

        cand_q.append(u)

def is_subgraph(S, G): #S is subgraph of G
    if set(list(S.nodes)).issubset(list(G.nodes)) and set(list(S.edges)).issubset(list(G.edges)):
        return True
    return False
def combinations(lst, t):
    combos = []
    for r in range(t, len(lst) + 1):
        combos.extend(list(combo) for combo in itertools.combinations(lst, r))
    return combos

def coreprune(G_, k, t):
    G = G_.copy()
    for v in list(G_.nodes()):
        if G_.degree(v) < t - k:
            G.remove_node(v)
    return G

def extract_number(s):
    return int(s[1:])

def run(G_, k, t): #  t is threshold
    G = coreprune(G_.copy(), k, t)

    print(nx.bipartite.sets(G))

    X, N_X, cand_p, cand_q = list(), list(), list(), list()

    N_X = list(v for v, d in G.nodes(data=True) if d['bipartite'] == 1)
    cand_p = list(u for u, d in G.nodes(data=True) if d['bipartite'] == 0)

    N_X = sorted(N_X, key=extract_number)  #sorting vertices
    cand_p = sorted(cand_p, key=extract_number)

    total_graph = list()
    # total_graph.append(G)

    iMB_Basic(G, k, t, X, N_X, cand_p, cand_q, total_graph)

    return total_graph


