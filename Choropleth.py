import plotly.plotly as py
import plotly.tools as plottools
import plotly.figure_factory as ff

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
		colors = ['#FAFF70','#FAEB69','#FAD862','#FBC55B','#FBB154','#FC9E4D','#FC8B46','#FD783F','#FD6438','#FE5131','#FE3E2A','#FF2B24']

		fig = ff.create_choropleth(
		    fips=fips, values=values, scope=['USA'],
		    show_state_data=True,
		    colorscale=colors,
		    binning_endpoints=intervals,
		    show_hover=True, centroid_marker={'opacity': 1},
		    asp=2.9, title='West Coast Sites Traceroute',
		    legend_title='Number of Hits',
		    round_legend_values=True
		)
		py.plot(fig, filename='Traceroute Choropleth')

	def createPlot(self):
		self.plotData(self.locData)

	def testPlot(self):
		testData = {'34017':1,'20155':6,'36059':12,'53033':17,'36001':21,'32510':27,'33001':34,'40001':39,'04001':40,'33001':45,'39001':57}
		self.plotData(testData)

	@staticmethod
	def openHelp():
		help(ff.create_choropleth)