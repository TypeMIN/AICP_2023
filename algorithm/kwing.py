import networkx as nx
from networkx.algorithms import bipartite

def run(G_, k):
    G = G_.copy()

    U, I = bipartite.sets(G)


