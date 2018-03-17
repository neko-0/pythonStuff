#########################
## ToA vs CFD
#########################

import ROOT

def getlinearY(x, slope, constant):
    return slope*x + constant

def getlinearX(y, slope, constant):
    return (y - constant)/(1.0*slope)

#====================================================================================================
#====================================================================================================

def GetLinearFit( fileName, toa, cfd ):
    root_file = ROOT.TFile.Open( fileName )
    root_tree = root_file.Get( "wfm" )

    linear_fit = ROOT.TF1("linear_fit", "pol1", -2000, 2000)

    profile = ROOT.TProfile("profile", "Profile of ToA{} vs CFD{}".format(toa, cfd), 300, -2000, 2000, -2000, 2000)
    hist2D = ROOT.TH2D("hist2D", "2D Histogram of ToA{} vs CFD {}".format(toa, cfd), 300, -2000, 2000, 150, -2000, 2000)

    for ientry, entry in enumerate(root_tree):
        if( entry.pmax2[0] > toa ):
            profile.Fill( entry.cfd2[cfd] - entry.thTime2[toa], entry.cfd2[cfd]-entry.cfd3[20], 1)
            hist2D.Fill( entry.cfd2[cfd] - entry.thTime2[toa], entry.cfd2[cfd]-entry.cfd3[20])
            #print(entry.thTime2[0])

    #print(cfd)
    hist2D.Fit(linear_fit, "Q0")
    hist2D.SetDirectory(0)

    return [linear_fit, hist2D]

#====================================================================================================
#====================================================================================================

def ExportFit2TxT( fileName ):
    out_file = open("_fit_of_ToACFD_{}.txt".format( fileName ), "w" )
    out_file.write("constatn slope toa cfd")
    for toa in range(49):
        for cfd in range(100):
            linear_fit = GetLinearFit( fileName, toa, cfd )
            out_file.write( "{} {} {} {}".format(linear_fit.GetParameter(0), linear_fit.GetParameter(1), toa, cfd ) )
            out_file.write("\n")
    out_file.close()
    print("finished")

#====================================================================================================
#====================================================================================================


