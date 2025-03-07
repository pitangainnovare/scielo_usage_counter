import datetime
import ipaddress
import re
import logging
import time
import urllib.parse

from device_detector import DeviceDetector

from . import exceptions, geo, values
from .utils import file_utils, resource_utils


IP_ORIGIN_REMOTE = 'remote'
IP_ORIGIN_LOCAL = 'local'
IP_ORIGIN_UNKNOWN = 'unknown'

RESPONSE_STATUS_REDIRECT = ['301', '302', '303', '307', '308']
RESPONSE_STATUS_SUPPORTED = ['200', '304',]
HTTP_METHOD_SUPPORTED = ['GET', 'HEAD']


class LogStats:
    def __init__(self):
        self.__ignored_lines_static_resources = 0
        self.__ignored_lines_bot = 0
        self.__ignored_lines_invalid_method = 0
        self.__ignored_lines_invalid_user_agent = 0
        self.__ignored_lines_invalid_client_name = 0
        self.__ignored_lines_invalid_client_version = 0
        self.__ignored_lines_invalid_country_code = 0
        self.__ignored_lines_invalid_local_datetime = 0
        self.__ignored_lines_http_redirects = 0
        self.__ignored_lines_http_errors = 0
        self.__total_ignored_lines = 0
        self.__total_imported_lines = 0
        self.__lines_parsed = 0
        self.__total_time = 0.0
        self.__output = None

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
    def ignored_lines_invalid_country_code(self):
        return self.__ignored_lines_invalid_country_code

    @ignored_lines_invalid_country_code.setter
    def ignored_lines_invalid_country_code(self, value):
        self.__ignored_lines_invalid_country_code = value

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
        except Exception as e:
            logging.error(f"Failed to open file: {e}")
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
            'ignored_lines_invalid_country_code',
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
            self.ignored_lines_invalid_country_code,
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
        if self.output is None:
            logging.error('You should define an output path before trying to save.\n\tTip: lp.output = <YOUR PATH GOES HERE>\n\t     lp.stats.output = <YOUR SUMMARY PATH GOES HERE>')
            return

        stats_kv = self.get_stats()

        try:
            for i in stats_kv:
                self.output.write(sep.join([str(x) for x in i]) + '\n')
        except Exception as e:
            logging.error(f"Failed to write stats to file: {e}")
        finally:
            if self.output:
                self.output.close()


