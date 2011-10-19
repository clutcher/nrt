# -*- coding: utf-8 -*-
"""Network generator"""

import networkx as nx
import random


def calculate_average_degree(aGraph):
    """Average degree of graph"""
    s = sum(aGraph.degree().values())
    nnodes = aGraph.number_of_nodes()
    avdegree = float(s) / float(nnodes)
    return avdegree


def evolveN(m, m0, r, n):
    """Adding nodes
        m - number of nodes to evolve
        m0 - number of initial nodes
        r - r(k)
        n - number of edges of each new node
    """
    #Initializing graph
    aGraph = nx.Graph()
    aGraph.probability = {}
    aGraph.name = "Barabasi-Albert Graph"

    #Add first n nodes
    for new in xrange(m0):
        aGraph.add_node(new)

    #Adding edges for first n nodes (circle)
    for new in xrange(1, m0):
        aGraph.add_edge(new - 1, new)
#    #Make circle
#    aGraph.add_edge(0,m0-1)

    #Calculating probability for first m0 nodes
    sumk = sum(aGraph.degree())
#    sumk = 0
#    for i in xrange(m0):
#        sumk += aGraph.degree(i)
    for k in xrange(m0):
        aGraph.probability[k] = aGraph.degree(k) / float(sumk)

    #Generating new nodes
    avdegr = calculate_average_degree(aGraph)
    for new in xrange(m0, m):
        #Add new node
        aGraph.add_node(new)
        while aGraph.degree(new) < n:
            for i in xrange(new - 1):
                #Add degrees
                if (random.random() <= aGraph.probability[i]) \
                    and (aGraph.degree(i) >= r * avdegr):
                    aGraph.add_edge(i, new)
                    avdegr = calculate_average_degree(aGraph)
                    if aGraph.degree(new) == n:
                        break

        #Recalculating probability
#        sumk = 0
#        for i in xrange(new):
#            sumk += aGraph.degree(i)
        sumk = sum(aGraph.degree())
        for k in xrange(new):
            aGraph.probability[k] = aGraph.degree(k) / float(sumk)
        print new
    return aGraph
