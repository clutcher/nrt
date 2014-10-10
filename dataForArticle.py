# -*- coding: utf-8 *-*
import networkx as nx

import lib.generator as generator
import lib.calculation as calculation


global n
global numberOfRealization
global step

n = 5000
numberOfRealization = 5
step = 0.01


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


def count_rc():
    rcAll = []

    for m in xrange(100, n, 500):

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

            r += step

    #Saving to file
    fc = open('data/rc-y.txt', 'w')
    for rc in rcAll:
        fc.write(str(rc) + '\n')
    fc.close()

    fc = open('data/rc-x.txt', 'w')
    for x in xrange(100, n, 500):
        fc.write(str(x) + '\n')
    fc.close()

    print 'Found rc'
    return rc


def count_parametrs(rc):
    nyu = []
    xi = []
    r = 0.0
    nyuAv = []
    nyuAll = []
    cAll = []
    cAv = []
    spAll = []
    spAv = []
    asortAll = []
    asortAv = []

    print 'And now we have a lot of computations! Wait a week.'

    while r < 0.9:
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

        # xi.append(float(r - rc) / rc)
        xi.append(r)
        if 0.40 <= r <= 0.60:
            r += step
        else:
            r += 0.01

    print 'Yes! It`s done! Writing data to file.'

    #Saving parametrs to file
    fc = open('data/x.txt', 'w')
    for x in xi:
        fc.write(str(x) + '\n')
    fc.close()

    fc = open('data/etta-razriv.txt', 'w')
    for nyu in nyuAll:
        fc.write(str(nyu) + '\n')
    fc.close()

    fc = open('data/clustering.txt', 'w')
    for c in cAll:
        fc.write(str(c) + '\n')
    fc.close()

    fc = open('data/shortpath.txt', 'w')
    for sp in spAll:
        fc.write(str(sp) + '\n')
    fc.close()

    fc = open('data/asortativity.txt', 'w')
    for asort in asortAll:
        fc.write(str(asort) + '\n')
    fc.close()


if __name__ == '__main__':
    make_dir()

    # count_rank_distribution()

    # rc = count_rc()
    rc = 0.51
    count_parametrs(rc)

    print 'End'
