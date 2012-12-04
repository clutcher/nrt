# -*- coding: utf-8 *-*
import matplotlib.pyplot as plt
import networkx as nx

import lib.generator as generator
import lib.calculation as calculation
import lib.graphics as graphics

global n
n = 5000


def make_dir():
    import os

    try:
        os.makedirs('Graphics/')
    except OSError:
        pass
    try:
        os.makedirs('Graphics/article/')
    except OSError:
        pass
    try:
        os.makedirs('data')
    except OSError:
        pass


def count_rank_distribution():
    G = generator.evolve_ba_with_briebery(n, 20, 0, 3)
    graphics.make_rank_distribution(G)
    G = generator.evolve_ba_with_briebery(n, 20, 0.6, 3)
    graphics.make_rank_distribution(G)

    print 'Made rank distribution'


def count_rc():
    numberOfRealization = 10
    rcAll = []

    for m in xrange(100, 10000, 500):

        r = 0.49
        rc = 0

        while r < 1:

            for i in xrange(numberOfRealization):
                G = generator.evolve_ba_with_briebery(m, 20, r, 3)
                nyutemp = calculation.calculate_nyu(G)
                if nyutemp:
                    rc = r

            if rc:
                rcAll.append(rc)
                break

            r += 0.001

    #Saving to file
    fc = open('data/rc.txt', 'w')
    for rc in rcAll:
        fc.write(str(rc) + '\n')
    fc.close()

    plt.plot(rcAll, range(100, 10000, 500), 'ro')
    fname = "Graphics/rc.png"
    plt.savefig(fname)
    plt.close('all')

    print 'Found rc'
    return rc


def make_parametr_plot(xi, param, fileName, log=1):

    xi, param = graphics.remove_zeros(xi, param)
    param, xi = graphics.remove_zeros(param, xi)

    #Calculating least square
    length = len(xi)
    startP = int(length * 0.2)
    endP = int(length * 0.8)
    c, t = calculation.calculate_degree_least_square(xi[startP:endP], param[startP:endP])

    plt.title(str(t))

    #Making plot
    if log:
        plt.yscale('log')
        plt.xscale('log')
    plt.plot(xi, param, 'ro')

    #Making approximation line
    yi = []
    for x in xi:
        yi.append(c * (x ** t))
    plt.plot(xi, yi, 'k')

    fname = "Graphics/article/" + fileName + ".png"
    plt.savefig(fname)
    plt.close('all')


def count_parametrs(rc):
    nyu = []
    xi = []
    numberOfRealization = 10
    r = rc
    nyuAv = []
    nyuAll = []
    cAll = []
    cAv = []
    spAll = []
    spAv = []
    asortAll = []
    asortAv = []

    print 'And now we have a lot of computations! Wait a week.'

    while r < rc + 0.1:
        nyuAv = []
        cAv = []
        spAv = []
        asortAv = []

        for i in xrange(numberOfRealization):
            G = generator.evolve_ba_with_briebery(n, 20, r, 3)

            nyuAv.append(calculation.calculate_nyu(G))
            cAv.append(nx.average_clustering(G))
            spAv.append(nx.average_shortest_path_length(G))
            asortAv.append(nx.degree_assortativity_coefficient(G))

        nyu = sum(nyuAv) / float(numberOfRealization)
        c = sum(cAv) / float(numberOfRealization)
        sp = sum(spAv) / float(numberOfRealization)
        asort = sum(asortAv) / float(numberOfRealization)

        nyuAll.append(nyu)
        cAll.append(c)
        spAll.append(sp)
        asortAll.append(asort)

        xi.append(float(r - rc) / rc)
        r += 0.0001

    print 'Yes! It`s done! Writing data to file.'

    #Saving parametrs to file
    fc = open('data/findTx.txt', 'w')
    for x in xi:
        fc.write(str(x) + '\n')
    fc.close()

    fc = open('data/findTEtta.txt', 'w')
    for nyu in nyuAll:
        fc.write(str(nyu) + '\n')
    fc.close()

    fc = open('data/findTc.txt', 'w')
    for c in cAll:
        fc.write(str(c) + '\n')
    fc.close()

    fc = open('data/findTsp.txt', 'w')
    for sp in spAll:
        fc.write(str(sp) + '\n')
    fc.close()

    fc = open('data/findTasort.txt', 'w')
    for asort in asortAll:
        fc.write(str(asort) + '\n')
    fc.close()

    print 'Making plots.'

    #Making plots
    try:
        make_parametr_plot(xi, nyuAll, 'nyuLogLog')
    except:
        print 'nyuLogLog - error!'
    try:
        make_parametr_plot(xi, cAll, 'clusteringLogLog')
    except:
        print 'clusteringLogLog - error!'
    try:
        make_parametr_plot(xi, spAll, 'spLogLog')
    except:
        print 'spLogLog - error!'
    try:
        make_parametr_plot(xi, asortAll, 'asortLogLog')
    except:
        print 'asortLogLog - error!'

    make_parametr_plot(xi, nyuAll, 'nyu', log=0)
    make_parametr_plot(xi, cAll, 'clustering', log=0)
    make_parametr_plot(xi, spAll, 'sp', log=0)
    make_parametr_plot(xi, asortAll, 'asort', log=0)


if __name__ == '__main__':

    make_dir()

    count_rank_distribution()

    rc = count_rc()

    count_parametrs(rc)

    print 'End'