class LogParser:
    def __init__(self, mmdb_path=None, robots_path=None, mmdb_data=None, robots_list=None):
        self.__geoip = geo.GeoIp()
        self.__geoip.map = resource_utils.load_mmdb(
            mmdb_data=mmdb_data,
            mmdb_path=mmdb_path,
        )
        self.__robots = resource_utils.load_robots(
            robots_list=robots_list, 
            robots_path=robots_path,
        )
        self.__stats = Stats()
        self.__output = None

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, path):
        self.__output = open(path, 'w')

    @property
    def logfile(self):
        return self.__logfile

    @logfile.setter
    def logfile(self, file_path):
        self.__logfile = file_utils.open_logfile(file_path)

    @property
    def geoip(self):
        return self.__geoip

    @property
    def robots(self):
        return self.__robots

    @robots.setter
    def robots(self, robots_list, robots_path):
        self.__robots = resource_utils.load_robots(
            robots_list=robots_list,
            robots_path=robots_path,
        )

    @property
    def stats(self):
        return self.__stats

    @stats.setter
    def stats(self):
        self.__stats = Stats()

    def has_valid_method(self, method):
        if method.upper() in HTTP_METHOD_SUPPORTED:
            return True
        return False

    def has_valid_status(self, status):
        if status in RESPONSE_STATUS_SUPPORTED:
            return True
        return False

    def status_is_redirect(self, status):
        return status.startswith('3') and status != '304'

    def status_is_error(self, status):
        return status.startswith('4') or status.startswith('5')

    def has_valid_user_agent(self, user_agent):
        if not self.user_agent_is_bot(user_agent):
            return True
        return False

    def user_agent_is_bot(self, user_agent):
        for regex in self.robots:
            if regex.search(user_agent):
                return True
        return False

    def has_supported_url(self, path):
        if not self.url_is_static_file(path):
            return True
        return False

    def url_is_static_file(self, path):
        try:
            file_from_url = urllib.parse.urlparse(path).path
        except ValueError:
            file_from_url = path.split('/')[-1]

        ext = file_from_url.rsplit('.')[-1].lower()

        if ext in values.EXTENSIONS_STATIC or file_from_url in values.EXTENSIONS_STATIC:
            return True

        return False

    def url_is_download(self, path):
        file_from_url = path.split('/')[-1]
        ext = file_from_url.rsplit('.')[-1].lower()

        if ext in values.EXTENSIONS_DOWNLOAD:
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
            return

    def format_user_agent(self, user_agent):
        fmt_ua = user_agent

        if fmt_ua and fmt_ua.startswith('"'):
            fmt_ua = fmt_ua[1:-1]

        return fmt_ua

    def format_client_name(self, device):
        return device.client_short_name() or device.client_name() or device.UNKNOWN

    def format_client_version(self, device):
        return device.client_version() or device.UNKNOWN

    def match_with_best_pattern(self, line):
        patterns = [
            values.PATTERN_NCSA_EXTENDED_LOG_FORMAT,
            values.PATTERN_NCSA_EXTENDED_LOG_FORMAT_DOMAIN,
            values.PATTERN_NCSA_EXTENDED_LOG_FORMAT_WITH_IP_LIST,
            values.PATTERN_NCSA_EXTENDED_LOG_FORMAT_DOMAIN_WITH_IP_LIST,
        ]

        match = None
        ip_origin_type = IP_ORIGIN_UNKNOWN
        ip_value = ''

        for pattern in patterns:
            match = re.match(pattern, line)

            if match:
                content = match.groupdict()
                
                ip_value = content.get('ip')
                ip_origin_type = self.get_ip_origin_type(ip_value)

                if ip_origin_type != IP_ORIGIN_UNKNOWN:
                    return match, ip_value

                else:
                    for i in content.get('ip_list', '').split(','):
                        ip_origin_type = self.get_ip_origin_type(i.strip())
                        if ip_origin_type != IP_ORIGIN_UNKNOWN:
                            return match, i.strip()
        
        return match, ip_value

    def get_ip_origin_type(self, ip):
        try:
            ipa = ipaddress.ip_address(ip)
        except ValueError:
            return IP_ORIGIN_UNKNOWN

        if ipa.is_global:
            return IP_ORIGIN_REMOTE
        elif ipa.is_private or ipa.is_loopback or ipa.is_link_local:
            return IP_ORIGIN_LOCAL

        return IP_ORIGIN_UNKNOWN

    def parse_line(self, line):
        self.stats.increment('lines_parsed')

        parsed_data = []
        try:
            decoded_line = line.decode().strip() if isinstance(line, bytes) else line.strip()
        except UnicodeDecodeError:
            decoded_line = line.decode('utf-8', errors='ignore').strip() if isinstance(line, bytes) else line.strip()

        match, ip_value = self.match_with_best_pattern(decoded_line)

        if match:
            processed_line = {
                'http_method': None,
                'http_response_status': None,
                'user_agent': None,
                'client_name': None,
                'client_version': None,
                'url': None,
                'ip_address': None,
                'country_code': None,
                'local_datetime': None,
                'is_valid': True,
            }

            data = match.groupdict()

            processed_line['http_method'] = data.get('method')
            if not self.has_valid_method(processed_line['http_method']):
                self.stats.increment('ignored_lines_invalid_method')
                processed_line['is_valid'] = False

            processed_line['http_response_status'] = data.get('status')
            if not self.has_valid_status(processed_line['http_response_status']):
                if self.status_is_redirect(processed_line['http_response_status']):
                    self.stats.increment('ignored_lines_http_redirects')
                elif self.status_is_error(processed_line['http_response_status']):
                    self.stats.increment('ignored_lines_http_errors')
                processed_line['is_valid'] = False

            processed_line['user_agent'] = self.format_user_agent(data.get('user_agent'))

            if self.user_agent_is_bot(processed_line['user_agent']):
                self.stats.increment('ignored_lines_bot')
                processed_line['is_valid'] = False

            try:
                device = DeviceDetector(processed_line['user_agent']).parse()
            except ZeroDivisionError:
                device = DeviceDetector('').parse()
                self.stats.increment('ignored_lines_invalid_user_agent')
                logging.error(exceptions.DeviceDetectionError(f"Não foi possível identificar UserAgent {processed_line['user_agent']} from line {decoded_line}"))
                processed_line['is_valid'] = False

            processed_line['client_name'] = self.format_client_name(device)
            if not processed_line['client_name']:
                self.stats.increment('ignored_lines_invalid_client_name')
                processed_line['is_valid'] = False

            processed_line['client_version'] = self.format_client_version(device)
            if not processed_line['client_version']:
                self.stats.increment('ignored_lines_invalid_client_version')
                processed_line['is_valid'] = False

            processed_line['url'] = data.get('path')
            if not self.has_supported_url(processed_line['url']):
                self.stats.increment('ignored_lines_static_resources')
                processed_line['is_valid'] = False

            processed_line['ip_address'] = ip_value
            processed_line['country_code'] = self.geoip.ip_to_country_code(processed_line['ip_address'])
            if not processed_line['country_code']:
                self.stats.increment('ignored_lines_invalid_country_code')
                processed_line['is_valid'] = False

            date = data.get('date')
            timezone = data.get('timezone')
            processed_line['local_datetime'] = self.format_date(date, timezone)
            if not processed_line['local_datetime']:
                self.stats.increment('ignored_lines_invalid_local_datetime')
                processed_line['is_valid'] = False

            if processed_line['is_valid']:
                self.stats.increment('total_imported_lines')

                parsed_data.append(hit.local_datetime)
                parsed_data.append(hit.client_name)
                parsed_data.append(hit.client_version)
                parsed_data.append(hit.ip)
                parsed_data.append(hit.country_code)
                parsed_data.append(hit.action)
            else:
                self.stats.increment('total_ignored_lines')
        else:
            self.stats.increment('total_ignored_lines')

        return parsed_data

    def parse(self):
        self.start = time.time()
        for line in self.logfile:
            res = self.parse_line(line)
            if res:
                yield res

    def save(self, data, sep='\t'):
        self.output.write(sep.join([
            'server_date',
            'browser_name',
            'browser_version',
            'user_ip',
            'country_code',
            'action_name']) + '\n')

        [self.output.write(sep.join([str(di) for di in d]) + '\n') for d in data if d]
        self.output.close()
        self.logfile.close()

        self.end = time.time()
        self.total_time = self.end - self.start

        self.stats.total_time = self.total_time
        self.stats.save()
