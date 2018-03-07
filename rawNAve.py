from ROOT import *
from optparse import OptionParser
import os

def plotRawPulse( fileName, aveFileName, voltage, entryStart, entryEnd ):

	ifile = TFile.Open(fileName)

	avePulseFile = TFile.Open(aveFileName)

	avePulse = avePulseFile.Get(voltage)

	iTree = ifile.Get("wfm")

	nEvent = iTree.GetEntries()

	iTree.SetMarkerStyle(20)

	cut = TCut()

	tcut1 = "tmax2[0]-cfd3[20] > {}".format(-500)
	tcut2 = "&&tmax2[0]-cfd3[20] < {}".format(500)
	pcut1 =  "&&pmax2[0] > {}".format(0)
	pcut2 = "&&pmax2[0] < {}".format(360)
	tcut3 = "&&tmax3[0]-cfd3[20] > {}".format(200)
	tcut4 =  "&&tmax3[0]-cfd3[20] < {}".format(500)
	pcut3 = "&&pmax3[0] > {}".format(70)
	pcut4 = "&&pmax3[0] < {}".format(375)

	cut = tcut1 + tcut2 + pcut1 + pcut2 + tcut3 + tcut4 + pcut3 + pcut4

	if( entryEnd > nEvent or entryStart > nEvent ):

		print('range error, total events = {}'.format(nEvent) )

	else:

		gROOT.SetBatch(kTRUE)

		while( entryStart < entryEnd ):

			oCanvas = TCanvas( 'raw_pulse_Entry= {}'.format(entryStart), '', 1618, 1000)

			oCanvas.Divide(1,2)

			oCanvas.cd(1)

			avePulse.SetLineColor(kRed)
			avePulse.GetXaxis().SetRangeUser(-10000,10000)
			avePulse.GetYaxis().SetRangeUser(-10,180)
			avePulse.Draw()

			check = iTree.Draw('-w2:t2-cfd3[20]', '{} && Entry$ == {}'.format(cut, entryStart), "same" )

			if(check == 0):
				print "no event, pass"
			else:
				oCanvas.cd(2)

				triggerWaveForm = TH2D("trigger","trigger", 20000/50, -10000, 10000, 200, -10, 180)
				iTree.Project("trigger","-w3:t3", "{} && Entry$=={}".format(cut, entryStart) )
				triggerWaveForm.GetXaxis().SetRangeUser(-10000,10000)
				triggerWaveForm.GetYaxis().SetRangeUser(-10,180)
				triggerWaveForm.SetMarkerStyle(20)
				triggerWaveForm.Draw()

				oCanvas.SaveAs( 'py_Event{}.png'.format(entryStart) )
				gROOT.FindObject("trigger").Delete()

			entryStart += 1

		print('finished')

if __name__ == "__main__":

	parser = OptionParser()
	parser.add_option('-f', '--fileName=', dest='fileName', type='string' )

	parser.add_option('-a', '--aveFileName', dest='aveFileName', type='string')

	parser.add_option('-v', '--voltage', dest='voltage', type='string')

	parser.add_option('-s', '--start=', dest='entryStart', type='int' )

	parser.add_option('-e', '--end=', dest='entryEnd', type='int' )

	(options, args) = parser.parse_args()

	fileName = options.fileName
	aveFileName = options.aveFileName
	voltage = options.voltage
	entryStart = options.entryStart
	entryEnd = options.entryEnd

	plotRawPulse( fileName, aveFileName, voltage, entryStart, entryEnd)
