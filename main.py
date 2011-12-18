# -*- coding: utf-8 -*-
"""Albert-Barabasi model"""

import networkx as nx
#import matplotlib.pyplot as plt
#import time

import lib.generator as generator
import lib.graphics as graphics
import lib.calculation as calculation

if __name__ == '__main__':

    #r - the coefficient of bribery
    r = 0.4
    #rc - critical coefficient of bribery
    rc = 0
    #rlist - list of r, where r > rc
    rlist = []
    #flag - finding first rc
    flag = 1

    nyu = []
    clustering = []
    shortpath = []
    assortativity = []
    #Temps for finding average by realization
    nyuT = []
    clusteringT = []
    shortpathT = []
    assortativityT = []

    numberOfRealization = 5
    network = 'BA'
    if network == 'BA':
        #Generate many networks for making nyu graphic
        while r < 0.6:
            for i in xrange(numberOfRealization):
                print r, i

                G = generator.evolveBA(1000, 20, r, 3, 0, 0)

                nyutemp = calculation.calculate_nyu(G)
                if (nyutemp != 0) and flag:
                    rc = r
                    flag = 0
                if rc != 0:
                    clusteringT.append(nx.average_clustering(G))
                    shortpathT.append(nx.average_shortest_path_length(G))
                    assortativityT.append(abs(nx.degree_assortativity(G)))
                    nyuT.append(nyutemp)

            #Finding average parameters
            if rc != 0:
                sum = 0.0
                for temp in clusteringT:
                    sum += temp
                sum = sum / (len(clusteringT) + 1)
                clustering.append(sum)

                sum = 0.0
                for temp in shortpathT:
                    sum += temp
                sum = sum / (len(shortpathT) + 1)
                shortpath.append(sum)

                sum = 0.0
                for temp in assortativityT:
                    sum += temp
                sum = sum / (len(assortativityT) + 1)
                assortativity.append(sum)

                sum = 0.0
                for temp in nyuT:
                    sum += temp
                sum = sum / (len(nyuT) + 1)
                nyu.append(sum)

                #Adding 0.001 to avoid log 0
                rlist.append(r - rc + 0.001)
            r = r + 0.001
            #Clearing
            nyuT = []
            clusteringT = []
            shortpathT = []
            assortativityT = []

        #Network graphics
#        graphics.make_graph(G)
#        graphics.make_betweenness_graphic(G)
#        graphics.make_probability_graphic(G)
#        graphics.make_degree_histogram(G)
            graphics.make_rank_distribution(G)

        #Parametr graphics
        graphics.make_coeficient_graphic(rlist, nyu, "nyu")
        graphics.make_coeficient_graphic(rlist, clustering, "clustering")
        graphics.make_coeficient_graphic(rlist, shortpath, "shortpath")
        graphics.make_coeficient_graphic(rlist, assortativity, "assortativity")

#    plt.show()

#    print nx.betweenness_centrality(G)
#    print nx.info(G)
#    print "Clustering: " + nx.average_clustering(G)
#    print "Shortest path length: " + nx.average_shortest_path_length(G)
#    nx.write_edgelist(G, "edgelist.graph")

#    G = generator.evolveFlower(2, 2, 8, 0)
#    graphics.make_graph(G)
#    graphics.make_rank_distribution(G)
#    plt.show()
#

#    #Saving coefficients to file
#    fc = open('data/clustering.txt', 'w')
#    fsh = open('data/shortpath.txt', 'w')
#
#    for cl in clustering:
#        line = repr(cl) + "\n"
#        fc.write(line)
#    fc.close()
#
#    for sp in shortpath:
#        line = repr(sp) + "\n"
#        fsh.write(line)
##    fsh.close()
