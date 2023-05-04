

def get_result(G, C):
    return get_average_size(G, C), get_number_of_cc(G, C)

def get_average_size(G, C):

    nodeCnt = 0
    E = G.number_of_edges()
    V = G.number_of_nodes()
    cnum = len(C)
    csum = 0
    for c in C:
        csum += len(c)
    return csum/cnum

def get_number_of_cc(G, C):
    return len(C)