import networkx as nx
import numpy.linalg
import matplotlib.pyplot as plt

import lib.generator as generator
import lib.graphics as graphics
import lib.matrix as matrix
import lib.calculation as calculation

G = generator.evolve_decorated_flower(1, 2, 4)
mapping={8: '10', 9:'11'}
H=nx.relabel_nodes(G,mapping)
matrix.write_image_from_matrix(H, '2')