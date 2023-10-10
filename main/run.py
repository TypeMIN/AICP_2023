import argparse
import networkx as nx
import os
import time
import sys
import reader
import measure
import numpy as np
# from scipy.sparse import coo_matrix

sys.path.append("..")

import algorithm.abcore
import algorithm.ktip
import algorithm.kwing
import algorithm.bitruss
import algorithm.bine
#import algorithm.deepcc
import algorithm.biplex
import algorithm.bilouvain
import algorithm.LPAb
import algorithm.LPAb_Plus
import algorithm.spec

sys.setrecursionlimit(10000)


def get_base(file_path):
    path = os.path.dirname(file_path)
    return path + "/"


def get_user_param(args_set, _alg):
    ret = dict()

    if _alg == 'abcore':
        ret['a'] = args_set.a
        ret['b'] = args_set.b

    elif _alg == 'ktip':
        ret['k'] = args_set.k

    elif _alg == 'kwing':
        ret['k'] = args_set.k

    elif _alg == 'bitruss':
        ret['k'] = args_set.k

    elif _alg == 'biplex':
        ret['k'] = args_set.k
        ret['t'] = args_set.t

    elif _alg == "biLouvain":
        ret['k'] = args_set.k

    elif _alg == "spec":
        ret['c'] = args_set.c
    return ret


#############################################################################
parser = argparse.ArgumentParser(description='value k')
parser.add_argument('--a', type=int, default=3,
                    help='user parameter for abcore')

parser.add_argument('--b', type=int, default=3,
                    help='user parameter for abcore')

parser.add_argument('--c', type=int, default=3,
                    help='user parameter for spec')

parser.add_argument('--k', type=int, default=2, help='user parameter for ktip, kwing, bitruss or biplex')

parser.add_argument('--t', type=int, default=1, help='user parameter for k-biplex')

parser.add_argument('--network', default="../dataset/bnoc/bnoc1.txt",
                    help='a folder name containing network.dat')

parser.add_argument('--algorithm', default="abcore",
                    help='specify algorithm name')

args = parser.parse_args()
print("network ", args.network)
print("algorithm ", args.algorithm)

user_params = get_user_param(args, args.algorithm)

output = "../result/"
output = output + args.network.split("/")[-1].split(".")[0] + "_"
output = output + args.algorithm
for key in user_params.keys():
    print("params ", key, user_params[key])
    output = output + "_" + str(key) + "_" + str(user_params[key])
output = output + ".dat"
print("output", output)

#############################################################################
#############################################################################

#############################################################################
# Global Parameter
G = None
C = None
X = None
#############################################################################
# read network
if args.algorithm == 'spec':
    with open(args.network, "r") as f:
        lines = f.readlines()
    edges = [tuple(line.strip().split()) for line in lines]

    u_nodes = sorted(list(set([edge[0] for edge in edges])))
    v_nodes = sorted(list(set([edge[1] for edge in edges])))

    u_mapping = {node: index for index, node in enumerate(u_nodes)}
    v_mapping = {node: index for index, node in enumerate(v_nodes)}

    matrix = np.zeros((len(u_nodes), len(v_nodes)))

    for edge in edges:
        u_index = u_mapping[edge[0]]
        v_index = v_mapping[edge[1]]
        matrix[u_index][v_index] = 1

    X = matrix

G = reader.readEdgeList(args.network)
G.remove_edges_from(nx.selfloop_edges(G))
G.remove_nodes_from(list(nx.isolates(G)))
print(G)
#############################################################################

start_time = time.time()

if args.algorithm == 'abcore':
    C = algorithm.abcore.run(G, args.a, args.b)

elif args.algorithm == 'ktip':
    C = algorithm.ktip.run(G, args.k)

elif args.algorithm == 'kwing':
    C = algorithm.kwing.run(G, args.k)

elif args.algorithm == 'bitruss':
    C = algorithm.bitruss.run(G, args.k)

elif args.algorithm == 'bine':
    import algorithm.bine
    C = algorithm.bine.run(G, args.network)
    print("")

