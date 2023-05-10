import networkx as nx
from networkx.algorithms import bipartite
from coclust.coclustering import CoclustMod

# Algorithms in  Ding, D., Li, H., Huang, Z., Mamoulis, N.: Efficient fault-tolerant group recommendation using alpha–beta–core. In: Proceedings of CIKM, pp 2047–2050 (2017)
# Time Complexity : O(|E|)
# https://dl.acm.org/doi/pdf/10.1145/3132847.3133130

def run(G_, n):
    G = G_.copy()

    U, I = bipartite.sets(G)
    data = bipartite.biadjacency_matrix(G, row_order=U)

    model = CoclustMod(n_clusters=n)
    model.fit(data)

    print(model.modularity)

    connected_components = []
    for cluster in range(n):
        connected_components.append(np.where(model.row_labels_ == cluster)[0])

    return nx.connected_components(G)
