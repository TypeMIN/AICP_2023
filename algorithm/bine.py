import networkx as nx
from networkx.algorithms import bipartite
import algorithm.bine_helper.train
from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter
import argparse
from collections import defaultdict


def run(G, data_path):

    args = argparse.Namespace()
    args.train_data = data_path
    args.test_data = r'../dataset/bine_test.dat'
    args.model_name = r'bine'
    args.vectors_u = r'../dataset/bine_vectors_u.dat'
    args.vectors_v = r'../dataset/bine_vectors_v.dat'
    args.case_train = r'../data/wiki/case_train.dat'
    args.case_test = r'../data/wiki/case_test.dat'
    args.ws = 5
    args.ns = 4
    args.d = 128
    args.maxT = 32
    args.minT = 1
    args.p = 0.15
    args.alpha = 0.01
    args.beta = 0.01
    args.gamma = 0.1
    args.lam = 0.01
    args.max_iter = 50
    args.top_n = 10
    args.rec = 0
    args.lip = 0
    args.large = 0
    args.mode = 'hits'

    result = algorithm.bine_helper.train.train_by_sampling(args)
    print("\nresult:",result)
    nodes = sorted(G.nodes())

    # Create a graph in which only nodes belonging to the same cluster are connected. (except -1)
    # test case: result = [0, 0, 1, 1, 0, 1, -1, -1, 1, 2, 3, 3, 2, 0, 1, 2]
    cluster_dict = defaultdict(list)
    for node, cluster in zip(nodes, result):
        cluster_dict[cluster].append(node)

    G = nx.Graph()

    for cluster, nodes_in_cluster in cluster_dict.items():
        if cluster == -1:
            continue
        for i in range(len(nodes_in_cluster)):
            for j in range(i + 1, len(nodes_in_cluster)):
                G.add_edge(nodes_in_cluster[i], nodes_in_cluster[j])

    return nx.connected_components(G)
