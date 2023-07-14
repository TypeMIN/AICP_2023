import networkx as nx

def iMB_Basic(G, k, t, X, N_X, cand_p, cand_q):

    while(len(cand_p) != 0):
        u = cand_p[0]
        new_X = X.union({u})
        cand_p.remove(u)
        new_cand_p = cand_p.copy()
        new_N_X = set()

        for v in N_X:
            count = 0
            for neighbor in G.neighbors(v):
                if neighbor in new_X:
                    count = count + 1
            if count >= (len(new_X) - k) and count > 0: #  count > 0 인 조건을 넣어야 하나? len(new_X) - k 가 음수로 가면 new_N_X가 이상해진다.
                new_N_X.add(v)

        # Apply the early stop strategy (Lemma 2)
        for vertex in cand_q:
            if set(N_X).issubset(set(G.neighbors(vertex))):
                print("early stop")
                cand_q = cand_q.union(new_cand_p)
                new_cand_p.clear()
                break

        # Apply the advanced node expansion (Lemma 4)
        for vertex in new_cand_p:
            if set(new_N_X).issubset(set(G.neighbors(vertex))):
                print("advanced node expansion")
                new_X.add(vertex)
                # cand_q.add(vertex) # 이거 넣어야 하나?
                new_cand_p.remove(vertex)
                # break

        if len(new_X) >= t:
            # List all bipartite subgraph make by new_X and y, y is subgraph of new_N_X and len(y) >= t
            if len(new_N_X) >= t:
                # print("graph")
                print(new_X)
                print(new_N_X)
            # Apply pruning strategies (Lemma 3 and Lemma 6)
            # Lemma 3 about new_N_X
            # Lemma 6 about new_cand_p

        if len(new_X) + len(new_cand_p) >= t and len(new_N_X) >= t:
            iMB_Basic(G, k, t, new_X, new_N_X, new_cand_p, cand_q)

        cand_q.add(u)

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

    X = set()  # 이게 X에 해당하는 vertices, 처음에는 비어있음
    N_X = set(v for v, d in G.nodes(data=True) if d['bipartite'] == 1)  # 이게 Y에 해당하는 vertices, 처음에 모든 v로 채워둬야 됨
    cand_p = set(u for u, d in G.nodes(data=True) if d['bipartite'] == 0)  # X에 들어갈 수 있는 vertices, 처음에 모든 u로 채워둬야 됨
    cand_q = set()  # 이미 방문한 vertices

    N_X = sorted(N_X, key=extract_number)  #sorting vertices
    cand_p = sorted(cand_p, key=extract_number)

    iMB_Basic(G, k, t, X, N_X, cand_p, cand_q)

    return nx.connected_components(G)


