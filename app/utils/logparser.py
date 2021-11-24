import datetime
import re
import logging
import time

from app.values import (
    EXTENSIONS_DOWNLOAD,
    PATTERN_NCSA_EXTENDED_LOG_FORMAT,
    EXTENSIONS_STATIC,
)
from app.utils.file import open_logfile
from app.utils.geo import GeoIp
from app.utils.robot import robot_reader
from app.utils.exceptions import DeviceDetectionError
from device_detector import DeviceDetector


class Stats:
    def __init__(self):
        self.__ignored_lines_static_resources = 0
        self.__ignored_lines_bot = 0
        self.__ignored_lines_invalid_method = 0
        self.__ignored_lines_invalid_user_agent = 0
        self.__ignored_lines_invalid_client_name = 0
        self.__ignored_lines_invalid_client_version = 0
        self.__ignored_lines_invalid_geolocation = 0
        self.__ignored_lines_invalid_local_datetime = 0
        self.__ignored_lines_http_redirects = 0
        self.__ignored_lines_http_errors = 0
        self.__total_ignored_lines = 0
        self.__total_imported_lines = 0
        self.__lines_parsed = 0
        self.__total_time = 0.0

    @property
    def ignored_lines_static_resources(self):
        return self.__ignored_lines_static_resources
    
    @ignored_lines_static_resources.setter
    def ignored_lines_static_resources(self, value):
        self.__ignored_lines_static_resources = value

    @property
    def ignored_lines_bot(self):
        return self.__ignored_lines_bot
    
    @ignored_lines_bot.setter
    def ignored_lines_bot(self, value):
        self.__ignored_lines_bot = value

    @property
    def ignored_lines_invalid_method(self):
        return self.__ignored_lines_invalid_method
    
    @ignored_lines_invalid_method.setter
    def ignored_lines_invalid_method(self, value):
        self.__ignored_lines_invalid_method = value

    @property
    def ignored_lines_invalid_user_agent(self):
        return self.__ignored_lines_invalid_user_agent
    
    @ignored_lines_invalid_user_agent.setter
    def ignored_lines_invalid_user_agent(self, value):
        self.__ignored_lines_invalid_user_agent = value

    @property
    def ignored_lines_invalid_client_name(self):
        return self.__ignored_lines_invalid_client_name
    
    @ignored_lines_invalid_client_name.setter
    def ignored_lines_invalid_client_name(self, value):
        self.__ignored_lines_invalid_client_name = value

    @property
    def ignored_lines_invalid_client_version(self):
        return self.__ignored_lines_invalid_client_version
    
    @ignored_lines_invalid_client_version.setter
    def ignored_lines_invalid_client_version(self, value):
        self.__ignored_lines_invalid_client_version = value

    @property
    def ignored_lines_invalid_geolocation(self):
        return self.__ignored_lines_invalid_geolocation
    
    @ignored_lines_invalid_geolocation.setter
    def ignored_lines_invalid_geolocation(self, value):
        self.__ignored_lines_invalid_geolocation = value

    @property
    def ignored_lines_invalid_local_datetime(self):
        return self.__ignored_lines_invalid_local_datetime
    
    @ignored_lines_invalid_local_datetime.setter
    def ignored_lines_invalid_local_datetime(self, value):
        self.__ignored_lines_invalid_local_datetime = value

    @property
    def ignored_lines_http_redirects(self):
        return self.__ignored_lines_http_redirects
    
    @ignored_lines_http_redirects.setter
    def ignored_lines_http_redirects(self, value):
        self.__ignored_lines_http_redirects = value

    @property
    def ignored_lines_http_errors(self):
        return self.__ignored_lines_http_errors
    
    @ignored_lines_http_errors.setter
    def ignored_lines_http_errors(self, value):
        self.__ignored_lines_http_errors = value

    @property
    def total_ignored_lines(self):
        return self.__total_ignored_lines
    
    @total_ignored_lines.setter
    def total_ignored_lines(self, value):
        self.__total_ignored_lines = value

    @property
    def total_imported_lines(self):
        return self.__total_imported_lines
    
    @total_imported_lines.setter
    def total_imported_lines(self, value):
        self.__total_imported_lines = value

    @property
    def lines_parsed(self):
        return self.__lines_parsed

    @lines_parsed.setter
    def lines_parsed(self, value):
        self.__lines_parsed = value
    
    @property
    def total_time(self):
        return self.__total_time

    @total_time.setter
    def total_time(self, value):
        self.__total_time = value

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, path):
        try:
            self.__output = open(path, 'w')
        except:
            logging.info(self.dump_to_str())

    def increment(self, measure):
        current_value = getattr(self, measure)
        new_value = current_value + 1
        setattr(self, measure, new_value)

    def get_stats(self):
        keys = [
            'ignored_lines_static_resources',
            'ignored_lines_bot',
            'ignored_lines_invalid_method',
            'ignored_lines_invalid_user_agent',
            'ignored_lines_invalid_client_name',
            'ignored_lines_invalid_client_version',
            'ignored_lines_invalid_geolocation',
            'ignored_lines_invalid_local_datetime',
            'ignored_lines_http_redirects',
            'ignored_lines_http_errors',
            'total_ignored_lines',
            'total_imported_lines',
            'lines_parsed',
            'total_time',
        ]

        values = [
            self.ignored_lines_static_resources,
            self.ignored_lines_bot,
            self.ignored_lines_invalid_method,
            self.ignored_lines_invalid_user_agent,
            self.ignored_lines_invalid_client_name,
            self.ignored_lines_invalid_client_version,
            self.ignored_lines_invalid_geolocation,
            self.ignored_lines_invalid_local_datetime,
            self.ignored_lines_http_redirects,
            self.ignored_lines_http_errors,
            self.total_ignored_lines,
            self.total_imported_lines,
            self.lines_parsed,
            self.total_time,
        ]

        return [keys, values]

    def dump_to_str(self, sep='\t'):
        stats_kv = self.get_stats()
        for i in stats_kv:
            logging(sep.join(i))

    def save(self, sep='\t'):
        stats_kv = self.get_stats()
        for i in stats_kv:
            self.output.write(sep.join([str(x) for x in i]) + '\n')
        self.output.close()
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

        decoded_line = line.decode().strip() if isinstance(line, bytes) else line.strip()

        match = re.match(PATTERN_NCSA_EXTENDED_LOG_FORMAT, decoded_line)
        if match:
            data = match.groupdict()

            method = data.get('method')
            if not self.has_valid_method(method):
                return

            status = data.get('status')
            if not self.has_valid_status(status):
                return

            user_agent = data.get('user_agent')
            try:
                device = DeviceDetector(user_agent).parse()
                if device.is_bot():
                    return
            except ZeroDivisionError:
                logging.error(DeviceDetectionError(f'Não foi possível identificar UserAgent {user_agent} from line {decoded_line}'))
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
