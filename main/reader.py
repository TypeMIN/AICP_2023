import networkx as nx
from itertools import chain
from networkx.algorithms import bipartite


def readEdgeList(fileName):
    #print(fileName)
    g1 = bipartite.read_edgelist(fileName)
    print("V=", g1.number_of_nodes(), "\tE=", g1.number_of_edges())
    return g1