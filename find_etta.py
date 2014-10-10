import lib.generator as generator

import numpy as np
import pylab
from scipy.optimize import curve_fit
from scipy.optimize import fsolve
from scipy.misc import derivative
import math

def sigmoid(x, a, b, c, d, f, alpha):
    y =np.sin(a- b / (c + np.exp(-d*(x-f))))
    return y

# def sigmoid(x, a1,b1,c1,a2,b2,c2,a3,b3,c3,a4,b4,c4):
#      y = a1/(1+(b1/x)**c1)+a2/(1+(b2/x)**c1)+a3/(1+(b3/x)**c1)
#      return y

# def sigmoid(x,a,b,c,d,s):
#     y = a-np.sign(x-d)*(1-np.exp(-1*( ((x-d)/s) ** 2 )))
#     return y

# def sigmoid(x,a,b,c,m):
#     y = 1-np.exp(-1*(((x)/c)**m))
#     return y

# def sigmoid(x, a, b, c, e, b1, c1, e1):
#     y = a + (1 - x ** e / (c ** b + x ** b)) + (1 - x ** e1 / (c1 ** b1 + x ** b1))
#     return y


def dersigmoid(x, a, b, c, e, b1, c1, e1):
    d = derivative(sigmoid, x, args=( a, b, c, e, b1, c1, e1))
    return d

# print sigmoid(50,2, 12, 103, 33, 2, 4, 3)
# print dersigmoid(50,2, 12, 103, 33, 2, 4, 3)
G = generator.evolve_decorated_flower_adj(1, 2, 8, 0.8)

yi = list(G.degree().values())
yi.sort(reverse=True)

# yi = [y for y in yi if y >= 2]
xi = [x for x in xrange(len(yi))]
#
xi = [np.log(x) for x in xi[1:]]
yi = [np.log(y) for y in yi[1:]]
#
xdata = np.array(xi)
ydata = np.array(yi)

# p0 = (2, 12, 103, 33, 2, 4, 3)
popt, pcov = curve_fit(sigmoid, xdata, ydata, p0=None, maxfev=100000000)
print popt

# a = fsolve(dersigmoid, 5., args=(popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6]), maxfev=10000000)
# print a
x = np.linspace(xi[0], xi[-1], len(xi))
y = sigmoid(x, *popt)

pylab.plot(xdata, ydata, 'o', label='data')
pylab.plot(x, y, label='fit')

pylab.legend(loc='best')
pylab.show()
