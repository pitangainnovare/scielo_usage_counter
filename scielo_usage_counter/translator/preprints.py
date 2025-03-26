import re

from urllib.parse import urlparse, unquote

from scielo_usage_counter.values import (
    DEFAULT_SCIELO_ISSN,
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_PDF,
    MEDIA_FORMAT_UNDEFINED,
    CONTENT_TYPE_ABSTRACT,
    CONTENT_TYPE_FULL_TEXT,
    CONTENT_TYPE_UNDEFINED,
)


# Patterns to support parameter extraction
REGEX_PREPRINTS_SITE_VIEW_ABSTRACT = re.compile(r'preprint/view/(?P<id>\d+)$', re.IGNORECASE)
REGEX_PREPRINTS_SITE_DOCUMENT_ABSTRACT = re.compile(r'documents/article/view/(?P<id>\d+)$', re.IGNORECASE)
REGEX_PREPRINTS_SITE_VERSION_ABSTRACT = re.compile(r'preprint/view/(?P<id>\d+)/version/(\d+)$', re.IGNORECASE)
REGEX_PREPRINTS_SITE_VIEW_PDF = re.compile(r'preprint/view/(?P<id>\d+)/(\d+)', re.IGNORECASE)
REGEX_PREPRINTS_SITE_DOWNLOAD_PDF = re.compile(r'preprint/download/(?P<id>\d+)/(\d+)', re.IGNORECASE)
REGEX_PREPRINTS_SITE_DOCUMENT_DOWNLOAD_PDF = re.compile(r'documents/article/download/(?P<id>\d+)/(\d+)', re.IGNORECASE)
REGEX_PREPRINTS_SITE_VERSION_DOWNLOAD_PDF = re.compile(r'preprint/download/(?P<id>\d+)/version/(\d+)/(\d+)', re.IGNORECASE)


class URLTranslatorPreprintsSite:
    def __init__(self, journals_metadata, articles_metadata):
        self.journals_metadata = journals_metadata
        self.articles_metadata = articles_metadata

    def pipeline_translate(self, url):
        parsed_url = urlparse(url)

        preprint_id = self.extract_preprint_id(parsed_url.path)
        scielo_issn = self.extract_issn(preprint_id)        
        media_format = self.extract_media_format(parsed_url.path)
        media_language = self.extract_media_language(preprint_id)

        content_type = self.extract_content_type(parsed_url.path)

        return {
            'scielo_issn': scielo_issn,
            'id': preprint_id,
            'pid_v2': None,
            'pid_v3': None,
            'media_format': media_format,
            'media_language': media_language,
            'content_type': content_type,
        }

    def extract_media_format(self, url):
        unquoted_url = unquote(url)

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

    def extract_issn(self, preprint_id):
        # TODO: Implement ISSN extraction logic using external data sources
        return DEFAULT_SCIELO_ISSN

    def extract_preprint_id(self, url):
        unquoted_url = unquote(url)

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

    def extract_content_type(self, url):
        for r in [
            REGEX_PREPRINTS_SITE_VIEW_ABSTRACT,
            REGEX_PREPRINTS_SITE_DOCUMENT_ABSTRACT,
            REGEX_PREPRINTS_SITE_VERSION_ABSTRACT
        ]:
            if re.search(r, url):
                return CONTENT_TYPE_ABSTRACT
        
        for r in [
            REGEX_PREPRINTS_SITE_VIEW_PDF,
            REGEX_PREPRINTS_SITE_DOWNLOAD_PDF,
            REGEX_PREPRINTS_SITE_DOCUMENT_DOWNLOAD_PDF,
            REGEX_PREPRINTS_SITE_VERSION_DOWNLOAD_PDF
        ]:
            if re.search(r, url):
                return CONTENT_TYPE_FULL_TEXT
            
        return CONTENT_TYPE_UNDEFINED
