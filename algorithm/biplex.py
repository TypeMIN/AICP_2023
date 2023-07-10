import networkx as nx
from itertools import combinations

def iMB_Basic(G, k, t, X, N_X, cand_p, cand_q):
    print(N_X)
    print(cand_p)

    # new_N_X = set()
    # new_cand_p = set()
    # new_cand_q = set()

    for u in cand_p:
        new_X = X.union({u})
        cand_p.remove(u)
        # new_N_X =
        # print(new_X)
        # print(cand_p)
        # iMB_Basic()


    # for u in list(cand_p):
    #     X_p = X.union({u})
    #     cand_p = cand_p.remove(u)
    #     cand_p_x_p = cand_p
    #     F_X_p = {v for v in F_X if G.degree(v) >= (len(X_p) - k)}
    #
    #     # Apply early stop strategy (Lemma 2)
    #     # Apply advanced node expansion (Lemma 4)
    #
    #     if len(X_p) >= t:
    #         # List all MBs here
    #         if len(F_X_p) >= t:
    #             for x in X_p:
    #                 G.add_node(x)
    #             for y in F_X_p:
    #                 G.add_node(y)
    #         # Apply pruning strategies (Lemma 3 and Lemma 6)
    #
    #     if len(X_p) + len(cand_p_x_p) >= t and len(F_X_p) >= t: #cand_p_x_p 얘를 어떻게 찾아야 되지?
    #
    #         iMB_Basic(G, k, t, X_p, cand_p_x_p, cand_q, F_X_p)
    #     cand_q = cand_q.union({u})
    return nx.connected_components(G)

def extract_number(s):
    return int(s[1:])

def run(G_, k, t): #t is threshold
    G = G_.copy()

    X = set()  # 이게 X에 해당하는 vertices, 처음에는 비어있음
    N_X = set(v for v, d in G.nodes(data = True) if d['bipartite'] == 1)  # 이게 Y에 해당하는 vertices, 처음에 모든 v로 채워둬야 됨
    cand_p = set(u for u, d in G.nodes(data = True) if d['bipartite'] == 0)  # X에 들어갈 수 있는 vertices, 처음에 모든 u로 채워둬야 됨
    cand_q = set()  # 이미 방문한 vertices

    N_X = sorted(N_X, key=extract_number)  #sorting vertices
    cand_p = sorted(cand_p, key=extract_number)

    # print(N_X)
    # print(cand_p)

    return iMB_Basic(G, k, t, X, N_X, cand_p, cand_q)



# G = nx.Graph()
# G.add_edge('A', 'B')
# G.add_edge('A', 'C')
# G.add_edge('C', 'D')
#
# G_retrun = run(G, 1, 1)
#
# print(G_retrun)


