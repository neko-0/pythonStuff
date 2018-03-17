#need python3

import numpy as np
import csv
from optparse import OptionParser
import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


#=======================================================================================
#============================read data file=============================================
#=======================================================================================

def txtReader(ifile):

	print('reading file...')

	data_list = []

	with open(ifile, 'r') as txtfile:
		data = csv.reader(txtfile, delimiter=' ')
		for row in data:
			data_list.append(row)

	return data_list


#=======================================================================================
#=======================Get time resolution=============================================
#=======================================================================================

def getRes(sigma, triggerRes):

	res = np.sqrt( np.power(sigma, 2) - np.power(triggerRes, 2) )

	return round(res, 2)


#=======================================================================================
#=====================Get error of the time resolution==================================
#=======================================================================================


def getResErr(sigma, sigmaErr, triggerRes, triggerResErr):

	diff = np.power(sigma, 2) - np.power(triggerRes, 2)

	resErr = np.sqrt( (np.power(sigmaErr,2)) * (np.power(sigma, 2)) / diff + (np.power(triggerResErr,2)) * (np.power(triggerRes, 2)) / diff )

	return round(resErr, 2)


#=======================================================================================
#=======================Find minimum resolution=========================================
#=======================================================================================

def getMin(data): #data format [CFD%, Res, ResErr]

	optimalCFD = [0, 1000.0, 1000.0]

	for item in data[:]:

		if( item[1] <= optimalCFD[1] ):

			for i in range(len(optimalCFD)):

				optimalCFD[i] = item[i]

	return optimalCFD


#=======================================================================================
#=======================Find difference of optimal Resolution===========================
#=======================================================================================


def diffOptimal(data, optimalRes):

	for item in data[:]:

		diff = item[1] - optimalRes

		item.append( round(diff, 2) )

	return data


#=======================================================================================
#========================================Find boundaries================================
#=======================================================================================


def findBound(data, optimalCFD ,tolerance): #data[CFD, Res, ResErr, diffOptimal]

	bound = []

	bound.append( data[optimalCFD[0]] )

	startPoint = optimalCFD[0]

	lowerCount = startPoint
	upperCount = startPoint

	while True:

		if(lowerCount > 0):
			if( data[lowerCount][3] <= tolerance ):
				bound.append( data[lowerCount] )
		lowerCount = lowerCount - 1

		if( upperCount < 99 ):
			if( data[upperCount][3] <= tolerance ):
				bound.append( data[upperCount] )
		upperCount = upperCount + 1

		if(lowerCount < 0 and upperCount > 99):
			break

	return bound


def func(x, a, b, c):
	return a*x**(2) + b*x + c

def fitBound(bound, optimalCFDValue, tolerance):

	var0 = np.array([2,4,1])

	X = np.array([])
	Y = np.array([])

	for item in bound[:]:

		X = np.append(X, item[0])
		Y = np.append(Y, item[3])

	x = np.arange(0,100,1)

	popt, pcov = curve_fit(func, X, Y, var0, maxfev=5000)
	plt.plot(x, func(x,*popt), 'b-', label='fit')
	plt.plot(X,Y,'ro', label = 'Data')
	plt.xlabel('CFD')
	plt.ylabel('diffOptimal')
	plt.legend()
	plt.show()

	maxBound = ( -popt[1] + np.sqrt( np.power(popt[1], 2) - 4 * popt[0] *(popt[2]-tolerance) ) ) / ( 2 * popt[0] )
	minBound = ( -popt[1] - np.sqrt( np.power(popt[1], 2) - 4 * popt[0] *(popt[2]-tolerance) ) ) / ( 2 * popt[0] )

	optimalCFDErr = [optimalCFDValue - minBound, maxBound - optimalCFDValue]

	return optimalCFDErr

#=======================================================================================
#=====================Make header and CFD scan==========================================
#=======================================================================================


def CFDvsRes(ifile, triggerRes, triggerResErr):

	data = txtReader(ifile)

	header = []

	result = []

	CFD = 0;

	for item in data[:4]:

		header.append(item)

	header.append( ['Trigger', triggerRes] )


	for item in data[5:]:

		res    = getRes( float(item[1]), triggerRes )

		resErr = getResErr( float(item[1]), float(item[2]), triggerRes, triggerResErr )

		result.append([CFD, res, resErr])

		CFD    = CFD + 1

	optimalCFD = getMin(result)

	header.append( ['CFD_Fraction', 'Res[ps]', 'Err[ps]', 'diffOptimal'] )

	result     = diffOptimal( result, optimalCFD[1] )

	tolerance = optimalCFD[1]*0.1

	#bound = findBound(result, optimalCFD, tolerance)

	#optimalCFDErr = fitBound(bound, optimalCFD[0], tolerance)

	result.append( [] )
	result.append( ['Opitmal_CFD', 'Optimal_Res[ps]', 'Err[ps]'] )
	result.append( optimalCFD )
	result.append( ['10%_of_optimal', tolerance] )
	#result.append( ['optimalCFDErrMin', optimalCFDErr[0]] )
	#result.append( ['optimalCFDErrMax', optimalCFDErr[1]] )

	return header, result


#=======================================================================================
#=============================Write data to file========================================
#=======================================================================================


def WriteToFile(ofile, header, result):

	ofile = 'parsed_' + ofile

	with open(ofile, 'w') as outfile:

		writer = csv.writer(outfile, delimiter=' ')

		for item in header[:]:

			writer.writerow(item)

		for item in result[:]:

			writer.writerow(item)

	print('finished')


#=======================================================================================
#=======================================================================================
#=======================================================================================


if __name__ == "__main__":

	listdir = os.listdir()

	parser = OptionParser()
	parser.add_option('-f', '--ifile', dest='filename', type='string')
	parser.add_option('-t', '--trigger', dest='triggerRes', type='float', default=10.0)
	parser.add_option('-e', '--triggerErr', dest='triggerResErr', type='float', default=10.0)

	(options, args) = parser.parse_args()
	'''
	for item in listdir[:]:
		print(item)
		ifile = item
		triggerRes = options.triggerRes
		triggerResErr = options.triggerResErr

		(header, result) = CFDvsRes(ifile, triggerRes, triggerResErr)

		WriteToFile(ifile, header, result)
	'''

	ifile = options.filename
	triggerRes = options.triggerRes
	triggerResErr = options.triggerResErr

	print("ifile = {}".format( ifile ))
	print("triggerRes = {}".format( triggerRes) )
	print("triggerResErr = {}".format( triggerResErr) )

	(header, result) = CFDvsRes(ifile, triggerRes, triggerResErr)
	WriteToFile(ifile, header, result)
