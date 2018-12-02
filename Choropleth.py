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
		intervals = range(0,51,5) # 10 Values

		colors = ['#4682B4','#ffff00','#ffe416','#ffc82c','#ffab3f','#fb8d4b','#f27151','#e55550','#d33a48','#be2239','#a70a23','#8b0000']
		county_outline_color = '#4682B4'

		fig = ff.create_choropleth(
			fips=fips, values=values, scope=['USA'],
			show_state_data=True,
			colorscale=colors,
			binning_endpoints=intervals,
			show_hover=True, centroid_marker={'opacity': 0},
			asp=2.9, title='Traceroute Choropleth',
			legend_title='Number of Hits',
			round_legend_values=True,
			county_outline={'color': county_outline_color, 'width': 0.3},
			state_outline={'color': '#A8A8A8', 'width': 0.5}
		)
		# df_flight_paths = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_aa_flight_paths.csv')
		# df_flight_paths.head()
		# flight_paths = []
		# for i in range( len( df_flight_paths ) ):
		# 	flight_paths.append(
		# 		dict(
		# 			type = 'scattergeo',
		# 			locationmode = 'USA-states',
		# 			lon = [ df_flight_paths['start_lon'][i], df_flight_paths['end_lon'][i] ],
		# 			lat = [ df_flight_paths['start_lat'][i], df_flight_paths['end_lat'][i] ],
		# 			mode = 'lines',
		# 			line = dict(
		# 				width = 1,
		# 				color = 'red',
		# 			),
		# 			opacity = float(df_flight_paths['cnt'][i])/float(df_flight_paths['cnt'].max()),
		# 		)
		# 	)

		pio.write_image(fig, "Output_Heatmap.png")
		print("Heatmap PNG file was saved to drive.")
		py.plot(fig, filename='Traceroute Choropleth')

	def createPlot(self):
		self.plotData(self.locData)
		print("Heatmap Created!")

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