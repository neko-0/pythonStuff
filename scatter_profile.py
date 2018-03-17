import ROOT

def ToA_CFD_Profile( fileName, toa, cfd):
    root_file = ROOT.TFile.Open( fileName )
    root_tree = root_file.Get( "wfm" )

    linear_fit = ROOT.TF1("linear_fit", "pol1", -300, 300)
    gaus = ROOT.TF1("gaus", "gaus")

    #ROOT.gROOT.SetBatch(ROOT.kTRUE)
    ROOT.gStyle.SetOptFit(1)

    #canvas = ROOT.TCanvas("c", "ToA{} vs CFD{}".format(toa, cfd), 2400, 1500)
    #canvas.Divide(2,4)

    profile = ROOT.TProfile("profile", "Profile of ToA{} vs CFD{}".format(toa, cfd), 300, -300, 300, -900, 900)
    hist2D = ROOT.TH2D("hist2D", "2D Histogram of ToA{} vs CFD {}".format(toa, cfd), 300, -300, 300, 150, -900, 900)

    hist1D = ROOT.TH1D("hist1D", "cfd2 - cfd3", 100, -400, 400)
    hist1D_2 = ROOT.TH1D("hist1D_2", "cfd2-ToA[5]", 100, -400, 400)

    for ientry, entry in enumerate(root_tree):
        if( entry.pmax2[0] > toa ):
            profile.Fill( entry.cfd2[cfd] - entry.thTime2[toa], entry.cfd2[cfd], 1)
            hist2D.Fill( entry.cfd2[cfd] - entry.thTime2[toa], entry.cfd2[cfd] )
            hist1D.Fill( entry.cfd2[cfd]-entry.cfd3[20] )
            hist1D_2.Fill( entry.cfd2[cfd] - entry.thTime2[toa] )


    hist2D.Fit(linear_fit)
    hist2D.SetMarkerStyle(7)
    hist2D.Draw()
    profile.Draw("same")

    canvas = ROOT.TCanvas("ccc")
    canvas.cd()
    hist1D.Draw()
    hist1D_2.Draw("same")
    raw_input()

ToA_CFD_Profile("Coin_stats_470V_trig395V_parse.root", 5, 50)