elif args.algorithm == 'deepcc':
    import algorithm.deepcc
    C = algorithm.deepcc.run(G)

elif args.algorithm == 'biplex':
    C = algorithm.biplex.run(G, args.k, args.t)

elif args.algorithm == 'biLouvain':
    C = algorithm.bilouvain.run(args.network)

elif args.algorithm == "spec":
    C = algorithm.spec.run(G, X, args.c)

elif args.algorithm == 'LPAb':
    C = algorithm.LPAb.LPAb(G)

elif args.algorithm == 'LPAb_Plus':
    C = algorithm.LPAb_Plus.LPAb_plus(G)

run_time = time.time() - start_time

if args.algorithm == 'biLouvain':
    pass
elif args.algorithm == "spec":
    print('running time', run_time)
    U_max = max(list(C.row_labels_))
    V_max = max(list(C.column_labels_))
    total_max = max(U_max, V_max)
    # vertex_density, edge_density, graph_density, barbers_modularity = measure.get_evaluation(G, C)
    with open(output, 'w') as f:
        # f.write("vertex_density" + "\t" + str(vertex_density) + '\n')
        # f.write("edge_density" + "\t" + str(edge_density) + '\n')
        # f.write("graph_density" + "\t" + str(graph_density) + '\n')
        # f.write("barbers_modularity" + "\t" + str(barbers_modularity) + '\n')
        f.write("seconds" + "\t" + str(run_time) + '\n' +'\n')
        print("----------------------------------------------------------")
        for i in range(total_max+1):
            U_matching = ["u" + str(j+1) for j, value in enumerate(list(C.row_labels_)) if value == i]
            V_matching = ["v" + str(j+1) for j, value in enumerate(list(C.column_labels_)) if value == i]
            total_matching = U_matching + V_matching
            result = " ".join(total_matching)
            # remove nodes which are not in the matching from G
            G_copy = G.copy()
            G_copy.remove_nodes_from([node for node in G.nodes() if node not in total_matching])
            print(G_copy)
            # # vertex density
            # U, V = nx.bipartite.sets(G)
            # E = G.number_of_edges()
            # vertex_density = E / (len(U) * len(V)) ** (1 / 2)
            # # edge density
            # E = G.number_of_edges()
            # edge_density = E / (len(U) + len(V))
            # # graph density
            # E = G.number_of_edges()
            # graph_density = E / (len(U) * len(V))
            # # barbers modularity
            # barbers_modularity = measure.get_barbers_modularity(G, [list(G.nodes())])
            # print(vertex_density, edge_density, graph_density, barbers_modularity)
            print(result)
            f.write(result + '\n')
        print("----------------------------------------------------------")
    f.close()
else :
    print('running time', run_time)

    result = list()
    if C is not None:
        result = list(C)
    print("----------------------------------------------------------")
    for comp in result:
        comp = sorted(comp, reverse=False)
        for u in list(comp):
            print(u, ' ', end="")
        print("")
    print("----------------------------------------------------------")

    size, num = measure.get_result(G, result)
    print("resultant_statistic ", run_time, size, num)

    vertex_density, edge_density, graph_density, barbers_modularity = measure.get_evaluation(G, result)
    with open(output, 'w') as f:
        f.write("vertex_density" + "\t" + str(vertex_density) + '\n')
        f.write("edge_density" + "\t" + str(edge_density) + '\n')
        f.write("graph_density" + "\t" + str(graph_density) + '\n')
        f.write("barbers_modularity" + "\t" + str(barbers_modularity) + '\n')
        f.write("seconds" + "\t" + str(run_time) + '\n')
        f.write("size" + "\t" + str(size) + '\n')
        f.write("num" + "\t" + str(num) + '\n')

        for comp in result:
           # comp = [int(x) for x in comp]
            comp = sorted(comp, reverse=False)
            for u in list(comp):
                f.write(str(u) + " ")
            f.write("\n")

    f.close()

