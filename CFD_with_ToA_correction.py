import ROOT

def CFD_with_ToA_correction( fileName, toa, cfd ):

    root_file = ROOT.TFile.Open( fileName )
    root_tree = root_file.Get( "wfm" )

    gaus = ROOT.TF1("gaus", "gaus")

    cfd_projection_corr = ROOT.TH1D( "cfd_projection_corr", "{} cfd2[{}]-cfd3[20] corr".format(fileName, cfd), 100, 1, 1)

    cfd_projection = ROOT.TH1D( "cfd_projection", "{} cfd2[{}]-cfd3[20]".format(fileName, cfd), 100, 1, 1)

    for ientry, entry in enumerate(root_tree):
        if( entry.pmax2[0] > toa ):
            cfd_projection_corr.Fill( entry.cfd2[cfd]-entry.thTime2[toa] )

    cfd_projection_corr.Fit(gaus,"Q")

    cfd_sigma_corr = gaus.GetParameter(2)

    return cfd_sigma_corr

ROOT.gROOT.SetBatch(ROOT.kTRUE)
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

file_list = preRad_file_list_s + _4e14_file_list_s + _1e15_file_list_s + _3e15_file_list_s + _6e15_file_list_s

for item in file_list[:]:
    out_name = item.split("/")
    cfd_out_txt = open( "_cfd-ToA_{}_{}_.txt".format(out_name[0],out_name[1]),"w")
    cfd_out_txt.write("cfd sigma")
    cfd_out_txt.write("\n")

    for cfd in range(100):
        sigma = CFD_with_ToA_correction( item, 5, cfd )
        cfd_out_txt.write("{} {}".format(cfd, sigma))
        cfd_out_txt.write("\n")

    cfd_out_txt.close()
