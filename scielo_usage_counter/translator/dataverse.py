import re

from urllib.parse import parse_qsl, urlsplit

from scielo_usage_counter.values import (
    MEDIA_LANGUAGE_UNDEFINED,
    CONTENT_TYPE_FULL_TEXT,
    CONTENT_TYPE_ABSTRACT,
    CONTENT_TYPE_UNDEFINED,
    CONTENT_TYPE_CITATION_EXPORT,
    DEFAULT_SCIELO_ISSN,
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_DATAVERSE,
    MEDIA_FORMAT_UNDEFINED,
)


# Patterns to support parameter extraction
REGEX_DATAVERSE_SITE_API_ACCESS_DATAFILE = re.compile(r'.*/api/access/datafile/(?P<id>\d+)', re.IGNORECASE)
REGEX_DATAVERSE_SITE_API_DATASETS_EXPORT = re.compile(r'.*/api/datasets/export', re.IGNORECASE)
REGEX_DATAVERSE_SITE_API_DATASETS = re.compile(r'.*/api/datasets/(?P<id>\d)?', re.IGNORECASE)
REGEX_DATAVERSE_SITE_DATASET = re.compile(r'.*/dataset.xhtml', re.IGNORECASE)
REGEX_DATAVERSE_SITE_FILE = re.compile(r'.*/file.xhtml', re.IGNORECASE)
REGEX_DATAVERSE_PID_GENERIC_AND_SUBPID = re.compile(r"(?P<pid_generic>doi:\d+\.\d+/\w+\.[^/]+)/(?P<file_id>[^/]+)", re.IGNORECASE)
REGEX_DATAVERSE_PID_GENERIC_ONLY = re.compile(r"(?P<pid_generic>doi:\d+\.\d+/\w+\.[^/]+)", re.IGNORECASE)


class URLTranslatorDataverseSite:
    def __init__(self, sources_metadata, documents_metadata):
        self.sources_metadata = sources_metadata
        self.documents_metadata = documents_metadata

    def pipeline_translate(self, url):
        self.url_params = self.extract_url_params(url)
        
        pid_generic, file_id = self.extract_identifiers(url)
        content_type = self.extract_content_type(url)
        media_format = self.extract_media_format(url)
        
        scielo_issn = self.extract_issn(pid_generic)

        return {
            'scielo_issn': scielo_issn,
            'journal_main_title': self.sources_metadata.get('issn_to_title', {}).get(scielo_issn),
            'journal_subject_area_capes': self.sources_metadata.get('issn_to_subject_area_capes', {}).get(scielo_issn),
            'journal_subject_area_wos': self.sources_metadata.get('issn_to_subject_area_wos', {}).get(scielo_issn),
            'journal_publisher_name': self.sources_metadata.get('issn_to_publisher_name', {}).get(scielo_issn),
            'journal_acronym': self.sources_metadata.get('issn_to_acronym', {}).get(scielo_issn),
            'pid_v2': None,
            'pid_v3': None,
            'pid_generic': pid_generic,
            'file_id': file_id,
            'content_type': content_type,
            'media_format': media_format,
            'media_language': MEDIA_LANGUAGE_UNDEFINED,
            'year_of_publication': self.documents_metadata.get('pid_generic_to_publication_date', {}).get(pid_generic),
        }

    def extract_media_format(self, url):
        for p in [
            REGEX_DATAVERSE_SITE_API_ACCESS_DATAFILE,
            REGEX_DATAVERSE_SITE_FILE,
        ]:
            if re.search(p, url):
                return MEDIA_FORMAT_DATAVERSE

        for p in [
            REGEX_DATAVERSE_SITE_API_DATASETS_EXPORT,
            REGEX_DATAVERSE_SITE_API_DATASETS,
            REGEX_DATAVERSE_SITE_DATASET,
        ]:
            if re.search(p, url):
                return MEDIA_FORMAT_HTML

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

    def extract_identifiers(self, url):
        if not hasattr(self, 'url_params'):
            self.url_params = self.extract_url_params(url)

        if 'persistentId' in self.url_params:
            return self.extract_pid_generic(self.url_params['persistentId']), None

        match = re.search(REGEX_DATAVERSE_SITE_API_ACCESS_DATAFILE, url)
        if match:
            file_id = match.groupdict().get('id')
            return self.documents_metadata['file_id_to_pid_generic'].get(file_id), file_id
        
        return None, None

    def extract_pid_generic(self, persistent_id):
        match = re.search(REGEX_DATAVERSE_PID_GENERIC_AND_SUBPID, persistent_id)
        if match:
            return match.groupdict().get('pid_generic')
        
        match_generic = re.search(REGEX_DATAVERSE_PID_GENERIC_ONLY, persistent_id)
        if match_generic:
            return match_generic.groupdict().get('pid_generic')
        
        return None
        
    def extract_url_params(self, url):
        url_split = urlsplit(url)
        url_qsl = parse_qsl(url_split.query)
        return dict([(x[0].strip(), x[1].strip()) for x in url_qsl])

    def extract_issn(self, pid_generic):
        return DEFAULT_SCIELO_ISSN
