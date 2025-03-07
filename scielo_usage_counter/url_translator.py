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

    def standardize_fields(self, fields: dict):
        std_fields = {}
        
        for k, v in fields.items():
            if k in ('scielo_issn', 'pid_v2', 'media_language'):
                if v:
                    std_fields[k] = v.strip().upper()
            if k in ('pid_v3', 'media_language', 'media_format'):
                if v:
                    std_fields[k] = v.strip()

        return std_fields


class URLTranslatorPreprintsSite:
    def __init__(self, journals_metadata, articles_metadata):
        self.journals_metadata = journals_metadata
        self.articles_metadata = articles_metadata
        self.name = NAME_PREPRINTS_SITE

    def pipeline_translate(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        preprint_id = self.extract_preprint_id(parsed_url, query_params)
        scielo_issn = self.extract_issn(preprint_id)        
        media_format = self.extract_media_format(parsed_url, query_params)
        media_language = self.extract_media_language(preprint_id)

        return {
            'scielo_issn': scielo_issn,
            'pid_v2': preprint_id,
            'pid_v3': None,
            'media_format': media_format,
            'media_language': media_language,
        }

    @classmethod
    def extract_media_format(cls, url):
        unquoted_url = urlparse.unquote(url)

        html_patterns = [
            REGEX_PREPRINTS_SITE_VIEW_ABSTRACT,
            REGEX_PREPRINTS_SITE_DOCUMENT_ABSTRACT,
            REGEX_PREPRINTS_SITE_VERSION_ABSTRACT
        ]

        pdf_patterns = [
            REGEX_PREPRINTS_SITE_VIEW_PDF,
            REGEX_PREPRINTS_SITE_DOWNLOAD_PDF,
            REGEX_PREPRINTS_SITE_DOCUMENT_DOWNLOAD_PDF,
            REGEX_PREPRINTS_SITE_VERSION_DOWNLOAD_PDF
        ]

        if any(re.search(pattern, unquoted_url) for pattern in html_patterns):
            return MEDIA_FORMAT_HTML

        if any(re.search(pattern, unquoted_url) for pattern in pdf_patterns):
            return MEDIA_FORMAT_PDF

        return MEDIA_FORMAT_UNDEFINED

    def extract_media_language(self, pid_v2):
        return self.articles_metadata['pid_v2_to_default_lang'].get(pid_v2)

    @classmethod
    def extract_issn():
        return DEFAULT_SCIELO_ISSN

    @classmethod
    def extract_preprint_id(url):
        unquoted_url = urlparse.unquote(url)

        for pattern in [
            REGEX_PREPRINTS_SITE_VIEW_ABSTRACT,
            REGEX_PREPRINTS_SITE_DOCUMENT_ABSTRACT,
            REGEX_PREPRINTS_SITE_VERSION_ABSTRACT,
            REGEX_PREPRINTS_SITE_VIEW_PDF,
            REGEX_PREPRINTS_SITE_DOWNLOAD_PDF,
            REGEX_PREPRINTS_SITE_DOCUMENT_DOWNLOAD_PDF,
            REGEX_PREPRINTS_SITE_VERSION_DOWNLOAD_PDF
        ]:
            match = re.search(pattern, unquoted_url)
            if match:
                return match.group('id')


class URLTranslatorOPACAlphaSite:
    def __init__(self, journals_metadata, articles_metadata):
        self.journals_metadata = journals_metadata
        self.articles_metadata = articles_metadata
        self.name = NAME_OPAC_ALPHA_SITE

    def pipeline_translate(self, url):
        self.url_params = self.extract_url_params(url)

        pid_v3 = self.extract_pid_v3(url)
        media_format = self.extract_media_format(url)
        media_language = self.extract_media_language(pid_v3)
        scielo_issn = self.extract_issn(url)

        return {
            'scielo_issn': scielo_issn,
            'pid_v2': None,
            'pid_v3': pid_v3,
            'media_format': media_format,
            'media_language': media_language,
        }

    def extract_url_params(self, url):
        url_params = {
            'pid_v3': '', 
            'journal_acronym': '',
            'media_format': '',
            'media_language': '',
            'resource_ssm_path': ''
        }

        url_evaluated = url
        if not url_evaluated.startswith('http'):
            url_evaluated = ''.join(['http://', url_evaluated])

        url_parsed = urlparse(url_evaluated)
        if 'resource_ssm_path' in url_evaluated:
            self._get_url_params_from_query_key(url_params, url_parsed.query)
        else:
            self._get_url_params_from_url_path(url_params, url_parsed.path)

        return url_params

    def _get_url_params_from_query_key(self, url_params, query):
        resource_path = dict(parse_qsl(query)).get('resource_ssm_path', '')
        match = re.search(REGEX_OPAC_ALPHA_JOURNAL_ARTICLE_MEDIA_ASSETS_DETAILS, resource_path)
        if match:
            url_params['journal_acronym'] = match.group(1)
            url_params['year_vol_issue'] = match.group(2)
            url_params['file'] = match.group(3)
            url_params['resource_ssm_path'] = resource_path

            if query.endswith('.pdf'):
                url_params['media_format'] = MEDIA_FORMAT_PDF

    def _get_url_params_from_url_path(self, url_params, url_path):
        for k, v in {
            MEDIA_FORMAT_HTML: REGEX_OPAC_ALPHA_JOURNAL_ARTICLE_HTML_DETAILS,
            MEDIA_FORMAT_PDF: REGEX_OPAC_ALPHA_JOURNAL_ARTICLE_PDF_DETAILS
        }.items():
            match = re.search(v, url_path)

            if match:
                url_params['media_format'] = k
                url_params['journal_acronym'] = match.group(1)
                url_params['year_vol_issue'] = match.group(2)
                url_params['pages'] = match.group(3)
                url_params['media_language'] = match.group(4)
                return

        path_match_assets = re.match(REGEX_OPAC_ALPHA_JOURNAL_ARTICLE_MEDIA_ASSETS_DETAILS, url_path)
        if path_match_assets:
            url_params['journal_acronym'] = path_match_assets.group(1)
            url_params['year_vol_issue'] = path_match_assets.group(2)
            url_params['file'] = path_match_assets.group(3)

            if url_path.endswith('.pdf'):
                url_params['media_format'] = MEDIA_FORMAT_PDF

    def extract_media_format(self):
        return self.url_params.get('media_format')

    def extract_media_language(self, pid_v3):
        media_language = self.url_params.get('media_language')
        if not media_language:
            media_language = self.articles_metadata['pid_v3_to_default_lang'].get(pid_v3, MEDIA_LANGUAGE_UNDEFINED)
        return media_language

    def extract_pid_v3(self):
        return self._get_ssp_pid()
    
    def _get_ssp_pid(self):
        artificial_pid = ':'.join([
            self.url_params.get('journal_acronym', ''),
            self.url_params.get('year_vol_issue', '')
        ])

        if 'pages' in self.url_params:
            return ':'.join([artificial_pid, self.url_params.get('pages', '')])

        if 'file' in self.url_params:
            return ':'.join([artificial_pid, self.url_params.get('file', '')])
    
    def extract_issn(self):
        return self.journals_metadata['acronym_to_scielo_issn'].get(self.url_params.get('journal_acronym'))


class URLTranslatorOPACSite:
    def __init__(self, journals_metadata, articles_metadata):
        self.journals_metadata = journals_metadata
        self.articles_metadata = articles_metadata
        self.name = NAME_OPAC_SITE

    def pipeline_translate(self, url):
        self.url_params = self.extract_url_params(url)

        pid_v3 = self.extract_pid_v3()
        media_format = self.extract_media_format()
        media_language = self.extract_media_language()
        scielo_issn = self.extract_issn()

        return {
            'scielo_issn': scielo_issn,
            'pid_v2': None,
            'pid_v3': pid_v3,
            'media_format': media_format,
            'media_language': media_language,
        }

    def extract_url_params(self, url):
        url_params = {
            'pid_v3': '',
            'journal_acronym': '',
            'media_format': MEDIA_FORMAT_HTML,
            'media_language': '',
            'fragment': '',
            'resource_ssm_path': ''
        }

        url_evaluated = url
        if not url_evaluated.startswith('http'):
            url_evaluated = ''.join(['http://', url_evaluated])

        url_parsed = urlparse(url_evaluated)
        params = dict(parse_qsl(url_parsed.query))
        for k, v in params.items():
            if k in url_params:
                url_params[k] = v

        url_params['fragment'] = url_parsed.fragment
        url_params['journal_acronym'], url_params['pid_v3'] = self._get_acronym_and_pid_from_action_new_url(url)

        if 'resource_ssm_path' in url_params:
            match = re.search(REGEX_OPAC_SITE_RAW_DETAIL, self.url_params['resource_ssm_path'])
            if match and len(match.groups()) == 3:
                url_params['scielo_issn'] = match.group(1).upper()
                url_params['pid_v3'] = match.group(2)
                url_params['file'] = match.group(3)
                if url_params['file'].endswith('.pdf'):
                    url_params['media_format'] = MEDIA_FORMAT_PDF

        return url_params
    
    def _get_acronym_and_pid_from_action_new_url(url):
        match = re.search(REGEX_OPAC_SITE_JOURNAL_ARTICLE, url)
        if match:
            if len(match.groups()) == 2:
                return match.group(1), match.group(2)
        return '', ''

    def extract_media_format(self):
        return self.url_params.get('media_format')

    def extract_media_language(self, pid_v3):
        media_language = self.url_params.get('media_language')
        if not media_language:
            media_language = self.articles_metadata['pid_v3_to_default_lang'].get(pid_v3, MEDIA_LANGUAGE_UNDEFINED)
        return media_language

    def extract_pid_v3(self):
        return self.url_params.get('pid_v3')
    
    def extract_issn(self):
        return self.journals_metadata['acronym_to_scielo_issn'].get(self.url_params.get('journal_acronym'))

