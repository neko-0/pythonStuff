import ROOT
'''
file_250 = ROOT.TFile.Open("run257_avePulse_less100.root")
file_250_600 = ROOT.TFile.Open("run257_avePulse_100_600.root")
file_600 = ROOT.TFile.Open("run257_avePulse_600.root")

p_250 = ROOT.TProfile()
p_250_600 = ROOT.TProfile()
p_600 = ROOT.TProfile()

file_250.GetObject("_90V", p_250)
file_250_600.GetObject("_90V", p_250_600)
file_600.GetObject("_90V", p_600)

legend = ROOT.TLegend()
legend.AddEntry(p_250, "rise time < 250 ps")
legend.AddEntry(p_250_600, "rise time [250,600] ps")
legend.AddEntry(p_600, "rise time > 600 ps")

p_250.SetLineColor(ROOT.kRed)
p_250.Draw()

p_250_600.SetLineColor(ROOT.kBlue)
#p_250_600.Draw("same")

p_600.SetLineColor(ROOT.kGreen)
#p_600.Draw("same")

#legend.Draw("same")

raw_input()
'''

tfile = ROOT.TFile.Open("../Coin_stats_Sr_Run257_user_trig_90V.root")
ttree = tfile.Get("wfm")


p_250 = ROOT.TProfile("p_250","", 100000/25, -50000, 50000, -50, 50)
p_250_600 = ROOT.TProfile("p_250_600","", 50000/25, -50000, 50000, -50, 50)
p_600 = ROOT.TProfile("p_600","", 100000/25, -50000, 50000, -50, 50)

ttree.Project("p_250", "-w2:t2-cfd3[20]", "rise2_1090[0]<250")
ttree.Project("p_250_600", "-w2:t2-cfd3[20]", "rise2_1090[0]>250&&rise2_1090[0]<600")
ttree.Project("p_600", "-w2:t2-cfd3[20]", "rise2_1090[0]>600")

legend = ROOT.TLegend(0.1,0.7,0.48,0.9)
legend.AddEntry(p_250, "rise time < 250 ps")
legend.AddEntry(p_250_600, "rise time [250,600] ps")
legend.AddEntry(p_600, "rise time > 600 ps")

ROOT.gROOT.SetBatch(ROOT.kTRUE)
p_250.GetXaxis().SetRangeUser(-1500,1500)
ttree.SetMarkerStyle(7)

p_250.SetLineColor(ROOT.kRed)
p_250_600.SetLineColor(ROOT.kBlue)
p_600.SetLineColor(ROOT.kGreen)
'''
for i in range(ttree.GetEntries()):
    canvas = ROOT.TCanvas("canvas")

    raw = ROOT.TH2D("raw","Event_{}".format(i), 100000/25, -50000, 50000, 100, -20, 80)
    raw.GetXaxis().SetRangeUser(-1500,1500)
    raw.GetYaxis().SetRangeUser(-10,35)

    ttree.Project("raw", "-w2:t2-cfd3[20]", "Entry$=={}".format(i) )

    raw.SetMarkerStyle(7)
    raw.Draw()
    #p_250.SetLineColor(ROOT.kRed)
    p_250.Draw("same")

    #p_250_600.SetLineColor(ROOT.kBlue)
    p_250_600.Draw("same")

    #p_600.SetLineColor(ROOT.kGreen)
    p_600.Draw("same")

    legend.Draw("same")

    canvas.SaveAs("event_{}.png".format(i) )
    canvas.Close()
    ROOT.gDirectory.FindObject("raw").Delete()

raw_input()
'''
canvas = ROOT.TCanvas("canvas")
p_250.Draw("same")
p_250_600.Draw("same")
p_600.Draw("same")
legend.Draw("same")
canvas.SaveAs("avearge_pulse.png" )
canvas.Close()
