from geocoder import ip
from requests import get
from urllib import urlencode

class LocData:
    
    def __init__(self, ipAddrs):
        self.ipAddrs = ipAddrs
        self.states = []
        self.coords = []
        self.FIPS = []
        self.FipsDict = {}
        for address in ipAddrs:
            g = ip(address)
            self.states.append(g.state)
            self.coords.append(g.latlng)
            fip = self.getFIPS(g.lat, g.lng)
            self.FIPS.append(fip)
            if fip not in self.FipsDict:
                self.FipsDict[fip] = 1
            else:
                self.FipsDict[fip] = self.FipsDict[fip] + 1

    def getFIPS(self, lat, lon):
        params = urlencode({'latitude': lat, 'longitude':lon, 'format':'json'})
        url = 'https://geo.fcc.gov/api/census/block/find?' + params
        response = get(url)
        data = response.json()
        return data['County']['FIPS']