def ToA_CFD_Profile( fileName ):
    root_file = ROOT.TFile.Open( fileName )
    root_tree = root_file.Get( "wfm" )

    linear_fit = ROOT.TF1("linear_fit", "pol1", -1200, 300)
    gaus = ROOT.TF1("gaus", "gaus")

    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    ROOT.gStyle.SetOptFit(1)

    for toa in range(49):
        for cfd in range(100):
            canvas = ROOT.TCanvas("c", "ToA{} vs CFD{}".format(toa, cfd), 2400, 1500)
            canvas.Divide(2,4)

            profile = ROOT.TProfile("profile", "Profile of ToA{} vs CFD{}".format(toa, cfd), 300, -1200, 300, -900, 900)
            hist2D = ROOT.TH2D("hist2D", "2D Histogram of ToA{} vs CFD {}".format(toa, cfd), 300, -1200, 300, 150, -900, 900)

            hist2D_along_toa = ROOT.TH2D("hist2D_toa", "Rotate along ToA{}".format(toa), 400, -3000, 3000, 100, -600, 600)
            hist2D_along_cfd = ROOT.TH2D("hist2D_cfd", "Rotate along CFD{}".format(cfd), 200, -800, 200, 100, -600, 600)

            cfd_projection = ROOT.TH1D( "cfd_projection", "cfd2[{}]-cfd3[20]".format(cfd), 100, 1, 1)
            toa_projection = ROOT.TH1D( "toa_projection", "ToA[{}]-cfd3[20]".format(toa), 100, 1, 1)

            cfd_projection_corr = ROOT.TH1D( "cfd_projection_corr", "cfd2[{}]-cfd3[20] corr".format(cfd), 100, 1, 1)
            toa_projection_corr = ROOT.TH1D( "toa_projection_corr", "ToA[{}]-cfd3[20] corr".format(toa), 100, 1, 1)

            for ientry, entry in enumerate(root_tree):
                if( entry.pmax2[0] > toa ):
                    profile.Fill( entry.cfd2[cfd] - entry.thTime2[toa], entry.cfd2[cfd]-entry.cfd3[20], 1)
                    hist2D.Fill( entry.cfd2[cfd] - entry.thTime2[toa], entry.cfd2[cfd]-entry.cfd3[20])
                    cfd_projection.Fill( entry.cfd2[cfd]-entry.cfd3[20] )
                    toa_projection.Fill( entry.thTime2[toa]-entry.cfd3[20] )
                    #print(entry.thTime2[0])

            #print(cfd)
            hist2D.Fit(linear_fit, "Q0")

            for ientry, entry in enumerate(root_tree):
                if( entry.pmax2[0] > toa ):
                    subtract_along_cfd = getlinearY( entry.thTime2[toa]-entry.cfd3[20], linear_fit.GetParameter(1), linear_fit.GetParameter(0) )
                    hist2D_along_cfd.Fill( entry.thTime2[toa]-entry.cfd3[20], entry.cfd2[cfd]-entry.cfd3[20]-subtract_along_cfd )

                    subtract_along_toa = getlinearX( entry.cfd2[cfd]-entry.cfd3[20], linear_fit.GetParameter(1), linear_fit.GetParameter(0) )
                    hist2D_along_toa.Fill( entry.thTime2[toa]-entry.cfd3[20]-subtract_along_toa, entry.cfd2[cfd]-entry.cfd3[20] )
                    #print(entry.thTime2[toa]-entry.cfd3[20]-subtract_along_toa)

                    cfd_projection_corr.Fill( entry.cfd2[cfd]-entry.cfd3[20]-subtract_along_cfd )
                    toa_projection_corr.Fill( entry.thTime2[toa]-entry.cfd3[20]-subtract_along_toa )

            canvas.cd(1)
            profile.GetYaxis().SetTitle( "cfd2[{}]-cfd3[20]".format(cfd) )
            profile.GetXaxis().SetTitle( "ToA[{}]-cfd3[20]".format(toa) )
            profile.SetLineColor(ROOT.kRed)
            profile.SetLineWidth(2)

            hist2D.GetYaxis().SetTitle( "cfd2[{}]-cfd3[20]".format(cfd) )
            hist2D.GetXaxis().SetTitle( "ToA[{}]-cfd3[20]".format(toa) )
            hist2D.SetMarkerStyle(7)

            hist2D.Draw("l")
            profile.Draw("same l")

            canvas.cd(2)
            hist2D.Draw("l")
            profile.Draw("same l")
            linear_fit.Draw("same")

            canvas.cd(3)
            hist2D_along_cfd.GetYaxis().SetTitle( "cfd2[{}]-cfd3[20]".format(cfd) )
            hist2D_along_cfd.GetXaxis().SetTitle( "ToA[{}]-cfd3[20]".format(toa) )
            hist2D_along_cfd.SetMarkerStyle(7)
            hist2D_along_cfd.Draw()
            linear_fit.Draw("same")

            canvas.cd(4)
            hist2D_along_toa.GetYaxis().SetTitle( "cfd2[{}]-cfd3[20]".format(cfd) )
            hist2D_along_toa.GetXaxis().SetTitle( "ToA[{}]-cfd3[20]".format(toa) )
            hist2D_along_toa.SetMarkerStyle(7)
            hist2D_along_toa.Draw()
            linear_fit.Draw("same")


            canvas.cd(5)
            cfd_projection.Fit(gaus,"Q")
            cfd_projection.Draw()

            canvas.cd(6)
            toa_projection.Fit(gaus,"Q")
            toa_projection.Draw()

            canvas.cd(7)
            cfd_projection_corr.Fit(gaus,"Q")
            cfd_projection_corr.Draw()

            canvas.cd(8)
            toa_projection_corr.Fit(gaus,"Q")
            toa_projection_corr.Draw()

            canvas.SaveAs("ToA{}_cfd{}.png".format(toa,cfd))


            canvas.Close()
            while( ROOT.gDirectory.FindObject("cfd_projection") ):
                ROOT.gDirectory.FindObject("cfd_projection").Delete()
            while( ROOT.gDirectory.FindObject("toa_projection") ):
                ROOT.gDirectory.FindObject("toa_projection").Delete()
            while( ROOT.gDirectory.FindObject("profile") ):
                ROOT.gDirectory.FindObject("profile").Delete()
            while( ROOT.gDirectory.FindObject("hist2D") ):
                ROOT.gDirectory.FindObject("hist2D").Delete()
            while( ROOT.gDirectory.FindObject("cfd_projection_corr") ):
                ROOT.gDirectory.FindObject("cfd_projection_corr").Delete()
            while( ROOT.gDirectory.FindObject("toa_projection_corr") ):
                ROOT.gDirectory.FindObject("toa_projection_corr").Delete()
            while( ROOT.gDirectory.FindObject("hist2D_cfd") ):
                ROOT.gDirectory.FindObject("hist2D_cfd").Delete()
            while( ROOT.gDirectory.FindObject("hist2D_toa") ):
                ROOT.gDirectory.FindObject("hist2D_toa").Delete()


