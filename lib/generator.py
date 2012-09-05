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


def remove_edges(aGraph, r, p):
    """aGraph - network
        r - coefficient of bribery
        p - probabilty of not concidering parametr r
    """
    n = min(aGraph.degree())
    allRemoved = 0
    while not allRemoved:
        allRemoved = 1
        avdegr = calculate_average_degree(aGraph)
        edges = aGraph.edges()
        for edg in edges:
            MN = min(aGraph.degree(edg[0]), aGraph.degree(edg[1]))
            if (MN < r * avdegr or random.random() < p) and MN > n:
                aGraph.remove_edge(edg[0], edg[1])
                avdegr = calculate_average_degree(aGraph)
                allRemoved = 0
    return aGraph


def evolve_ba_removing_edges(m, m0, n, r, p):
    """Barabasi-Albert model generator
        Adding nodes
        m - number of nodes to evolve
        m0 - number of initial nodes
        n - number of edges of each new node
    """
    #Initializing graph
    aGraph = nx.Graph()
    aGraph.probability = {}
    name = "ba_m=" + repr(m) + "_n=" + repr(n) + \
    "_r=" + repr(r) + "_p=" + repr(p)
    aGraph.name = name

    #Add first m0 nodes
    aGraph.add_node(0)
    for new in xrange(1, m0):
        aGraph.add_node(new)
        aGraph.add_edge(new - 1, new)
    #Calculating probability for first m0 nodes
    sumk = float(aGraph.number_of_edges() * 2)
    for k in xrange(m0):
        aGraph.probability[k] = aGraph.degree(k) / sumk

    #Generating new nodes
    for new in xrange(m0, m):
        #Add new node
        aGraph.add_node(new)
        n1 = new - 1
        while aGraph.degree(new) < n:
            for i in xrange(n1):
                #Add degrees
                if random.random() <= aGraph.probability[i]:
                    aGraph.add_edge(new, i)
                    if aGraph.degree(new) == n:
                        break

        #Recalculating probability
        sumk = float(aGraph.number_of_edges() * 2)
        for k in xrange(new):
            aGraph.probability[k] = aGraph.degree(k) / sumk

    #Removing edges
    remove_edges(aGraph, r, 0)
    return aGraph


def evolve_ba_with_briebery(m, m0, r, n, di = 0, p = 0):
    """Barabasi-Albert model generator
        Adding nodes
        m - number of nodes to evolve
        m0 - number of initial nodes
        r - coefficient of bribery
        n - number of edges of each new node
        di - 1 -make directed graph, 0 - usual graph
        p - probabilty of not concidering parametr r
    """
    #Initializing graph
    if di:
        aGraph = nx.DiGraph()
    else:
        aGraph = nx.Graph()
    aGraph.probability = {}
    name = "ba_m=" + repr(m) + "_r=" + repr(r) + \
    "_n=" + repr(n) + "_p=" + repr(p)
    aGraph.name = name

    #Add first m0 nodes
    aGraph.add_node(0)
    for new in xrange(1, m0):
        aGraph.add_node(new)
        aGraph.add_edge(new - 1, new)
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
        n1 = new - 1
        while aGraph.degree(new) < n:
            for i in xrange(n1):
                #Add degrees
                if (random.random() <= aGraph.probability[i]) \
                and ((aGraph.degree(i) >= rnorm) or random.random() <= p):
                    aGraph.add_edge(new, i)
                    if aGraph.degree(new) == n:
                        break
        avdegr = calculate_average_degree(aGraph)
        rnorm = r * avdegr

        #Recalculating probability
        sumk = float(aGraph.number_of_edges() * 2)
        for k in xrange(new):
            aGraph.probability[k] = aGraph.degree(k) / sumk
    return aGraph


def evolve_ba_with_briebery_adj(m, m0, r, n, di = 0, p = 0):
    """ Barabasi-Albert model generator
         Adding nodes
         m - number of nodes to evolve
         m0 - number of initial nodes
         r - coefficient of bribery
         n - number of edges of each new node
         di - 1 -make directed graph, 0 - usual graph
         p - probabilty of not concidering parametr r
    """
    edgeList = []
    edgeNumber = (m - m0) * n

    #Because matrix index are from 0 to m-1
    m = m - 1
    briebery = (1 - r) * 2 * m
    while edgeNumber > 0:
        edge = (random.randint(0, m), random.randint(0, m))
        if sum(edge) < briebery and edge not in edgeList:
            edgeList.append(edge)
            edgeNumber -= 1

    aGraph = nx.from_edgelist(edgeList)
    name = "ba_adj_m=" + repr(m) + "_r=" + repr(r) + \
    "_n=" + repr(n) + "_p=" + repr(p)
    aGraph.name = name
    return aGraph


