# -*- coding: utf-8 -*-
"""Network generator"""
# @ToDO: Extremly need full refactor of this module.

import random

import networkx as nx


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
    # Initializing graph
    aGraph = nx.Graph()
    aGraph.probability = {}
    name = "ba_m=" + repr(m) + "_n=" + repr(n) + \
           "_r=" + repr(r) + "_p=" + repr(p)
    aGraph.name = name

    # Add first m0 nodes
    aGraph.add_node(0)
    for new in xrange(1, m0):
        aGraph.add_node(new)
        aGraph.add_edge(new - 1, new)
    # Calculating probability for first m0 nodes
    sumk = float(aGraph.number_of_edges() * 2)
    for k in xrange(m0):
        aGraph.probability[k] = aGraph.degree(k) / sumk

    # Generating new nodes
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


def evolve_ba_with_briebery(m, m0, r, n, di=0, p=0):
    """Barabasi-Albert model generator
        Adding nodes
        m - number of nodes to evolve
        m0 - number of initial nodes
        r - coefficient of bribery
        n - number of edges of each new node
        di - 1 -make directed graph, 0 - usual graph
        p - probabilty of not concidering parametr r
    """
    # Initializing graph
    if di:
        aGraph = nx.DiGraph()
    else:
        aGraph = nx.Graph()
    aGraph.probability = {}
    name = "ba_m=" + repr(m) + "_r=" + repr(r) + \
           "_n=" + repr(n) + "_p=" + repr(p)
    aGraph.name = name

    # Add first m0 nodes
    aGraph.add_node(0)
    for new in xrange(1, m0):
        aGraph.add_node(new)
        aGraph.add_edge(new - 1, new)
    # Calculating probability for first m0 nodes
    sumk = float(aGraph.number_of_edges() * 2)
    for k in xrange(m0):
        aGraph.probability[k] = aGraph.degree(k) / sumk

    # Generating new nodes
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


def evolve_ba_with_briebery_adj(m, m0, r, n, di=0, p=0):
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

    # Because matrix index are from 0 to m-1
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
    # Initializing graph
    aGraph = nx.Graph()
    aGraphRemovedEdges = nx.Graph()
    name = "flower_decor_x=" + repr(x) + "_y=" + repr(y) + \
           "_n=" + repr(n)
    aGraph.name = name

    # Add first 2 nodes and 1 edge
    aGraph.add_node(0)
    aGraph.add_node(1)
    aGraph.add_edge(0, 1)

    # Generating new nodes
    for iterations in xrange(1, n):
        # List of edges
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


