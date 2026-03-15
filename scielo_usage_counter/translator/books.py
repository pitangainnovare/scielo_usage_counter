import re

from urllib.parse import urlparse, parse_qsl

from scielo_usage_counter.values import (
    MEDIA_LANGUAGE_UNDEFINED,
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_PDF,
    MEDIA_FORMAT_XML,
    MEDIA_FORMAT_UNDEFINED,
    CONTENT_TYPE_ABSTRACT,
    CONTENT_TYPE_FULL_TEXT,
    CONTENT_TYPE_UNDEFINED,
    DEFAULT_SCIELO_ISSN,
)


# Patterns to support parameter extraction for SciELO Books
# Pattern for PDF files: /id/{book_id}/pdf/{filename}.pdf
REGEX_BOOKS_SITE_PDF = re.compile(r'/id/(?P<book_id>\w+)/pdf/(?P<filename>[\w\-]+\.pdf)', re.IGNORECASE)
# Pattern for chapter pages: /id/{book_id}/{chapter_number}
REGEX_BOOKS_SITE_CHAPTER = re.compile(r'/id/(?P<book_id>\w+)/(?P<chapter_id>\d+)(?:[?#]|$)', re.IGNORECASE)
# Pattern for book landing pages: /id/{book_id}
REGEX_BOOKS_SITE_BOOK = re.compile(r'/id/(?P<book_id>\w+)(?:[?#]|$)', re.IGNORECASE)


