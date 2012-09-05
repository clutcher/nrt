import networkx as nx
import numpy.linalg
import matplotlib.pyplot as plt

import lib.generator as generator
import lib.graphics as graphics
import lib.matrix as matrix

def spectrum(aGraph):
    spectrum = nx.adjacency_spectrum(aGraph)
    l = len(spectrum)
    freq = {}
    for eigenvalue in spectrum:
        freq[eigenvalue] = 0
    for eigenvalue in spectrum:
        freq[eigenvalue] += 1./l
    return freq

if __name__ == '__main__':
#    G = generator.evolve_ba_with_briebery_adj(1000, 20, 0, 3)
#    graphics.make_rank_distribution(G)
#    matrix.write_image_from_matrix(nx.adjacency_matrix(G))
    #graphics.make_graph(G)
    #frequency = spectrum(G)
    #print frequency.keys()
    #print nx.adjacency_matrix(G)
    #print G.edges()
    #plt.plot(frequency.keys(), frequency.values(), 'ro')
    #plt.show()



#    G = generator.evolve_decorated_flower_adj(1, 2, 7)
#    graphics.make_rank_distribution(G)
#    graphics.make_probability_graphic(G)
##    graphics.make_graph(G)
#    matrix.write_image_from_matrix(G)
#    G1 = generator.evolve_decorated_flower(2, 2, 8)
#    graphics.make_rank_distribution(G1)
#    graphics.make_probability_graphic(G1)
##    graphics.make_graph(G1)
##    matrix.write_image_from_matrix(G1)
#    G2 = generator.evolve_flower(1, 2, 8)
#    graphics.make_rank_distribution(G2)
#    graphics.make_probability_graphic(G2)
##    graphics.make_graph(G2)
#    matrix.write_image_from_matrix(G2)
    G3 = generator.evolve_ba_with_briebery(1000, 20, 0, 3)
    matrix.write_image_from_matrix(G3)
