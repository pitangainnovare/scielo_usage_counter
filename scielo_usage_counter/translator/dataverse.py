import re

from urllib.parse import parse_qsl, urlsplit

from scielo_usage_counter.values import (
    MEDIA_FORMAT_UNDEFINED,
    MEDIA_LANGUAGE_UNDEFINED,
    CONTENT_TYPE_FULL_TEXT,
    CONTENT_TYPE_ABSTRACT,
    CONTENT_TYPE_UNDEFINED,
    CONTENT_TYPE_CITATION_EXPORT,
)


# Patterns to support parameter extraction
REGEX_DATAVERSE_SITE_API_ACCESS_DATAFILE = re.compile(r'.*/api/access/datafile/(?P<id>\d+)', re.IGNORECASE)
REGEX_DATAVERSE_SITE_API_DATASETS_EXPORT = re.compile(r'.*/api/datasets/export', re.IGNORECASE)
REGEX_DATAVERSE_SITE_API_DATASETS = re.compile(r'.*/api/datasets/(?P<id>\d)?', re.IGNORECASE)
REGEX_DATAVERSE_SITE_DATASET = re.compile(r'.*/dataset.xhtml', re.IGNORECASE)
REGEX_DATAVERSE_SITE_FILE = re.compile(r'.*/file.xhtml', re.IGNORECASE)


class URLTranslatorDataverseSite:
    def __init__(self, journals_metadata, articles_metadata):
        self.journals_metadata = journals_metadata
        self.articles_metadata = articles_metadata

    def pipeline_translate(self, url):
        self.url_params = self.extract_url_params(url)
        
        identifier = self.extract_identifier(url)
        content_type = self.extract_content_type(url)
        media_format = self.extract_media_format(url)
        
        return {
            'scielo_issn': None,
            'pid_v2': None,
            'pid_v3': None,
            'id': identifier,
            'content_type': content_type,
            'media_format': media_format,
            'media_language': MEDIA_LANGUAGE_UNDEFINED,
        }

    def extract_media_format(self, url):
        # Dataverse URLs do not have a media_format parameter
        if not hasattr(self, 'url_params'):
            self.url_params = self.extract_url_params(url)

        # TODO: We should identify the media_format using external metadata
        return MEDIA_FORMAT_UNDEFINED

    def extract_media_language(self, url):
        if not hasattr(self, 'url_params'):
            self.url_params = self.extract_url_params(url)

        # Dataverse URLs do not have a media_language parameter
        # TODO: We should identify the media_language using external metadata        
        return MEDIA_LANGUAGE_UNDEFINED

    def extract_content_type(self, url):
        for p in [
            REGEX_DATAVERSE_SITE_API_DATASETS,
            REGEX_DATAVERSE_SITE_DATASET,
        ]:
            if re.search(p, url):
                return CONTENT_TYPE_ABSTRACT

        for p in [
            REGEX_DATAVERSE_SITE_FILE,
            REGEX_DATAVERSE_SITE_API_ACCESS_DATAFILE
        ]:
            if re.search(p, url):
                return CONTENT_TYPE_FULL_TEXT        

        if re.search(REGEX_DATAVERSE_SITE_API_DATASETS_EXPORT, url):
            return CONTENT_TYPE_CITATION_EXPORT
             
        return CONTENT_TYPE_UNDEFINED

    def extract_identifier(self, url):
        if not hasattr(self, 'url_params'):
            self.url_params = self.extract_url_params(url)

        if 'persistentId' in self.url_params:
            return self.url_params['persistentId']
        
        # If there is no persistentId,
        #   we should extract the identifier from the url
        # If the URL is similar to /api/access/datafile/12530,
        #   we should extract the persistentId from external metadata using the id

        match = re.search(REGEX_DATAVERSE_SITE_API_ACCESS_DATAFILE, url)
        if match:
            return match.groupdict().get('id')

    def extract_url_params(self, url):
        url_split = urlsplit(url)
        url_qsl = parse_qsl(url_split.query)
        return dict([(x[0].strip(), x[1].strip()) for x in url_qsl])
