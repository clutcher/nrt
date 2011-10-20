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
    name = "ba_m=" + repr(m) + "_r=" + repr(r) + "_n=" + repr(n)
    aGraph.name = name

    #Add first n nodes
    for new in xrange(0, m0, 2):
        aGraph.add_node(new)
        n1 = new + 1
        aGraph.add_node(n1)
        aGraph.add_edge(new, n1)

    #Calculating probability for first m0 nodes
    sumk = float(aGraph.number_of_edges() * 2)
    for k in xrange(m0):
        aGraph.probability[k] = aGraph.degree(k) / sumk

    #Generating new nodes
    avdegr = calculate_average_degree(aGraph)
    #Normalizing r = r * average_degree
    rnorm = r * avdegr
    for new in xrange(m0, m):
        #Add new node
        aGraph.add_node(new)
        newdegr = 0
        n1 = new - 1
        while newdegr < n:
            for i in xrange(n1):
                #Add degrees
                if (random.random() <= aGraph.probability[i]) \
                and (aGraph.degree(i) >= rnorm):
                    aGraph.add_edge(i, new)
                    newdegr += 1
                    avdegr = calculate_average_degree(aGraph)
                    rnorm = r * avdegr
                    if newdegr == n:
                        break

        #Recalculating probability
        sumk = float(aGraph.number_of_edges() * 2)
        for k in xrange(new):
            aGraph.probability[k] = aGraph.degree(k) / sumk
        print new
    return aGraph
