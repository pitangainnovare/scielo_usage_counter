from scielo_usage_counter import geo


class Country:
    iso_code = 'BR'


class CountryResponse:
    country = Country()


class CountingMap:
    def __init__(self):
        self.calls = []

    def country(self, ip):
        self.calls.append(ip)
        return CountryResponse()


def test_reuses_country_for_repeated_ip():
    reader = CountingMap()
    geoip = geo.GeoIp()
    geoip._GeoIp__map = reader

    assert geoip.ip_to_country_code('185.29.10.0') == 'BR'
    assert geoip.ip_to_country_code('185.29.10.0') == 'BR'
    assert reader.calls == ['185.29.10.0']
