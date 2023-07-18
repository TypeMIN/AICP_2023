from __future__ import division
import os
import tensorflow as tf
import algorithm.deepcc_helper.core.paegmm.kddcup10.kddcup10_pae_gmm as paegmm
import numpy as np

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "2,3"

def run():
    tf.compat.v1.disable_eager_execution()
    # data_path
    Coil20 = ['../dataset/deepcc_sample.mat', 20, 'coil20'] # cora dataset
    
    filename   = Coil20[0]
    num_clus_r = Coil20[1]
    num_clus_c = Coil20[1]

    ae_config = [1433, 500, 200, 100, 40]

    ae_col_config = [2708, 500, 200, 100, 40]

    gmm_config = [[num_clus_r, 5], 40, 160, 80, 40, num_clus_r]

    accuracy     = []
    NMI          = []
    pred_label_list = []

    rounds = 1 # 10
    epochs = 1 # 3000
    epochs_pretrain = 1 # 1000
    for k in range(rounds):
        tf.compat.v1.reset_default_graph()
        machine = paegmm.KddcupPaeGmm(1024, num_clus_r, num_clus_c, ae_config, ae_col_config, gmm_config, 0)
        data = machine.get_data(filename)
        acc, nmi, pred_label_list = machine.run(data, epochs, epochs_pretrain)

        accuracy      = np.append(accuracy, acc)
        NMI           = np.append(NMI, nmi)

    print(pred_label_list)
    return 0