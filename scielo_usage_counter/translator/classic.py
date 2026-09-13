import re
from urllib.parse import parse_qsl, urlsplit

from scielo_usage_counter.values import (
    MEDIA_LANGUAGE_UNDEFINED,
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_PDF,
    MEDIA_FORMAT_XML,
    CONTENT_TYPE_FULL_TEXT,
    CONTENT_TYPE_ABSTRACT,
    CONTENT_TYPE_HOW_TO_CITE,
    CONTENT_TYPE_CITATION_EXPORT,
    CONTENT_TYPE_REFERENCES_LIST,
    CONTENT_TYPE_RELATED_DOCUMENTS,
    CONTENT_TYPE_TRANSLATE_DOCUMENT,
    CONTENT_TYPE_UNDEFINED,
)


# Patterns to support parameter extraction
REGEX_CLASSIC_SITE_SCIELO_PHP = re.compile(r'/?scielo.php', re.IGNORECASE)
REGEX_CLASSIC_SITE_ARTICLE_PLUS_PHP = re.compile(r'/?articleplus.php', re.IGNORECASE)
REGEX_CLASSIC_SITE_PDF_READCUBE_EPDF_PHP = re.compile(r'/?pdf/readcube/epdf.php', re.IGNORECASE)
REGEX_CLASSIC_SITE_SCIELO_ORG_PHP = re.compile(r'/?scieloorg/php/', re.IGNORECASE)
ARTICLE_XML_MARKER = 'articlexml'
PDF_EXTENSION = '.pdf'
PDF_PATH_MARKER = '/pdf/'


