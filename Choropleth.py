import plotly.plotly as py
import plotly.tools as plottools
import plotly.figure_factory as ff

import numpy as np
import pandas as pd

from TracerouteData import TracerouteData
from LocData import LocData

class Choropleth:

	def _init_(self,locData):
		self.locData = locData

	def plotData(self):
		plottools.set_credentials_file(username='mintyshoes', api_key='6EAJ1duK8IeBcbjMuoEg')

		fips = self.locData.FipsDict.keys()
		values = self.locData.FipsDict.values()

		fig = ff.create_choropleth(
		    fips=fips, values=values, scope=['USA'],
		    show_state_data=False,
		    show_hover=True, centroid_marker={'opacity': 0},
		    asp=2.9, title='USA by Unemployment %',
		    legend_title='% unemployed'
		)
		py.plot(fig, filename='Traceroute Choropleth')