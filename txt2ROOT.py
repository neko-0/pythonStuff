import numpy as np
from optparse import OptionParser
import os
from ROOT import *

def txtToROOT( fileName ):
    dataHolder = [np.array(map(str, line.split(","))) for line in open(fileName)]

    print(len(dataHolder))

    tfile = TFile.Open("tdc.root","RECREATE","8")
    ttree = TTree("wfm","tdc wave")

    filler = vector("double")()
    filler2 = vector("double")()

    ttree.Branch("col1", filler)
    ttree.Branch("col2", filler2)

    for i in range(2, len(dataHolder)):
        filler.push_back(float(dataHolder[i][0]))
        filler2.push_back(float(dataHolder[i][2]))
        ttree.Fill()
        filler.clear()
        filler2.clear()
        if(i % 200 == 0):
            print(i)

    tfile.Write()
    tfile.Close()

    print("finished")


if __name__ == "__main__":

    parser = OptionParser()

    parser.add_option('-f', '--fileName=', dest='fileName', type='string')

    (options, args) = parser.parse_args()

    fileName = options.fileName

    txtToROOT(fileName)
