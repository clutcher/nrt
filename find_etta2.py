import lib.generator as generator

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import scipy.interpolate
import scipy.misc
import sympy
import cmath
import math


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

def curvature(x, a, b, c, d, e, f):
    res = ((-(2 * d * (f + e * x) * e * e) / ((f + e * x) ** 2 + 1) ** 2 - (2 * c * x) / (x * x + 1) ** 2)) / ((b + c / (
    x * x + 1) + (d * e) / ((e * x + f) ** 2 + 1)) ** 2 + 1) ** (3 / 2)
    return res

def curvature_for_opt(x, a, b, c, d, e, f, revert=0):
    res = ((-(2 * d * (f + e * x) * e * e) / ((f + e * x) ** 2 + 1) ** 2 - (2 * c * x) / (x * x + 1) ** 2)) / ((b + c / (x * x + 1) + (d * e) / ((e * x + f) ** 2 + 1)) ** 2 + 1) ** (3 / 2)
    # res = (-2*c*x/((x**2+1)**2)-2*d*e*e*(e*x+f)/(((e*x+f)**2+1)**2))
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

def resize(arr, lower=0.0, upper=1.0):
    arr = arr.copy()
    if lower > upper: lower, upper = upper, lower
    arr -= arr.min()
    arr *= (upper - lower) / arr.max()
    arr += lower
    return arr


def make_log(xi, yi):
    x = [np.log(x) for x in xi[1:]]
    y = [np.log(y) for y in yi[1:]]
    return x, y


def normalize(xi, yi):
    x = resize(-np.array(xi), lower=0.)
    y = resize(np.array(yi), lower=0.)
    return x, y


def interpolate(xi, yi):
    interpolation = scipy.interpolate.interp1d(xi, yi)
    xpi = np.linspace(xi[0], xi[-1], len(xi))
    pxi = interpolation(xpi)
    return xpi, pxi


def get_fit_params(xi, yi):
    popt, pcov = scipy.optimize.curve_fit(sigmoid_curve, xi, yi, p0=None, maxfev=100000000)
    return popt


if __name__ == "__main__":
    G = generator.evolve_decorated_flower_adj(1, 2, 8, 0.835)

    yi = list(G.degree().values())
    yi.sort(reverse=True)
    xi = [x for x in xrange(len(yi))]

    xi, yi = remove_stages(xi, yi)
    xi, yi = make_log(xi, yi)
    # xi, yi = normalize(xi,yi)

    xi = np.array(xi[20:])
    yi = np.array(yi[20:])

    # xi, yi = interpolate(xi, yi)
    popt = get_fit_params(xi, yi)
    print popt
    y_sigmoid = sigmoid_curve(xi, *popt)
    # guess_point = scipy.optimize.minimize(lambda arg: -curvature(arg, *popt), xi[10]).x
    guess_point =  find_zero_point(*popt)
    x_hight = scipy.optimize.basinhopping(lambda arg: curvature_for_opt(arg, *popt), guess_point, niter_success=100000).x
    x_low =  scipy.optimize.basinhopping(lambda arg: curvature_for_opt(arg, *popt, revert = 1), guess_point, niter_success=100000).x
    etta = abs(np.e**sigmoid_curve(x_hight, *popt)-np.e**sigmoid_curve(x_low, *popt))
    print etta