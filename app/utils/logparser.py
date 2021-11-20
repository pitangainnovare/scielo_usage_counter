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