def evolve_decorated_flower_adj(x, y, n, r=0., p=0.8):
    """(x,y) flower network generator by adjacency matrix
        x, y - number of nodes on edges
        n - number of transformation of all edges
        p - probability of offset
        r - briebery
    """

    import math

    def numberOfEdgesAndNodes():
        numberOfEdges = []
        numberOfEdges.append(3)

        for i in xrange(1, n):
            numberOfEdges.append(numberOfEdges[-1] * (x + y))

        numberOfNodes = []
        numberOfNodes.append(3)
        for i in xrange(1, n):
            numberOfNodes.append((x + y) * numberOfNodes[-1] - (x + y))
        return numberOfNodes, numberOfEdges

    def get_probability_y(nodes, substracted=0):

        probabiltyMask = [0.57,0.88,0.98,1]
        probability = random.random()

        intervals = nodes/4
        segments = [intervals, 2*intervals, 3*intervals, nodes]

        if substracted:
            segments.append(nodes-substracted)
            segments = [i for i in segments if i<=nodes-substracted]
            segments = list(set(segments))
            segments.sort()

        if probability<=probabiltyMask[0]:
            yProbability = random.randint(1, segments[0])
        elif probability<=probabiltyMask[1] and len(segments)>=2:
            yProbability = random.randint(segments[0], segments[1])
        elif probability<=probabiltyMask[1] and len(segments)>=3:
            yProbability = random.randint(segments[1], segments[2])
        elif probability<=probabiltyMask[1] and len(segments)>=4:
            yProbability = random.randint(segments[2], segments[3])
        else:
            yProbability = random.randint(1, nodes-substracted)


        return yProbability

    def get_yi(xI):
        if xI > (numNodes[i] - exceptiveRx):
            yI = get_probability_y(numNodes[i - 1], exceptiveRy)
        elif xI < (numNodes[i - 1] + numNodes[i - 2]):
            yI = get_probability_y(numNodes[i - 1], numNodes[i - 2])
            # yI = random.randint(1, numNodes[i - 1])
        else:
            yI = get_probability_y(numNodes[i - 1])

        # if xI > (numNodes[i] - exceptiveRx):
        # if (numNodes[i-1]-exceptiveRy)>numNodes[i-2]:
        #         if random.random()<p:
        #             yI = random.randint(1, numNodes[i-2])
        #         else:
        #             yI = random.randint(1, numNodes[i-1]-exceptiveRy)
        #     else:
        #         yI = random.randint(1, numNodes[i-1]-exceptiveRy)
        # elif xI < (numNodes[i - 1] + numNodes[i - 2]):
        #     if (numNodes[i - 1]-numNodes[i-2])>numNodes[i-2]:
        #         if random.random()<p:
        #             yI = random.randint(1, numNodes[i-2])
        #         else:
        #             yI = random.randint(1, numNodes[i - 1]-numNodes[i-2])
        #     else:
        #         yI = random.randint(1, numNodes[i - 1]-numNodes[i-2])
        # else:
        #     if random.random()<p:
        #         yI = random.randint(1, numNodes[i-2])
        #     else:
        #         yI = random.randint(1, numNodes[i - 1])
        return yI

    if x < 1 or y < 2 or n < 2:
        return "Error in input data"

    # Generate init generation
    edgeList = []
    edgeList.append([1, 4])
    edgeList.append([1, 3])
    edgeList.append([1, 2])
    edgeList.append([1, 6])
    edgeList.append([2, 3])
    edgeList.append([2, 5])
    edgeList.append([2, 6])
    edgeList.append([3, 4])
    edgeList.append([3, 5])

    numNodes, numEdges = numberOfEdgesAndNodes()
    # print numNodes, numEdges
    for i in xrange(2, n):
        exceptiveRy = math.trunc(r * numNodes[i - 1])
        # exceptiveRx = math.trunc(r * numNodes[i - 1])
        exceptiveRx = math.trunc(r * (numNodes[i] - numNodes[i - 1]))
        squareR = math.trunc(r * numNodes[i - 1])
        for xI in xrange(numNodes[i - 1], numNodes[i] + 1):
            yI = get_yi(xI)
            edgeList.append([xI, yI])

        while len(edgeList) < numEdges[i]:
            xI = random.randint(numNodes[i - 1], numNodes[i])
            interval = (numNodes[i] - numNodes[i-1])/4
            if xI <= (numNodes[i-1]+interval):
                pass
            elif (numNodes[i-1]+interval)<=xI<=(numNodes[i-1]+2*interval):
                pass
            elif (numNodes[i-1]+2*interval)<=xI<=(numNodes[i-1]+3*interval):
                pass
            else:
                pass

            yI = get_yi(xI)

            # if (2 * numNodes[i - 1] - numNodes[i - 2]) < xI < (numNodes[i] - squareR):
            # if random.random() < p:
            #         yI = random.randint(1, numNodes[i - 2])
            #     else:
            #         yI = random.randint(numNodes[i - 2], numNodes[i - 1])
            # elif xI <= (2 * numNodes[i - 1] - numNodes[i - 2]):
            #     if random.random() < p:
            #         yI = random.randint(1, numNodes[i - 2])
            #     else:
            #         yI = random.randint(numNodes[i - 2], numNodes[i - 1] - numNodes[i - 2])
            # elif xI >= (numNodes[i] - squareR):
            #     yI = random.randint(1, numNodes[i - 1] - squareR)
            #
            if [xI, yI] not in edgeList:
                edgeList.append([xI, yI])

    aGraph = nx.from_edgelist(edgeList)
    name = "flower_decor_adj_x=" + repr(x) + "_y=" + repr(y) + \
           "_n=" + repr(n) + "_r=" + repr(r)
    aGraph.name = name
    return aGraph


def evolve_flower(x, y, n):
    """(x,y) flower network generator
        x, y - number of nodes on edges
        n - number of transformation of all edges
    """
    if x < 1 or y < 2 or n < 2:
        return "Error in input data"
    # Initializing graph
    aGraph = nx.Graph()
    name = "flower_x=" + repr(x) + "_y=" + repr(y) + \
           "_n=" + repr(n)
    aGraph.name = name

    # Add first 2 nodes and 1 edge
    aGraph.add_node(0)
    aGraph.add_node(1)
    aGraph.add_edge(0, 1)

    # Generating new nodes
    for iterations in xrange(1, n):
        # List of edges
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


