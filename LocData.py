from geocoder import ip
from requests import get
from urllib import urlencode

class LocData:
    
    def __init__(self, ipAddrs):
        self.ipAddrs = ipAddrs
        self.states = []
        self.coords = []
        self.FIPS = []
        for address in ipAddrs:
            g = ip(address)
            self.states.append(g.state)
            self.coords.append(g.latlng)
            self.FIPS.append(self.getFIPS(g.lat, g.lng))

    def getFIPS(self, lat, lon):
        params = urlencode({'latitude': lat, 'longitude':lon, 'format':'json'})
        url = 'https://geo.fcc.gov/api/census/block/find?' + params
        response = get(url)
        data = response.json()
        return data['County']['FIPS']

