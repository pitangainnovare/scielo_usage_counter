import re

from urllib.parse import urlparse, parse_qsl

from scielo_usage_counter.values import (
    MEDIA_LANGUAGE_UNDEFINED,
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_PDF,
    MEDIA_FORMAT_XML,
    CONTENT_TYPE_ABSTRACT,
    CONTENT_TYPE_CITATION_EXPORT,
    CONTENT_TYPE_FULL_TEXT,
    CONTENT_TYPE_UNDEFINED,
)


# Patterns to support parameter extraction
REGEX_OPAC_SITE_JOURNAL_ARTICLE_ABSTRACT = re.compile(r'.*/j/(?P<journal_acronym>\w*)/a/(?P<pid_v3>\w*)/abstract', re.IGNORECASE)
REGEX_OPAC_SITE_JOURNAL_ARTICLE = re.compile(r'.*/j/(?P<journal_acronym>\w*)/a/(?P<pid_v3>\w*)', re.IGNORECASE)
REGEX_OPAC_SITE_DOCUMENT_STORE = re.compile(r'documentstore/(?P<journal_issn>[\w|-]*)/(?P<pid_v3>\w*)/(?P<file>[\w|\.]*)', re.IGNORECASE)
REGEX_OPAC_SITE_CITATION_EXPORT = re.compile(r'.*/?citation/export/(?P<pid_v3>\w*)/', re.IGNORECASE)


class URLTranslatorOPACSite:
    def __init__(self, sources_metadata, documents_metadata):
        self.sources_metadata = sources_metadata
        self.documents_metadata = documents_metadata

    def pipeline_translate(self, url):
        self.url_params = self.extract_url_params(url)

        pid_v3 = self.extract_pid_v3()
        media_format = self.extract_media_format()
        media_language = self.extract_media_language(pid_v3)
        scielo_issn = self.extract_issn()
        content_type = self.extract_content_type()

        return {
            'scielo_issn': scielo_issn,
            'journal_main_title': self.sources_metadata.get('issn_to_title', {}).get(scielo_issn),
            'journal_subject_area_capes': self.sources_metadata.get('issn_to_subject_area_capes', {}).get(scielo_issn),
            'journal_subject_area_wos': self.sources_metadata.get('issn_to_subject_area_wos', {}).get(scielo_issn),
            'journal_publisher_name': self.sources_metadata.get('issn_to_publisher_name', {}).get(scielo_issn),
            'journal_acronym': self.sources_metadata.get('issn_to_acronym', {}).get(scielo_issn),
            'pid_v2': self.documents_metadata.get('pid_v3_to_pid_v2', {}).get(pid_v3),
            'pid_v3': pid_v3,
            'media_format': media_format,
            'media_language': media_language,
            'content_type': content_type,
            'year_of_publication': self.documents_metadata.get('pid_v3_to_publication_year', {}).get(pid_v3),
        }

    def extract_url_params(self, url):
        url_params = {
            'pid_v3': '',
            'journal_acronym': '',
            'media_format': '',
            'media_language': '',
            'resource_ssm_path': ''
        }

        parsed_url = urlparse(url)
        params = dict(parse_qsl(parsed_url.query))
        for k, v in params.items():
            if k == 'lang':
                url_params['media_language'] = v
            elif k == 'format':
                url_params['media_format'] = v
            else:
                url_params[k] = v

        self.url_matches = {
            'abstract': REGEX_OPAC_SITE_JOURNAL_ARTICLE_ABSTRACT.search(parsed_url.path),
            'article': REGEX_OPAC_SITE_JOURNAL_ARTICLE.search(parsed_url.path),
            'citation': REGEX_OPAC_SITE_CITATION_EXPORT.search(parsed_url.path),
            'documentstore': None,
        }

        article_match = self.url_matches['article']
        citation_match = self.url_matches['citation']
        if article_match:
            url_params['journal_acronym'] = article_match.groupdict().get('journal_acronym')
            url_params['pid_v3'] = article_match.groupdict().get('pid_v3')
        elif citation_match:
            url_params['pid_v3'] = citation_match.groupdict().get('pid_v3')

        if url_params['resource_ssm_path']:
            match = REGEX_OPAC_SITE_DOCUMENT_STORE.search(url_params['resource_ssm_path'])
            self.url_matches['documentstore'] = match
            if match and len(match.groups()) == 3:
                url_params['scielo_issn'] = match.groupdict().get('journal_issn')
                url_params['pid_v3'] = match.groupdict().get('pid_v3')
                url_params['file'] = match.groupdict().get('file')
                if url_params['file'].endswith('.pdf'):
                    url_params['media_format'] = MEDIA_FORMAT_PDF
        
        return url_params

    def extract_media_format(self, url=None):
        if url is not None:
            self.url_params = self.extract_url_params(url)

        if self.url_matches['citation']:
            self.url_params['media_format'] = MEDIA_FORMAT_HTML

        return self.url_params.get('media_format') or MEDIA_FORMAT_HTML

    def extract_media_language(self, pid_v3):
        media_language = self.url_params.get('media_language')
        if not media_language:
            media_language = self.documents_metadata['pid_v3_to_default_lang'].get(pid_v3, MEDIA_LANGUAGE_UNDEFINED)
        return media_language

    def extract_pid_v3(self):
        return self.url_params.get('pid_v3')

    def extract_issn(self):
        if not self.url_params.get('journal_acronym'):
            return self.documents_metadata['pid_v3_to_scielo_issn'].get(self.url_params.get('pid_v3'))
        return self.sources_metadata['acronym_to_scielo_issn'].get(self.url_params.get('journal_acronym'))
    
    def extract_content_type(self, url=None):
        if url is not None:
            self.url_params = self.extract_url_params(url)

        if self.url_matches['abstract']:
            return CONTENT_TYPE_ABSTRACT
        
        if self.url_matches['citation']:
            return CONTENT_TYPE_CITATION_EXPORT
        
        if self.url_params['media_format'] in (
            MEDIA_FORMAT_XML,
            MEDIA_FORMAT_PDF,
        ):
            return CONTENT_TYPE_FULL_TEXT
        
        match = self.url_matches['documentstore']
        if match and match.groupdict().get('file', '').endswith('.pdf'):
            return CONTENT_TYPE_FULL_TEXT
        
        if self.url_matches['article']:
            return CONTENT_TYPE_FULL_TEXT

        return CONTENT_TYPE_UNDEFINED
