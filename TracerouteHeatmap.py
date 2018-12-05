from TracerouteData import TracerouteData
from Choropleth import Choropleth
from LocData import LocData

# Choropleth.openHelp()

filename = "westcoastips.txt"
ips_file = open(filename,"r")
input_ips = []
for line in ips_file:
	input_ips.append(line.strip())
locData = LocData()
# print(input_ips)
trData = TracerouteData(input_ips) 	
trData.updateProtocol("ICMP")
output_ips = trData.genIPs()
output_dict = trData.ipsDict
# print(trData.ipsDict)
locData.genFIPS(output_dict)
# print(locData.FipsList)
# print(locData.masterData)
locData.writeToCSV('LocData.csv')
# print(locData.counties)

choropleth = Choropleth(locData.FipsDict)
choropleth.createPlot()