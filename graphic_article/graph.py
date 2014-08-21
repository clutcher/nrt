import lib.generator as generator

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc

rc('text', usetex=True)


def make_rank_distribution(aGraph):
    # plt.title("Rank distribution")
    yi = list(aGraph.degree().values())
    yi.sort(reverse=True)
    xi = [x for x in xrange(len(yi))]
    plt.plot(xi, yi, 'o', mfc='none', mec='r')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel("Node")
    plt.ylabel("Degree")
    fname = aGraph.name + ".eps"
    plt.savefig(fname)
    plt.close('all')


def make_coeficient_graphic(fnameX, fnameY, a, b, c, name, ylabel):
    with open(fnameX) as f:
        lines = f.read().splitlines()
        xi = map(float, lines)

    with open(fnameY) as f:
        lines = f.read().splitlines()
        yi = map(float, lines)

    for i, value in enumerate(yi):
        yi[i] = yi[i] - c

    plt.plot(xi, yi, 'o', mfc='none', mec='r')
    # plt.yscale('log')
    # plt.xscale('log')
    plt.xlabel(r'$\frac{r-r_c}{r_c}$')
    plt.ylabel(ylabel)

    yLine = []
    for x in xi:
        yLine.append(a * (x ** b))
    plt.plot(xi, yLine, 'k')

    fname = name + ".eps"
    plt.savefig(fname)
    plt.close('all')


# BA = generator.evolve_ba_with_briebery(1000, 20, 0.7, 3)
# make_rank_distribution(BA)
# F = generator.evolve_decorated_flower_adj(1,2,11,0.)
# make_rank_distribution(F)
make_coeficient_graphic('data/flower/xManual.txt', 'data/flower/ettaManual.txt', -0.781, 0.448, -0.258, 'ettaManual',
'Etta')
# make_coeficient_graphic('data/ba/x.txt', 'data/ba/asortativity.txt', -0.781, 0.448, -0.258, 'baAsort',
# 'Assortativity')
# make_coeficient_graphic('data/ba/x.txt', 'data/ba/clustering.txt', 0.28, 0.543, 0.039, 'baClustering',
# 'Clustering')
# make_coeficient_graphic('data/ba/x.txt', 'data/ba/shortpath.txt', -1.615, 0.516, 3.551, 'baShort',
# 'Shortest path')
# make_coeficient_graphic('data/ba/x.txt', 'data/ba/etta-razriv.txt', 472.59, 1.303, 2.898, 'baGap',
#                         'Gap')


# make_coeficient_graphic('data/flower/x.txt', 'data/flower/asortativity.txt', -1.054, 0.963, -0.181, 'flowerAsort',
#                         'Assortativity')
# make_coeficient_graphic('data/flower/x.txt', 'data/flower/clustering.txt', 0.229, 1.216, 0.005919, 'flowerClustering',
#                         'Clustering')
# make_coeficient_graphic('data/flower/x.txt', 'data/flower/shortpath.txt', 0.22, 0.817, 1.336, 'flowerShort',
#                         'Shortest path')
# make_coeficient_graphic('data/flower/x-non.txt', 'data/flower/eta-razriv-non.txt', 1.505, 0.256, 3.863, 'flowerGap',
#                         'Gap')