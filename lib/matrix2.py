from PIL import Image
import networkx as nx
import os

def write_image_from_matrix(aGraph):

    try:
        os.makedirs('Graphics/adj')
    except OSError:
        pass

    adj = nx.adjacency_matrix(aGraph)
    adj_non_zero = adj.nonzero()
    adjacency_matrix = zip(adj_non_zero[0], adj_non_zero[1])

    width = len(aGraph)
    im = Image.new("RGB", (width, width), "white")
    adjacency_matrix = zip(adj_non_zero[0], adj_non_zero[1])
    for item in adjacency_matrix:
        im.putpixel(item, (0,0,0))

    fname = "Graphics/adj/" + aGraph.name + ".png"
    im.save(fname)

