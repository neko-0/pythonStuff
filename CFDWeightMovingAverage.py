from optparse import OptionParser
import os
import numpy as np
import csv
import math

def getMinIndex(data): #find the minimum of np array

	minRes = 999.0

	minIndex = 0

	step = 0

	for item in data[:]:
		if( float(item) <= minRes ):
			minRes = item
			minIndex = step
		step += 1

	return minIndex

def getResAtCFD(percentage, cfd, res, err): #accept 3 np arrays cfd res and err

	result = np.empty([1,3])

	for i in range(len(cfd)):
		if( abs(cfd[i] - percentage) < 1.0 ):
			temp = np.array([cfd[i], res[i], err[i]])
			result = np.vstack((result,temp))
	return result

def findBoundIndex(minIndex, minValue, cfd, res):

	_10percent = 0.1 * minValue

	highB = 0
	lowB = 0

	lowBstep = minIndex
	highBstep = minIndex

	confirmRange = 5
	confirmStep  = 0

	while(lowBstep > 0.0):
		if( abs(res[lowBstep-1] - minValue) < _10percent ):
			lowB = lowBstep - 1
		else:
			confirmStep += 1
			if( confirmStep == confirmRange ):
				confirmStep = 0
				break
		lowBstep += -1

	while( highBstep < (len(cfd) - 1) ):
		if( abs(res[highBstep+1] - minValue) < _10percent ):
			highB = highBstep + 1
		else:
			confirmStep += 1
			if( confirmStep == confirmRange ):
				confirmStep = 0
				break
		highBstep += 1

	return np.array([cfd[lowB],cfd[highB]])



def weightMovingAverage( iFileName, npt = 6, totalStep = 500, toRealCFD = 0.2):

	###################################################

	#preparing and reading file

	holder = [np.array(map(str, line.split())) for line in open(iFileName)]

	cfdIndex = 0;
	resIndex = 1;
	errIndex = 2;

	numRowInHeader = 6;

	CFD = np.array([])
	timeResolution = np.array([])
	error = np.array([])

	CFD_w = np.array([])
	timeResolution_w = np.array([])
	error_w = np.array([])

	###################################################

	#first 6 rows are headers

	for i in range(numRowInHeader):
		for j in range( len(holder[i]) ):
			print holder[i][j],
		print

	###################################################

	#next 500 are data

	print "preparing data..."

	#for item in holder[numRowInHeader:numRowInHeader+totalStep]:
		#print item[cfdIndex]

	for item in holder[numRowInHeader:numRowInHeader+totalStep]:
		CFD = np.append( CFD, toRealCFD * float(item[cfdIndex]) )
		timeResolution = np.append( timeResolution, float(item[resIndex]) )
		error = np.append( error, float(item[errIndex]) )

	###################################################

	print "using ", npt, " for weight moving average"

	lastPoint = totalStep - npt - 1

	for i in range(lastPoint):

		top = 0.0
		bot = 0.0
		cfd = 0.0

		for j in range(npt):

			weight = 1.0/(error[i]*error[i])

			cfd = cfd + CFD[i]
			top = top + timeResolution[i] * weight
			bot = bot + weight
			i += 1

		CFD_w = np.append( CFD_w, cfd/npt )
		timeResolution_w = np.append( timeResolution_w, top/bot )
		error_w = np.append( error_w, math.sqrt(1.0/bot) )

	print "finished"

	###################################################

	#finding the minimum res...etc

	minIndex = getMinIndex( timeResolution_w )

	minCFD = CFD_w[minIndex]
	minRes = np.array( [timeResolution_w[minIndex], error_w[minIndex]] )

	minCFDErr = findBoundIndex(minIndex, minRes[0], CFD_w, timeResolution_w)

	_203050 = np.array( [getResAtCFD(20.0, CFD_w, timeResolution_w, error_w), getResAtCFD(30.0, CFD_w, timeResolution_w, error_w), getResAtCFD(50.0, CFD_w, timeResolution_w, error_w)] )




	###################################################

	ofile = '_averaged_' + str(npt) + iFileName

	output = open(ofile, 'w')

	Write_csv = csv.writer(output, delimiter = " ")

	#header
	for i in range(numRowInHeader):
		for j in range( len(holder[i]) ):
			output.write( holder[i][j] )
			output.write( '|' )
		output.write('\n')

	#average data
	for i in range(len(timeResolution_w)):
		output.write( str( CFD_w[i]) )
		output.write( '|' )
		output.write( str( timeResolution_w[i]) )
		output.write( '|' )
		output.write( str( error_w[i]) )
		output.write( '|' )
		output.write('\n')

	#minimum and desired cfd
	output.write('\n')
	output.write( 'MinCFD|MinRes|MinResErr|MinCFDlow|minCFDhigh' )
	output.write('\n')
	output.write( str(minCFD) )
	output.write( '|' )
	output.write( str(minRes[0]) )
	output.write( '|' )
	output.write( str(minRes[1]) )
	output.write( '|' )
	output.write( str(minCFDErr[0]) )
	output.write( '|' )
	output.write( str(minCFDErr[1]) )
	output.write('\n')

	output.write('\n')
	for item in _203050[:]:
		for subItem in item[:]:
			for i in range(len(subItem)):
				output.write(str(subItem[i]))
				output.write( '|' )
			output.write( '\n' )
		output.write( '\n' )



	output.close()

	###################################################



if __name__ == "__main__":

	parser = OptionParser()

	parser.add_option('-f', '--fileName=', dest='fileName', type='string' )

	parser.add_option('-p', '--npt=', dest='npt', type='int' )

	(options, args) = parser.parse_args()
	
	ifileName = options.fileName
	npt = options.npt

	weightMovingAverage(ifileName,npt)
