import networkx as nx
from networkx.algorithms import bipartite
from collections import defaultdict
import math

def D2(u, G):
    D = []
    c = defaultdict(int)

    d1 = G.neighbors(u)
    for neighbor1 in d1:
        d2 = G.neighbors(neighbor1)
        for neighbor2 in d2:
            if neighbor2 is not u:
                c[neighbor2] += 1
                if neighbor2 not in D:
                    D.append(neighbor2)
    return c, D

def run(G_, k):
    G = G_.copy()

    I, U = bipartite.sets(G)
    B = defaultdict(int)
    T = defaultdict(int)

    for u in U:
        c, D = D2(u, G)
        bnum = 0
        for count in c.values():
            bnum += math.comb(count, 2)
        B[u] = bnum

    for _ in range(len(B)):
        u = min(B, key=lambda k: B[k])
        T[u] = B[u]
        c, D = D2(u, G)
        for d in D:
            if d not in T:
                if B[d] - math.comb(c[d], 2) < B[u]:
                    B[d] = B[u]
                else:
                    B[d] = B[d] - math.comb(c[d], 2)
        del B[u]

    remover = set()
    for key, value in T.items():
        if value < k:
            remover.add(key)
            G.remove_node(key)
    U = U - remover

    connected_nodes = set()
    for u in U:
        connected_nodes.update(G.neighbors(u))

    remover = set()
    for v in I:
        if v not in connected_nodes:
            remover.add(v)
            G.remove_node(v)
    I = I - remover

    return nx.connected_components(G)
