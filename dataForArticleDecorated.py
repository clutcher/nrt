# -*- coding: utf-8 *-*
import networkx as nx

import lib.generator as generator
import lib.calculation as calculation

numberOfRealization = 5
generation = 10


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

    for m in xrange(7, 15, 1):

        r = 0.84
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
            print rcAll, r
            r += 0.01

    #Saving to file
    fc = open('data/rcDecor.txt', 'w')
    for rc in rcAll:
        fc.write(str(rc) + '\n')
    fc.close()


    print 'Found rc'
    return rc


def count_parametrs(rc):
    nyu = []
    xi = []
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
            G = generator.evolve_decorated_flower_adj(1, 2, generation, r, 0.)

            nyuAv.append(calculation.calculate_nyu_decorated(G))
            cAv.append(nx.average_clustering(G))
            spComponent = 0
            for spGraph in nx.connected_component_subgraphs(G):
                spComponent += nx.average_shortest_path_length(spGraph)
            spAv.append(float(spComponent) / len(nx.connected_component_subgraphs(G)))
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

    fc = open('data/findTspDecor.txt', 'w')
    for sp in spAll:
        fc.write(str(sp) + '\n')
    fc.close()

    fc = open('data/findTasortDecor.txt', 'w')
    for asort in asortAll:
        fc.write(str(asort) + '\n')
    fc.close()



if __name__ == '__main__':
    make_dir()

    # count_rank_distribution()

    rc = count_rc()
    # rc = 0.89
    count_parametrs(rc)
    # print rc
    print 'End'
