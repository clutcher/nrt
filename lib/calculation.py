# -*- coding: utf-8 -*-
"""Mathemathic function"""

import math


def calculate_nyu(aGraph):
    """Calculating razriv on rank distribution graphic
        nyu ~ (r-rc)^t
    """
    n = 0
    nyu = 0
    yi = list(aGraph.degree().values())
    yi.sort()
    for iterator in xrange(len(yi) - 1):
        if yi[iterator] == yi[iterator + 1]:
            n += 1
        else:
            if n > aGraph.number_of_nodes() / 2:
                nyu = yi[iterator + 1] - yi[iterator]
            n = 0
    return nyu

def calculate_nyu_decorated_old(aGraph):
    """Calculating razriv on rank distribution graphic
        nyu ~ (r-rc)^t for decorated flowers
    """
    nyu = 0
    degreeDif = []
    yi = list(aGraph.degree().values())
    yi = list(set(yi))
    yi.sort()
    # yi.reverse()
    for i in xrange(len(yi)/2):
        degreeDif.append(yi[i+1]-yi[i])
    nyu = max(degreeDif)
    if max(degreeDif) < 4:
        nyu = 0
    return nyu


def calculate_nyu_decorated(aGraph):
    """Calculating razriv on rank distribution graphic
        nyu ~ (r-rc)^t for decorated flowers
    """
    nyu = 0
    degreeDif = []
    yi = list(aGraph.degree().values())
    yi.sort(reverse=True)
    yi = list(set(yi))
    print yi
    for i in xrange(len(yi)-1):
        degreeDif.append(yi[i+1]-yi[i])
    nyu = max(degreeDif)
    if max(degreeDif) < 1:
        nyu = 0

    degreeOpt = []
    tmp = 0
    for degr in degreeDif:
        if degr == 1:
            if tmp == 0:
                degreeOpt.append(1)
            else:
                degreeOpt.append(tmp)
                degreeOpt.append(1)
                tmp = 0
        else:
            tmp += degr
    if tmp != 0:
        degreeOpt.append(tmp)

    print degreeDif
    print degreeOpt
    return degreeOpt[0]



def calculate_linear_least_square(x, y):
    """Using least square method for linear function.
        Returning coeficient k,b of y = kx + b
    """
    if len(x) != len(y):
        return "Length of x and y are not valid!"
    sumx = 0.0
    sumy = 0.0
    sumx2 = 0.0
    sumxy = 0.0
    n = len(x)  # -3
    for i in range(n):
        sumx += x[i]
        sumx2 += x[i] * x[i]
        sumxy += x[i] * y[i]
        sumy += y[i]
    k = (sumxy * n - sumx * sumy) / (sumx2 * n - sumx * sumx)
    b = (sumx2 * sumy - sumx * sumxy) / (sumx2 * n - sumx * sumx)
    return k, b


def calculate_degree_least_square(x, y):
    """Using least square method for degree function.
        Returning coeficient c, t of y = c*x^t.
    """
    xi = [math.log(xt) for xt in x]
    yi = [math.log(yt) for yt in y]
    t, b = calculate_linear_least_square(xi, yi)
    c = math.e ** b
    return c, t
