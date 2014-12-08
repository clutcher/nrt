import networkx as nx
import numpy.linalg
import matplotlib.pyplot as plt

import lib.generator as generator
import lib.graphics as graphics
import lib.matrix2 as matrix
import lib.calculation as calculation

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

    r = 0.7
    while r<0.81:
        G = generator.evolve_decorated_flower_adj(1, 2, 8, r)
        nyutemp = calculation.calculate_nyu_decorated(G)
        print r, nyutemp
        r += 0.01

    # for i in xrange(10):
    #     G = generator.evolve_decorated_flower_adj(1, 2, 8, 0)
    #     nyutemp = calculation.calculate_nyu_decorated(G)
    #     print '0: ', nyutemp

    # for i in xrange(10):
    #     G = generator.evolve_decorated_flower_adj(1, 2, 8, 0.65)
    #     nyutemp = calculation.calculate_nyu_decorated(G)
    #     print '0.65: ', nyutemp

    # for i in xrange(10):
    #     G = generator.evolve_decorated_flower_adj(1, 2, 8, 0.8)
    #     nyutemp = calculation.calculate_nyu_decorated(G)
    #     print '0.8: ', nyutemp

#        graphics.make_rank_distribution(G)
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
#    G3 = generator.evolve_ba_with_briebery(1000, 20, 0, 3)
#    matrix.write_image_from_matrix(G3)
#     r = 0.51
#     maxAll = []
#     minAll = []
#     while r<0.92:
#         G = generator.evolve_decorated_flower_adj(1, 2, 7, r)
#         dgr = calculation.calculate_nyu_decorated(G)
#         graphics.make_rank_distribution(G)
#         print r,  dgr
#         r += 0.1
#     r =0.78
#     while r<0.84:
#     G = generator.evolve_decorated_flower_adj(1, 2, 8, 0.81)
    # matrix.write_image_from_matrix(G)
    # graphics.make_rank_distribution(G)
    # dgr = calculation.calculate_nyu_decorated(G)
    # print dgr
        # r = r+0.01
    G = generator.evolve_decorated_flower(1,2,7)
    # print G.number_of_nodes()
    # print G.number_of_edges()
    # matrix.write_image_from_matrix(G)
    # dgr = calculation.calculate_nyu_decorated(G)
    # print dgr, len(G)
    # graphics.make_rank_distribution(G)
    #     print r
    # print minAll
    # print max
    # print nx.average_clustering(G)
    # giant = next(nx.connected_component_subgraphs(G))
    # print nx.average_shortest_path_length(giant)
    # print nx.degree_assortativity_coefficient(G)

    # print nx.average_clustering(G)
    # print G.number_of_edges()
    # matrix.write_image_from_matrix(G)
    # graphics.make_rank_distribution(G)
    # x = [0.77, 0.78, 0.8, 0.9]
    # y = [3., 4., 7., 27.]
    # graphics.make_coeficient_graphic(x, y, 'test')
    # print sorted(G.degree(), reverse=True)
    # G.edges()
    # for edge in G.edges():
    #     print edge
    # mapping=dict(zip(G.nodes(),"abcde"))
    # nx.relabel_nodes(G, mapping, copy=False)