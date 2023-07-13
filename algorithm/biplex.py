import networkx as nx
import itertools

def iMB_Basic(G, k, t, X, N_X, cand_p, cand_q):

    while(len(cand_p) != 0):
        u = cand_p[0]

        # print("u", u)
        # print("X", X)
        new_X = X.union({u})
        # print("new_X", new_X)
        cand_p.remove(u)

        new_cand_p = cand_p.copy()

        new_N_X = set()
        for v in N_X:
            neighbors_in_new_X = set(G.neighbors(v)).intersection(new_X)
            # print(neighbors_in_new_X)
            if len(neighbors_in_new_X) >= (len(new_X) - k):
                new_N_X.add(v)

        # print("new_N_X", new_N_X)
        # print("new_cand_p", new_cand_p)
        # Apply the early stop strategy (Lemma 2) 만약 cand_q 에 있는 u에 대해서 N_X가 u의 이웃들을 담은 set에 포함될 떄, expand stop
        for vertex in cand_q:
            if set(N_X).issubset(set(G.neighbors(vertex))):
                continue

        # Apply the advanced node expansion (Lemma 4)
        # for vertex in cand_p:
        #     if set(N_X).issubset(set(G.neighbors(vertex))):
        #         new_X = new_X.union(cand_p)
        #         cand_q.update(cand_p)
        #         cand_p.clear()


        if len(new_X) >= t:
            # List all bipartite subgraph make by new_X and y, y is subgraph of new_N_X and len(y) >= t

            if len(new_N_X) >= t:
                print("graph")
                print(new_X)
                print(new_N_X)

                # n = len(new_N_X)
                # subsets = []
                # for r in range(t, n + 1):
                #     subsets.extend(list(itertools.combinations(new_N_X, r)))
                # print(subsets)
            # Apply pruning strategies (Lemma 3 and Lemma 6)



        if len(new_X) + len(cand_p) >= t and len(new_N_X) >= t:
            # print("test")
            iMB_Basic(G, k, t, new_X, new_N_X, new_cand_p, cand_q)

        cand_q.add(u)
        # print(new_X)
        # print(cand_p)
        # print(new_N_X)
        # print(new_cand_p)
        # print(cand_q)
        # iMB_Basic()
    return nx.connected_components(G)

def coreprune(G_, k, t):
    G = G_.copy()
    #for each vertex in G, if degree of vertex is less than t - k, remove vertex
    for v in list(G_.nodes()):
        if G_.degree(v) < t - k:
            G.remove_node(v)
    return G

def extract_number(s):
    return int(s[1:])

def run(G_, k, t): #t is threshold
    G = coreprune(G_.copy(), k, t)
    #print a bipartite set of G
    print(nx.bipartite.sets(G))

    X = set()  # 이게 X에 해당하는 vertices, 처음에는 비어있음
    N_X = set(v for v, d in G.nodes(data=True) if d['bipartite'] == 1)  # 이게 Y에 해당하는 vertices, 처음에 모든 v로 채워둬야 됨
    cand_p = set(u for u, d in G.nodes(data=True) if d['bipartite'] == 0)  # X에 들어갈 수 있는 vertices, 처음에 모든 u로 채워둬야 됨
    cand_q = set()  # 이미 방문한 vertices

    N_X = sorted(N_X, key=extract_number)  #sorting vertices
    cand_p = sorted(cand_p, key=extract_number)

    return iMB_Basic(G, k, t, X, N_X, cand_p, cand_q)


