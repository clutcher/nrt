# -*- coding: utf-8 -*-
"""Albert-Barabasi model"""

import networkx as nx
import matplotlib.pyplot as plt

import lib.generator as generator
import lib.graphics as graphics
import lib.calculation as calculation

if __name__ == '__main__':

    #r - the coefficient of bribery
    r = 0.0
    #rc - critical coefficient of bribery
    rc = 0
    #rlist - list of r, where r > rc
    rlist = []
    #rfull - list of  r
    rfull = []
    #flag - finding first rc
    flag = 1

    nyu = []
    clustering = []
    shortpath = []
    assortativity = []

    G = nx.Graph()

    #Generate many networks for making nyu graphic
    while r < 1:
        G = generator.evolveN(1000, 20, r, 3)
        rfull.append(r)
        clustering.append(nx.average_clustering(G))
        shortpath.append(nx.average_shortest_path_length(G))
        assortativity.append(nx.degree_assortativity(G))
        nyutemp = calculation.calculate_nyu(G)
        if (nyutemp != 0) and flag:
            rc = r
            flag = 0
        if rc != 0:
            rlist.append(r - rc)
            nyu.append(nyutemp)
        r = r + 0.01
        
#        graphics.make_graph(G)
        graphics.make_probability_graphic(G)
#        graphics.make_degree_histogram(G)
        graphics.make_rank_distribution(G)
        
    #Saving coefficients to file
	fc = open('data/clustering.txt', 'w')
	fsh = open('data/shortpath.txt', 'w')

    for cl in clustering:
        line = repr(cl) + "\n"
        fc.write(line)
    fc.close()

    for sp in shortpath:
        line = repr(sp) + "\n"
        fsh.write(line)
    fsh.close()

    graphics.make_nyu_graphic(nyu, rlist)
    graphics.make_clustering_graphic(clustering, rfull)
    graphics.make_shortest_path_graphic(shortpath, rfull)
    graphics.make_assortativity_graphic(assortativity, rfull)

#    plt.show()

#    print nx.betweenness_centrality(G)
#    print nx.info(G)
#    print "Clustering: " + nx.average_clustering(G)
#    print "Shortest path length: " + nx.average_shortest_path_length(G)
#    nx.write_edgelist(G, "edgelist.graph")
