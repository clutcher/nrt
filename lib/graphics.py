# -*- coding: utf-8 -*-
"""Graphics drawing"""

import os
import networkx as nx

import calculation
# matplotlib is imported localy to avoid magic crashes in Windows


def remove_zeros(xi, yi):
    """Deleting zero y from x"""
    xitemp = []
    yitemp = []
    iterator = 0
    for y in yi:
        if y != 0:
            yitemp.append(y)
            xitemp.append(xi[iterator])
            iterator += 1
        else:
            iterator += 1
    return xitemp, yitemp


def make_graph(aGraph):
    """Make graph of network"""
    import matplotlib.pyplot as plt

    plt.title("Network graph " + aGraph.name)
    pos = nx.graphviz_layout(aGraph, prog="dot", root=0)
    nx.draw(aGraph, pos, with_labels=False, alpha=0.5,
        node_size=[30 * float(aGraph.degree(v)) for v in aGraph],
        node_color=[float(aGraph.degree(v)) for v in aGraph])
    try:
        os.makedirs('Graphics/graph')
    except OSError:
        pass
    fname = "Graphics/graph/" + aGraph.name + ".png"
    plt.savefig(fname)
    plt.close('all')


def make_probability_graphic(aGraph):
    """Make a probability graphic with log axes and
       outputting alpha p ~ k^(-a)
    """
    import matplotlib.pyplot as plt

    plt.title("Probability graph " + aGraph.name)
    plt.yscale('log')
    plt.xscale('log')
    histTemp = nx.degree_histogram(aGraph)
    sumk = sum(aGraph.degree().values())
    yi = []
    #Calculating probability
    for y in histTemp:
        p = float(y) / sumk
        yi.append(p)
    xi = range(len(yi))
    #Removing zero points
    xi, yi = remove_zeros(xi, yi)
    plt.plot(xi, yi, 'ro')
    #Making approximation line
    c, t = calculation.calculate_degree_least_square(xi, yi)
    yi = []
    for x in xi:
        yi.append(c * (x ** t))
    plt.plot(xi, yi, 'k')

    text = "t= " + repr(t)
    plt.text(1, 0.01, text)
    plt.xlabel("Degree of nodes")
    plt.ylabel("Probability P(k)")
    try:
        os.makedirs('Graphics/probability')
    except OSError:
        pass
    fname = "Graphics/probability/" + aGraph.name + ".png"
    plt.savefig(fname)
    plt.close('all')


def make_betweenness_graphic(aGraph):
    """ Make betweenness graphic
    """
    import matplotlib.pyplot as plt

    plt.title("Betweenness graph " + aGraph.name)
    plt.yscale('log')
    plt.xscale('log')
    yi = nx.betweenness_centrality(aGraph).values()
    xi = aGraph.nodes()
    plt.plot(xi, yi, 'ro')
    plt.xlabel("Node")
    plt.ylabel("Betweenness")
    try:
        os.makedirs('Graphics/betweenness')
    except OSError:
        pass
    fname = "Graphics/betweenness/" + aGraph.name + ".png"
    plt.savefig(fname)
    plt.close('all')


def make_degree_histogram(aGraph):
    """Make a histogram of degrees"""
    import matplotlib.pyplot as plt

    plt.title("Degree histogram " + aGraph.name)
    yi = nx.degree_histogram(aGraph)
    xi = range(len(yi))
    plt.bar(xi, yi, align="center")
    plt.xlim(0, len(xi))
    plt.xlabel("Degree of node")
    plt.ylabel("Number of nodes with x degree")
    try:
        os.makedirs('Graphics/degree_hist')
    except OSError:
        pass
    fname = "Graphics/degree_hist/" + aGraph.name + ".png"
    plt.savefig(fname)
    plt.close('all')


def make_rank_distribution(aGraph):
    """Make rank distribution by degree graphic"""
    import matplotlib.pyplot as plt

    plt.title("Rank distribution")
    yi = list(aGraph.degree().values())
    yi.sort(reverse=True)
    xi = [x for x in xrange(len(yi))]
    plt.plot(xi, yi, 'ro')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel("Node")
    plt.ylabel("Degree")
    try:
        os.makedirs('Graphics/rank')
    except OSError:
        pass
    fname = "Graphics/rank/" + aGraph.name + ".png"
    plt.savefig(fname)
    plt.close('all')


def make_coeficient_graphic(r, coef, name):
    """Graphic of coefficient distribution from r-rc in log axes"""
    import matplotlib.pyplot as plt

    if len(coef) != len(r):
        print "Length of coeficient or r is invalid!"
        print len(coef), len(r)
        return 0

    title = str(name) + " distribution"
    plt.title(title)
    plt.plot(r, coef, 'ro')
    #Making approximation line
    c, t = calculation.calculate_degree_least_square(r, coef)
    yi = []
    for x in r:
        yi.append(c * (x ** t))
    plt.plot(r, yi, 'k')

    text = "t= " + repr(t)
    plt.text(1, 1, text)

    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel("r-rc")
    plt.ylabel(name)
    try:
        os.makedirs('Graphics')
    except OSError:
        pass
    fname = "Graphics/" + name + ".png"
    plt.savefig(fname)
    plt.close('all')