#====================================================================================================
#====================================================================================================

def CorrectedProjection( fileName, toa, cfd, slope, constant ):

    root_file = ROOT.TFile.Open( fileName )
    root_tree = root_file.Get( "wfm" )

    linear_fit = ROOT.TF1("linear_fit", "pol1", -1200, 300)
    gaus = ROOT.TF1("gaus", "gaus")

    cfd_projection_corr = ROOT.TH1D( "cfd_projection_corr", "{} cfd2[{}]-cfd3[20] corr".format(fileName, cfd), 100, 1, 1)
    toa_projection_corr = ROOT.TH1D( "toa_projection_corr", "{} ToA[{}]-cfd3[20] corr".format(fileName, toa), 100, 1, 1)

    cfd_projection = ROOT.TH1D( "cfd_projection", "{} cfd2[{}]-cfd3[20]".format(fileName, cfd), 100, 1, 1)
    toa_projection = ROOT.TH1D( "toa_projection", "{} ToA[{}]-cfd3[20]".format(fileName, toa), 100, 1, 1)

    for ientry, entry in enumerate(root_tree):
        if( entry.pmax2[0] > toa ):
            subtract_along_cfd = getlinearY( entry.cfd2[cfd] - entry.thTime2[toa], slope, constant )

            subtract_along_toa = getlinearX( entry.cfd2[cfd]-entry.cfd3[20], slope, constant )

            cfd_projection_corr.Fill( entry.cfd2[cfd]-entry.cfd3[20]-subtract_along_cfd )
            toa_projection_corr.Fill( entry.thTime2[toa]-entry.cfd3[20]-subtract_along_toa )

            cfd_projection.Fill( entry.cfd2[cfd]-entry.cfd3[20] )
            toa_projection.Fill( entry.thTime2[toa]-entry.cfd3[20] )

    toa_projection_corr.Fit(gaus,"Q")
    cfd_projection_corr.Fit(gaus,"Q")

    cfd_sigma_corr = gaus.GetParameter(2)

    toa_projection.Fit(gaus,"Q")
    cfd_projection.Fit(gaus,"Q")

    cfd_sigma = gaus.GetParameter(2)

    toa_projection_corr.SetDirectory(0)
    cfd_projection_corr.SetDirectory(0)
    toa_projection.SetDirectory(0)
    cfd_projection.SetDirectory(0)

    return [cfd_projection, cfd_projection_corr, toa_projection, toa_projection_corr, cfd_sigma, cfd_sigma_corr]

#====================================================================================================
#====================================================================================================

