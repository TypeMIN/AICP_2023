import networkx as nx
from collections import defaultdict
from networkx.algorithms import bipartite

def count_rectangles(G_):
    # c[e] keeps the number of rectangles in G counting e
    G = G_.copy()
    c = defaultdict(int)

    for edge in list(G.edges()):
        u, v = edge
        if G.nodes[u]['bipartite'] == 1:
            u, v = v, u

        v_prime = set(G.neighbors(u))
        u_prime = set(G.neighbors(v))
        v_prime.remove(v)
        u_prime.remove(u)
        for v_p in v_prime:
            for u_p in u_prime:
                if G.has_edge(u_p, v_p):
                    c[(u, v)] += 1
                    c[(u, v_p)] += 1
                    c[(u_p, v)] += 1
                    c[(u_p, v_p)] += 1
        G.remove_edge(u, v)
    return c

def run(G_, k):
    G = G_.copy()
    G_r = G_.copy()
    c = count_rectangles(G)
    # print(c)
    t = {}
    k_ = 0
    # bitruss number 계산
    while len(G.edges()) > 0:

        for edge in G.edges():
            u, v = edge
            if G.nodes[u]['bipartite'] == 1:
                u, v = v, u

            if c[(u, v)] <= k_:
                for v_prime in G.neighbors(u):
                    for u_prime in G.neighbors(v):
                        if G.has_edge(u_prime, v_prime) and u_prime != u and v_prime != v:
                            c[(u, v_prime)] -= 1
                            c[(u_prime, v)] -= 1
                            c[(u_prime, v_prime)] -= 1
                t[(u, v)] = k_
                G.remove_edge(u, v)
                break

        else:
            k_ += 1

    # k-bitruss subgraph 구성
    for edge in G_r.edges():
        u, v = edge
        if G_r.nodes[u]['bipartite'] == 1:
            u, v = v, u

        if t[(u, v)] < k:
            G_r.remove_edge(u, v)

    # edge 없는 node 삭제
    isolated_nodes = list(nx.isolates(G_r))
    G_r.remove_nodes_from(isolated_nodes)

    return nx.connected_components(G_r)