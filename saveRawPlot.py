from ROOT import *
from optparse import OptionParser
import os

def plotRawPulse( fileName, entryStart, entryEnd ):
	
	ifile = TFile.Open(fileName)
	
	iTree = ifile.Get("wfm")
	
	nEvent = iTree.GetEntries()
	
	iTree.SetMarkerStyle(7)
	
	if( entryEnd > nEvent or entryStart > nEvent ):
		
		print('range error, total events = {}'.format(nEvent) )
		
	else:
		
		gROOT.SetBatch(kTRUE)
		
		while( entryStart < entryEnd ):
			
			oCanvas = TCanvas( 'raw_pulse_Entry= {}'.format(entryStart), '', 1000, 1000)
			oCanvas.Divide(1,2)
			
			oCanvas.cd(1)
			
			iTree.Draw('-w2:t2', 'Entry$ == {}'.format(entryStart) )
			
			oCanvas.cd(2)
			
			iTree.Draw('-w3:t3', 'Entry$ == {}'.format(entryStart) )
			
			oCanvas.SaveAs( 'pyPlotRaw_Entry_{}.png'.format(entryStart) )
			
			entryStart += 1
	
		print('finished')

if __name__ == "__main__":
	
	parser = OptionParser()
	parser.add_option('-f', '--fileName=', dest='fileName', type='string' )
	
	parser.add_option('-s', '--start=', dest='entryStart', type='int' )
	
	parser.add_option('-e', '--end=', dest='entryEnd', type='int' )
	
	(options, args) = parser.parse_args()
	
	fileName = options.fileName
	entryStart = options.entryStart
	entryEnd = options.entryEnd
	
	plotRawPulse( fileName, entryStart, entryEnd)
	

	
