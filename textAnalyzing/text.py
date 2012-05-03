# -*- coding: utf-8 *-*


import networkx as nx
import random
import string
import lib.graphics as graphics

import matplotlib.pyplot as plt

def words_in_line(line):
    line = line.replace(u':', u' ')
    line = line.replace(u';', u' ')
    line = line.replace(u'!', u' ')
    line = line.replace(u'?', u' ')
    line = line.replace(u'.', u' ')
    line = line.replace(u',', u' ')
    line = line.replace(u'*', u' ')
    #Maybe defis in one word
    line = line.replace(u'—', u'')
    line = line.replace(u'-', u'')

    line = line.replace(u')', u' ')
    line = line.replace(u'(', u' ')
    line = line.replace(u'»', u' ')
    line = line.replace(u'«', u' ')
    line = line.replace(u'"', u' ')
    line = line.replace(u'\'', u' ')
    return line.lower().split()


def make_graph_from_line(aGraph, line):
    lenOfLine = len(line) - 1

    for iterator in xrange(lenOfLine):
        aGraph.add_node(line[iterator])
        aGraph.add_node(line[iterator+1])
        aGraph.add_edge(line[iterator], line[iterator+1])
    return aGraph


if __name__ == "__main__":

    file = open('input.txt', 'r')
    fileO = open('output.txt', 'w')

    all = []
    lastPrev = None

    for line in file:
        line = line.decode('utf-8')
        line = words_in_line(line)
        #If line not empty
        if line:
            all.extend(line)

#    for i in xrange(5):
    random.shuffle(all)

#    for word in all:
#        word = word + ' '
#        fileO.write(word.encode('utf-8'))

    G = nx.Graph()
    G.name = 'words'
    make_graph_from_line(G, all)
    del all

#    graphics.make_probability_graphic(G)
#    graphics.make_betweenness_graphic(G)
#    graphics.make_rank_distribution(G)

    print nx.average_clustering(G)
    print nx.average_shortest_path_length(G)
    print nx.degree_assortativity_coefficient(G)
    print nx.info(G)
#
#    nx.draw(G)
#    plt.show()