def evolve_decorated_flower(x, y, n):
    """(x,y) flower network generator
        x, y - number of nodes on edges
        n - number of transformation of all edges
    """

    if x < 1 or y < 2 or n < 2:
        return "Error in input data"
    #Initializing graph
    aGraph = nx.Graph()
    aGraphRemovedEdges = nx.Graph()
    name = "flower_decor_x=" + repr(x) + "_y=" + repr(y) + \
    "_n=" + repr(n)
    aGraph.name = name

    #Add first 2 nodes and 1 edge
    aGraph.add_node(0)
    aGraph.add_node(1)
    aGraph.add_edge(0, 1)

    #Generating new nodes
    for iterations in xrange(1, n):
        #List of edges
        edges = aGraph.edges()

        for edge in edges:
            #Transforming one edge
            aGraph.remove_edge(edge[0], edge[1])
            aGraphRemovedEdges.add_edge(edge[0], edge[1])

            #len(aGraph) calculate length from 1
            #we calculate nodes from 0

            #Adding line x
            if x != 1:
                length = len(aGraph)
                #First node at line x
                aGraph.add_node(length)
                aGraph.add_edge(edge[0], length)

                #Rest nodes at line x
                if x > 1:
                    for new in xrange(length + 1, length + x - 1):
                        aGraph.add_node(new)
                        aGraph.add_edge(new - 1, new)
                #Last edge
                aGraph.add_edge(edge[1], len(aGraph) - 1)
            else:
                aGraph.add_edge(edge[0], edge[1])
            #Adding line y

            length = len(aGraph)
            #First node at line y
            aGraph.add_node(length)
            aGraph.add_edge(edge[0], length)

            #Rest nodes at line y
            if y > 1:
                for new in xrange(length + 1, length + y - 1):
                    aGraph.add_node(new)
                    aGraph.add_edge(new - 1, new)
            #Last edge
            aGraph.add_edge(edge[1], len(aGraph) - 1)
    aGraph.add_edges_from(e for e in aGraphRemovedEdges.edges_iter(data=True))
    return aGraph

def evolve_decorated_flower_adj(x, y, n, p = 0.9):
    """(x,y) flower network generator by adjacency matrix
        x, y - number of nodes on edges
        n - number of transformation of all edges
        p - probability of eding edge in area
    """

    def numberOfEdgesAndNodes():
        numberOfEdges = []
        numberOfEdges.append(1)

        if (x+y) == 3:
            for i in xrange(1, n):
                numberOfEdges.append(numberOfEdges[-1]*(x+y))
        else:
            for i in xrange(1, n):
                numberOfEdges.append(numberOfEdges[-1]*(x+y+1))

        numberOfNodes = []
        numberOfNodes.append(2)
        for i in xrange(1,n):
            numberOfNodes.append(numberOfNodes[-1] + numberOfEdges[i-1]*(x+y-2))
        return numberOfNodes, numberOfEdges


    if x < 1 or y < 2 or n < 2:
        return "Error in input data"
    p = 1 -p
    numNodes, numEdges = numberOfEdgesAndNodes()

    #Adjacency matrix is simmetric, so
    #we will work with bottom triangle matrix
    edgeList = []
    edgeList.append([1, 0])
    for i in xrange(1, n):
        while len(edgeList) < numEdges[i]:
            #numNodes - list with number of nodes
            #adjacency marix has numeration from 0
            #so there is -1
            xI = random.randint(numNodes[i-1] + 1 - 1, numNodes[i]-1)
            yI = random.randint(0, numNodes[i-1]-1)

            if yI < numNodes[i-1]/4:
#            if (numNodes[i-1] + numNodes[i])*0.9/2 < (xI + yI) < (numNodes[i-1] + numNodes[i])*1.1/2:
                if [xI,yI] not in edgeList:
                    edgeList.append([xI, yI])
            elif random.random() < p:
                if [xI,yI] not in edgeList:
                    edgeList.append([xI, yI])

    aGraph = nx.from_edgelist(edgeList)
    name = "flower_decor_adj_x=" + repr(x) + "_y=" + repr(y) + \
    "_n=" + repr(n)
    aGraph.name = name
    return aGraph



