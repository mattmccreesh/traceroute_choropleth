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
		self.counties = []
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

	def getFIPSbyLatLong(self, address, lat, lon):
		params = urlencode({'latitude': lat, 'longitude':lon, 'format':'json'})
		url = 'https://geo.fcc.gov/api/census/block/find?' + params
		response = get(url)
		# print(str(lat) + "," + str(lon))
		if response.text.find("<html>") == -1 and response.json() is not None and response.json()['County']['FIPS'] is not None:
			self.counties.append(response.json()['County']['name'] + ", " + response.json()['State']['name'])
			self.ipResponse[address] = response
			data = response.json()['County']['FIPS']
			return data.encode('ascii','ignore')
		else:
			print("Bad Response from FCC for ip (" + address + ")\n")
			print(response.json())

	#replaces geocoder module with GET reqeust to API to avoid query limit
	def getGeoDataFromIP(self, ip):
		# sleep(0.25)
		url = 'http://api.petabyet.com/geoip/' + ip
		response = get(url)
		jsonData = response.json()
		# print(jsonData)
		if 'latitude' in jsonData.keys() and 'longitude' in jsonData.keys():
			lat = jsonData['latitude']
			lng = jsonData['longitude']
		else:
			print("Error: \'" + ip + "\' does not have a longitude or latitude.")
			print(jsonData)
			raw_input("Paused\n")
		if 'country' not in jsonData.keys():
			print("Error: \'" + ip + "\' does not have a country.")
			# print(jsonData)
			country = 'N/A'
		else:
			country = jsonData['country']
		if 'region' not in jsonData.keys():
			print("Error: \'" + ip + "\' does not have a state.")
			# print(jsonData)
			state = 'N/A'
		else:
			state = jsonData['region']
		return GeoData(country, state, lat, lng)

	# Takes a dictionary with an IP Address as key and Count as Value
	def genFIPS(self, ipAddrs):
		self.ipAddrs = ipAddrs.keys()
		for ip in self.ipAddrs:
			g = self.getGeoDataFromIP(ip)
			self.countries.append(g.country)
			self.states.append(g.state)
			self.coords.append([g.lat,g.lng])
			fip = self.getFIPSbyLatLong(ip, g.lat, g.lng)
			if fip is not None:
				self.FipsList.append(fip)
				self.FipsDict[fip] += ipAddrs[ip]
			print("Done generating FIPS of IP: " + ip)