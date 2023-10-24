with open("../statistic.csv", 'w') as f:
    f.write("dataset" + "," + "algorithm" + "," + "vertex_density" + "," + "edge_density" + "," + "graph_density" + "," + "barbers_modularity" + "," + "run_time" + "," + "graph_size" + "," + "community_num" + "\n")
    f.close()