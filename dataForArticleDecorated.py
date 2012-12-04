# -*- coding: utf-8 *-*
import matplotlib.pyplot as plt
import networkx as nx

import lib.generator as generator
import lib.calculation as calculation
import lib.graphics as graphics


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
    G = generator.evolve_decorated_flower_adj(1, 2, 8, 0., 0.)
    graphics.make_rank_distribution(G)
    G = generator.evolve_decorated_flower_adj(1, 2, 8, 0.95, 0.)
    graphics.make_rank_distribution(G)

    print 'Made rank distribution'


def count_rc():
    numberOfRealization = 1
    rcAll = []

    for m in xrange(7, 17, 1):

        r = 0.8
        rc = 0

        while r < 1:

            for i in xrange(numberOfRealization):
                G = generator.evolve_decorated_flower_adj(1, 2, m, r, 0.)
                nyutemp = calculation.calculate_nyu_decorated(G)
                if nyutemp:
                    rc = r

            if rc:
                rcAll.append(rc)
                break

            r += 0.01

    #Saving to file
    fc = open('data/rcDecor.txt', 'w')
    for rc in rcAll:
        fc.write(str(rc) + '\n')
    fc.close()

    plt.plot(rcAll, range(7, 17, 1), 'ro')
    fname = "Graphics/rcDecor.png"
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
            G = generator.evolve_decorated_flower_adj(1, 2, 10, r, 0.)

            nyuAv.append(calculation.calculate_nyu_decorated(G))
            cAv.append(nx.average_clustering(G))
#            spAv.append(nx.average_shortest_path_length(G))
            asortAv.append(nx.degree_assortativity_coefficient(G))

        nyu = sum(nyuAv) / float(numberOfRealization)
        c = sum(cAv) / float(numberOfRealization)
#        sp = sum(spAv)/float(numberOfRealization)
        asort = sum(asortAv) / float(numberOfRealization)

        nyuAll.append(nyu)
        cAll.append(c)
#        spAll.append(sp)
        asortAll.append(asort)

        xi.append(float(r - rc) / rc)
        r += 0.001

    print 'Yes! It`s done! Writing data to file.'

    #Saving parametrs to file
    fc = open('data/findTxDecor.txt', 'w')
    for x in xi:
        fc.write(str(x) + '\n')
    fc.close()

    fc = open('data/findTEttaDecor.txt', 'w')
    for nyu in nyuAll:
        fc.write(str(nyu) + '\n')
    fc.close()

    fc = open('data/findTcDecor.txt', 'w')
    for c in cAll:
        fc.write(str(c) + '\n')
    fc.close()

#    fc = open('data/findTspDecor.txt', 'w')
#    for sp in spAll:
#        fc.write(str(sp) + '\n')
#    fc.close()

    fc = open('data/findTasortDecor.txt', 'w')
    for asort in asortAll:
        fc.write(str(asort) + '\n')
    fc.close()

    print 'Making plots.'

    try:
        make_parametr_plot(xi, nyuAll, 'nyuLogLogDecor')
    except:
        print 'nyuLogLogDecor - error!'
    try:
        make_parametr_plot(xi, cAll, 'clusteringLogLogDecor')
    except:
        print 'clusteringLogLogDecor - error!'
    try:
        make_parametr_plot(xi, spAll, 'spLogLogDecor')
    except:
        print 'spLogLogDecor - error!'
    try:
        make_parametr_plot(xi, asortAll, 'asortLogLogDecor')
    except:
        print 'asortLogLogDecor - error!'

    try:
        make_parametr_plot(xi, nyuAll, 'nyuDecor', log=0)
    except:
        print 'nyuDecor - error!'
    try:
        make_parametr_plot(xi, cAll, 'clusteringDecor', log=0)
    except:
        print 'clusteringDecor - error!'
    try:
        make_parametr_plot(xi, spAll, 'spDecor', log=0)
    except:
        print 'spDecor - error!'
    try:
        make_parametr_plot(xi, asortAll, 'asortDecor', log=0)
    except:
        print 'asortDecor - error!'

if __name__ == '__main__':

    make_dir()

    count_rank_distribution()

    rc = count_rc()

    count_parametrs(rc)

    print 'End'
