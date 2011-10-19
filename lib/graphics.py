# -*- coding: utf-8 -*-
"""Graphics drawing"""

import networkx as nx
import matplotlib.pyplot as plt
import math

import calculation


def remove_zeros(yi):
    """Deleting zero y from x"""
    xitemp = []
    yitemp = []
    iterator = 0
    for y in yi:
        iterator += 1
        if y != 0:
            yitemp.append(y)
            xitemp.append(iterator)
        else:
            iterator += 1
    return xitemp, yitemp


def make_graph(aGraph):
    """Make graph of network"""
    plt.figure()
    plt.title("Network graph " + aGraph.name)
    pos = nx.graphviz_layout(aGraph, prog="dot", root=0)
    nx.draw(aGraph, pos, with_labels=False, alpha=0.5,
        node_size=[30 * float(aGraph.degree(v)) for v in aGraph],
        node_color=[float(aGraph.degree(v)) for v in aGraph])
    # Adjust the plot limits
    xmax = 1.02 * max(xx for xx, yy in pos.values())
    ymax = 1.02 * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)
    fname = "Graphics/graph/" + aGraph.name + ".png"
    plt.savefig(fname)


def make_probability_graphic(aGraph):
    """Make a probability graphic with log axes and
       outputting alpha p ~ k^(-a)
    """
    fig = plt.figure()
    plt.title("Probability graph " + aGraph.name)
    plt.yscale('log')
    plt.xscale('log')
    histTemp = nx.degree_histogram(aGraph)
    doubleNumberOfEdges = 2 * aGraph.number_of_edges()
    yi = []
    # p ~ k^(-a)
    ai = []
    #iterator - degree for nodes with p probability
    iterator = 0
    a = 0.0
    #Calculating probability and alpha
    for y in histTemp:
        p = float(y) / doubleNumberOfEdges
        yi.append(p)
        if y > 0 and iterator > 1:
            ai.append(math.log(1 / p, iterator))
        iterator += 1

    for i in ai:
        a += i
    a = a / len(ai)

    xi = range(len(yi))

    xi, yi = remove_zeros(yi)
    plt.plot(xi, yi, 'ro')
    plt.xlim(0, len(xi))
    #Outputing alpha
    text = "alpha= " + repr(a)
    plt.text(1, 0.01, text)

#    @fixme interpolate by logarithm
    #Interpolation line
#    xitemp = []
#    yitemp = []
#    for x in xi:
#        xitemp.append(math.exp(x))
#    for y in yi:
#        yitemp.append(math.exp(y))
#    xi = xitemp
#    yi = yitemp
    func = calculation.calculate_interpolation_line(xi, yi)
    yi = []
    n = int(math.ceil(max(xi)) + 1)
    for x in xrange(n):
        yi.append(func[1] * x + func[2])
    plt.plot(range(n), yi, 'k')
    text = "Angle= " + repr(func[0])
    plt.text(1, 0.02, text)
    plt.xlabel("Degree of nodes")
    plt.ylabel("Probability P(k)")
    fname = "Graphics/probability/" + aGraph.name + ".png"
    plt.savefig(fname)
    return fig


def make_degree_histogram(aGraph):
    """Make a histogram of degrees"""
    fig = plt.figure()
    plt.title("Degree histogram " + aGraph.name)
    yi = nx.degree_histogram(aGraph)
    xi = range(len(yi))
    plt.bar(xi, yi, align="center")
    plt.xlim(0, len(xi))
    plt.xlabel("Degree of node")
    plt.ylabel("Number of nodes with x degree")
    fname = "Graphics/degree_hist/" + aGraph.name + ".png"
    plt.savefig(fname)
    return fig


def make_rank_distribution(aGraph):
    """Make rank distribution by degree graphic"""
    fig = plt.figure()
    plt.title("Rank distribution")
    yi = list(aGraph.degree().values())
    yi.sort(reverse=True)
    xi = [x for x in xrange(len(yi))]
    plt.plot(xi, yi, 'ro')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel("Node")
    plt.ylabel("Degree")
    fname = "Graphics/rank/" + aGraph.name + ".png"
    plt.savefig(fname)
    return fig


def make_nyu_graphic(nyu, r):
    """Graphic of nyu distribution from r"""
    if len(nyu) != len(r):
        print "Len of nyu or r is invalid!"
        return 0
    fig = plt.figure()
    plt.title("Nyu distribution")
    xi = r
    yi = nyu
    plt.plot(xi, yi, 'ro')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel("r")
    plt.ylabel("Nyu")
    fig.savefig("Graphics/nyu.png")
    return fig


def make_clustering_graphic(cluster, r):
    """Graphic of cluster distribution from r"""
    if len(cluster) != len(r):
        print "Len of cluster or r is invalid!"
        return 0
    fig = plt.figure()
    plt.title("Average clustering distribution")
    xi = r
    yi = cluster
    plt.plot(xi, yi, 'ro')
#    plt.yscale('log')
#    plt.xscale('log')
    plt.xlabel("r")
    plt.ylabel("Average clustering")
    fig.savefig("Graphics/cluster.png")
    return fig


def make_shortest_path_graphic(shortpath, r):
    """Graphic of average shortest path distribution from r"""
    if len(shortpath) != len(r):
        print "Len of shortest path or r is invalid!"
        return 0
    fig = plt.figure()
    plt.title("Average shortest path distribution")
    xi = r
    yi = shortpath
    plt.plot(xi, yi, 'ro')
#    plt.yscale('log')
#    plt.xscale('log')
    plt.xlabel("r")
    plt.ylabel("Average shortest path")
    fig.savefig("Graphics/shortpath.png")
    return fig