def evolve_flower_removing_edges(x, y, n, r=0):
    """(x,y) flower network generator
        x, y - number of nodes on edges
        n - number of transformation of all edges
    """
    import numpy as np
    import math
    from scipy import sparse

    def numberOfEdgesAndNodes(startEdge, startNode):
        numberOfEdges = []
        numberOfEdges.append(startEdge)
        for i in xrange(1, n):
            numberOfEdges.append(numberOfEdges[-1] * (x + y))

        numberOfNodes = []
        numberOfNodes.append(startNode)
        for i in xrange(1, n):
            numberOfNodes.append((x + y) * numberOfNodes[-1] - (x + y))
        return numberOfNodes, numberOfEdges



    def remove_edges():
        adj = nx.adjacency_matrix(aGraph)
        adj_temp = adj.nonzero()
        row = adj_temp[0]
        col = adj_temp[1]

        removedItems = []

        for gen in xrange(2, n):
            item = 0
            len_adj = row.shape[0]

            xMin = -1 + numberOfNodes[gen] - r * (numberOfNodes[gen] - numberOfNodes[gen-1])
            xMax = -1 + numberOfNodes[gen]
            yMin = -1 + numberOfNodes[gen-1] - r * numberOfNodes[gen-1]
            yMax = -1 + numberOfNodes[gen-1]

            for element in xrange(len_adj - 1, -1, -1):
                if xMin <= row[element] <= xMax:
                    if yMin <= col[element] <= yMax:
                        row = np.delete(row, element)
                        col = np.delete(col, element)
                        item += 1
                elif yMin <= row[element] <= yMax:
                    if xMin <= col[element] <= xMax:
                        row = np.delete(row, element)
                        col = np.delete(col, element)
                        item += 1
            removedItems.append(item)

        data = np.array([1 for i in xrange(row.shape[0])])
        mtx = sparse.csr_matrix((data, (row, col)))

        return nx.from_scipy_sparse_matrix(mtx), removedItems

    def add_new_edges(aGraph, removed):

        def get_yi(xI):

            if xI > (numberOfNodes[i] - exceptiveRx):
                yI = random.randint(1, numberOfNodes[i - 1] - exceptiveRy)
            elif xI < (numberOfNodes[i - 1] + numberOfNodes[i - 2]):
                yI = random.randint(1, numberOfNodes[i - 1] - numberOfNodes[i - 2])
                # yI = random.randint(1, numberOfNodes[i - 1])
            else:
                yI = random.randint(1, numberOfNodes[i - 1])
            return yI

        edgeList = aGraph.edges()
        for i in xrange(2, n):
            exceptiveRy = math.trunc(r * numberOfNodes[i - 1])
            # exceptiveRx = math.trunc(r * numberOfNodes[i - 1])
            exceptiveRx = math.trunc(r * (numberOfNodes[i] - numberOfNodes[i - 1]))
            squareR = math.trunc(r * numberOfNodes[i - 1])


            for j in xrange(removed[i-2]):
                xI = random.randint(numberOfNodes[i - 1], numberOfNodes[i])
                yI = get_yi(xI)
                # print i, xI, yI
                if [xI, yI] not in edgeList:
                    edgeList.append([xI, yI])

        aGraph = nx.from_edgelist(edgeList)
        return aGraph

    n += 1
    if x < 1 or y < 2 or n < 2:
        return "Error in input data"
    # Initializing graph
    aGraph = nx.Graph()
    name = "flower_x=" + repr(x) + "_y=" + repr(y) + \
           "_n=" + repr(n)
    aGraph.name = name

    # Add first 2 nodes and 1 edge
    aGraph.add_node(0)
    aGraph.add_node(1)
    aGraph.add_edge(0, 1)

    numberOfNodes, numberOfEdges = numberOfEdgesAndNodes(1, 2)
    # Generating new nodes
    for generation in xrange(1, n):
        # List of edges
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

    if r != 0:
        aGraph, removed = remove_edges()
        aGraph = add_new_edges(aGraph, removed)
    # print len(aGraph.edges())
    name = "flower_removing_x=" + repr(x) + "_y=" + repr(y) + \
           "_n=" + repr(n - 1) + "_r=" + repr(r)
    aGraph.name = name
    return aGraph


def evolve_flower_with_briebery(x, y, n, r=0, p=0):
    """(x,y) flower network generator
        x, y - number of nodes on edges
        n - number of transformation of all edges
        r - coeficient of bribery
        p - probabilty of not concidering parametr r
    """
    if x < 1 or y < 2 or n < 2:
        return "Error in input data"
    # Initializing graph
    aGraph = nx.Graph()
    aGraph.probability = {}
    name = "flower_x=" + repr(x) + "_y=" + repr(y) + \
           "_n=" + repr(n) + "_r=" + repr(r)
    aGraph.name = name

    # Add first 2 nodes and 1 edge
    aGraph.add_node(0)
    aGraph.add_node(1)
    aGraph.add_edge(0, 1)

    # Generating new nodes
    for iterations in xrange(1, n):
        # List of edges
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
