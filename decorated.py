import networkx as nx
import numpy.linalg
import matplotlib.pyplot as plt

import lib.generator as generator
import lib.graphics as graphics
import lib.matrix as matrix

def spectrum(aGraph):
    spectrum = nx.adjacency_spectrum(aGraph)
    freq = range(len(spectrum))
    return spectrum, freq

if __name__ == '__main__':
    G = generator.evolve_decorated_flower(2, 2, 7)
    matrix.write_image_from_matrix(nx.adjacency_matrix(G))
