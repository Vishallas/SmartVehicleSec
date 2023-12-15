import random
import geocoder

class Location: 
    def lat(self):
        lat = f"{random.randint(-90,90)}.{random.randint(0,10**6)}"
        return lat
    def long(self):
        long = f"{random.randint(-90,90)}.{random.randint(0,10**6)}"
        return long

class IPLocation:
    def __init__(self):
        self.g = geocoder.ip('me')
        #self._lat,self._long  = 1.0,1.0
    def lat(self):
        return self.g.latlng[0]
    def long(self):
        return self.g.latlng[1]