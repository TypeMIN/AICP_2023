import math
import networkx as nx
from networkx.algorithms import bipartite

def find_nodes_at_distance_2(node, graph):
	"""
	combine the distance is 2 neighbor nodes and counts of unique items
	:param node: vertex
	:param graph:  bipartite graph
	:return:  counts of unique items, combine dist-2 neigs
	"""
	distance_2_nodes = []
	counts = {}
	# 주어진 노드로부터 거리가 1인 이웃 노드 찾기
	for neighbor in graph.neighbors(node):
		# 각 이웃 노드로부터 거리가 1인 이웃 노드 찾기 (즉, 원래 노드로부터 거리가 2인 노드 찾기)
		for neighbor_2 in graph.neighbors(neighbor):
			# 원래 노드와 거리가 2인 이웃 노드는 서로 다른 bipartite set에 속해야 한다.
			distance_2_nodes.append(neighbor_2)
	# 본인 제거
	distance_2_nodes = [i for i in distance_2_nodes if i != node]
	# counts of unique items
	for i in distance_2_nodes:
		if i in counts:
			counts[i] +=1
		else:
			counts[i] = 1
	result = list(set(distance_2_nodes))
	return counts, result

def run(G, k):
	"""
	find the number of butterflies each vertex u in U participates
	:param U: list of each vertex
	:param G: bipartite Graph
	:return: the dictionary that is the number of butterflies each vertex
	"""
	G.remove_nodes_from(list(nx.isolates(G)))
	print(nx.is_connected(G))
	I,U = bipartite.sets(G)
	D = []
	betas = {}
	c= {}
	theta = {}
	for u in sorted(U):
		c, D = find_nodes_at_distance_2(u, G)
		for d in sorted(D):
			if u in betas:
				betas[u] += math.comb(c[d], 2)
			else:
				betas[u] = math.comb(c[d], 2)

	for _ in range(len(betas)):
		u = min(betas, key=lambda i: betas[i])
		theta[u] = betas[u]
		c, D = find_nodes_at_distance_2(u, G)
		for d in sorted(D):
			if d not in theta:
				if betas[d] - math.comb(c[d], 2)  < betas[u]:
					betas[d] = betas[u]
				else:
					betas[d] = betas[d] - math.comb(c[d], 2)
		del  betas[u]

	remover = set()
	for key, value in theta.items():
		if value < k:
			remover.add(key)
			G.remove_node(key)
	U = U - remover

	connected_nodes = set()
	for u in sorted(U):
		connected_nodes.update(G.neighbors(u))

	remover = set()
	for v in sorted(I):
		if v not in connected_nodes:
			remover.add(v)
			G.remove_node(v)

	return nx.connected_components(G)