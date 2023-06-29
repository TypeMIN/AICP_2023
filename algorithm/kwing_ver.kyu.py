import networkx as nx

def wing(U, G):
  """
  find the number of each edge butterfly e in E participates
  :param U: list of each vertex
  :param G: bipartite Graph
  :return: the dictionary that is wing number of butterflies each edge
  """
  beta = {}
  betterfly = []
  for u in U:
    neig = list(G.neighbors(u))
    for v1 in range(0, len(neig)-1):
      for v2 in range(v1+1, len(neig)):
        inter  = list(set(G.neighbors(neig[v1])) & set(G.neighbors(neig[v2])))
        if len(inter)  >= 2:
          for i in inter:
            if (i, neig[v1]) in beta:
              beta[(i, neig[v1])] +=1
            else:
              beta[(i, neig[v1])] = 0
            if (i, neig[v2]) in beta:
              beta[(i, neig[v2])] +=1
            else:
              beta[(i, neig[v2])] = 0
            betterfly.append((u, i, neig[v1], neig[v2]))
  psi = {}
  for e in beta:
    psi[e] = beta[e]
    for t in betterfly:
      if e[0] in t  and e[1] in t:
        for _ in range(2):
          if (t[i], t[2]) != e:
            if beta[(t[i], t[2])] > beta[e]:
              beta[(t[i], t[2])] -= 1
          if (t[i], t[3]) != e:
            if beta[(t[i], t[3])] > beta[e]:
              beta[(t[i], t[3])] -= 1
  return psi






if __name__=="__main__":
  B = nx.Graph()
  B.add_nodes_from([1,2,3,4,5,6], bipartite = 0)
  B.add_nodes_from(["a", "b", "c", "d", "e", "f", "g"], bipartite = 1)
  B.add_edges_from([(1,"a"), (1, "b"), (1, "c"), (2, "a"), (2, "b"), (2, "c"), (3, "c"), (3,"d"), (4, "c"), (4, "d"), (5, "d"), (5, "e"), (5, "f"), (6, "d"), (6, "e"), (6, "f"), (6, "g")])
  node = ["a", "b", "c", "d", "e", "f", "g"]

  print(f"result of wing decomposition: {wing(node, B)}")