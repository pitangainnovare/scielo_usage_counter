import datetime
import re
import time

from app.values import (
    EXTENSIONS_DOWNLOAD,
    PATTERN_NCSA_EXTENDED_LOG_FORMAT,
    EXTENSIONS_STATIC,
)
from app.utils.file import open_logfile
from app.utils.geo import GeoIp
from app.utils.robot import robot_reader
from device_detector import DeviceDetector


class LogParser:
    def __init__(self, mmdb_path, robots_path):
        self.__geoip = GeoIp()
        self.__geoip.map = mmdb_path
        self.__robots = robot_reader(robots_path)

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, path):
        self.__output = open(path, 'w')

    def close(self):
        self.output.close()

    @property
    def logfile(self):
        return self.__logfile

    @logfile.setter
    def logfile(self, file_path):
        self.__logfile = open_logfile(file_path)

    @property
    def geoip(self):
        return self.__geoip

    @property
    def robots(self):
        return self.__robots

    @robots.setter
    def robots(self, robots_path):
        self.__robots = robot_reader(robots_path)

    def has_valid_method(self, method):
        if method == 'GET':
            return True
        return False

    def has_valid_status(self, status):
        if status in {'200', '304'}:
            return True
        return False

    def has_valid_user_agent(self, user_agent):
        if not self.user_agent_is_bot(user_agent):
            return True
        return False

    def user_agent_is_bot(self, user_agent):
        user_agent_lowered = user_agent.lower()
        for regex in self.robots:
            if regex.search(user_agent_lowered):
                return True
        return False

    def has_valid_path(self, path):
        if not self.action_is_static_file(path):
            return True
        return False

    def action_is_static_file(self, path):
        file_from_url = path.split('/')[-1]
        ext = file_from_url.rsplit('.')[-1].lower()

        if ext in EXTENSIONS_STATIC or file_from_url in EXTENSIONS_STATIC:
            return True
        return False

    def action_is_download(self, path):
        file_from_url = path.split('/')[-1]
        ext = file_from_url.rsplit('.')[-1].lower()

        if ext in EXTENSIONS_DOWNLOAD:
            return True
        return False

    def timedelta_from_timezone(self, timezone):
        timezone = int(timezone)
        sign = 1 if timezone >= 0 else -1
        n = abs(timezone)

        hours = n / 100 * sign
        minutes = n % 100 * sign

        return datetime.timedelta(hours=hours, minutes=minutes)

    def format_date(self, date, timezone):
        try:
            date = datetime.datetime.strptime(date, '%d/%b/%Y:%H:%M:%S')
            date -= self.timedelta_from_timezone(timezone)
            return date.strftime('%Y-%m-%d %H:%M:%S')
        except:
            raise

    def parse_line(self, line):
        parsed_data = []

        decoded_row = line.decode().strip()

        match = re.match(PATTERN_NCSA_EXTENDED_LOG_FORMAT, decoded_row)
        if match:
            data = match.groupdict()

            method = data.get('method')
            if not self.has_valid_method(method):
                return

            status = data.get('status')
            if not self.has_valid_status(status):
                return

            user_agent = data.get('user_agent')
            device = DeviceDetector(user_agent).parse()
            if device.is_bot():
                return

            client_name = device.client_short_name()
            if not client_name:
                return

            client_version = device.client_version()
            if not client_version:
                return
            client_version_str = str(client_version)

            action = data.get('path')
            if not self.has_valid_path(action):
                return

            ip = data.get('ip')
            geolocation = self.geoip.ip_to_geolocation(ip)
            if not geolocation:
                return
            geolocation_str = self.geoip.geolocation_to_str(geolocation)

            date = data.get('date')
            timezone = data.get('timezone')
            formatted_date = self.format_date(date, timezone)
            if not formatted_date:
                return

            parsed_data.append(formatted_date)
            parsed_data.append(client_name)
            parsed_data.append(client_version_str)
            parsed_data.append(ip)
            parsed_data.append(geolocation_str)
            parsed_data.append(action)

            # atributos ignorados
            userid = data.get('userid')
            length = data.get('length')
            referrer = data.get('referrer')

        return parsed_data

    def parse(self):
        self.start = time.time()
        for line in self.logfile:
            res = self.parse_line(line)
            if res:
                yield res

    def save(self, data, sep='\t'):
        self.output.write(sep.join([
            'serverTime',
            'browserName',
            'browserVersion',
            'ip',
            'latitude',
            'longitude',
            'actionName']) + '\n')

        [self.output.write(sep.join(d) + '\n') for d in data if d]
        self.end = time.time()
        self.total_time = self.end - self.start