#ToA_CFD_Profile( "../Coin_stats_90V_trig395V_parse.root" )
'''
_90V = GetLinearFit( "Coin_stats_90V_trig395V_parse.root", 20, 20 )
_100V = GetLinearFit( "Coin_stats_100V_trig395V_parse.root", 20, 20 )
_110V = GetLinearFit( "Coin_stats_110V_trig395V_parse.root", 20, 20 )
_120V = GetLinearFit( "Coin_stats_120V_trig395V_parse.root", 20, 20 )
_130V = GetLinearFit( "Coin_stats_130V_trig395V_parse.root", 20, 20 )
canvas = ROOT.TCanvas("c", " linear fit ")
canvas.cd()
_90V.SetLineColor(ROOT.kRed)
_90V.Draw()
_100V.SetLineColor(ROOT.kGreen)
_100V.Draw("same")
_110V.SetLineColor(ROOT.kBlue)
_110V.Draw("same")
_120V.SetLineColor(ROOT.kYellow)
_120V.Draw("same")
_130V.SetLineColor(ROOT.kBlack)
_130V.Draw("same")
raw_input()
'''

'''
ROOT.gROOT.SetBatch(ROOT.kTRUE)
#for toa in range(49):
    #for cfd in range(100):
#ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetOptFit(1)
_prerad = GetLinearFit( "_prerad_Coin_stats_120V_trig395V_parse.root", 5, 60 )
_4E14 = GetLinearFit( "_4E14_Coin_stats_400V_trig395V_parse.root", 5, 60 )
_1E15 = GetLinearFit( "_1E15_Coin_stats_460V_trig400V_parse.root", 5, 60 )
_3E15 = GetLinearFit( "_3E15_Coin_stats_470V_trig395V_parse.root", 5, 60 )
_6E15 = GetLinearFit( "_6E15_Coin_stats_470V_trig395V_parse.root", 5, 60 )
canvas = ROOT.TCanvas("c")
canvas.cd()

_prerad[0].SetLineColor(ROOT.kRed)
_prerad[1].SetMarkerStyle(7)
_prerad[1].SetMarkerColor(ROOT.kRed)
_prerad[0].Draw()
_prerad[1].Draw("same")

_4E14[0].SetLineColor(ROOT.kGreen)
_4E14[1].SetMarkerStyle(7)
_4E14[1].SetMarkerColor(ROOT.kGreen)
_4E14[0].Draw("same")
_4E14[1].Draw("same")

_1E15[0].SetLineColor(ROOT.kBlue)
_1E15[1].SetMarkerStyle(7)
_1E15[1].SetMarkerColor(ROOT.kBlue)
_1E15[0].Draw("same")
_1E15[1].Draw("same")

_3E15[0].SetLineColor(ROOT.kYellow)
_3E15[1].SetMarkerStyle(7)
_3E15[1].SetMarkerColor(ROOT.kYellow)
_3E15[0].Draw("same")
_3E15[1].Draw("same")

_6E15[0].SetLineColor(ROOT.kBlack)
_6E15[1].SetMarkerStyle(7)
_6E15[1].SetMarkerColor(ROOT.kBlack)
_6E15[0].Draw("same")
_6E15[1].Draw("same")

#canvas.SaveAs("ToA{}_cfd{}.png".format(5,60))
#canvas.Close()
#raw_input()

mean_constant = ( _prerad[0].GetParameter(0) + _4E14[0].GetParameter(0) + _1E15[0].GetParameter(0) + _3E15[0].GetParameter(0) + _6E15[0].GetParameter(0) )/5.0
mean_slope = ( _prerad[0].GetParameter(1) + _4E14[0].GetParameter(1) + _1E15[0].GetParameter(1) + _3E15[0].GetParameter(1) + _6E15[0].GetParameter(1) )/5.0

_prerad_histo = CorrectedProjection( "_prerad_Coin_stats_120V_trig395V_parse.root", 5, 60, mean_slope, mean_constant )
_4E14_histo = CorrectedProjection( "_4E14_Coin_stats_400V_trig395V_parse.root", 5, 60, mean_slope, mean_constant )
_1E15_histo = CorrectedProjection( "_1E15_Coin_stats_460V_trig400V_parse.root", 5, 60, mean_slope, mean_constant )
_3E15_histo = CorrectedProjection( "_3E15_Coin_stats_470V_trig395V_parse.root", 5, 60, mean_slope, mean_constant )
_6E15_histo = CorrectedProjection( "_6E15_Coin_stats_470V_trig395V_parse.root", 5, 60, mean_slope, mean_constant )

projection_canvas = ROOT.TCanvas("pc","pc",3200,2000)
projection_canvas.Divide(5, 2)

projection_canvas.cd(1)
_prerad_histo[0].SetLineColor(ROOT.kRed)
_prerad_histo[0].Draw()

projection_canvas.cd(2)
_4E14_histo[0].SetLineColor(ROOT.kGreen)
_4E14_histo[0].Draw()

projection_canvas.cd(3)
_1E15_histo[0].SetLineColor(ROOT.kBlue)
_1E15_histo[0].Draw()

projection_canvas.cd(4)
_3E15_histo[0].SetLineColor(ROOT.kYellow)
_3E15_histo[0].Draw()

projection_canvas.cd(5)
_6E15_histo[0].SetLineColor(ROOT.kBlack)
_6E15_histo[0].Draw()

projection_canvas.cd(6)
_prerad_histo[1].SetLineColor(ROOT.kRed)
_prerad_histo[1].Draw()

projection_canvas.cd(7)
_4E14_histo[1].SetLineColor(ROOT.kGreen)
_4E14_histo[1].Draw()

projection_canvas.cd(8)
_1E15_histo[1].SetLineColor(ROOT.kBlue)
_1E15_histo[1].Draw()

projection_canvas.cd(9)
_3E15_histo[1].SetLineColor(ROOT.kYellow)
_3E15_histo[1].Draw()

projection_canvas.cd(10)
_6E15_histo[1].SetLineColor(ROOT.kBlack)
_6E15_histo[1].Draw()

projection_canvas.SaveAs("lowerBias_projection_toa{}_cfd{}.png".format(5, 60))
projection_canvas.Close()

raw_input()

'''

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetOptFit(1)
'''
file_list = ["Coin_stats_90V_trig395V_parse.root",
             "Coin_stats_100V_trig395V_parse.root",
             "Coin_stats_110V_trig395V_parse.root",
             "preRad/Coin_stats_120V_trig395V_parse.root",
             "preRad/Coin_stats_130V_trig395V_parse.root" ]
'''

