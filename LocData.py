import geocoder
import requests
import urllib

class LocData:
    
    def __init__(self, ipAddrs):
        self.ipAddrs = ipAddrs
        self.states = []
        self.coords = []
        self.FIPS = []
        for address in ipAddrs:
            g = geocoder.ip(address)
            self.states.append(g.state)
            self.coords.append(g.latlng)
            self.FIPS.append(self.getFIPS(g.lat, g.lng))

    def getFIPS(self, lat, lon):
        params = urllib.urlencode({'latitude': lat, 'longitude':lon, 'format':'json'})
        url = 'https://geo.fcc.gov/api/census/block/find?' + params
        response = requests.get(url)
        data = response.json()
        return data['County']['FIPS']

