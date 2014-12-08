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
    import numpy as np
    import scipy.optimize
    import scipy.interpolate
    import scipy.misc
    import sympy


    def remove_stages(x, y):
        i = 0
        length = len(x)
        while i < length - 1:
            j = i
            counter = 0
            while y[i] == y[j + 1]:
                j += 1
                counter += 1

                if len(y) <= j + 1:
                    break

            if counter:
                xp = sum(x[i:j + 1]) / (counter + 1)
                yp = y[i]

                del x[i:j + 1]
                del y[i:j + 1]

                x.insert(i, xp)
                y.insert(i, yp)

            i += 1
            length = len(x)
        return x, y

    def sigmoid_curve(x, a, b, c, d, e, f):
        y = a + b * x + c * np.arctan(x) + d * np.arctan(e * x + f)
        return y

    def curvature_for_opt(x, a, b, c, d, e, f, revert=0):
        res = ((-(2 * d * (f + e * x) * e * e) / ((f + e * x) ** 2 + 1) ** 2 - (2 * c * x) / (x * x + 1) ** 2)) / ((b + c / (x * x + 1) + (d * e) / ((e * x + f) ** 2 + 1)) ** 2 + 1) ** (3 / 2)
        if revert:
            res = -res
        if res>0:
            res = 0
        return res

    def find_zero_point(a, b, c, d, e, f):
        x = sympy.symbols('x')
        res = sympy.solve(b+c/(x*x+1)+d*e/((e*x+f)**2+1),x,exclude=[a,b,c,d,e,f])
        for num in res:
            dotx = math.sqrt(complex(num).real ** 2 + complex(num).imag ** 2)
        return dotx

    def make_log(xi, yi):
        x = [np.log(x) for x in xi[1:]]
        y = [np.log(y) for y in yi[1:]]
        return x, y

    def get_fit_params(xi, yi):
        popt, pcov = scipy.optimize.curve_fit(sigmoid_curve, xi, yi, p0=None, maxfev=100000000)
        return popt

    yi = list(aGraph.degree().values())
    yi.sort(reverse=True)
    xi = [x for x in xrange(len(yi))]

    xi, yi = remove_stages(xi, yi)
    xi, yi = make_log(xi, yi)
    xi = np.array(xi[20:])
    yi = np.array(yi[20:])

    popt = get_fit_params(xi, yi)
    try:
        guess_point =  find_zero_point(*popt)
    except:
        guess_point = 3.0
    x_hight = scipy.optimize.basinhopping(lambda arg: curvature_for_opt(arg, *popt), guess_point, niter_success=100000).x
    x_low =  scipy.optimize.basinhopping(lambda arg: curvature_for_opt(arg, *popt, revert = 1), guess_point, niter_success=100000).x

    etta = abs(np.e**sigmoid_curve(x_hight, *popt)-np.e**sigmoid_curve(x_low, *popt))
    if etta>10 or etta<1 or (abs(popt[4])<10 and abs(popt[5])<100):
        etta = 0
    return float(etta)


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
