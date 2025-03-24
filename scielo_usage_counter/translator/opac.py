import re

from urllib.parse import urlparse, parse_qsl

from scielo_usage_counter.values import (
    MEDIA_LANGUAGE_UNDEFINED,
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_PDF,
    MEDIA_FORMAT_XML,
    R5_CONTENT_TYPE_INVESTIGATION,
    R5_CONTENT_TYPE_REQUEST,
    R5_CONTENT_TYPE_UNDEFINED,
)


NAME_OPAC_SITE = 'opac_site'

# Patterns to support parameter extraction and determine whether a URL is an Investigation or a Request
REGEX_OPAC_SITE_JOURNAL_ARTICLE_ABSTRACT = re.compile(r'.*/j/(?P<journal_acronym>\w*)/a/(?P<pid_v3>\w*)/abstract', re.IGNORECASE)   # Investigation
REGEX_OPAC_SITE_JOURNAL_ARTICLE = re.compile(r'.*/j/(?P<journal_acronym>\w*)/a/(?P<pid_v3>\w*)', re.IGNORECASE) # Request
REGEX_OPAC_SITE_RAW_DETAIL = re.compile(r'.*/documentstore/([\w|-]*)/(\w*)/(?P<path>[\w|\.]*)', re.IGNORECASE)  # Request


class URLTranslatorOPACSite:
    def __init__(self, journals_metadata, articles_metadata):
        self.journals_metadata = journals_metadata
        self.articles_metadata = articles_metadata
        self.name = NAME_OPAC_SITE

    def pipeline_translate(self, url):
        self.url_params = self.extract_url_params(url)

        pid_v3 = self.extract_pid_v3()
        media_format = self.extract_media_format(url)
        media_language = self.extract_media_language(pid_v3)
        scielo_issn = self.extract_issn()

        content_type = self.extract_content_type(url)

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
            'pid_v3': '',
            'journal_acronym': '',
            'media_format': '',
            'media_language': '',
            'fragment': '',
            'resource_ssm_path': ''
        }

        url_evaluated = url
        if not url_evaluated.startswith('http'):
            url_evaluated = ''.join(['http://', url_evaluated]).replace('//', '/')

        url_parsed = urlparse(url_evaluated)
        params = dict(parse_qsl(url_parsed.query))
        for k, v in params.items():
            if k == 'lang':
                url_params['media_language'] = v
            elif k == 'format':
                url_params['media_format'] = v
            else:
                url_params[k] = v

        url_params['fragment'] = url_parsed.fragment
        url_params['journal_acronym'], url_params['pid_v3'] = self._get_acronym_and_pid_from_url(url)

        if 'resource_ssm_path' in url_params:
            match = re.search(REGEX_OPAC_SITE_RAW_DETAIL, url_params['resource_ssm_path'])
            if match and len(match.groups()) == 3:
                url_params['scielo_issn'] = match.group(1).upper()
                url_params['pid_v3'] = match.group(2)
                url_params['file'] = match.group(3)
                if url_params['file'].endswith('.pdf'):
                    url_params['media_format'] = MEDIA_FORMAT_PDF

        return url_params
    
    def _get_acronym_and_pid_from_url(self, url):
        journal_acronym = ''
        pid_v3 = ''

        match = re.search(REGEX_OPAC_SITE_JOURNAL_ARTICLE, url)
        if match:
            journal_acronym = match.groupdict().get('journal_acronym')
            pid_v3 = match.groupdict().get('pid_v3')

        return journal_acronym, pid_v3

    def extract_media_format(self, url):
        if not hasattr(self, 'url_params'):
            self.extract_url_params(url)

        return self.url_params.get('media_format') or MEDIA_FORMAT_HTML

    def extract_media_language(self, pid_v3):
        media_language = self.url_params.get('media_language')
        if not media_language:
            media_language = self.articles_metadata['pid_v3_to_default_lang'].get(pid_v3, MEDIA_LANGUAGE_UNDEFINED)
        return media_language

    def extract_pid_v3(self):
        return self.url_params.get('pid_v3')
    
    def extract_issn(self):
        return self.journals_metadata['acronym_to_scielo_issn'].get(self.url_params.get('journal_acronym'))
    
    def extract_content_type(self, url):
        if not hasattr(self, 'media_format'):
            self.extract_media_format(url)

        if re.search(REGEX_OPAC_SITE_JOURNAL_ARTICLE_ABSTRACT, url):
            return R5_CONTENT_TYPE_INVESTIGATION
        
        if re.search(REGEX_OPAC_SITE_JOURNAL_ARTICLE, url):
            return self._identify_content_type_by_fragment(self.url_params.get('fragment', ''))
        
        if self.url_params['media_format'] in (
            MEDIA_FORMAT_XML,
            MEDIA_FORMAT_PDF,
        ):
            return R5_CONTENT_TYPE_REQUEST
        
        match = re.search(REGEX_OPAC_SITE_RAW_DETAIL, url)
        if match and match.groupdict().get('path', '').endswith('.pdf'):
            return R5_CONTENT_TYPE_REQUEST

        return R5_CONTENT_TYPE_UNDEFINED
    
    def _identify_content_type_by_fragment(self, fragment):
        # The OPAC site currently does not have a way to identify modal pages
        if fragment in set([
            'modaltutors',
            'modaltablesfigures',
            'modaldownloads',
            'modalarticles',
            'modalversionstranslations',
        ]):
            return R5_CONTENT_TYPE_INVESTIGATION
        return R5_CONTENT_TYPE_REQUEST
