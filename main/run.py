import argparse
import networkx as nx
import os
import time
import sys
import reader
import measure

sys.path.append("..")

import algorithm.abcore
import algorithm.ktip
import algorithm.kwing
import algorithm.bitruss
import algorithm.bine
import algorithm.deepcc


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

    return ret


#############################################################################
parser = argparse.ArgumentParser(description='value k')
parser.add_argument('--a', type=int, default=3,
                    help='user parameter for abcore')

parser.add_argument('--b', type=int, default=3,
                    help='user parameter for abcore')

parser.add_argument('--k', type=int, default=2, help='user parameter for ktip, kwing or bitruss')

parser.add_argument('--network', default="../dataset/alphabeta_sample.txt",
                    help='a folder name containing network.dat')

parser.add_argument('--algorithm', default="abcore",
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
#############################################################################
# read network
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
    # C = algorithm.bine.run()
    C = nx.connected_components(G)
    algorithm.bine.run()

elif args.algorithm == 'deepcc':
    # C = algorithm.deepcc.run()
    C = nx.connected_components(G)
    algorithm.deepcc.run()

run_time = time.time() - start_time

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

