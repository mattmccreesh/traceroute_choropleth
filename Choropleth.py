import plotly.plotly as py
import plotly.tools as plottools
import plotly.figure_factory as ff

import numpy as np
import pandas as pd

from TracerouteData import TracerouteData
from LocData import LocData

trData = TracerouteData("172.64.111.36")
trData.traceroute2List()
ips = trData.genIPs()
print(ips)
locData = LocData(trData.genIPs())
locData.genFIPSList()
# print(locData.FipsDict)
# print(locData.FipsDict.keys())
# print(locData.FipsDict.values())

# plottools.set_credentials_file(username='mintyshoes', api_key='6EAJ1duK8IeBcbjMuoEg')

# df_sample = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/laucnty16.csv')
# df_sample['State FIPS Code'] = df_sample['State FIPS Code'].apply(lambda x: str(x).zfill(2))
# df_sample['County FIPS Code'] = df_sample['County FIPS Code'].apply(lambda x: str(x).zfill(3))
# df_sample['FIPS'] = df_sample['State FIPS Code'] + df_sample['County FIPS Code']

# colorscale = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
#               "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
#               "#08519c","#0b4083","#08306b"]
# endpts = list(np.linspace(1, 10, len(colorscale) - 1))
# # fips = df_sample['FIPS'].tolist()
# # values = df_sample['Unemployment Rate (%)'].tolist()
# fips = locData.FipsDict.keys()
# values = locData.FipsDict.values()

# fig = ff.create_choropleth(
#     fips=fips, values=values, scope=['usa'],
#     binning_endpoints=endpts, colorscale=colorscale,
#     show_state_data=False,
#     show_hover=True, centroid_marker={'opacity': 0},
#     asp=2.9, title='USA by Unemployment %',
#     legend_title='% unemployed'
# )
# py.plot(fig, filename='choropleth_full_usa')