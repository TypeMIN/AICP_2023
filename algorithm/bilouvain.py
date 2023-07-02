import networkx as nx
from networkx.algorithms import bipartite

def CAL_dQ(node, communities_cadi, edge_init):
	result = []
	return result

def run(G: nx.Graph):
	phase_cutoff = 0
	""" Phase """
	while phase_cutoff != 1:
		iteration_cutoff  = 0
		communities_init = [ [i] for i in list(G.nodes)]
		node_init = [ i for i in list(G.nodes())]
		edge_init = list(G.edges.data('weight', default=True))
		""" Iteration """
		while iteration_cutoff !=0:
			for node in node_init:
				""" Computing Candidate Communities """
				N = list(G.neighbors(node))
				cadi = []
				for neigh in N:
					cadi.append(neigh)
				communities_cadi = [ i for i in communities_init if any( j in i for j in cadi)]
				""" Evaluate Modularity Gain """
				result = CAL_dQ(node, communities_cadi, edge_init)

				""" Convert Vertex i to Candidate Community """

			if communities_init == result:
				iteration_cutoff +=1
			else:
				communities_init = result

		""" Compaction Step """
		result_G = nx.Graph()
		# add node and edge+weight after compaction
		if result_G == G:
			phase_cutoff = 1
		else:
			G = result_G



if __name__ == "__main__":
	B = nx.Graph()
	B.add_nodes_from(["u1", "u2", "u3", "u4", "u5"], bipartite=0)
	B.add_nodes_from(["v1", "v2", "v3", "v4", "v5", "v6", "v7"], bipartite=1)
	B.add_weighted_edges_from(
		[("u1", "v1", 3), ("u1", "v4",3), ("u2", "v1",3), ("u2", "v3",3), ("u3", "v1",2), ("u3", "v2",1), ("u3", "v3",4), ("u3", "v4",1),
		 ("u4", "v4", 2), ("u4", "v5", 3), ("u4", "v6", 2), ("u4", "v7",5), ("u5", "v5",6), ("u5", "v6",2), ("u5", "v7",3)])
	run(B)
