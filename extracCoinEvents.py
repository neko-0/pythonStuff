import numpy as np
import os
from ROOT import *
import argparse

class getCoinEvents:

    cut = TCut()
    iFileName = ""
    oFileName = ""

    def __init__(self):
        print("object is created")

    def regularCuts(self, iFileName, dutTmin, dutTmax, dutPmin, dutPmax, trigTmin, trigTmax, trigPmin, trigPmax):
        tcut1 = "tmax2[0]-cfd3[20] > {}".format(dutTmin)
        tcut2 = "&&tmax2[0]-cfd3[20] < {}".format(dutTmax)
        pcut1 =  "&&pmax2[0] > {}".format(dutPmin)
        pcut2 = "&&pmax2[0] < {}".format(dutPmax)
        tcut3 = "&&tmax3[0]-cfd3[20] > {}".format(trigTmin)
        tcut4 =  "&&tmax3[0]-cfd3[20] < {}".format(trigTmax)
        pcut3 = "&&pmax3[0] > {}".format(trigPmin)
        pcut4 = "&&pmax3[0] < {}".format(trigPmax)

        self.iFileName = iFileName
        self.oFileName = "Coin_" + iFileName
        self.cut = tcut1 + tcut2 + pcut1 + pcut2 + tcut3 + tcut4 + pcut3 + pcut4

    def regularWithExtraCuts(self, iFileName, dutTmin, dutTmax, dutPmin, dutPmax, trigTmin, trigTmax, trigPmin, trigPmax, extra):
        tcut1 = "tmax2[0]-cfd3[20] > {}".format(dutTmin)
        tcut2 = "&&tmax2[0]-cfd3[20] < {}".format(dutTmax)
        pcut1 = "&&pmax2[0] > {}".format(dutPmin)
        pcut2 = "&&pmax2[0] < {}".format(dutPmax)
        tcut3 = "&&tmax3[0]-cfd3[20] > {}".format(trigTmin)
        tcut4 = "&&tmax3[0]-cfd3[20] < {}".format(trigTmax)
        pcut3 = "&&pmax3[0] > {}".format(trigPmin)
        pcut4 = "&&pmax3[0] < {}".format(trigPmax)
        extraCut = "&&{}".format(extra)

        self.iFileName = iFileName
        self.oFileName = "Coin_" + iFileName
        self.cut = tcut1 + tcut2 + pcut1 + pcut2 + tcut3 + tcut4 + pcut3 + pcut4 + extraCut

    def customCut(self, iFileName, cuts):
        self.iFileName = iFileName
        self.oFileName = "Coin_" + iFileName
        self.cut = cuts

def extracCoinEvents(iFileName, cutArray):

    if( len(cutArray) == 8 ):
        print("using regular cut")
        data = getCoinEvents()
        data.regularCuts(iFileName, cutArray[0], cutArray[1], cutArray[2], cutArray[3], cutArray[4], cutArray[5], cutArray[6], cutArray[7] )
    elif( len(cutArray) == 9 ):
        print("with addition cuts")
        data = getCoinEvents()
        data.regularWithExtraCuts(iFileName, cutArray[0], cutArray[1], cutArray[2], cutArray[3], cutArray[4], cutArray[5], cutArray[6], cutArray[7], cutArray[8] )
    elif( len(cutArray) == 1 ):
        print("with custom cut")
        data = getCoinEvents()
        data.customCut(iFileName, cutArray[0])
    else:
        print("invalid cuts")
        return None

    ifile = TFile.Open(data.iFileName,"READ")
    itree = ifile.Get("wfm")

    ofile = TFile.Open(data.oFileName, "RECREATE", "8")
    otree = itree.CopyTree(data.cut)

    ofile.Write()
    ofile.Close()
    ifile.Close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="new arg parser")
    parser.add_argument("--nargs", nargs="+")
    parser.add_argument("--fileName", type=str)
    args = parser.parse_args()
    print("Your input:")
    print(args.nargs)
    extracCoinEvents(args.fileName,args.nargs)
