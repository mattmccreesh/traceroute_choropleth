from requests import get
from time import sleep
from urllib import urlencode
import csv

#to provide similar objects to geocoder
#allows us to have more modularity
class GeoData(object):
	def __init__(self):
		self.country = ""
		self.address = ""
		self.county = ""
		self.state = ""
		self.lat = ""
		self.lng = ""
		self.FIPS = ""
		self.hits = 0
		self.response = {}
	
	def toDict(self):
		result = {}
		result['IP Address'] = self.address
		result['Hits'] = self.hits
		result['Latitude'] = self.lat
		result['Longitude'] = self.lng
		result['FIPS'] = self.FIPS
		result['County'] = self.county
		result['State'] = self.state
		result['Response'] = self.response
		result['Country'] = self.country

		return result

class LocData:
	
	def __init__(self):
		self.ipAddrs = []
		self.masterData = []
		self.FipsList = []
		self.FipsDict = {}
		counties_text_file = open("national_county.txt","r")
		for line in counties_text_file:
			line = line.split(',')
			FIPS = line[1]+line[2]
			self.FipsDict[FIPS] = 0
		counties_text_file.close()

	def getFIPSbyLatLong(self, gd):
		params = urlencode({'latitude': gd.lat, 'longitude':gd.lng, 'format':'json'})
		url = 'https://geo.fcc.gov/api/census/block/find?' + params
		gd.response = get(url)
		# print(gd.response.json())
		if gd.response.json() is not None and gd.response.json()['County']['FIPS'] is not None:
			gd.response
			if gd.response.json()['State']['name'] == "":
				print("Error: \'" + gd.address + "\' does not have a state.")
				gd.state = 'N/A'
			else:
				gd.state = gd.response.json()['State']['name']
			if gd.response.json()['County']['name'] == "":
				print("Error: \'" + gd.address + "\' does not have a state.")
				gd.county = 'N/A'
			else:
				gd.county = gd.response.json()['County']['name']
			if gd.response.json()['County']['FIPS'] == "":
				print("Error: \'" + gd.address + "\' does not have an FIPS.")
				gd.FIPS = 'N/A'
			else:
				gd.FIPS = gd.response.json()['County']['FIPS']
			return gd.FIPS.encode('ascii','ignore')
		else:
			print("Bad Response from FCC for ip (" + gd.address + ")\n")
			print(gd.response.json())

	#replaces geocoder module with GET reqeust to API to avoid query limit
	def getGeoDataFromIP(self, gd):
		url = 'http://api.petabyet.com/geoip/' + gd.address
		response = get(url)
		jsonData = response.json()
		# print(jsonData)
		if 'latitude' in jsonData.keys() and 'longitude' in jsonData.keys():
			gd.lat = jsonData['latitude']
			gd.lng = jsonData['longitude']
		else:
			print("Error: \'" + gd.address + "\' does not have a longitude or latitude.")
			print(jsonData)
			raw_input("Paused\n")
		if 'country' not in jsonData.keys():
			print("Error: \'" + gd.address + "\' does not have a country.")
			# print(jsonData)
			gd.country = 'N/A'
		else:
			gd.country = jsonData['country']
		return gd

	# Takes a dictionary with an IP Address as key and Count as Value
	def genFIPS(self, ipAddrs):
		self.ipAddrs = ipAddrs.keys()
		for ip in self.ipAddrs:
			gd = GeoData()
			gd.address = ip
			gd.hits = ipAddrs[ip]
			gd = self.getGeoDataFromIP(gd)
			fip = self.getFIPSbyLatLong(gd)
			self.masterData.append(gd.toDict())
			if fip is not None:
				self.FipsList.append(fip)
				self.FipsDict[fip] += ipAddrs[ip]
			print("Done generating FIPS of IP: " + ip)

	def writeToCSV(self, CSVpath):
		with open(CSVpath, 'w') as csv_file:
			scribe = csv.DictWriter(csv_file, fieldnames=['IP Address', 'Latitude', 'Longitude', 'FIPS', 'Hits', 'County', 'State','Country', 'Response'])
			scribe.writeheader()
			for row in self.masterData:
				scribe.writerow(row)	
		print("Completed writing to CSV!")