preRad_file_list_s = ["preRad/Coin_stats_120V_trig395V_parse.root",
                     "preRad/Coin_stats_130V_trig395V_parse.root" ]

_4e14_file_list_s  = ["_4E14/Coin_stats_430V_trig395V_parse.root",
                     "_4E14/Coin_stats_400V_trig395V_parse.root" ]

_1e15_file_list_s  = ["_1E15/Coin_stats_475V_trig400V_parse.root",
                     "_1E15/Coin_stats_460V_trig400V_parse.root" ]

_3e15_file_list_s  = ["_3E15/Coin_stats_495V_trig395V_parse.root",
                     "_3E15/Coin_stats_470V_trig395V_parse.root" ]

_6e15_file_list_s  = ["_6E15/Coin_stats_495V_trig395V_parse.root",
                     "_6E15/Coin_stats_470V_trig395V_parse.root" ]

file_list = list()
'''
file_list.append(preRad_file_list_s)
file_list.append(_4e14_file_list_s)
file_list.append(_1e15_file_list_s)
file_list.append(_3e15_file_list_s)
file_list.append(_6e15_file_list_s)
'''
file_list = preRad_file_list_s + _4e14_file_list_s + _1e15_file_list_s + _3e15_file_list_s + _6e15_file_list_s

fit_list = list()

#color_list = [ROOT.kRed, ROOT.kGreen, ROOT.kBlue, ROOT.kYellow, ROOT.kBlack]
color_list = [2,3,4,5,6,7,8,9,10,11,12,13,14]

for file in file_list:
    fit_list.append( GetLinearFit( file, 5, 60 ) )

canvas = ROOT.TCanvas("c","c")
canvas.cd()
i = 0

