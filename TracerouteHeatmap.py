from TracerouteData import TracerouteData
from LocData import LocData

locData = LocData()
for number in range(0,30):
	trData = TracerouteData("172.64.111.36")
	trData = TracerouteData("www.google.com")
	trData.updateProtocol("TCP")
	ips = trData.genIPs()
	print(ips)
	locData.genFIPSList(ips)
print(locData.FIPS)
print(locData.FipsDict)
print(locData.countries)

choropleth = Choropleth(locData.FipsDict)