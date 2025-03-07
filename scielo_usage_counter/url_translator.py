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


class URLTranslationManager:
    def __init__(self, journals_metadata, articles_metadata):
        self.load_journals(journals_metadata)
        self.load_articles(articles_metadata)
        self.translator = None

    def load_articles(self, data):
        logging.info('Loading articles metadata...')

        self.articles_metadata = {
            'pid_v3_to_pid_v2': {},
            'pid_v3_to_default_lang': {},
            'pid_v3_to_available_langs': {},
            'pid_v3_to_scielo_issn': {},
            'pid_v3_to_publication_year': {},
            'pid_v2_to_pid_v3': {},
            'pid_v2_to_default_lang': {},
            'pid_v2_to_available_langs': {},
            'pid_v2_to_scielo_issn': {},
            'pid_v2_to_publication_year': {},
            'pdf_to_pid_v2': {},
            'doi_to_pid_v2': {},
            'doi_to_pid_v3': {},            
        }

        count = 0
        for art in data:
            count += 1
            key_pid_v2 = art.get('pid_v2')
            key_pid_v3 = art.get('pid_v3')

            self.articles_metadata['pid_v2_to_pid_v3'][key_pid_v2] = key_pid_v3
            self.articles_metadata['pid_v2_to_default_lang'][key_pid_v2] = art.get('default_lang')
            self.articles_metadata['pid_v2_to_available_langs'][key_pid_v2] = art.get('text_langs')
            self.articles_metadata['pid_v2_to_scielo_issn'][key_pid_v2] = art.get('scielo_issn')
            self.articles_metadata['pid_v2_to_publication_year'][key_pid_v2] = art.get('publication_year')

            for pdf_data in art.get('pdfs'):
                pdf_key = pdf_data.get('path')
                if not pdf_key.startswith('/'):
                    pdf_key = f'/{pdf_key}'
                self.articles_metadata['pdf_to_pid_v2'][pdf_key] = key_pid_v2

                doi_key = pdf_data.get('doi')
                self.articles_metadata['doi_to_pid_v2'][doi_key] = key_pid_v2
                self.articles_metadata['doi_to_pid_v3'][doi_key] = key_pid_v3

            self.articles_metadata['pid_v3_to_pid_v2'][key_pid_v3] = key_pid_v2
            self.articles_metadata['pid_v3_to_default_lang'][key_pid_v3] = art.get('default_lang')
            self.articles_metadata['pid_v3_to_available_langs'][key_pid_v3] = art.get('text_langs')
            self.articles_metadata['pid_v3_to_scielo_issn'][key_pid_v3] = art.get('scielo_issn')
            self.articles_metadata['pid_v3_to_publication_year'][key_pid_v3] = art.get('publication_year')

        logging.info(f'Loaded {count} articles metadata.')

    def load_journals(self, data):
        logging.info('Loading journals metadata...')

        self.journals_metadata = {
            'acronym_to_scielo_issn': {},
            'issn_to_title': {},
            'issn_to_publisher_name': {},
        }

        count = 0
        for j in data:
            count += 1
            self.journals_metadata['acronym_to_scielo_issn'][j.get('acronym')] = j.get('scielo_issn')

            for issn in j.get('issns'):
                self.journals_metadata['issn_to_title'][issn] = j.get('title')
                self.journals_metadata['issn_to_publisher_name'][issn] = j.get('publisher_name')

        logging.info(f'Loaded {count} journals metadata.')

    def identify_translator_class(self, url):
        parsed_url = urlparse(url)

        for pattern, url_translator_class  in [
            (PATTERNS_CLASSIC_SITE, URLTranslatorClassicSite),
            (PATTERNS_OPAC_SITE, URLTranslatorOPACSite),
            (PATTERNS_OPAC_ALPHA_SITE, URLTranslatorOPACAlphaSite),
            (PATTERNS_PREPRINTS_SITE, URLTranslatorPreprintsSite),
            (PATTERNS_DATAVERSE_SITE, URLTranslatorDataverseSite),
        ]:
            if any(re.search(p, parsed_url.path) for p in pattern):
                self.translator = url_translator_class(self.journals_metadata, self.articles_metadata)
                return
        
        if not self.translator:
            self.translator = URLTranslatorClassicSite(self.journals_metadata, self.articles_metadata)

    def translate(self, url: str):
        self.identify_translator_class(url)
        data = self.translator.pipeline_translate(url)
        return self.standardize_fields(data)