class URLTranslatorBooksSite:
    """
    Translator for SciELO Livros (Books) URLs.
    
    This class handles URL translation for the SciELO Books platform, extracting
    relevant metadata such as book IDs, chapter IDs, media formats, and content types.
    """
    
    def __init__(self, journals_metadata, articles_metadata):
        """
        Initialize the URLTranslatorBooksSite.
        
        :param journals_metadata: Dictionary containing journal metadata
        :param articles_metadata: Dictionary containing article/book metadata
        """
        self.journals_metadata = journals_metadata
        self.articles_metadata = articles_metadata

    def pipeline_translate(self, url):
        """
        Execute the complete translation pipeline for a SciELO Books URL.
        
        :param url: URL string to translate
        :return: Dictionary containing extracted metadata
        """
        self.url_params = self.extract_url_params(url)
        
        book_id, chapter_id, filename = self.extract_identifiers(url)
        pid_generic = self._build_pid_generic(book_id, chapter_id)
        
        media_format = self.extract_media_format(url, filename)
        media_language = self.extract_media_language(pid_generic)
        content_type = self.extract_content_type(url, chapter_id, filename)
        scielo_issn = self.extract_issn(book_id)

        return {
            'scielo_issn': scielo_issn,
            'journal_main_title': self.journals_metadata.get('issn_to_title', {}).get(scielo_issn),
            'journal_subject_area_capes': self.journals_metadata.get('issn_to_subject_area_capes', {}).get(scielo_issn),
            'journal_subject_area_wos': self.journals_metadata.get('issn_to_subject_area_wos', {}).get(scielo_issn),
            'journal_publisher_name': self.journals_metadata.get('issn_to_publisher_name', {}).get(scielo_issn),
            'journal_acronym': self.journals_metadata.get('issn_to_acronym', {}).get(scielo_issn),
            'pid_v2': None,
            'pid_v3': None,
            'pid_generic': pid_generic,
            'book_id': book_id,
            'chapter_id': chapter_id,
            'media_format': media_format,
            'media_language': media_language,
            'content_type': content_type,
            'year_of_publication': self.articles_metadata.get('pid_generic_to_publication_date', {}).get(pid_generic),
        }

    def extract_url_params(self, url):
        """
        Extract query parameters from URL.
        
        :param url: URL string
        :return: Dictionary of URL parameters
        """
        url_params = {
            'book_id': '',
            'chapter_id': '',
            'media_format': '',
            'media_language': '',
        }

        url_parsed = urlparse(url)
        params = dict(parse_qsl(url_parsed.query))
        
        for k, v in params.items():
            if k == 'lang':
                url_params['media_language'] = v
            elif k == 'format':
                url_params['media_format'] = v
            else:
                url_params[k] = v

        return url_params

    def extract_identifiers(self, url):
        """
        Extract book ID and chapter ID from URL.
        
        Supports SciELO Books URL patterns:
        - /id/{book_id}/pdf/{filename}.pdf - PDF download
        - /id/{book_id}/{chapter_number} - Chapter page
        - /id/{book_id} - Book landing page
        
        :param url: URL string
        :return: Tuple of (book_id, chapter_id, filename)
        """
        # Try to match PDF pattern first (most specific)
        match = re.search(REGEX_BOOKS_SITE_PDF, url)
        if match:
            book_id = match.group('book_id')
            filename = match.group('filename')
            # Extract chapter number from filename if present
            # Pattern: author-ISBN-CHAPTER.pdf where ISBN is 10 or 13 digits
            # Examples: magalhaes-9788578791889-18.pdf (chapter 18), sadek-9788579820342.pdf (no chapter)
            chapter_match = re.search(r'-(\d{10,13})-(\d+)\.pdf$', filename)
            chapter_id = chapter_match.group(2) if chapter_match else None
            return book_id, chapter_id, filename
        
        # Try to match chapter pattern
        match = re.search(REGEX_BOOKS_SITE_CHAPTER, url)
        if match:
            return match.group('book_id'), match.group('chapter_id'), None
        
        # Try to match book landing page pattern
        match = re.search(REGEX_BOOKS_SITE_BOOK, url)
        if match:
            return match.group('book_id'), None, None
        
        return None, None, None

    def _build_pid_generic(self, book_id, chapter_id):
        """
        Build a generic PID from book and chapter IDs.
        
        :param book_id: Book identifier
        :param chapter_id: Chapter identifier (optional)
        :return: Generic PID string or None
        """
        if not book_id:
            return None
        
        if chapter_id:
            return f"book:{book_id}/chapter:{chapter_id}"
        
        return f"book:{book_id}"

    def extract_media_format(self, url, filename=None):
        """
        Determine the media format from URL.
        
        :param url: URL string
        :param filename: Optional filename from URL
        :return: Media format string (html, pdf, xml, etc.)
        """
        # Check for explicit format in query params
        if self.url_params.get('media_format'):
            return self.url_params['media_format']
        
        # Check if it's a PDF file
        if filename and filename.endswith('.pdf'):
            return MEDIA_FORMAT_PDF
        
        # Check URL patterns for PDF
        if re.search(REGEX_BOOKS_SITE_PDF, url):
            return MEDIA_FORMAT_PDF
        
        # Default to HTML for book/chapter landing pages
        return MEDIA_FORMAT_HTML

    def extract_media_language(self, pid_generic):
        """
        Extract media language from metadata or URL parameters.
        
        :param pid_generic: Generic PID
        :return: Language code string
        """
        media_language = self.url_params.get('media_language')
        if media_language:
            return media_language
        
        # Try to get from metadata if available
        # Note: Using pid_v2_to_default_lang as a fallback for compatibility,
        # though books use pid_generic format. This allows for potential
        # future metadata storage if book language metadata becomes available.
        if pid_generic:
            stored_lang = self.articles_metadata.get('pid_v2_to_default_lang', {}).get(pid_generic)
            if stored_lang:
                return stored_lang
        
        return MEDIA_LANGUAGE_UNDEFINED

    def extract_content_type(self, url, chapter_id, filename=None):
        """
        Determine content type from URL and identifiers.
        
        :param url: URL string
        :param chapter_id: Chapter identifier (optional)
        :param filename: Optional filename from URL
        :return: Content type string
        """
        # Get media_format if not already extracted
        if not hasattr(self, 'url_params'):
            self.url_params = self.extract_url_params(url)
        
        # PDF files are full text
        if filename and filename.endswith('.pdf'):
            return CONTENT_TYPE_FULL_TEXT
        
        # Check URL patterns for PDF
        if re.search(REGEX_BOOKS_SITE_PDF, url):
            return CONTENT_TYPE_FULL_TEXT
        
        # Chapter pages are considered full text
        if chapter_id:
            return CONTENT_TYPE_FULL_TEXT
        
        # Book landing pages without chapter are abstracts
        return CONTENT_TYPE_ABSTRACT

    def extract_issn(self, book_id):
        """
        Extract ISSN for a book. Books may not have ISSNs like journals.
        
        :param book_id: Book identifier
        :return: ISSN string (defaults to DEFAULT_SCIELO_ISSN)
        """
        # Books typically don't have ISSNs (journals do)
        # Using default ISSN for books platform
        return DEFAULT_SCIELO_ISSN
