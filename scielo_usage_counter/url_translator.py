import logging
import re

from urllib.parse import urlparse, urlsplit, parse_qs, parse_qsl


NAME_CLASSIC_SITE = 'classic_site'
NAME_OPAC_ALPHA_SITE = 'opac_alpha_site'
NAME_OPAC_SITE = 'opac_site'
NAME_PREPRINTS_SITE = 'preprints_site'
NAME_DATAVERSE_SITE = 'dataverse_site'

PATTERNS_CLASSIC_SITE = [
    re.compile(r'/scielo.php', re.IGNORECASE),
    re.compile(r'/scieloorg/php/', re.IGNORECASE),
    re.compile(r'/popup/', re.IGNORECASE),
    re.compile(r'/google_metrics/', re.IGNORECASE),
    re.compile(r'/pdf/', re.IGNORECASE),
]

PATTERNS_OPAC_SITE = [
    re.compile(r'/?j/[^/]+/', re.IGNORECASE),
]

PATTERNS_PREPRINTS_SITE = [
    re.compile(r'/?index.php/documents/article/(download|view)/', re.IGNORECASE),
    re.compile(r'/?index.php/scielo/preprint/', re.IGNORECASE),
    re.compile(r'/?plugins/generic/(hypothesis|pdfJsViewer)/', re.IGNORECASE),
]

PATTERNS_OPAC_ALPHA_SITE = [
    re.compile(r'/?j/[^/]+/', re.IGNORECASE),
    re.compile(r'/?article/[^/]+/[^/]+/[^/]+', re.IGNORECASE),
    re.compile(r'/?pdf/[^/]+/[^/]+/', re.IGNORECASE),
]

PATTERNS_DATAVERSE_SITE = [
    re.compile(r'dataset.xhtml', re.IGNORECASE),
    re.compile(r'dataverse', re.IGNORECASE),
    re.compile(r'logingpage.xhtml', re.IGNORECASE),
]

DEFAULT_SCIELO_ISSN = '0000-0000'

MEDIA_LANGUAGE_UNDEFINED = 'un'

MEDIA_FORMAT_HTML = 'html'
MEDIA_FORMAT_PDF = 'pdf'
MEDIA_FORMAT_XML = 'xml'
MEDIA_FORMAT_UNDEFINED = 'und'

# Patterns related to Preprints site
REGEX_PREPRINTS_SITE_VIEW_ABSTRACT = re.compile(r'preprint/view/(?P<id>\d+)$', re.IGNORECASE)
REGEX_PREPRINTS_SITE_DOCUMENT_ABSTRACT = re.compile(r'documents/article/view/(?P<id>\d+)$', re.IGNORECASE)
REGEX_PREPRINTS_SITE_VERSION_ABSTRACT = re.compile(r'preprint/view/(\d+)/version/(?P<id>\d+)$', re.IGNORECASE)
REGEX_PREPRINTS_SITE_VIEW_PDF = re.compile(r'preprint/view/(?P<id>\d+)/(\d+)', re.IGNORECASE)
REGEX_PREPRINTS_SITE_DOWNLOAD_PDF = re.compile(r'preprint/download/(?P<id>\d+)/(\d+)', re.IGNORECASE)
REGEX_PREPRINTS_SITE_DOCUMENT_DOWNLOAD_PDF = re.compile(r'documents/article/download/(?P<id>\d+)/(\d+)', re.IGNORECASE)
REGEX_PREPRINTS_SITE_VERSION_DOWNLOAD_PDF = re.compile(r'preprint/download/(?P<id>\d+)/version/(\d+)/(\d+)', re.IGNORECASE)

# Patterns related to OPAC Alpha site
REGEX_OPAC_ALPHA_JOURNAL_ARTICLE_HTML_DETAILS = re.compile(r'.*/article/(\w*)/?([\d|\w|\.|\-]*)/?([\d|\w|\-]*)/?(\w*|)', re.IGNORECASE)
REGEX_OPAC_ALPHA_JOURNAL_ARTICLE_PDF_DETAILS = re.compile(r'.*/pdf/(\w*)/([\d|\w|\.|\-]*)/?([\d|\w|\-]*)/?(\w*|)', re.IGNORECASE)
REGEX_OPAC_ALPHA_JOURNAL_ARTICLE_MEDIA_ASSETS_DETAILS = re.compile(r'.*/media/assets/(\w*)/?([\d|\w|\.|\-]*)/?([\d|\w|\-|\.|\_]*)', re.IGNORECASE)

# Patterns related to OPAC Site
REGEX_OPAC_SITE_JOURNAL_ARTICLE = re.compile(r'.*/j/(\w*)/a/(\w*)', re.IGNORECASE)  # grupo 1 = acrônimo, grupo 2 = PID
REGEX_OPAC_SITE_RAW_DETAIL = re.compile(r'.*/documentstore/([\w|-]*)/(\w*)/([\w|\.]*)', re.IGNORECASE)

# Patterns related to Classic Site
REGEX_CLASSIC_SITE_ARTICLE_PDF = re.compile(r'.*\.pdf$', re.IGNORECASE)
REGEX_CLASSIC_SITE_ARTICLE_PDF_PATH = re.compile(r'.*(/pdf/.*/.*)', re.IGNORECASE)
REGEX_CLASSIC_SITE_ARTICLE_PDF_FULL_PATH = re.compile(r'(.*)(/pdf/.*/.*)', re.IGNORECASE)
REGEX_CLASSIC_SITE_ARTICLE_XML = re.compile(r'articlexml', re.IGNORECASE)


