#!/usr/bin/python
import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

title = ROOT.TPaveLabel(.11,.91,.89,.99,"FNAL 2018 test beam data, CNM W4 AC-2 detector","brNDC")

ch = ROOT.TChain("wfm")
ch.Add("AC_170V/SCIPP*")
ch.SetMarkerStyle(20)

posxs = [[23600, 23800], [23850, 24150], [24100, 24300]]
posys = [[15800, 16000], [16050, 16350], [16300, 16500]]

for ientry, entry in enumerate(ch):
    if not(entry.nTracks[0] > 0 and entry.chi2[0] < 10): continue
    ipos = 0
    for posx in posxs:
        for  posy in posys:
            if entry.x1[0] > posx[0] and entry.x1[0] < posx[1] and entry.y1[0] > posy[0] and entry.y1[0] < posy[1]\
                                                            and entry.pmax[7][0] > 20 and entry.tmax[7][0] > 80 and entry.tmax[7][0] < 120 \
                                                            and entry.pmax[4][0] > 20 and entry.tmax[4][0] > 80 and entry.tmax[4][0] < 120 \
                                                            and entry.pmax[5][0] > 20 and entry.tmax[5][0] > 80 and entry.tmax[5][0] < 120 :
                print "On position %i: (%1.f, %1.f)x(%1.f, %1.f)" %(ipos, posx[0]/100., posx[1]/100., posy[0]/100., posy[1]/100.)
                print entry.pmax[4][0], entry.pmax[5][0], entry.pmax[7][0]

                vx4 = ROOT.TVectorF(entry.ch[4].size())
                vy4 = ROOT.TVectorF(entry.time.size())
                for i, (y, x) in enumerate(zip(entry.ch[4], entry.time)):
                    vx4[i] = x
                    vy4[i] = y
                g4 = ROOT.TGraph(vx4, vy4)

                vx5 = ROOT.TVectorF(entry.ch[5].size())
                vy5 = ROOT.TVectorF(entry.time.size())
                for i, (y, x) in enumerate(zip(entry.ch[5], entry.time)):
                    vx5[i] = x
                    vy5[i] = y
                g5 = ROOT.TGraph(vx5, vy5)

                vx6 = ROOT.TVectorF(entry.ch[6].size())
                vy6 = ROOT.TVectorF(entry.time.size())
                for i, (y, x) in enumerate(zip(entry.ch[6], entry.time)):
                    vx6[i] = x
                    vy6[i] = y
                g6 = ROOT.TGraph(vx6, vy6)

                vx7 = ROOT.TVectorF(entry.ch[7].size())
                vy7 = ROOT.TVectorF(entry.time.size())
                for i, (y, x) in enumerate(zip(entry.ch[7], entry.time)):
                    vx7[i] = x
                    vy7[i] = y
                g7 = ROOT.TGraph(vx7, vy7)

                can = ROOT.TCanvas("c", "c", 1920, 1280)
                g7.GetXaxis().SetRangeUser(80,150)
                g7.GetYaxis().SetRangeUser(-800,800)
                g4.SetLineColor(ROOT.kRed)
                g5.SetLineColor(ROOT.kBlue)
                g6.SetLineColor(ROOT.kGreen)
                g7.SetLineColor(ROOT.kBlack)

                g4.SetLineWidth(3)
                g5.SetLineWidth(3)
                g6.SetLineWidth(3)
                g7.SetLineWidth(3)

                g7.Draw("Al")
                g5.Draw("samel")
                g6.Draw("samel")
                g4.Draw("samel")

                leg = ROOT.TLegend(0.5, 0.11, 0.89, 0.4)
                leg.SetHeader("Position %i (x,y): (%1.f, %1.f)x(%1.f, %1.f)" %(ipos, posx[0]/100., posx[1]/100., posy[0]/100., posy[1]/100.))
                leg.AddEntry(g4, "Pixel 1", "l")
                leg.AddEntry(g5, "Pixel 2", "l")
                leg.AddEntry(g7, "Pixel 3", "l")
                leg.AddEntry(g6, "Strip", "l")
                leg.Draw()
                title.Draw()

                can.SaveAs("Plot_pulseshapes_evt_pos_%i_%i.png" %(ipos, ientry))
            ipos = ipos + 1
