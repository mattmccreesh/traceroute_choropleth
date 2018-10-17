import geocoder

class LocData:
    
    def __init__(self, ipAddrs):
        self.ipAddrs = ipAddrs
        self.states = []
        for address in ipAddrs:
            g = geocoder.ip(address)
            self.states.append(g.state)

        
