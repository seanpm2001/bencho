#!/usr/bin/env python
# a line plot with errorbars
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import csv
import string
import sys
from optparse import OptionParser
from matplotlib.ticker import MaxNLocator


class Pyplot:

	def __init__(self):
		parser = self.getOptionParser()
		(options, args) = parser.parse_args(sys.argv, None)

		if options.file == None:
			parser.print_help()
			sys.exit(0)

		self.plots=list()
		self.settings = {}

		self.setUp()
		self.plot(options.file, options.scriptfile)

	def getOptionParser(self):
	    parser = OptionParser()
	    parser.add_option('-f', '--file', help="set csv file", type='string', dest='file')
	    parser.add_option('-s', '--scriptfile', help="set benchmarks script file", type='string', dest='scriptfile')
	    return parser

	def setUp(self):

		#defining default settings
		self.settings['title'] = scriptFile[:scriptFile.find('.')]
		self.settings['type'] ='line'
		self.settings['xScale'] = 'linear'
		self.settings['xScaleBase'] = 10
		self.settings['xLabel'] = 'par_stride'
		self.settings['yLabel'] = 'CPU Cycles'
		self.settings['yDivider'] = 1
		self.settings['xDivider'] = 1
		self.settings['grid'] = 'none'
		self.settings['plotList'] = []
		self.settings['figureSize'] = (6.5, 6)
		self.settings['numberOfYTicks'] = False

		self.plots.append(dict(self.settings))

	def plot(self, csvFile, scriptFile):

		plotNumber = 1
		plotDir = csvFile[:csvFile.rfind('/') + 1]
		plotName = csvFile[csvFile.rfind('/'):]
		plotName = plotName[:plotName.find('.')]

		plotList = list()

		for settingsList in self.plots:

			data = list()
			if settingsList['type'] == 'boxplot':
				data = self.getDataForBoxplot(csvFile, settingsList)
			else:
				data = self.getDataForNormalPlot(csvFile, settingsList)

			if data:

				mpl.rc('lines', linewidth=2)

				fig = plt.figure(1, figsize=settingsList['figureSize'])
				mpl.rcParams['axes.color_cycle'] = ['r', 'g', 'b', 'c']
				ax = fig.add_subplot(2,1,1)

				if settingsList['type'] == 'boxplot':
					for i in range(0,len(data[1])):
						ax.boxplot(data[1][i], positions=data[0])
				else:
					for i in range(0,len(data[1])):
						ax.plot(data[0], data[1][i], label=data[2][i])

				ax.set_title(settingsList['title'])
				ax.set_xlabel(settingsList['xLabel'])
				ax.set_ylabel(settingsList['yLabel'])
				ax.set_xscale(settingsList['xScale'], basex=settingsList['xScaleBase'])
				if settingsList['numberOfYTicks']:
					ax.yaxis.set_major_locator(MaxNLocator(settingsList['numberOfYTicks']))
				if settingsList['grid'] is 'yAxis':
					ax.yaxis.grid(True)

				# ax.annotate('Cache Linesize', (64, 500), xytext=None, xycoords='data', textcoords='data', arrowprops=None)
				
				ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True)

				resultPlot = plotDir + plotName + '_Py_' + str(plotNumber) + '.pdf'
				plotList.append(resultPlot)
				plt.savefig(resultPlot)
				plotNumber += 1
				plt.close()

		return plotList

	def getDataForNormalPlot(self, csvFile, settingsList):

		csvReader = csv.reader(open(csvFile))
		line = csvReader.next()
		lineContents = line[0].split(' ')
		lineIndices = list()
		lineLabels = list()
		for counter in settingsList['plotList']:
			for entry in lineContents:
				if type(counter) is tuple: 
					if entry == counter[0]:
						lineIndices.append(lineContents.index(entry))
						lineLabels.append(counter[1])
				else:
					if entry == counter:
						lineIndices.append(lineContents.index(entry))
						lineLabels.append(counter)

		if len(lineIndices) > 0:
			x = list()
			y = list()
			for index in lineIndices:
				z = list()
				y.append(z)

			for line in csvReader:
				lineContents = line[0].split(' ')
				x.append(float(lineContents[0]) / settingsList['xDivider'])
				for i in range(0,len(lineIndices)):
					y[i].append(float(lineContents[lineIndices[i]]) / settingsList['yDivider'])
			
			return [x, y, lineLabels]
		return False

	def getDataForBoxplot(self, csvFile, settingsList):

		csvReader = csv.reader(open(csvFile))
		line = csvReader.next()
		lineContents = line[0].split(' ')
		plotLabels = list()
		plotIndices = list()
		for counter in settingsList['plotList']:
			if type(counter) is tuple: 

				valueNumber = 0
				indices = list()
				while counter[0] + '_raw_' + str(valueNumber) in lineContents:
					indices.append(lineContents.index(counter[0] + '_raw_' + str(valueNumber)))
					valueNumber += 1
				if indices:
					plotIndices.append(indices)
					plotLabels.append(counter[1])

			else:
				valueNumber = 0
				indices = list()
				while counter + '_raw_' + str(valueNumber) in lineContents:
					indices.append(lineContents.index(counter + '_raw_' + str(valueNumber)))
					valueNumber += 1
				if indices:
					plotIndices.append(indices)
					plotLabels.append(counter)

		if len(plotIndices) > 0:
			x = list()
			y = list()
			for indexList in plotIndices:
				z = list()
				y.append(z)

			lineCount = 0
			for line in csvReader:
				lineContents = line[0].split(' ')
				x.append(float(lineContents[0]) / settingsList['xDivider'])
				for i in range(0,len(plotIndices)):
					y[i].append(list())
					for j in range(0,len(plotIndices[i])):
						y[i][lineCount].append(float(lineContents[plotIndices[i][j]]) / settingsList['yDivider'])
				lineCount += 1
				
			return [x, y, plotLabels]
		return False