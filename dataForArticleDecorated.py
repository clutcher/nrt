# -*- coding: utf-8 *-*
import networkx as nx

import lib.generator as generator
import lib.calculation as calculation

numberOfRealization = 15
numberOfRealizationRc = 1
generation = 8


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

    for m in xrange(7, 12, 1):

        r = 0.84
        rc = 0

        while r < 1:

            for i in xrange(numberOfRealizationRc):
                G = generator.evolve_decorated_flower_adj(1, 2, m, r, 0.)
                nyutemp = calculation.calculate_nyu_decorated(G)
                if nyutemp:
                    rc = r

            if rc:
                rcAll.append(rc)
                break
            r += 0.01
        print rcAll
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
    # try:
    while r < 0.83:
        print r
        nyuAv = []
        cAv = []
        spAv = []
        asortAv = []

        for i in xrange(numberOfRealization):
            G = generator.evolve_decorated_flower_adj(1, 2, generation, r)
            nyuTmp = calculation.calculate_nyu_decorated(G)
            if nyuTmp:
                nyuAv.append(nyuTmp)
            # cAv.append(nx.average_clustering(G))
            # spComponent = 0
            # for spGraph in nx.connected_component_subgraphs(G):
            #     spComponent += nx.average_shortest_path_length(spGraph)
            # spAv.append(float(spComponent) / len(nx.connected_component_subgraphs(G)))
            # giant = next(nx.connected_component_subgraphs(G))
            # spAv.append(nx.average_shortest_path_length(giant))
            # asortAv.append(nx.degree_assortativity_coefficient(G))

        if len(nyuAv) != 0:
            nyu = sum(nyuAv) / float(len(nyuAv))
        else:
            nyu = 0
        # c = sum(cAv) / float(numberOfRealization)
        # sp = sum(spAv) / float(numberOfRealization)
        # asort = sum(asortAv) / float(numberOfRealization)

        nyuAll.append(nyu)
        # cAll.append(c)
        # spAll.append(sp)
        # asortAll.append(asort)

        # xi.append(float(r - rc) / rc)
        xi.append(r)
        r += 0.005
    # except:
    #     pass
    print 'Yes! It`s done! Writing data to file.'

    #Saving parametrs to file
    fc = open('data-flower/x.txt', 'w')
    for x in xi:
        fc.write(str(x) + '\n')
    fc.close()

    fc = open('data-flower/etta-razriv.txt', 'w')
    for nyu in nyuAll:
        fc.write(str(nyu) + '\n')
    fc.close()

    # fc = open('data-flower/clustering.txt', 'w')
    # for c in cAll:
    #     fc.write(str(c) + '\n')
    # fc.close()

    # fc = open('data-flower/shortpath.txt', 'w')
    # for sp in spAll:
    #     fc.write(str(sp) + '\n')
    # fc.close()

    # fc = open('data-flower/asortativity.txt', 'w')
    # for asort in asortAll:
    #     fc.write(str(asort) + '\n')
    # fc.close()

    # fX = open('data/eta_findTxDecor.txt', 'w')
    # fE = open('data/etafindTEttaDecor.txt', 'w')
    # for i, nyu in enumerate(nyuAll):
    #     if nyu != 0:
    #         fE.write(str(nyu) + '\n')
    #         fX.write(str(xi[i]) + '\n')
    # fX.close()
    # fE.close()

if __name__ == '__main__':
    make_dir()

    # count_rank_distribution()

    # rc = count_rc()
    rc = 0.6
    count_parametrs(rc)
    # print rc
    print 'End'
