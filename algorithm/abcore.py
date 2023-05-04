import networkx as nx
from networkx.algorithms import bipartite

# Algorithms in  Ding, D., Li, H., Huang, Z., Mamoulis, N.: Efficient fault-tolerant group recommendation using alpha–beta–core. In: Proceedings of CIKM, pp 2047–2050 (2017)
# Time Complexity : O(|E|)
# https://dl.acm.org/doi/pdf/10.1145/3132847.3133130

def run(G_, a, b):
    G = G_.copy()

    U, I = bipartite.sets(G)

    while True :
        changed = False
        remover = set()
        for u in U:
            if G.degree(u) < a:
                G.remove_node(u)
                changed = True
                remover.add(u)

        U = U - remover
        remover = set()
        for v in I:
            if G.degree(v) < b:
                G.remove_node(v)
                changed = True
                remover.add(v)
        I = I - remover
        if changed is False :
            break

    return nx.connected_components(G)
