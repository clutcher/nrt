# -*- coding: utf-8 *-*
import matplotlib.pyplot as plt
import networkx as nx

import lib.generator as generator
import lib.calculation as calculation


if __name__ == '__main__':

    nyu = []
    xi = []
    numberOfRealization = 5
    flag = 1
    r = 0.50
    rc = 0
    nyuAv = []
    nyuAll = []

    while r<1:
        print r
        for i in xrange(numberOfRealization):
            G = generator.evolve_ba_with_briebery(5000, 20, r, 3, 0, 0)
            nyuTemp = calculation.calculate_nyu(G)
            if (nyuTemp != 0) and flag:
                #-0.0001 to avoid log 0 in graphics
                rc = r - 0.00001
                flag = 0
            nyuAv.append(nyuTemp)
        nyu = sum(nyuAv)/10.0
        if rc:
            nyuAll.append(nyu)
            xi.append(float(r-rc)/rc)

        if r<0.525:
            r += 0.0001
        elif r<0.6:
            r += 0.001
        else:
            r += 0.01

    #Saving to file x and nyu
    fc = open('data/findTx.txt', 'w')
    for x in xi:
        fc.write(str(x) + '\n')
    fc.close()

    fc = open('data/findTEtta.txt', 'w')
    for nyu in nyuAll:
        fc.write(str(nyu) + '\n')
    fc.close()

#    #Calculating least square
#    length = len(xi)
#    startP = int(length*0.2)
#    endP = int(length*0.8)
#    c, t = calculation.calculate_degree_least_square(xi[startP:endP], nyuAll[startP:endP])
#    print t
#
#    #Making plot
#    plt.yscale('log')
#    plt.xscale('log')
#    plt.title(str(t))
#
#    plt.plot(xi, nyuAll, 'ro')
#
#    yi = []
#    for x in xi:
#        yi.append(c * (x ** t))
#    plt.plot(xi, yi, 'k')
#
#    plt.show()

