import networkx as nx
from networkx.algorithms import bipartite

def run(G, k):
  """
  find the number of each edge butterfly e in E participates
  :param U: list of each vertex
  :param G: bipartite Graph
  :return: the dictionary that is wing number of butterflies each edge
  """
  I,U = bipartite.sets(G)
  beta = {}
  B = set()
  for u in sorted(U):
    neig = list(G.neighbors(u))
    for v1 in range(0, len(neig)-1):
      for v2 in range(v1+1, len(neig)):
        inter  = list(set(G.neighbors(neig[v1])) & set(G.neighbors(neig[v2])))
        for i in inter:
          if i == u:
            continue
          if (i, neig[v1]) in beta:
            beta[(i, neig[v1])] +=1
          else:
            beta[(i, neig[v1])] = 1
          if (i, neig[v2]) in beta:
            beta[(i, neig[v2])] +=1
          else:
            beta[(i, neig[v2])] = 1
          if (i, u, neig[v1], neig[v2]) not in B:
            B.add((u, i, neig[v1], neig[v2]))
  psi = {}
  for _ in range(len(beta)):
    e = min(beta, key=lambda i: beta[i])
    psi[e] = beta[e]
    for t in sorted(B):
      if e[0] in t  and e[1] in t:
        for i in range(2):
          if (t[i], t[2]) != e:
            if beta[(t[i], t[2])] > beta[e]:
              beta[(t[i], t[2])] -= 1
          if (t[i], t[3]) != e:
            if beta[(t[i], t[3])] > beta[e]:
              beta[(t[i], t[3])] -= 1
        B.remove(t)
    del  beta[e]

  T = set()
  for key, value in psi.items():
    if value != k:
      G.remove_edge(key[0], key[1])
    else:
      T.add(key[0])
      T.add(key[1])
  for u in U:
    if u not in T:
      G.remove_node(u)
  U = U & T
  connected_nodes = set()
  for u in U:
    connected_nodes.update(G.neighbors(u))

  for v in I:
    if v not in T:
      G.remove_node(v)
  return nx.connected_components(G)

if __name__=="__main__":
  B = nx.Graph()
  B.add_nodes_from([1,2,3,4,5,6], bipartite = 0)
  B.add_nodes_from(["a", "b", "c", "d", "e", "f", "g"], bipartite = 1)
  B.add_edges_from([(1,"a"), (1, "b"), (1, "c"), (2, "a"), (2, "b"), (2, "c"), (3, "c"), (3,"d"), (4, "c"), (4, "d"), (5, "d"), (5, "e"), (5, "f"), (6, "d"), (6, "e"), (6, "f"), (6, "g")])

  print(f"result of wing decomposition: {sorted(run(B, 2))}")
  # result of wing decomposition: [{1, 2, 'a', 'c', 'b'}, {5, 6, 'f', 'e', 'd'}]