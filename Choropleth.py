import plotly.plotly as py
import plotly.tools as plottools
import plotly.figure_factory as ff
import plotly.io as pio

import numpy as np
import pandas as pd

from TracerouteData import TracerouteData
from LocData import LocData

class Choropleth:

	def __init__(self,locData):
		self.locData = locData

	def plotData(self,data):
		plottools.set_credentials_file(username='mintyshoes', api_key='6EAJ1duK8IeBcbjMuoEg')

		fips = data.keys()
		values = data.values()
		intervals = range(0,51,5)

		colors = ["#ffffe0", "#ffffe0", "#ffd196", "#ffb67f", "#ff9b6f", "#f98065", "#ee665d", "#e14d54", "#cf3548", "#bb1e37", "#a40921", "#8b0000"]
		# colors = ["#FFFED1","#FFEAB6","#FFD5A6","#FFC096","#FFAB85","#FF9675","#FF8265","#FF6D55","#FF5844","#FF4334","#FF2E24","#FF1A14"]
		# colors = ['#FAFF70','#FAEB69','#FAD862','#FBC55B','#FBB154','#FC9E4D','#FC8B46','#FD783F','#FD6438','#FE5131','#FE3E2A','#FF2B24']

		fig = ff.create_choropleth(
			fips=fips, values=values, scope=['USA'],
			show_state_data=True,
			colorscale=colors,
			binning_endpoints=intervals,
			show_hover=True, centroid_marker={'size':6,'opacity': 1, 'color':'black'},
			asp=2.9, title='West Coast Sites Traceroute',
			legend_title='Number of Hits',
			round_legend_values=True
		)
		# py.plot(fig, filename='Traceroute Choropleth')
		pio.write_image(fig, "Output_Heatmap.png")
		print("Heatmap Created!")

	def createPlot(self):
		self.plotData(self.locData)

	def testPlot(self):
		testData = {'34017':1,'20155':6,'36059':12,'53033':17,'36001':21,'32510':27,'33001':34,'40001':39,'04001':40,'33001':45,'39001':57}
		counties_text_file = open("national_county.txt","r")
		for line in counties_text_file:
			line = line.split(',')
			FIPS = line[1]+line[2]
			if FIPS not in testData.keys():
				testData[FIPS] = 1
		counties_text_file.close()
		self.plotData(testData)

	@staticmethod
	def openHelp():
		help(ff.create_choropleth)