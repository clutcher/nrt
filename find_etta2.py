import lib.generator as generator

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import scipy.interpolate

def remove_stages(x,y):
    i = 0
    length = len(x)
    while i<length-1:
        j = i
        counter = 0
        while y[i] == y[j+1]:
            j += 1
            counter += 1

            if len(y)<=j+1:
                break

        if counter:
            xp = sum(x[i:j+1])/(counter+1)
            yp = y[i]

            del x[i:j+1]
            del y[i:j+1]

            x.insert(i,xp)
            y.insert(i,yp)

        i += 1
        length = len(x)

def sigmoid(p,x):
    x0,y0,c,k=p
    y = c / (1 + np.exp(-k*(x-x0))) + y0
    return y

def hill(p,x):
    a,b,c,d=p
    y = a + ((b-a)/(a+(c/x)**d))
    return y

def residuals(p,x,y):
    return y - sigmoid(p,x)

def residuals_hill(p,x,y):
    return y - hill(p,x)

def resize(arr,lower=0.0,upper=1.0):
    arr=arr.copy()
    if lower>upper: lower,upper=upper,lower
    arr -= arr.min()
    arr *= (upper-lower)/arr.max()
    arr += lower
    return arr


G = generator.evolve_decorated_flower_adj(1, 2, 8, 0.8)

yi = list(G.degree().values())
yi.sort(reverse=True)

# yi = [y for y in yi if y >= 4]
xi = [x for x in xrange(len(yi))]

remove_stages(xi,yi)

xi = [np.log(x) for x in xi[1:]]
yi = [np.log(y) for y in yi[1:]]

x = np.array(xi)
y = np.array(yi)


x=resize(-x,lower=0.)
y=resize(y,lower=0.)

# middle =
interpolation = scipy.interpolate.interp1d(x,y)

p_guess=(np.median(x),np.median(y),1.0,1.0)
# p_guess_hill = (1.0,1.0,np.median(x))
p_guess_hill = (0., 1.6,0.9, 1.)

p, cov, infodict, mesg, ier = scipy.optimize.leastsq(
    residuals_hill,p_guess_hill,args=(x,y),full_output=1)
print p

xp = np.linspace(x[0], x[-1], len(x))
pxp = hill(p,xp)
pxi = interpolation(xp)
# poly = np.poly1d(np.polyfit(x, y, 16))
# pxp=poly(xp)

# Plot the results
# plt.plot(x, y, '.')
plt.plot(xp, pxi, '.')
plt.plot(xp, pxp, '-')
plt.xlabel('x')
plt.ylabel('y',rotation='horizontal')
plt.grid(True)
plt.show()