# -*- coding: utf-8 -*-

"""Rc finding module"""

import matplotlib.pyplot as plt

import lib.generator as generator
import lib.calculation as calculation


if __name__ == '__main__':

    numberOfRealization = 10
    rcAll = []

    for m in xrange(100, 10000, 500):

        r = 0.49
        rc = 0

        while r < 1:

            print r

            for i in xrange(numberOfRealization):
                G = generator.evolve_ba_with_briebery(m, 20, r, 3, 0, 0)
                nyutemp = calculation.calculate_nyu(G)
                if nyutemp:
                    rc = r

            if rc:
                rcAll.append(rc)
                break

            r += 0.001

    #Saving to file
    fc = open('data/rc.txt', 'w')
    fc.write(rcAll)
    fc.close()

    plt.plot(rcAll, range(100, 10000, 500), 'ro')
    fname = "Graphics/rc.png"
    plt.savefig(fname)
    plt.close('all')

#100 - 0.597
#200 - 0.595
