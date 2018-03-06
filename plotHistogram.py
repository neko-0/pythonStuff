from ROOT import *
from optparse import OptionParser
import os

class cutRange:

    cut = TCut()

    def __init__(self, dutTmin, dutTmax, dutPmin, dutPmax, trigTmin, trigTmax, trigPmin, trigPmax):
        tcut1 = "tmax2[0]-cfd3[20] > {}".format(dutTmin)
        tcut2 = "&&tmax2[0]-cfd3[20] < {}".format(dutTmax)
        pcut1 =  "&&pmax2[0] > {}".format(dutPmin)
        pcut2 = "&&pmax2[0] < {}".format(dutPmax)
        tcut3 = "&&tmax3[0]-cfd3[20] > {}".format(trigTmin)
        tcut4 =  "&&tmax3[0]-cfd3[20] < {}".format(trigTmax)
        pcut3 = "&&pmax3[0] > {}".format(trigPmin)
        pcut4 = "&&pmax3[0] < {}".format(trigPmax)

        self.cut = tcut1 + tcut2 + pcut1 + pcut2 + tcut3 + tcut4 + pcut3 + pcut4

    def setCut(self, customCut):
        self.cut = customCut

def plotHistogram( fileName, cut ):

    ifile = list()
    itree = list()
    histogram = list()

    for i in range(len(fileName)):
        fileTemp = TFile.Open(fileName[i])
        ifile.append(fileTemp)
        treeTemp = ifile[i].Get("wfm")
        itree.append(treeTemp)
        histogram.append(TH1D("{}".format(i),fileName[i], 100, 0, 100))
        itree[i].Project("{}".format(i), "pmax2[0]", cut[i])
        histogram[i].SetDirectory(0)

    print(histogram)
    return histogram


fileName = list()
fileName.append("stats_500V_trig390V_parse.root")
fileName.append("../Sr_Run230_HPK_S12023_10_typeB_W4_16_PRO_1E15_neg20C/stats_500V_trig395V_parse.root")

cut1 = cutRange(-500 ,500 ,0 ,360 ,200 ,500 ,70 ,375)
cut2 = cutRange(-500 ,500 ,0 ,360 ,200 ,500 ,70 ,375)

cut = list()
cut.append(cut1.cut)
cut.append(cut2.cut)

histo = plotHistogram(fileName, cut)
for item in histo[:]:
    item.Draw("same")

raw_input()
