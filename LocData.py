from requests import get
from time import sleep
from urllib import urlencode

#to provide similar objects to geocoder
#allows us to have more modularity
class GeoData(object):
	def __init__(self, country, state, lat, lng):
		self.country = country
		self.state = state
		self.lat = lat
		self.lng = lng

class LocData:
	
	def __init__(self):
		self.ipAddrs = []
		self.coords = []
		self.states = []
		self.countries = []
		self.FipsList = []
		self.FipsDict = {}
		self.ipResponse = {}
		counties_text_file = open("national_county.txt","r")
		for line in counties_text_file:
			line = line.split(',')
			FIPS = line[1]+line[2]
			self.FipsDict[FIPS] = 0
		counties_text_file.close()

	def getFIPSbyLatLong(self, address,lat, lon):
		params = urlencode({'latitude': lat, 'longitude':lon, 'format':'json'})
		url = 'https://geo.fcc.gov/api/census/block/find?' + params
		response = get(url)
		# print(str(lat) + "," + str(lon))
		if response.text.find("<html>") == -1:
			# print(response)
			self.ipResponse[address] = response
			data = response.json()['County']['FIPS']
			if data is not None:
				return data.encode('ascii','ignore')
			else:
				print("FCC FIPS is None")
		else:
			print("Bad Response from FCC")

	#replaces geocoder module with GET reqeust to API to avoid query limit
	def getGeoDataFromIP(self, testIP):
		# sleep(0.25)
		url = 'http://api.petabyet.com/geoip/' + testIP
		response = get(url)
		jsonData = response.json()
		# print(jsonData)
		lat = jsonData['latitude']
		lng = jsonData['longitude']
		country = jsonData['country']
		if 'region' in jsonData.keys():
			state = jsonData['region']
		else:
			state = ""
		return GeoData(country, state, lat, lng)

	def genFIPSList(self, ipAddrs):
		self.ipAddrs.extend(ipAddrs)
		for address in ipAddrs:
			g = self.getGeoDataFromIP(address)
			self.countries.append(g.country)
			self.states.append(g.state)
			self.coords.append([g.lat,g.lng])
			fip = self.getFIPSbyLatLong(address,g.lat, g.lng)
			if fip is not None:
				self.FipsList.append(fip)
				self.FipsDict[fip] += 1

