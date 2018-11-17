from TracerouteData import TracerouteData
from Choropleth import Choropleth
from LocData import LocData

# Choropleth.openHelp()
locData = LocData()
for number in range(0,10):
	# trData = TracerouteData("172.64.111.36")	# Cali
	trData = TracerouteData("128.95.155.197") 	# Washington State
	trData.updateProtocol("TCP")
	ips = trData.genIPs()
	print(ips)
	locData.genFIPSList(ips)
print(locData.FipsList)
# print(locData.FipsDict)
# print(locData.countries)

choropleth = Choropleth(locData.FipsDict)
choropleth.createPlot()
# choropleth.testPlot()