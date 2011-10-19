# -*- coding: utf-8 -*-
"""Albert-Barabasi model"""

import networkx as nx
import matplotlib.pyplot as plt
import time

import lib.generator as generator
import lib.graphics as graphics
import lib.calculation as calculation

if __name__ == '__main__':

    startTime = time.time()
    #r -
    r = 0.0
    #rc -
    rc = 0
    #rlist - list of r, where r>rc
    rlist = []
    #rfull - list of  r
    rfull = []
    #flag - finding first rc
    flag = 1

    nyu = []
    clustering = []
    shortpath = []

    G = nx.Graph()

    #Generate many networks for making nyu graphic
    while r < 1:
#        @fixme test generator BA, sumk
        G = generator.evolveN(1000, 20, r, 3)
#        graphics.make_rank_distribution(G, r)
#        line = repr(calculation.calculate_nyu(G))
#        line += '\n'
#        f.write(line.encode('utf-8'))
        rfull.append(r)
        clustering.append(nx.average_clustering(G))
        shortpath.append(nx.average_shortest_path_length(G))
        nyutemp = calculation.calculate_nyu(G)
        if (nyutemp != 0) and flag:
            rc = r
            flag = 0
        if rc != 0:
            rlist.append(r - rc)
            nyu.append(nyutemp)
        r = r + 0.01

#    G = generator.evolveN(N, 20, r, 3)
#    BA = nx.generators.random_graphs.barabasi_albert_graph(100,3)

    endTime = time.time()
#    print endTime-startTime

#    graphics.make_graph(G)
#    graphics.make_graph(BA)
#    graphics.make_probability_graphic(G)
#    graphics.make_probability_graphic(BA)
#    graphics.make_degree_histogram(BA)
#    graphics.make_rank_distribution(G, r)
#    graphics.make_rank_distribution(BA)
    graphics.make_nyu_graphic(nyu, rlist)
    graphics.make_clustering_graphic(clustering, rfull)
    graphics.make_shortest_path_graphic(shortpath, rfull)
#    print time.time()-endTime

    #nyu ~ (r-rc)^t
#    print calculation.calculate_nyu(G)
#    print nx.clustering(G)

#    print nx.betweenness_centrality(G)
#    print nx.info(G)
#    print "Clustering: " + nx.average_clustering(G)
#    print "Shortest path length: " + nx.average_shortest_path_length(G)
#    nx.write_edgelist(G, "edgelist.graph")
    plt.show()
