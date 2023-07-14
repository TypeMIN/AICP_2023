import networkx as nx
import numpy as np
from scipy.sparse import coo_matrix
from coclust.coclustering import CoclustSpecMod

def run(file_name, n_clust):
	a = np.loadtxt(file_name, delimiter=',', skiprows=1)
	X = (coo_matrix((a[:, 2], (a[:, 0].astype(int), a[:, 1].astype(int))))).tocsr()

	model = CoclustSpecMod(n_clusters=n_clust, random_state=0)
	model.fit(X)


if __name__=="__main__":
	B = nx.Graph()
	B.add_nodes_from([1,2,3,4,5,6], bipartite = 0)
	B.add_nodes_from(["a", "b", "c", "d", "e", "f", "g"], bipartite = 1)
	B.add_edges_from([(1,"a"), (1, "b"), (1, "c"), (2, "a"), (2, "b"), (2, "c"), (3, "c"), (3,"d"), (4, "c"), (4, "d"), (5, "d"), (5, "e"), (5, "f"), (6, "d"), (6, "e"), (6, "f"), (6, "g")])
	run(B, 3)