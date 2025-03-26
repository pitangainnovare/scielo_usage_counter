import re

from urllib.parse import urlparse, parse_qsl

from scielo_usage_counter.values import (
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_PDF,
    MEDIA_LANGUAGE_UNDEFINED,
    R5_CONTENT_TYPE_INVESTIGATION,
    R5_CONTENT_TYPE_REQUEST,
)   


# Patterns to support parameter extraction and determine whether a URL is an Investigation or a Request
REGEX_OPAC_ALPHA_ARTICLE_ACRONYM_YEAR_VOL_ISSUE_PAGES_LANGUAGE = re.compile(r'article/(?P<journal_acronym>\w*)/(?P<year>\d{0,4})\.(?P<vol_issue>[\d|\w]+)/(?P<pages>[\d-]+|e[\w\d]+)/?(?P<media_language>\w{2})?', re.IGNORECASE) # Request or Investigation
REGEX_OPAC_ALPHA_PDF_ACRONYM_YEAR_VOL_ISSUE_PAGES_LANGUAGE = re.compile(r'pdf/(?P<journal_acronym>\w*)/(?P<year>\d{0,4})\.(?P<vol_issue>[\d|\w]+)/(?P<pages>[\d-]+|e[\w\d]+)/?(?P<media_language>\w{2})?', re.IGNORECASE) # Request
REGEX_OPAC_ALPHA_PDF_PATH = r'.*/?pdf/(?P<journal_acronym>\w*)/(?P<vol_issue>[\d|\w]*)/(?P<pages>[\d-]+|e[\w\d]+)/(?P<file>[\d|\w|-]*\.pdf)'    # Request
REGEX_OPAC_ALPHA_MEDIA_ASSETS_ACRONYM = re.compile(r'.*/media/assets/(?P<journal_acronym>\w*)/(?P<vol_issue>[\d|\w]*)/(?P<file>[\d|\w|-]*\.pdf)', re.IGNORECASE)   # Request


class URLTranslatorOPACAlphaSite:
    def __init__(self, journals_metadata, articles_metadata):
        self.journals_metadata = journals_metadata
        self.articles_metadata = articles_metadata

    def pipeline_translate(self, url):
        self.url_params = self.extract_url_params(url)

        pid_v3 = self.extract_pid_v3()
        media_format = self.extract_media_format()
        media_language = self.extract_media_language(pid_v3)
        scielo_issn = self.extract_issn()

        content_type = self.extract_content_type()

        return {
            'scielo_issn': scielo_issn,
            'pid_v2': None,
            'pid_v3': pid_v3,
            'media_format': media_format,
            'media_language': media_language,
            'content_type': content_type,
        }

    def extract_url_params(self, url):
        url_params = {
            'pid_v3': None, 
            'journal_acronym': None,
            'media_format': None,
            'media_language': None,
            'resource_ssm_path': None,
        }

        url_parsed = urlparse(url)
        if 'resource_ssm_path' in url:
            self._get_url_params_from_query_key(url_params, url_parsed.query)
        else:
            self._get_url_params_from_url_path(url_params, url_parsed.path)

        params = dict(parse_qsl(url_parsed.query))
        for k, v in params.items():
            if k == 'lang':
                url_params['media_language'] = v
            elif k == 'format':
                url_params['media_format'] = v
            else:
                url_params[k] = v

        return url_params

    def _get_url_params_from_query_key(self, url_params, query):
        resource_path = dict(parse_qsl(query)).get('resource_ssm_path', '')
        match = re.search(REGEX_OPAC_ALPHA_MEDIA_ASSETS_ACRONYM, resource_path)
        if match:
            url_params['journal_acronym'] = match.groupdict().get('journal_acronym')
            url_params['file'] = match.groupdict().get('file')

            if query.endswith('.pdf'):
                url_params['media_format'] = MEDIA_FORMAT_PDF

    def _get_url_params_from_url_path(self, url_params, url_path):
        for media_format, p in [
            (MEDIA_FORMAT_HTML, REGEX_OPAC_ALPHA_ARTICLE_ACRONYM_YEAR_VOL_ISSUE_PAGES_LANGUAGE),
            (MEDIA_FORMAT_PDF, REGEX_OPAC_ALPHA_PDF_ACRONYM_YEAR_VOL_ISSUE_PAGES_LANGUAGE),
            (MEDIA_FORMAT_PDF, REGEX_OPAC_ALPHA_PDF_PATH),
        ]:
    
            match = re.search(p, url_path)

            if match:
                url_params['media_format'] = media_format
                url_params['journal_acronym'] = match.groupdict().get('journal_acronym')
                url_params['year'] = match.groupdict().get('year')
                url_params['vol_issue'] = match.groupdict().get('vol_issue')
                url_params['pages'] = match.groupdict().get('pages')
                url_params['media_language'] = match.groupdict().get('language')
                return

        path_match_assets = re.match(REGEX_OPAC_ALPHA_MEDIA_ASSETS_ACRONYM, url_path)
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
        return self._extract_artifitial_pid()
    
    def _extract_artifitial_pid(self):        
        artificial_pid = ':'.join([
            self.url_params.get('journal_acronym') or '',
            self.url_params.get('year') or '',
            self.url_params.get('vol_issue') or '',
        ])

        if self.url_params.get('pages'):
            return ':'.join([artificial_pid, self.url_params.get('pages', '')])

        if self.url_params.get('file'):
            key = self.url_params.get('file', '').lstrip('/')
            key = f'/{key}' if key else ''
            return self.articles_metadata.get('pdf_to_pid_v3').get(key)
    
    def extract_issn(self):
        return self.journals_metadata['acronym_to_scielo_issn'].get(self.url_params.get('journal_acronym'))

    def extract_content_type(self):
        if 'abstract_lang' in self.url_params:
            return R5_CONTENT_TYPE_INVESTIGATION
        return R5_CONTENT_TYPE_REQUEST
