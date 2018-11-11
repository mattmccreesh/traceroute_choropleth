from geocoder import ip
from geocoder import geocodefarm
from requests import get
from time import sleep
from urllib import urlencode

class LocData:
    
    def __init__(self, ipAddrs):
        self.ipAddrs = ipAddrs
        self.coords = []
        self.states = []
        self.FIPS = []
        self.FipsDict = {}

    def getFIPSbyLatLong(self, lat, lon):
    	sleep(1)
        params = urlencode({'latitude': lat, 'longitude':lon, 'format':'json'})
        url = 'https://geo.fcc.gov/api/census/block/find?' + params
        response = get(url)
        # print(str(lat) + "," + str(lon))
        if response.text.find("<html>") != -1:
	        r = geocodefarm([lat, lon], method='reverse')
	        # print(r.json['country'])
        else:
        	data = response.json()['County']['FIPS']
        	if data is None:
	        	r = geocodefarm([lat, lon], method='reverse')
	        	# print(r.json['country'])
        	else:
        		# print("Found")
        		return data.encode('ascii','ignore')

    def genFIPSList(self):
        for address in self.ipAddrs:
            g = ip(address)
            self.states.append(g.state)
            self.coords.append(g.latlng)
            fip = self.getFIPSbyLatLong(g.lat, g.lng)
            if fip is not None:
				self.FIPS.append(fip)
				if fip not in self.FipsDict:
					self.FipsDict[fip] = 1
				else:
					self.FipsDict[fip] = self.FipsDict[fip] + 1

