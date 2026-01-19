import geoip2.database
import ipaddress

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

    def _normalize_ip(self, ip):
        if not ip:
            return

        if not isinstance(ip, str):
            ip = str(ip)

        ip = ip.strip()
        if not ip:
            return

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
            return

    def ip_to_geolocation(self, ip):
        try:
            normalized = self._normalize_ip(ip)
            if not normalized:
                return

            reader = getattr(self, '_GeoIp__map', None)
            if not reader:
                return

            return reader.city(normalized)
        except AddressNotFoundError:
            return
        except (ValueError, AttributeError):
            return

    def geolocation_to_str(self, map_geo, sep='\t'):
        try:
            return sep.join([str(i) for i in [
                map_geo.location.latitude,
                map_geo.location.longitude,
            ]])
        except AttributeError:
            return
