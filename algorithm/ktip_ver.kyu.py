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

def  tip(G, k):
  """
  find the number of butterflies each vertex u in U participates
  :param U: list of each vertex
  :param G: bipartite Graph
  :return: the dictionary that is the number of butterflies each vertex
  """
  I,U = bipartite.sets(G)
  D = []
  betas = {}
  c= {}
  theta = {}
  for u in U:
    c, D = find_nodes_at_distance_2(u, G)
    for d in D:
      if u in betas:
        betas[u] += math.comb(c[d], 2)
      else:
        betas[u] = math.comb(c[d], 2)
  for u in U:
    theta[u] = betas[u]
    c, D = find_nodes_at_distance_2(u, G)
    for d in D:
      if betas[d] == 0:
        continue
      if (betas[d] - math.comb(c[d], 2) ) < betas[u]:
        betas[d] = betas[u]
      else:
        betas[d] -= math.comb(c[d], 2)

  remover = set()
  for key, value in theta.items():
    if value < k:
      remover.add(key)
      G.remove_node(key)
  U = U - remover

  connected_nodes = set()
  for u in U:
    print(u)
    connected_nodes.update(G.neighbors(u))

  remover = set()
  for v in I:
    if v not in connected_nodes:
      remover.add(v)
      G.remove_node(v)
  I = I - remover
  return nx.connected_components(G)

if __name__=="__main__":
  B = nx.Graph()
  B.add_nodes_from([1,2,3,4,5,6], bipartite = 0)
  B.add_nodes_from(["a", "b", "c", "d", "e", "f", "g"], bipartite = 1)
  B.add_edges_from([(1,"a"), (1, "b"), (1, "c"), (2, "a"), (2, "b"), (2, "c"), (3, "c"), (3,"d"), (4, "c"), (4, "d"), (5, "d"), (5, "e"), (5, "f"), (6, "d"), (6, "e"), (6, "f"), (6, "g")])

  print(f"result of tip decomposition: {sorted(tip(B, 2))}")
  #[{1, 2, 'c', 3, 4, 5, 6, 'd', 'a', 'b', 'f', 'e'}]