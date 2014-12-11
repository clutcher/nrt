import lib.generator as generator
import numpy as np

import matplotlib
from matplotlib import rc
import matplotlib.pyplot as plt
import scipy.optimize

matplotlib.use('Agg')
rc('text', usetex=True)

def sigmoid_curve(x, a, b, c):
    y =b*(x**(-c))
    return y


def get_fit_params(xi, yi):
    popt, pcov = scipy.optimize.curve_fit(sigmoid_curve, xi, yi, p0=None, maxfev=100000000)
    return popt

def make_rank_distribution(aGraph):
    # plt.title("Rank distribution")
    yi = list(aGraph.degree().values())
    yi.sort(reverse=True)
    xi = [x for x in xrange(len(yi))]
    plt.plot(xi, yi, 'o', mfc='none', mec='r')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel("rank")
    plt.ylabel("degree")
    fname = aGraph.name + ".png"
    plt.savefig(fname)
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

    firstvalue = yi[0]
    linestyle = 'None'

    for i, value in enumerate(yi):
        yi[i] = yi[i]/firstvalue


    # xi = [(x-0.75)/0.75 for x in xi[:]]

    # xi = [math.log(x) for x in xi]
    # yi = [math.log(y/firstvalue) for y in yi[55:]]
    # xi = xi[201:]
    # xi = [x/0.51 for x in xi]
    # yi = yi[201:]
    # yi = [y/firstvalue for y in yi]

    # plt.xlim([0.4,0.7])
    # plt.ylim([0,1.5])

    # plt.xlim([xi[0],xi[-1]])
    # plt.ylim([1,10])
    if 'Asort' in name:
        mfc = color = 'b'
        mfc = 'w'
        marker = 'o'

    elif 'Clustering' in name:
        mfc = color = 'r'
        mfc = 'w'
        marker = 's'

    elif 'Short' in name:
        mfc = color = 'k'
        mfc = 'w'
        marker = 'd'

    else:
        color = 'r'
        mfc = 'w'
        marker = 'o'
        linestyle = 'None'

    plt.plot(xi, yi, marker, linestyle=linestyle, mfc=mfc, mec=color, color=color, label=ylabel)
    plt.xlabel(r'$(r-r_c)/r_c$')
    plt.ylabel('parameters')
    # plt.legend()
    #
    # popt = get_fit_params(xi, yi)
    # print popt
    # y_sigmoid = sigmoid_curve(xi, *popt)
    #
    # mfc = color = 'k'
    # plt.plot(xi, y_sigmoid,'-',mfc=mfc, mec=color, color=color)

    # plt.yscale('log')
    # plt.xscale('log')


# F = generator.evolve_ba_with_briebery(5000, 20, 0.6, 3)
# F = generator.evolve_decorated_flower_adj(1,2,8,0.8)
# make_rank_distribution(F)
# make_coeficient_graphic('data/flower/xManual.txt', 'data/flower/ettaManual.txt', -0.781, 0.448, -0.258, 'ettaManual',
# 'Etta')
# make_coeficient_graphic('data/ba_1/x.txt', 'data/ba_1/asortativity.txt', -0.781, 0.448, -0.258, 'baAsort',
# r'Assortativity $A/A_0$')
# make_coeficient_graphic('data/ba_1/x.txt', 'data/ba_1/clustering.txt', 0.28, 0.543, 0.039, 'baClustering',
# r'Clustering $C/C_0$')
# make_coeficient_graphic('data/ba/x.txt', 'data/ba/s7hortpath.txt', -1.615, 0.516, 3.551, 'baShort',
# 'Shortest path')
# make_coeficient_graphic('data/ba_1/x.txt', 'data/ba_1/etta-razriv.txt', 472.59, 1.303, 2.898, 'baGap',
#                         'gap')


make_coeficient_graphic('data/flower_753/x.txt', 'data/flower_753/asortativity.txt', -1.054, 0.963, -0.181, 'flowerAsort',
                        'Assortativity')
make_coeficient_graphic('data/flower_753/x.txt', 'data/flower_753/clustering.txt', 0.229, 1.216, 0.005919, 'flowerClustering',
                        'Clustering')
# make_coeficient_graphic('data/flower/x.txt', 'data/flower/shortpath.txt', 0.22, 0.817, 1.336, 'flowerShort',
#                         'Shortest path')
# make_coeficient_graphic('data/flower_75/x.txt', 'data/flower_75/etta-razriv.txt', 1.505, 0.256, 3.863, 'flowerGap',
#                         'Gap')

fname = "flowerParams333.eps"
plt.savefig(fname)
plt.show()
plt.close('all')