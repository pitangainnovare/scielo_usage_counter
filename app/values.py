# https://github.com/matomo-org/matomo-log-analytics/blob/4.x-dev/import_logs.py
PATTERN_COMMON_LOG_FORMAT = (
    r'(?P<ip>[\w*.:-]+)\s+\S+\s+(?P<userid>\S+)\s+\[(?P<date>.*?)\s+(?P<timezone>.*?)\]\s+'
    r'"(?P<method>\S+)\s+(?P<path>.*?)\s+\S+"\s+(?P<status>\d+)\s+(?P<length>\S+)'
)

# https://github.com/matomo-org/matomo-log-analytics/blob/4.x-dev/import_logs.py
PATTERN_NCSA_EXTENDED_LOG_FORMAT = (
    PATTERN_COMMON_LOG_FORMAT + r'\s+"(?P<referrer>.*?)"\s+"(?P<user_agent>.*?)"'
)

# https://github.com/matomo-org/matomo-log-analytics/blob/4.x-dev/import_logs.py
EXTENSIONS_STATIC = set([
    'gif',
    'jpg',
    'jpeg',
    'png',
    'bmp',
    'ico',
    'svg',
    'svgz',
    'ttf',
    'otf',
    'eot',
    'woff',
    'woff2',
    'class',
    'swf',
    'css',
    'js',
    'xml',
    'webp'
])

# https://github.com/matomo-org/matomo-log-analytics/blob/4.x-dev/import_logs.py
EXTENSIONS_DOWNLOAD = set([
    '7z',
    'aac',
    'arc',
    'arj',
    'asf',
    'asx',
    'avi',
    'bin',
    'csv',
    'deb',
    'dmg',
    'doc',
    'docx',
    'exe',
    'flac',
    'flv',
    'gz',
    'gzip',
    'hqx',
    'ibooks',
    'jar',
    'json',
    'mpg',
    'mp2',
    'mp3',
    'mp4',
    'mpeg',
    'mov',
    'movie',
    'msi',
    'msp',
    'odb',
    'odf',
    'odg',
    'odp',
    'ods',
    'odt',
    'ogg',
    'ogv',
    'pdf',
    'phps',
    'ppt',
    'pptx',
    'qt',
    'qtm',
    'ra',
    'ram',
    'rar',
    'rpm',
    'rtf',
    'sea',
    'sit',
    'tar',
    'tbz',
    'bz2',
    'tbz',
    'tgz',
    'torrent',
    'txt',
    'wav',
    'webm',
    'wma',
    'wmv',
    'wpd',
    'xls',
    'xlsx',
    'xml',
    'xsd',
    'z',
    'zip',
    'azw3',
    'epub',
    'mobi',
    'apk',
    'md5',
    'sig'
])

PRETABLE_FILE_HEADER = [
    'serverTime', 
    'browserName', 
    'browserVersion', 
    'ip', 
    'latitude', 
    'longitude', 
    'actionName'
]

LOGFILE_STATUS_QUEUE = 0
LOGFILE_STATUS_PARTIAL = 1
LOGFILE_STATUS_LOADED = 2
LOGFILE_STATUS_INVALIDATED = -9

DATE_STATUS_QUEUE = 0
DATE_STATUS_PARTIAL = 1
DATE_STATUS_LOADED = 2
DATE_STATUS_PRETABLE = 3
DATE_STATUS_COMPUTED = 4
DATE_STATUS_COMPLETED = 5
DATE_STATUS_EXTRACTING_PRETABLE = -3

SORT_RESULT_SUCCESS = 0

LOG_PATH_TRANSLATOR = {
    '/app/usage-logs-ratchet': '/logs-ratchet',
    '/app/usage-logs-dataverse': '/logs-dataverse',
    '/app/usage-logs-preprints': '/logs-submission-node01',
    '/app/usage-logs-venezuela': '/logs-venezuela',
    '/app/usage-logs-hiperion': '/logs-oldscielobr',
    '/app/usage-logs-node03': '/logs-node03-oldscielobr',
    '/app/usage-logs-newbrvarnish02': '/logs-newbrvarnish02',
    '/app/usage-logs-newbrvarnish03': '/logs-newbrvarnish03',
}
