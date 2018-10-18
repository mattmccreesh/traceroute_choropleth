from TracerouteData import TracerouteData
from LocData import LocData

trData = TracerouteData("www.google.com")
trData.traceroute2List()
ips = trData.genIPs()
print(ips)
locData = LocData(trData.genIPs())
print(locData.FIPS)