class URLTranslatorClassicSite:
    def __init__(self, sources_metadata, documents_metadata):
        self.sources_metadata = sources_metadata
        self.documents_metadata = documents_metadata

    def pipeline_translate(self, url):
        self.url_params = self.extract_url_params(url)

        pid_v2 = self.extract_pid_v2(url)
        media_format = self.extract_media_format(url)
        media_language = self.extract_media_language(pid_v2)
        scielo_issn = self.extract_issn(pid_v2)

        content_type = self.extract_content_type(url)

        return {
            'scielo_issn': scielo_issn,
            'journal_main_title': self.sources_metadata.get('issn_to_title', {}).get(scielo_issn),
            'journal_subject_area_capes': self.sources_metadata.get('issn_to_subject_area_capes', {}).get(scielo_issn),
            'journal_subject_area_wos': self.sources_metadata.get('issn_to_subject_area_wos', {}).get(scielo_issn),
            'journal_publisher_name': self.sources_metadata.get('issn_to_publisher_name', {}).get(scielo_issn),
            'journal_acronym': self.sources_metadata.get('issn_to_acronym', {}).get(scielo_issn),
            'pid_v2': pid_v2,
            'pid_v3': self.documents_metadata.get('pid_v2_to_pid_v3', {}).get(pid_v2),
            'media_format': media_format,
            'media_language': media_language,
            'content_type': content_type,
            'year_of_publication': self.documents_metadata.get('pid_v2_to_publication_year', {}).get(pid_v2),
        }

    def extract_url_params(self, url):
        url_split = urlsplit(url)
        url_qsl = parse_qsl(url_split.query)
        url_params = dict([(x[0].strip(), x[1].strip()) for x in url_qsl])

        if 'download' in url_split.query:
            url_params['download'] = 'true'

        # Perform additional processing to handle malformed URLs
        if len(url_qsl) == 1 and len(url_qsl[0]) == 2 and 'pid' in url_qsl[0]:
            url_qsl = parse_qsl('='.join(url_qsl[0]))
            url_params = dict([(x[0].strip(), x[1].strip()) for x in url_qsl])

        # Remove unnecessary spaces in the most important keys and values
        for k, v in url_params.items():
            if k in {'issn', 'script', 'pid', 'tlng', 'download'}:
                sanitized_value = v.split(' ')[0]

                # Remove the final period that occurs in some situations
                if sanitized_value.endswith('.'):
                    sanitized_value = sanitized_value[:-1]

                # Remove any character from the PID that is not S or a digit
                if k == 'pid':
                    sanitized_pid = ''
                    for c in sanitized_value:
                        if c.isdigit() or c in {'S', 's', '-', 'x', 'X'}:
                            sanitized_pid += c
                    sanitized_value = sanitized_pid

                url_params[k] = sanitized_value

        url_params = self._standardize_param_keys(url_params)

        return url_params
    
    def _standardize_param_keys(self, url_params):
        new_url_params = {}

        for k, v in url_params.items():
            if k == 'pid':
                new_url_params['pid_v2'] = v
            elif k == 'tlng':
                new_url_params['media_language'] = v
            elif k == 'issn':
                new_url_params['scielo_issn'] = v
            else:
                new_url_params[k] = v

        return new_url_params

    def extract_media_format(self, url):
        normalized_url = url.lower()
        pdf_path = normalized_url.partition(PDF_PATH_MARKER)[2]

        if normalized_url.endswith(PDF_EXTENSION) or (
            pdf_path and '/' in pdf_path
        ):
            return MEDIA_FORMAT_PDF

        if ARTICLE_XML_MARKER in normalized_url:
            return MEDIA_FORMAT_XML

        return MEDIA_FORMAT_HTML

    def extract_media_language(self, pid_v2):
        media_language = self.url_params.get('media_language')
        default_media_language = self.documents_metadata['pid_v2_to_default_lang'].get(pid_v2, MEDIA_LANGUAGE_UNDEFINED)
        
        if media_language:
            pid_v2_published_languages = self.documents_metadata['pid_v2_to_available_langs'].get(pid_v2, [])
            if media_language in pid_v2_published_languages:
                return media_language
        
        return default_media_language

    def extract_pid_v2(self, url):
        pid_v2 = self.url_params.get('pid_v2')
        if not pid_v2:
            pid_v2 = self._get_pid_from_pdf_path(url)

        return pid_v2

    def _get_pid_from_pdf_path(self, url):
        path = urlsplit(url).path
        normalized_path = path.lower()
        marker_index = normalized_path.rfind(PDF_PATH_MARKER)

        # Preserve the previous greedy match: use the last /pdf/ segment that
        # still contains both the journal directory and the file name.
        while marker_index >= 0:
            path_after_marker = normalized_path[
                marker_index + len(PDF_PATH_MARKER):
            ]
            if '/' in path_after_marker:
                break
            marker_index = normalized_path.rfind(
                PDF_PATH_MARKER,
                0,
                marker_index,
            )

        if marker_index < 0:
            return ''

        pdf_path = path[marker_index:]

        # Remove the trailing slash, if it exists
        # All dictionary keys do not contain the trailing slash
        if pdf_path.endswith('/'):
            pdf_path = pdf_path[:-1]

        # Add .pdf extension, if not present
        # All dictionary keys pdf2pid contain the pdf extension
        if not pdf_path.endswith('.pdf'):
            pdf_path += '.pdf'

        return self.documents_metadata['pdf_to_pid_v2'].get(pdf_path)
    
    def extract_issn(self, pid_v2):
        scielo_issn = self.documents_metadata['pid_v2_to_scielo_issn'].get(pid_v2)

        if not scielo_issn:
            if pid_v2 and pid_v2.startswith('S') and len(pid_v2) == 23 and '-' in pid_v2:
                scielo_issn = pid_v2[1:10]

        return scielo_issn

    def extract_content_type(self, url):
        if not hasattr(self, 'url_params'):
            self.extract_url_params(url)

        normalized_url = url.lower()
            
        if re.search(REGEX_CLASSIC_SITE_SCIELO_PHP, url):
            if 'script' in self.url_params:
                if self.url_params['script'] == 'sci_abstract':
                    return CONTENT_TYPE_ABSTRACT
                
                if self.url_params['script'] in ('sci_arttext', 'sci_arttext_plus', 'sci_pdf'):
                    return CONTENT_TYPE_FULL_TEXT
                
                if self.url_params['script'] == 'sci_isoref':
                    return CONTENT_TYPE_HOW_TO_CITE
                
            elif 'download' in self.url_params:
                return CONTENT_TYPE_CITATION_EXPORT
            
        if re.search(REGEX_CLASSIC_SITE_ARTICLE_PLUS_PHP, url):
            return CONTENT_TYPE_FULL_TEXT
        
        if normalized_url.endswith(PDF_EXTENSION):
            return CONTENT_TYPE_FULL_TEXT
        
        if re.search(REGEX_CLASSIC_SITE_PDF_READCUBE_EPDF_PHP, url):
            return CONTENT_TYPE_FULL_TEXT
        
        if re.search(REGEX_CLASSIC_SITE_SCIELO_ORG_PHP, url):
            if ARTICLE_XML_MARKER in normalized_url:
                return CONTENT_TYPE_FULL_TEXT
            
            if 'reference' in normalized_url:
                return CONTENT_TYPE_REFERENCES_LIST

            if 'related' in normalized_url:
                return CONTENT_TYPE_RELATED_DOCUMENTS
            
            if 'translate' in normalized_url:
                return CONTENT_TYPE_TRANSLATE_DOCUMENT

        return CONTENT_TYPE_UNDEFINED
