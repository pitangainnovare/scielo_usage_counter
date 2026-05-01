import re

from urllib.parse import parse_qsl, unquote, urlparse

from scielo_usage_counter.values import (
    MEDIA_LANGUAGE_UNDEFINED,
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_PDF,
    MEDIA_FORMAT_EPUB,
    CONTENT_TYPE_ABSTRACT,
    CONTENT_TYPE_FULL_TEXT,
)


IGNORED_EXACT_PATHS = {
    "",
    "/",
    "/favicon.ico",
    "/robots.txt",
}

IGNORED_PREFIXES = (
    "/.bunny-shield/",
    "/api/",
    "/search/",
    "/setlang/",
    "/static/",
    "/wp-content/",
)

# Patterns to support parameter extraction for SciELO Books
REGEX_BOOKS_SITE_PDF = re.compile(
    r"^/id/(?P<book_id>[-\w]+)/pdf/(?P<filename>[-\w]+\.pdf)",
    re.IGNORECASE,
)
REGEX_BOOKS_SITE_EPUB = re.compile(
    r"^/id/(?P<book_id>[-\w]+)/epub/(?P<filename>[-\w]+\.epub)$",
    re.IGNORECASE,
)
REGEX_BOOKS_SITE_CHAPTER_XHTML = re.compile(
    r"^/id/(?P<book_id>[-\w]+)/(?:Text|epub)/(?P<chapter_id>\d+)\.(?:xhtml|html)$",
    re.IGNORECASE,
)
REGEX_BOOKS_SITE_CHAPTER = re.compile(
    r"^/id/(?P<book_id>[-\w]+)/(?P<chapter_id>\d+)/?$",
    re.IGNORECASE,
)
REGEX_BOOKS_SITE_BOOK = re.compile(r"^/id/(?P<book_id>[-\w]+)/?$", re.IGNORECASE)


