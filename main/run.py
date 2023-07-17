import argparse
import networkx as nx
import os
import time
import sys
import reader
import measure
import numpy as np
from scipy.sparse import coo_matrix

sys.path.append("..")

import algorithm.abcore
import algorithm.ktip
import algorithm.kwing
import algorithm.bitruss
#import algorithm.bine
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

parser.add_argument('--network', default="../dataset/alphabeta_sample.txt",
                    help='a folder name containing network.dat')

parser.add_argument('--algorithm', default="LPAb_Plus",
                    help='specify algorithm name')

args = parser.parse_args()
print("network ", args.network)
print("algorithm ", args.algorithm)

user_params = get_user_param(args, args.algorithm)

output = get_base(args.network)
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
    a = np.loadtxt(args.network, delimiter=',', skiprows=1)
    X = (coo_matrix((a[:, 2], (a[:, 0].astype(int), a[:, 1].astype(int))))).tocsr()
else:
    G = reader.readEdgeList(args.network)
    G.remove_edges_from(nx.selfloop_edges(G))
#############################################################################

start_time = time.time()

if args.algorithm == 'abcore':
    C =  algorithm.abcore.run(G, args.a, args.b)

elif args.algorithm == 'ktip':
    C = algorithm.ktip.run(G, args.k)

elif args.algorithm == 'kwing':
    C = algorithm.kwing.run(G, args.k)

elif args.algorithm == 'bitruss':
    C = algorithm.bitruss.run(G, args.k)

elif args.algorithm == 'bine':
    import algorithm.bine
    # C = algorithm.bine.run()
    C = nx.connected_components(G)
    algorithm.bine.run()

elif args.algorithm == 'deepcc':
    # C = algorithm.deepcc.run()
    import algorithm.deepcc
    C = nx.connected_components(G)
    algorithm.deepcc.run()

elif args.algorithm == 'biplex':
    C = algorithm.biplex.run(G, args.k, args.t)

elif args.algorithm == 'biLouvain':
    C = algorithm.bilouvain.run(args.network)

elif args.algorithm == "spec":
    C = algorithm.spec.run(X, args.c)

elif args.algorithm == 'LPAb':
    C = algorithm.LPAb.LPAb(G)

elif args.algorithm == 'LPAb_Plus':
    C = algorithm.LPAb_Plus.LPAb_plus(G)

run_time = time.time() - start_time

if args.algorithm == 'biLouvain':
    pass
elif args.algorithm == "spec":
    print('running time', run_time)
    print("----------------------------------------------------------")
    for i in range(args.c):
        print("Clustering {0} : ".format(i), C.get_indices(i))
    print("----------------------------------------------------------")
    with open(output, 'w') as f:
        f.write("seconds" + "\t" + str(run_time) + '\n')
        for i in range(args.c):
            f.write("Clustering {0} : ".format(i) + str(C.get_indices(i)) + '\n')
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

    with open(output, 'w') as f:
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

