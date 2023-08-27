from __future__ import division
import os
import tensorflow as tf
import algorithm.deepcc_helper.core.paegmm.kddcup10.kddcup10_pae_gmm as paegmm
import numpy as np
from scipy.io import savemat
import networkx as nx
from collections import defaultdict

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "2,3"

def run(G):
    tf.compat.v1.disable_eager_execution()

    # data_path
    top_nodes = set(n for n, d in G.nodes(data=True) if d['bipartite'] == 0)
    adjacency_matrix = nx.bipartite.biadjacency_matrix(G, row_order=top_nodes).toarray().astype('int32')

    mdict = {
        'gnd': np.ones((adjacency_matrix.shape[0],1)).astype('int'),
        'fea': adjacency_matrix
    }
    savemat('../dataset/deepcc_data.mat', mdict)


    #Coil20 = ['../dataset/deepcc_sample.mat', 20, 'coil20'] # cora dataset
    Coil20 = ['../dataset/deepcc_data.mat', 3, 'coil20'] #aicp
    
    filename   = Coil20[0]
    num_clus_r = Coil20[1]
    num_clus_c = Coil20[1]

    from scipy import io
    mat_file = io.loadmat(filename)
    row_num = mat_file['fea'].shape[0]
    col_num = mat_file['fea'].shape[1]

    ae_config = [col_num, 500, 200, 100, 40]

    ae_col_config = [row_num, 500, 200, 100, 40]

    gmm_config = [[num_clus_r, 5], 40, 160, 80, 40, num_clus_r]

    accuracy     = []
    NMI          = []
    pred_label_list = []

    rounds = 5 # 10
    epochs = 300 # 3000
    epochs_pretrain = 100 # 1000
    for k in range(rounds):
        tf.compat.v1.reset_default_graph()
        machine = paegmm.KddcupPaeGmm(1024, num_clus_r, num_clus_c, ae_config, ae_col_config, gmm_config, 0)
        data = machine.get_data(filename)
        acc, nmi, pred_label_list = machine.run(data, epochs, epochs_pretrain)

        accuracy      = np.append(accuracy, acc)
        NMI           = np.append(NMI, nmi)

    print(pred_label_list)
    cluster_dict = defaultdict(list)
    nodes = sorted(G.nodes())
    for node, cluster in zip(nodes, pred_label_list):
        cluster_dict[cluster].append(node)

    G_result = nx.Graph()

    for cluster, nodes_in_cluster in cluster_dict.items():
        if cluster == -1:
            continue
        for i in range(len(nodes_in_cluster)):
            for j in range(i + 1, len(nodes_in_cluster)):
                G_result.add_edge(nodes_in_cluster[i], nodes_in_cluster[j])
    print(G_result)
    return nx.connected_components(G_result)