def evolve_flower(x, y, n):
    """(x,y) flower network generator
        x, y - number of nodes on edges
        n - number of transformation of all edges
    """
    if x < 1 or y < 2 or n < 2:
        return "Error in input data"
    #Initializing graph
    aGraph = nx.Graph()
    name = "flower_x=" + repr(x) + "_y=" + repr(y) + \
    "_n=" + repr(n)
    aGraph.name = name

    #Add first 2 nodes and 1 edge
    aGraph.add_node(0)
    aGraph.add_node(1)
    aGraph.add_edge(0, 1)

    #Generating new nodes
    for iterations in xrange(1, n):
        #List of edges
        edges = aGraph.edges()

        for edge in edges:
            #Transforming one edge
            aGraph.remove_edge(edge[0], edge[1])

            #len(aGraph) calculate length from 1
            #we calculate nodes from 0

            #Adding line x
            if x != 1:
                length = len(aGraph)
                #First node at line x
                aGraph.add_node(length)
                aGraph.add_edge(edge[0], length)

                #Rest nodes at line x
                if x > 1:
                    for new in xrange(length + 1, length + x - 1):
                        aGraph.add_node(new)
                        aGraph.add_edge(new - 1, new)
                #Last edge
                aGraph.add_edge(edge[1], len(aGraph) - 1)
            else:
                aGraph.add_edge(edge[0], edge[1])
            #Adding line y

            length = len(aGraph)
            #First node at line y
            aGraph.add_node(length)
            aGraph.add_edge(edge[0], length)

            #Rest nodes at line y
            if y > 1:
                for new in xrange(length + 1, length + y - 1):
                    aGraph.add_node(new)
                    aGraph.add_edge(new - 1, new)
            #Last edge
            aGraph.add_edge(edge[1], len(aGraph) - 1)

    return aGraph


def evolve_flower_removing_edges(x, y, n, r = 0, p = 0):
    """(x,y) flower network generator
        x, y - number of nodes on edges
        n - number of transformation of all edges
        r - coeficient of bribery
        p - probabilty of not concidering parametr r
    """
    if x < 1 or y < 2 or n < 2:
        return "Error in input data"
    #Initializing graph
    aGraph = nx.Graph()
    aGraph.probability = {}
    name = "flower_x=" + repr(x) + "_y=" + repr(y) + \
    "_n=" + repr(n) + "_r=" + repr(r)
    aGraph.name = name

    #Add first 2 nodes and 1 edge
    aGraph.add_node(0)
    aGraph.add_node(1)
    aGraph.add_edge(0, 1)

    #Generating new nodes
    for iterations in xrange(1, n):
        #List of edges
        edges = aGraph.edges()

        for edge in edges:
            #Transforming one edge
            aGraph.remove_edge(edge[0], edge[1])

            #len(aGraph) calculate length from 1
            #we calculate nodes from 0

            #Adding line x

            length = len(aGraph)
            #First node at line x
            aGraph.add_node(length)
            aGraph.add_edge(edge[0], length)

            #Rest nodes at line x
            if x > 1:
                for new in xrange(length + 1, length + x - 1):
                    aGraph.add_node(new)
                    aGraph.add_edge(new - 1, new)
            #Last edge
            aGraph.add_edge(edge[1], len(aGraph) - 1)

            #Adding line y

            length = len(aGraph)
            #First node at line y
            aGraph.add_node(length)
            aGraph.add_edge(edge[0], length)

            #Rest nodes at line y
            if y > 1:
                for new in xrange(length + 1, length + y - 1):
                    aGraph.add_node(new)
                    aGraph.add_edge(new - 1, new)
            #Last edge
            aGraph.add_edge(edge[1], len(aGraph) - 1)
    #Removing edges
    remove_edges(aGraph, r, p)
    return aGraph


def evolve_flower_with_briebery(x, y, n, r = 0, p = 0):
    """(x,y) flower network generator
        x, y - number of nodes on edges
        n - number of transformation of all edges
        r - coeficient of bribery
        p - probabilty of not concidering parametr r
    """
    if x < 1 or y < 2 or n < 2:
        return "Error in input data"
    #Initializing graph
    aGraph = nx.Graph()
    aGraph.probability = {}
    name = "flower_x=" + repr(x) + "_y=" + repr(y) + \
    "_n=" + repr(n) + "_r=" + repr(r)
    aGraph.name = name

    #Add first 2 nodes and 1 edge
    aGraph.add_node(0)
    aGraph.add_node(1)
    aGraph.add_edge(0, 1)

    #Generating new nodes
    for iterations in xrange(1, n):
        #List of edges
        edges = aGraph.edges()

        for edge in edges:
            avdegr = calculate_average_degree(aGraph)
            if min(edge) / avdegr > r * avdegr or random.random() < p:
                #Transforming one edge
                aGraph.remove_edge(edge[0], edge[1])

                #len(aGraph) calculate length from 1
                #we calculate nodes from 0

                #Adding line x

                length = len(aGraph)
                #First node at line x
                aGraph.add_node(length)
                aGraph.add_edge(edge[0], length)

                #Rest nodes at line x
                if x > 1:
                    for new in xrange(length + 1, length + x - 1):
                        aGraph.add_node(new)
                        aGraph.add_edge(new - 1, new)
                #Last edge
                aGraph.add_edge(edge[1], len(aGraph) - 1)

                #Adding line y

                length = len(aGraph)
                #First node at line y
                aGraph.add_node(length)
                aGraph.add_edge(edge[0], length)

                #Rest nodes at line y
                if y > 1:
                    for new in xrange(length + 1, length + y - 1):
                        aGraph.add_node(new)
                        aGraph.add_edge(new - 1, new)
                #Last edge
                aGraph.add_edge(edge[1], len(aGraph) - 1)
    return aGraph
