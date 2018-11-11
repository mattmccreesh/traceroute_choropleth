from geocoder import ip
from geocoder import geocodefarm
from requests import get
from time import sleep
from urllib import urlencode

class LocData:
    
    def __init__(self):
        self.ipAddrs = []
        self.coords = []
        self.states = []
        self.countries = []
        self.FIPS = []
        self.FipsDict = {}

    def getFIPSbyLatLong(self, lat, lon):
    	sleep(1)
        params = urlencode({'latitude': lat, 'longitude':lon, 'format':'json'})
        url = 'https://geo.fcc.gov/api/census/block/find?' + params
        response = get(url)
        # print(str(lat) + "," + str(lon))
        if response.text.find("<html>") == -1:
        	print(response)
        	data = response.json()['County']['FIPS']
        	if data is None:
	        	r = geocodefarm([lat, lon], method='reverse')
	        	self.countries.append(r.json['country'])
	        	print("FCC FIPS is None")
        	else:
        		return data.encode('ascii','ignore')
        else:
        	print("Bad Response from FCC")

    def genFIPSList(self, ipAddrs):
    	self.ipAddrs.extend(ipAddrs)
        for address in ipAddrs:
            g = ip(address)
            self.countries.append(g.country)
            self.states.append(g.state)
            self.coords.append(g.latlng)
            fip = self.getFIPSbyLatLong(g.lat, g.lng)
            if fip is not None:
				self.FIPS.append(fip)
				if fip not in self.FipsDict:
					self.FipsDict[fip] = 1
				else:
					self.FipsDict[fip] = self.FipsDict[fip] + 1