for j in range(len(fit_list)):
    print(i)
    if i < len(fit_list):
        fit_list[i][0].SetLineColor( color_list[i] )
        fit_list[i+1][0].SetLineColor( color_list[i] )
        fit_list[i+1][0].SetLineStyle( 2 )

        fit_list[i][1].SetMarkerColor( color_list[i] )
        fit_list[i][1].SetMarkerStyle(7)
        fit_list[i+1][1].SetMarkerColor( color_list[i] )
        fit_list[i+1][1].SetMarkerStyle(7)

        if i == 0:
            fit_list[i][0].Draw()
            fit_list[i+1][0].Draw("same")
        else:
            fit_list[i][0].Draw("same")
            fit_list[i+1][0].Draw("same")

        fit_list[i][1].Draw("same")
        fit_list[i+1][1].Draw("same")
        i = i + 2

canvas.SaveAs("sub_cfd{}-ToA{}.png".format(5,60))
canvas.Close()

mean_constant = 0.0
mean_slope = 0.0
for i in range(len(fit_list)):
    mean_constant = fit_list[i][0].GetParameter(0) + mean_constant
    mean_slope = fit_list[i][0].GetParameter(1) + mean_slope

mean_constant = mean_constant/5.0
mean_slope = mean_slope/5.0

histo_list = list()
for file in file_list:
    histo_list.append( CorrectedProjection( file, 5, 60, mean_slope, mean_constant ) )

projection_canvas = ROOT.TCanvas("pc","pc",6400,2000)
projection_canvas.Divide( len(file_list), 2 )


print(len(fit_list))
for i in range(1, len(fit_list)*2+1):
    if i < len(fit_list)+1:
        projection_canvas.cd( i )
        histo_list[i-1][0].SetLineColor( 2 )
        histo_list[i-1][0].Draw()
    else:
        projection_canvas.cd( i )
        print("i {}".format(i))
        print(i-len(fit_list)-1)
        histo_list[i-len(fit_list)-1][1].SetLineColor( 2 )
        histo_list[i-len(fit_list)-1][1].Draw()

projection_canvas.SaveAs("sub_projection_toa{}_cfd{}.png".format(5, 60))
projection_canvas.Close()


for i in range( len(file_list) ):
    out_name = file_list[i].split("/")
    cfd_out_txt = open( "_sub_{}_{}_.txt".format(out_name[0],out_name[1]),"w")
    cfd_out_txt.write("cfd sigma")
    cfd_out_txt.write("\n")

    cfd_corr_out_txt = open( "_sub_{}_{}_corr.txt".format(out_name[0],out_name[1]),"w")
    cfd_corr_out_txt.write("cfd sigma")
    cfd_corr_out_txt.write("\n")

    for cfd in range(100):

        new_fit_list = list()
        for file in file_list:
            new_fit_list.append( GetLinearFit( file, 5, cfd ) )

        mean_constant = 0.0
        mean_slope = 0.0
        for k in range(len(new_fit_list)):
            mean_constant = new_fit_list[k][0].GetParameter(0) + mean_constant
            mean_slope = new_fit_list[k][0].GetParameter(1) + mean_slope

        mean_constant = mean_constant/(1.0*len(new_fit_list))
        mean_slope = mean_slope/(1.0*len(new_fit_list))

        histo = CorrectedProjection( file_list[i], 5, cfd, mean_slope, mean_constant )
        cfd_out_txt.write("{} {}".format(cfd, histo[4]))
        cfd_corr_out_txt.write("{} {}".format(cfd, histo[5]))

        cfd_out_txt.write("\n")
        cfd_corr_out_txt.write("\n")
        print(cfd)

    cfd_out_txt.close()
    cfd_corr_out_txt.close()
    print("finished")

raw_input()


'''
ExportFit2TxT( "Coin_stats_90V_trig395V_parse.root" )
ExportFit2TxT( "Coin_stats_100V_trig395V_parse.root" )
ExportFit2TxT( "Coin_stats_110V_trig395V_parse.root" )
ExportFit2TxT( "Coin_stats_120V_trig395V_parse.root" )
ExportFit2TxT( "Coin_stats_130V_trig395V_parse.root" )
'''
