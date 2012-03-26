# -*- coding: utf-8 -*-
"""Main research module"""

import networkx as nx
#import matplotlib.pyplot as plt
#import time

#import gui.main as gui
from PyQt4 import QtCore, QtGui
import sys
import threading

import lib.generator as generator
import lib.graphics as graphics
import lib.calculation as calculation

from gui.mainForm import Ui_MainWindow as MainWindow


class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.ui.buidProgress.setProperty("value", 0)
        self.ui.gdataBgr_FL.hide()
        self.ui.startr.setText('0.0')
        self.ui.endr.setText('1.0')
        self.ui.stepr.setText('0.01')
        self.ui.numr.setText('1')

        self.connect(self.ui.graphList,
            QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.GraphDisplay)
        self.connect(self.ui.magikBtn,
            QtCore.SIGNAL("clicked()"), self.makeResearch)

    def GraphDisplay(self):
        if self.ui.graphList.currentIndex() < 2:
            self.ui.gdataBgr_FL.hide()
            self.ui.gdataBgr_BA.show()
        else:
            self.ui.gdataBgr_BA.hide()
            self.ui.gdataBgr_FL.show()

    def makeResearch(self):
        self.ui.buidProgress.setProperty("value", 0)
        flagList = {'graph': self.ui.chackGraph.isChecked(),
                    'betweenneess': self.ui.checkBtw.isChecked(),
                    'probability': self.ui.checkProb.isChecked(),
                    'degree': self.ui.checkDeghist.isChecked(),
                    'rank': self.ui.checkRankdisp.isChecked(),
                    'nyu': self.ui.checkNyu.isChecked(),
                    'clustering': self.ui.checkClust.isChecked(),
                    'shortpath': self.ui.checkSP.isChecked(),
                    'assortativity': self.ui.checkAssort.isChecked()}

        globalCheckFlag = 0

        if flagList['nyu'] or flagList['clustering'] or flagList['shortpath'] \
          or flagList['assortativity']:
            globalCheckFlag = 1

        #r - the coefficient of bribery
        startr = float(self.ui.startr.text())
        endr = float(self.ui.endr.text())
        stepr = float(self.ui.stepr.text())

        if self.ui.graphList.currentIndex() < 2:
            m = int(self.ui.mBA.text())
            m0 = int(self.ui.m0BA.text())
            n = int(self.ui.nBA.text())
            p = int(self.ui.pBA.text())
            di = int(self.ui.diBA.text())

        if self.ui.graphList.currentIndex() > 1:
            x = int(self.ui.xFL.text())
            y = int(self.ui.yFL.text())
            n = int(self.ui.nFL.text())
            p = int(self.ui.pFL.text())
        #rc - critical coefficient of bribery
        rc = 0
        #rlist - list of r, where r > rc
        rlist = []
        #flag - finding first rc
        flag = 1

        nyu = []
        clustering = []
        shortpath = []
        assortativity = []

        #Temps for finding average by realization
        nyuT = []
        clusteringT = []
        shortpathT = []
        assortativityT = []

        numberOfRealization = int(self.ui.numr.text())
        r = startr

        #Generate many networks for making nyu graphic
        while r < endr:
            for i in xrange(numberOfRealization):
                network = self.ui.graphList.currentIndex()
                if network == 1:
                    G = generator.evolve_ba_with_briebery(m, m0, r, n, di, p)
                elif network == 3:
                    G = generator.evolve_flower_with_briebery(x, y, n, r, p)
                elif not network:
                    G = generator.evolve_ba_removing_edges(m, m0, n, r, p)
                elif network == 2:
                    G = generator.evolve_flower_removing_edges(x, y, n, r, p)

                nyutemp = calculation.calculate_nyu(G)
                if (nyutemp != 0) and flag:
                    #-0.0001 to avoid log 0 in graphics
                    rc = r - 0.0001
                    flag = 0
                if rc != 0 and globalCheckFlag:
                    if flagList['clustering'] == 1:
                        clusteringT.append(nx.average_clustering(G))
                    if flagList['shortpath'] == 1:
                        shortpathT.append(nx.average_shortest_path_length(G))
                    if flagList['assortativity'] == 1:
                        assortativityT.append(abs(nx.degree_assortativity(G)))
                    if flagList['nyu'] == 1:
                        nyuT.append(nyutemp)

            #Finding average parameters
            if rc != 0 and globalCheckFlag:
                if flagList['clustering'] == 1:
                    sum = 0.0
                    for temp in clusteringT:
                        sum += temp
                    sum = sum / (len(clusteringT) + 1)
                    clustering.append(sum)

                if flagList['shortpath'] == 1:
                    sum = 0.0
                    for temp in shortpathT:
                        sum += temp
                    sum = sum / (len(shortpathT) + 1)
                    shortpath.append(sum)

                if flagList['assortativity'] == 1:
                    sum = 0.0
                    for temp in assortativityT:
                        sum += temp
                    sum = sum / (len(assortativityT) + 1)
                    assortativity.append(sum)

                if flagList['nyu'] == 1:
                    sum = 0.0
                    for temp in nyuT:
                        sum += temp
                    sum = sum / (len(nyuT) + 1)
                    nyu.append(sum)

                rlist.append(r - rc)
            r += stepr
            self.ui.buidProgress.setProperty("value", 100 * r / endr)

            #Clearing temporary variables
            nyuT = []
            clusteringT = []
            shortpathT = []
            assortativityT = []

            #Network graphics
            if flagList['graph'] == 1:
                graphics.make_graph(G)
            if flagList['betweenneess'] == 1:
                graphics.make_betweenness_graphic(G)
            if flagList['probability'] == 1:
                graphics.make_probability_graphic(G)
            if flagList['degree'] == 1:
                graphics.make_degree_histogram(G)
            if flagList['rank'] == 1:
                graphics.make_rank_distribution(G)

        #Parametr graphics
        if flagList['nyu'] == 1:
            graphics.make_coeficient_graphic(rlist, nyu, "nyu")
        if flagList['clustering'] == 1:
            graphics.make_coeficient_graphic(rlist, clustering, "clustering")
        if flagList['shortpath'] == 1:
            graphics.make_coeficient_graphic(rlist, shortpath, "shortpath")
        if flagList['assortativity'] == 1:
            graphics.make_coeficient_graphic(rlist, assortativity,
            "assortativity")


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    myapp = MainForm()
    myapp.show()
    sys.exit(app.exec_())




#    plt.show()

#    #Outputting information about graph
#    print nx.betweenness_centrality(G)
#    print nx.info(G)
#    print "Clustering: " + nx.average_clustering(G)
#    print "Shortest path length: " + nx.average_shortest_path_length(G)

#    #Saving graph
#    nx.write_edgelist(G, "edgelist.graph")


#    #Saving coefficients to file
#    fc = open('data/clustering.txt', 'w')
#    fsh = open('data/shortpath.txt', 'w')
#
#    for cl in clustering:
#        line = repr(cl) + "\n"
#        fc.write(line)
#    fc.close()
#
#    for sp in shortpath:
#        line = repr(sp) + "\n"
#        fsh.write(line)
##    fsh.close()

################GOGOGO!!!
