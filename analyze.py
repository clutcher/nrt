import lib.calculation as calculation
import lib.graphics as graphics


if __name__ == '__main__':

    xi = []
    yi = []

    numberOfReadPoint = 60

    #Saving to file x and nyu
    fc = open('data/findTx.txt', 'r')
    for line in xrange(numberOfReadPoint):
        xi.append(float(fc.readline()))
    fc.close()

    fc = open('data/findTEtta.txt', 'r')
    for line in xrange(numberOfReadPoint):
        yi.append(float(fc.readline()))
    fc.close()

    c, t = calculation.calculate_degree_least_square(xi[4:], yi[4:])

    print t

    graphics.make_coeficient_graphic(xi, yi, 'nyu5000')
