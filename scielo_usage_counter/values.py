# https://github.com/matomo-org/matomo-log-analytics/blob/4.x-dev/import_logs.py
PATTERN_COMMON_LOG_FORMAT = (
    r'(?P<ip>[\w*.:-]+)\s+\S+\s+(?P<userid>\S+)\s+\[(?P<date>.*?)\s*(?P<timezone>[+-]?\d{4})\]\s+'
    r'"(?P<method>\S+)\s+(?P<path>.*?)\s+\S+"\s+(?P<status>\d+)\s+(?P<length>\S+)'
)

PATTERN_COMMON_LOG_FORMAT_WITH_IP_LIST = (
    r'(?P<ip>[\w*.:-]+)\s(?P<ip_list>[\w*.:,\s-]+)\s+(?P<userid>\S+)\s+\[(?P<date>.*?)\s*(?P<timezone>[+-]?\d{4})\]\s+'
    r'"(?P<method>\S+)\s+(?P<path>.*?)\s+\S+\"\s+(?P<status>\d+)\s+(?P<length>\S+)'
)

# https://github.com/matomo-org/matomo-log-analytics/blob/4.x-dev/import_logs.py
PATTERN_NCSA_EXTENDED_LOG_FORMAT = (
    PATTERN_COMMON_LOG_FORMAT + r'\s+"(?P<referrer>.*?)"\s+"(?P<user_agent>.*?)"'
)

PATTERN_NCSA_EXTENDED_LOG_FORMAT_WITH_IP_LIST = (
    PATTERN_COMMON_LOG_FORMAT_WITH_IP_LIST + r'\s+"(?P<referrer>.*?)"\s+"(?P<user_agent>.*?)"'
)

# Pattern designed to capture rows that begin with the domain name
PATTERN_NCSA_EXTENDED_LOG_FORMAT_DOMAIN = (
    r'(?P<domain>.*?)\s' + PATTERN_COMMON_LOG_FORMAT + r'\s+"(?P<referrer>.*?)"\s+"(?P<user_agent>.*?)"'
)

PATTERN_NCSA_EXTENDED_LOG_FORMAT_DOMAIN_WITH_IP_LIST = (
    r'(?P<domain>.*?)\s' + PATTERN_COMMON_LOG_FORMAT_WITH_IP_LIST + r'\s+"(?P<referrer>.*?)"\s+"(?P<user_agent>.*?)"'
)

PATTERN_BUNNYCDN_LOG_FORMAT = (
    r'^(?P<cache>HIT|MISS|BYPASS|EXPIRED|STALE|REVALIDATED|-)\|'
    r'(?P<status>\d{3})\|'
    r'(?P<unix_ts>\d{10}(?:\d{3})?)\|'
    r'(?P<length>\d+)\|'
    r'(?P<zone>\d+)\|'
    r'(?P<ip>[a-fA-F0-9:.]+)\|'
    r'(?P<referrer>[^|]*)\|'
    r'(?P<path>[^|]+)\|'
    r'(?P<edge_location>[^|]+)\|'
    r'(?P<user_agent>[^|]+)\|'
    r'(?P<request_id>[a-f0-9]{32})\|'
    r'(?P<country_code>[A-Z]{2})$'
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
    'webp',
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

# Default ISSN for documents that do not have an ISSN
DEFAULT_SCIELO_ISSN = '0000-0000'

# Default language for documents that do not have a language
MEDIA_LANGUAGE_UNDEFINED = 'un'

# Media formats
MEDIA_FORMAT_HTML = 'html'
MEDIA_FORMAT_PDF = 'pdf'
MEDIA_FORMAT_EPUB = 'epub'
MEDIA_FORMAT_SWF = 'swf'
MEDIA_FORMAT_XML = 'xml'
MEDIA_FORMAT_DATAVERSE = 'dat'
MEDIA_FORMAT_UNDEFINED = 'und'

# Content types
CONTENT_TYPE_FULL_TEXT = 'full_text'
CONTENT_TYPE_ABSTRACT = 'abstract'
CONTENT_TYPE_HOW_TO_CITE = 'how_to_cite'
CONTENT_TYPE_CITATION_EXPORT = 'citation_export'
CONTENT_TYPE_REFERENCES_LIST = 'references_list'
CONTENT_TYPE_RELATED_DOCUMENTS = 'related_documents'
CONTENT_TYPE_TRANSLATE_DOCUMENT = 'translate_document'
CONTENT_TYPE_UNDEFINED = 'undefined'
CONTENT_TYPE_DATA = 'data'

DEFAULT_REQUEST_TYPES = [
    CONTENT_TYPE_FULL_TEXT, 
    CONTENT_TYPE_DATA,
]

LOG_FILE_PROCESSED = 1
LOG_FILE_INVALIDATED = -1
