import ROOT

def MakeHistogramComparison( fileName, sensor ):
    tfile = ROOT.TFile.Open( fileName )
    ttree = tfile.Get("wfm")

    histo = ROOT.TH1D("histo", sensor, 80, 1, 1)

    for ientry, entry in enumerate(ttree):
        histo.Fill( entry.rise2_1090[0] )

    histo.SetDirectory(0)

    return histo

histo1 = MakeHistogramComparison("Coin_50D_300V.root", "50D 300V")

histo2 = MakeHistogramComparison("Coin_B35_130V.root","B35 130V")

histo3 = MakeHistogramComparison("Coin_sample_H_90V.root", "sample H 90V")

ROOT.gROOT.SetBatch(ROOT.kTRUE)
canvas = ROOT.TCanvas("c","", 1600, 1000)
canvas.Divide(3,1)

canvas.cd(1)
histo1.Draw()

canvas.cd(2)
histo2.Draw()

canvas.cd(3)
histo3.Draw()

canvas.SaveAs("rise_time.png")
canvas.Close()
