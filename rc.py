# -*- coding: utf-8 *-*
# -*- coding: utf-8 -*-
"""Main research module"""

import matplotlib.pyplot as plt

import lib.generator as generator
import lib.calculation as calculation


if __name__ == '__main__':

    numberOfRealization = 10
    rcAll = []

    for m in xrange(100, 5100, 500):

        r = 0.48
        rc = 0

        while r < 1:

            print r

            for i in xrange(numberOfRealization):
                G = generator.evolveBA(m, 20, r, 3, 0, 0)
                nyutemp = calculation.calculate_nyu(G)
                if nyutemp != 0:
                    rc = r

            if rc != 0:
                rcAll.append(rc)
                break

            r = r + 0.001

    plt.plot(rcAll, range(100, 5100, 500), 'ro')
    fname = "Graphics/rc.png"
    plt.savefig(fname)
    plt.close('all')

#100 - 0.597
#200 - 0.595
