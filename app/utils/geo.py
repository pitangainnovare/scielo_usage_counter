import geoip2.database

from geoip2.errors import AddressNotFoundError


class GeoIp:
    @property
    def map(self):
        return self.__map

    @map.setter
    def map(self, mmbd):
        try:
            self.__map = geoip2.database.Reader(mmbd)
        except FileNotFoundError:
            return

    def ip_to_geolocation(self, ip):
        try:
            return self.map.city(ip)
        except AddressNotFoundError:
            return

    def geolocation_to_str(self, map_geo, sep='\t'):
        try:
            return sep.join([str(i) for i in [
                map_geo.location.latitude,
                map_geo.location.longitude,
            ]])
        except AttributeError:
            return