class URLTranslatorBooksSite:
    """
    Translator for SciELO Livros (Books) URLs.
    
    This class handles URL translation for the SciELO Books platform, extracting
    relevant metadata such as book IDs, chapter IDs, media formats, and content types.
    """

    def __init__(self, sources_metadata, documents_metadata):
        """
        Initialize the URLTranslatorBooksSite.
        
        :param sources_metadata: Dictionary containing sources metadata
        :param documents_metadata: Dictionary containing documents metadata
        """
        self.sources_metadata = sources_metadata or {}
        self.documents_metadata = documents_metadata or {}

    def pipeline_translate(self, url):
        """
        Execute the complete translation pipeline for a SciELO Books URL.
        
        :param url: URL string to translate
        :return: Dictionary containing extracted metadata
        """
        normalized_url = self.normalize_url(url)
        if not normalized_url:
            return {}

        self.url_params = self.extract_url_params(url)
        resource_kind = self.detect_resource_kind(normalized_url)

        book_id, chapter_id, filename = self.extract_identifiers(normalized_url)

        resolved_chapter_id = self.resolve_chapter_id(book_id, chapter_id)

        pid_generic = self.extract_pid_generic(book_id, resolved_chapter_id)
        title_pid_generic = self.extract_pid_generic(book_id, None)
        segment_pid_generics = self.extract_segment_pid_generics(
            book_id=book_id,
            chapter_id=resolved_chapter_id,
            resource_kind=resource_kind,
        )

        media_language = self.extract_media_language(pid_generic)
        media_format = self.extract_media_format(pid_generic, url, resource_kind, filename)
        content_type = self.extract_content_type(resource_kind)

        return {
            'source_type': 'book',
            'source_id': book_id,
            'document_type': 'chapter' if resolved_chapter_id else 'book',
            'isbn': self.sources_metadata.get('book_id_to_isbn', {}).get(book_id),
            'book_title': self.extract_book_title(book_id),
            'chapter_title': self.extract_chapter_title(book_id, resolved_chapter_id, pid_generic),
            'book_id': book_id,
            'chapter_id': resolved_chapter_id,
            'source_identifiers': self.sources_metadata.get('source_id_to_identifiers', {}).get(book_id),
            'source_publisher_name': self.sources_metadata.get('source_id_to_publisher_name', {}).get(book_id),
            'source_access_type': self.sources_metadata.get('source_id_to_access_type', {}).get(book_id),
            'source_city': self.sources_metadata.get('source_id_to_city', {}).get(book_id),
            'source_country': self.sources_metadata.get('source_id_to_country', {}).get(book_id),
            'title_pid_generic': title_pid_generic,
            'segment_pid_generics': segment_pid_generics,
            'pid_generic': pid_generic,
            'media_format': media_format,
            'media_language': media_language,
            'content_type': content_type,
            'access_url': normalized_url,
            'normalized_url': normalized_url,
            'year_of_publication': self.extract_year_of_publication(book_id, pid_generic),
        }

    def normalize_url(self, url):
        if not url:
            return None

        parsed_url = urlparse(str(url).strip())
        path = parsed_url.path if parsed_url.scheme or parsed_url.netloc else str(url).strip()
        path = unquote(path or "")
        path = path.split("?", 1)[0].split("#", 1)[0].split()[0]
        path = re.sub(r"/+", "/", path)
        path = path.rstrip(".,;:")

        if path in IGNORED_EXACT_PATHS:
            return None

        if any(path.startswith(prefix) for prefix in IGNORED_PREFIXES):
            return None

        if "/cover/" in path or "/swf/" in path:
            return None

        match = REGEX_BOOKS_SITE_PDF.match(path)
        if match:
            return f"/id/{match.group('book_id')}/pdf/{match.group('filename')}"

        match = REGEX_BOOKS_SITE_EPUB.match(path)
        if match:
            return f"/id/{match.group('book_id')}/epub/{match.group('filename')}"

        match = REGEX_BOOKS_SITE_CHAPTER_XHTML.match(path)
        if match:
            return f"/id/{match.group('book_id')}/epub/{match.group('chapter_id')}.html"

        match = REGEX_BOOKS_SITE_CHAPTER.match(path)
        if match:
            return f"/id/{match.group('book_id')}/{match.group('chapter_id')}"

        match = REGEX_BOOKS_SITE_BOOK.match(path)
        if match:
            return f"/id/{match.group('book_id')}"

        return path

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
        for regex, kind in (
            (REGEX_BOOKS_SITE_PDF, 'pdf'),
            (REGEX_BOOKS_SITE_EPUB, 'book_epub'),
            (REGEX_BOOKS_SITE_CHAPTER_XHTML, 'chapter_xhtml'),
            (REGEX_BOOKS_SITE_CHAPTER, 'chapter_html'),
            (REGEX_BOOKS_SITE_BOOK, 'book_html'),
        ):
            match = re.search(regex, url)
            if not match:
                continue

            book_id = match.group('book_id')
            filename = match.groupdict().get('filename')

            if kind == 'pdf':
                return book_id, self.extract_chapter_id_from_pdf_filename(filename), filename

            if kind in ('chapter_xhtml', 'chapter_html'):
                return book_id, match.group('chapter_id'), filename

            return book_id, None, filename

        return None, None, None

    def detect_resource_kind(self, url):
        for regex, kind in (
            (REGEX_BOOKS_SITE_PDF, 'pdf'),
            (REGEX_BOOKS_SITE_EPUB, 'book_epub'),
            (REGEX_BOOKS_SITE_CHAPTER_XHTML, 'chapter_xhtml'),
            (REGEX_BOOKS_SITE_CHAPTER, 'chapter_html'),
            (REGEX_BOOKS_SITE_BOOK, 'book_html'),
        ):
            if re.search(regex, url):
                return kind

        return None

    def extract_pid_generic(self, book_id, chapter_id):
        if not book_id:
            return None

        if chapter_id:
            return f"book:{book_id}/chapter:{chapter_id}"

        return f"book:{book_id}"

    def resolve_chapter_id(self, book_id, chapter_id):
        if not book_id or not chapter_id:
            return chapter_id

        order_map = self.sources_metadata.get(
            'book_id_and_order_to_chapter_pid_generic', {}
        )
        pid_generic = order_map.get(f'{book_id}:{chapter_id}')
        if not pid_generic:
            return chapter_id

        if '/chapter:' in (pid_generic or ''):
            return pid_generic.split('/chapter:')[-1]

        return chapter_id

    def extract_media_format(self, pid_generic, url, resource_kind=None, filename=None):
        if self.url_params.get('media_format'):
            return self.url_params['media_format']

        if resource_kind == 'pdf' or (filename and filename.endswith('.pdf')):
            return MEDIA_FORMAT_PDF

        if resource_kind == 'book_epub':
            return MEDIA_FORMAT_EPUB

        if filename and filename.endswith('.pdf'):
            return MEDIA_FORMAT_PDF

        if pid_generic:
            default_format = self.documents_metadata.get('pid_generic_to_default_format', {}).get(pid_generic)
            if default_format:
                return default_format

            default_format = self.sources_metadata.get('pid_generic_to_default_format', {}).get(pid_generic)
            if default_format:
                return default_format

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

        if pid_generic:
            media_language = self.documents_metadata.get('pid_generic_to_default_lang', {}).get(pid_generic)
            if media_language:
                return media_language

            media_language = self.sources_metadata.get('pid_generic_to_default_lang', {}).get(pid_generic)
            if media_language:
                return media_language

        return MEDIA_LANGUAGE_UNDEFINED

    def extract_content_type(self, resource_kind):
        """
        Determine content type from URL and identifiers.
        
        :param resource_kind: Kind of books resource identified from the URL
        :return: Content type string
        """
        if resource_kind in (
            'pdf',
            'book_epub',
            'chapter_xhtml',
            'chapter_html',
        ):
            return CONTENT_TYPE_FULL_TEXT

        return CONTENT_TYPE_ABSTRACT

    def extract_segment_pid_generics(self, book_id, chapter_id, resource_kind):
        if not book_id or chapter_id or resource_kind not in ('pdf', 'book_epub'):
            return None

        book_pid_generic = self.extract_pid_generic(book_id, None)
        candidates = (
            self.documents_metadata.get('book_pid_generic_to_chapter_pid_generics', {}).get(
                book_pid_generic
            )
            or self.sources_metadata.get('book_id_to_chapter_pid_generics', {}).get(book_id)
            or []
        )
        if not candidates:
            return None

        return sorted(set(candidates), key=self._sort_pid_generic_by_chapter)

    def extract_chapter_id_from_pdf_filename(self, filename):
        if not filename:
            return None

        chapter_match = re.search(r'-(\d{10,13})-(\d+)\.pdf$', filename)
        if chapter_match:
            return chapter_match.group(2)

        chapter_match = re.match(r'(?P<chapter_id>\d+)\.pdf$', filename)
        if chapter_match:
            return chapter_match.group('chapter_id')

        return None

    def extract_book_title(self, book_id):
        if not book_id:
            return None

        return (
            self.sources_metadata.get('book_id_to_title', {}).get(book_id)
            or self.documents_metadata.get('pid_generic_to_title', {}).get(
                self.extract_pid_generic(book_id, None)
            )
        )

    def extract_chapter_title(self, book_id, chapter_id, pid_generic):
        if not chapter_id:
            return None

        chapter_key = None
        if book_id:
            chapter_key = f'{book_id}:{chapter_id}'

        return (
            self.documents_metadata.get('pid_generic_to_title', {}).get(pid_generic)
            or self.sources_metadata.get('chapter_key_to_title', {}).get(chapter_key)
            or self.sources_metadata.get('chapter_id_to_title', {}).get(chapter_id)
        )

    def extract_year_of_publication(self, book_id, pid_generic):
        if book_id:
            year = self.sources_metadata.get('book_id_to_year_of_publication', {}).get(book_id)
            if year:
                return year

        if pid_generic:
            return self.documents_metadata.get('pid_generic_to_publication_date', {}).get(pid_generic)

        return None

    @staticmethod
    def _sort_pid_generic_by_chapter(pid_generic):
        match = re.search(r'/chapter:(\d+)$', pid_generic or '', re.IGNORECASE)
        if not match:
            return (1, pid_generic or '')

        chapter_id = match.group(1)
        try:
            return (0, int(chapter_id))
        except ValueError:
            return (0, chapter_id)
