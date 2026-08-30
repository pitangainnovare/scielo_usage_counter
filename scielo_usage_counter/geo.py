from collections import OrderedDict

import ipaddress

import geoip2.database

from geoip2.errors import AddressNotFoundError


COUNTRY_CACHE_MAX_SIZE = 4096


class GeoIp:
    def __init__(self):
        self.__map = None
        self.__country_cache = OrderedDict()

    @property
    def map(self):
        return self.__map

    @map.setter
    def map(self, mmbd):
        self.__country_cache.clear()
        try:
            self.__map = geoip2.database.Reader(mmbd)
        except FileNotFoundError:
            return
        
    def ip_to_country_code(self, ip):
        try:
            country_code = self.__country_cache.pop(ip)
        except KeyError:
            country_code = None
        else:
            self.__country_cache[ip] = country_code
            return country_code

        try:
            normalized = self.normalize_ip(ip)
            if not normalized:
                return None

            country_code = self.map.country(normalized).country.iso_code

        except AddressNotFoundError:
            country_code = None

        except (AttributeError, ValueError):
            country_code = None

        if len(self.__country_cache) >= COUNTRY_CACHE_MAX_SIZE:
            self.__country_cache.popitem(last=False)
        self.__country_cache[ip] = country_code

        return country_code

    def ip_to_geolocation(self, ip):
        try:
            normalized = self.normalize_ip(ip)
            if not normalized:
                return None

            reader = self.map
            if not reader:
                return None

            return reader.city(normalized)

        except AddressNotFoundError:
            return None

        except (ValueError, AttributeError):
            return None

    @staticmethod
    def normalize_ip(ip):
        if not ip:
            return None

        if not isinstance(ip, str):
            ip = str(ip)

        ip = ip.strip()
        if not ip:
            return None

        # If we ever receive a list here, take the first entry.
        if ',' in ip:
            ip = ip.split(',', 1)[0].strip()

        # Common representation for IPv6 with port: [2001:db8::1]:443
        if ip.startswith('['):
            end = ip.find(']')
            if end != -1:
                ip = ip[1:end]

        # Common representation for IPv4 with port: 1.2.3.4:443
        if '.' in ip and ip.count(':') == 1:
            ip = ip.rsplit(':', 1)[0]

        try:
            return str(ipaddress.ip_address(ip))

        except ValueError:
            return None

    @staticmethod
    def geolocation_to_str(map_geo, sep='\t'):
        try:
            return sep.join([str(i) for i in [
                map_geo.location.latitude,
                map_geo.location.longitude,
            ]])
        except AttributeError:
            return None
