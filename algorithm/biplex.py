import networkx as nx
from itertools import combinations

def iMB_Basic(G, k, t, X, N_X, cand_p, cand_q):

    while(len(cand_p) != 0):
        u = cand_p[0]
        expand = True

        new_X = X.union({u})
        cand_p.remove(u)
        new_N_X = {v for v in N_X if G.degree(v) >= (len(cand_p) - k)}
        new_cand_p = cand_p
        # Apply the early stop strategy (Lemma 2) 만약 cand_q 에 있는 u에 대해서 N_X가 u의 이웃들을 담은 set에 포함될 떄, expand stop
        for vertex in cand_q:
            if N_X.issubset(set(G.neighbors(vertex))):
                expand = False

        # Apply the advanced node expansion (Lemma 4)

        if len(new_X) >= t:
            # List all MBs
            if len(new_N_X) >= t:
                print(new_X)
                print(new_N_X)
            # Apply pruning strategies (Lemma 3 and Lemma 6)

        if len(new_X) + len(cand_p) >= t and len(new_N_X) >= t and expand:
            # print("test")
            iMB_Basic(G, k, t, new_X, new_N_X, new_cand_p, cand_q)

        cand_q.union({u})
        # print(new_X)
        # print(cand_p)
        # print(new_N_X)
        # print(new_cand_p)
        # iMB_Basic()



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

    return iMB_Basic(G, k, t, X, N_X, cand_p, cand_q)


