import unittest

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.translator.books import URLTranslatorBooksSite

from scielo_usage_counter.values import (
    CONTENT_TYPE_FULL_TEXT,
    CONTENT_TYPE_ABSTRACT,
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_PDF,
    MEDIA_FORMAT_EPUB,
)

BOOKS_LOG_EXPECTED = [
    {'book_id': 'xjcw9', 'chapter_id': None, 'pid_generic': 'BOOK:XJCW9', 'media_format': MEDIA_FORMAT_HTML, 'content_type': CONTENT_TYPE_ABSTRACT},
    {'book_id': 'h8pyf', 'chapter_id': '08', 'pid_generic': 'BOOK:H8PYF/CHAPTER:08', 'media_format': MEDIA_FORMAT_HTML, 'content_type': CONTENT_TYPE_FULL_TEXT},
    {'book_id': '3hs', 'chapter_id': None, 'pid_generic': 'BOOK:3HS', 'media_format': MEDIA_FORMAT_PDF, 'content_type': CONTENT_TYPE_FULL_TEXT},
    {'book_id': 'hd5d8', 'chapter_id': None, 'pid_generic': 'BOOK:HD5D8', 'media_format': MEDIA_FORMAT_EPUB, 'content_type': CONTENT_TYPE_FULL_TEXT},
    {'book_id': '96spq', 'chapter_id': None, 'pid_generic': 'BOOK:96SPQ', 'media_format': MEDIA_FORMAT_HTML, 'content_type': CONTENT_TYPE_ABSTRACT},
    {'book_id': '3dqnm', 'chapter_id': '10', 'pid_generic': 'BOOK:3DQNM/CHAPTER:10', 'media_format': MEDIA_FORMAT_HTML, 'content_type': CONTENT_TYPE_FULL_TEXT},
    {'book_id': 'htnbt', 'chapter_id': '10', 'pid_generic': 'BOOK:HTNBT/CHAPTER:10', 'media_format': MEDIA_FORMAT_PDF, 'content_type': CONTENT_TYPE_FULL_TEXT},
    {'book_id': 'wg88m', 'chapter_id': None, 'pid_generic': 'BOOK:WG88M', 'media_format': MEDIA_FORMAT_EPUB, 'content_type': CONTENT_TYPE_FULL_TEXT},
    {'book_id': 'p8kpd', 'chapter_id': '12', 'pid_generic': 'BOOK:P8KPD/CHAPTER:12', 'media_format': MEDIA_FORMAT_HTML, 'content_type': CONTENT_TYPE_FULL_TEXT},
]


class TestTranslatorBooks(unittest.TestCase):
    """
    Test suite for the SciELO Books URL translator.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        self.sources_metadata = []
        self.documents_metadata = []
        self.tm = URLTranslationManager(self.sources_metadata, self.documents_metadata)

    def test_translate_book_id_extraction(self):
        """Test that book IDs are correctly extracted from actual SciELO Books URL formats."""
        urls_with_expected_ids = [
            ("https://books.scielo.org/id/q7gtd", "q7gtd"),
            ("https://books.scielo.org/id/4ndgv", "4ndgv"),
            ("/id/gbvb4", "gbvb4"),
            ("/id/y742k", "y742k"),
        ]
        
        for url, expected_book_id in urls_with_expected_ids:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorBooksSite)
                self.assertEqual(result['book_id'], expected_book_id)

    def test_translate_chapter_id_extraction(self):
        """Test that chapter IDs are correctly extracted from URLs."""
        urls_with_expected_ids = [
            ("https://books.scielo.org/id/vdywc/03", "vdywc", "03"),
            ("https://books.scielo.org/id/mj4jm/11", "mj4jm", "11"),
            ("/id/abc123/05", "abc123", "05"),
        ]
        
        for url, expected_book_id, expected_chapter_id in urls_with_expected_ids:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorBooksSite)
                self.assertEqual(result['book_id'], expected_book_id)
                self.assertEqual(result['chapter_id'], expected_chapter_id)

    def test_translate_pid_generic_generation(self):
        """Test that generic PIDs are correctly generated."""
        test_cases = [
            ("https://books.scielo.org/id/q7gtd", "BOOK:Q7GTD"),
            ("https://books.scielo.org/id/vdywc/03", "BOOK:VDYWC/CHAPTER:03"),
            ("/id/gbvb4", "BOOK:GBVB4"),
            ("/id/mj4jm/11", "BOOK:MJ4JM/CHAPTER:11"),
        ]
        
        for url, expected_pid in test_cases:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertEqual(result['pid_generic'], expected_pid)

    def test_translate_content_type_is_abstract(self):
        """Test that book landing pages are classified as abstract."""
        urls = [
            "https://books.scielo.org/id/q7gtd",
            "https://books.scielo.org/id/4ndgv",
            "/id/gbvb4",
            "/id/y742k",
        ]
        
        for url in urls:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorBooksSite)
                self.assertEqual(result['content_type'], CONTENT_TYPE_ABSTRACT)

    def test_translate_content_type_is_full_text(self):
        """Test that PDF/chapter pages are classified as full text."""
        urls = [
            "https://books.scielo.org/id/y742k/pdf/magalhaes-9788578791889-18.pdf",
            "https://books.scielo.org/id/4ndgv/pdf/paim-9788575413593-05.pdf",
            "https://books.scielo.org/id/vdywc/03",
            "https://books.scielo.org/id/mj4jm/11",
            "/id/82r9t/pdf/sadek-9788579820342.pdf",
            "/id/abc123/05",
        ]
        
        for url in urls:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorBooksSite)
                self.assertEqual(result['content_type'], CONTENT_TYPE_FULL_TEXT)

    def test_translate_media_format_html(self):
        """Test that HTML format is correctly identified."""
        urls = [
            "https://books.scielo.org/id/q7gtd",
            "https://books.scielo.org/id/4ndgv",
            "https://books.scielo.org/id/vdywc/03",
            "https://books.scielo.org/id/mj4jm/11",
            "/id/gbvb4",
        ]
        
        for url in urls:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorBooksSite)
                self.assertEqual(result['media_format'], MEDIA_FORMAT_HTML)

    def test_translate_media_format_pdf(self):
        """Test that PDF format is correctly identified."""
        urls = [
            "https://books.scielo.org/id/y742k/pdf/magalhaes-9788578791889-18.pdf",
            "https://books.scielo.org/id/4ndgv/pdf/paim-9788575413593-05.pdf",
            "/id/82r9t/pdf/sadek-9788579820342.pdf",
            "/id/5v9s3/pdf/rivera-9788575413036.pdf",
        ]
        
        for url in urls:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorBooksSite)
                self.assertEqual(result['media_format'], MEDIA_FORMAT_PDF)

    def test_translate_media_format_epub(self):
        urls = [
            "https://books.scielo.org/id/k3w36/epub/daza-9789978105689.epub",
            "/id/wg88m/epub/ortigoza-9788579831287.epub",
        ]

        for url in urls:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorBooksSite)
                self.assertEqual(result['media_format'], MEDIA_FORMAT_EPUB)
                self.assertEqual(result['content_type'], CONTENT_TYPE_FULL_TEXT)

    def test_translate_ignores_swf_assets(self):
        result = self.tm.translate("/id/xstc2/swf/18.swf")
        self.assertEqual(result, {})

    def test_translate_ignores_cover_assets(self):
        result = self.tm.translate("/id/c2248/cover/cover_thumbnail.jpeg")
        self.assertEqual(result, {})

    def test_translate_normalizes_pdf_variants(self):
        test_cases = [
            "https://books.scielo.org/id/c2248/pdf/freitas-9788599662830.pdf?utm_source=chatgpt.com",
            "/id/c2248/pdf/freitas-9788599662830.pdf%3E.%20Acesso:%20jan.%202018.",
        ]

        for url in test_cases:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertEqual(result["book_id"], "c2248")
                self.assertEqual(result["pid_generic"], "BOOK:C2248")
                self.assertEqual(result["media_format"], MEDIA_FORMAT_PDF)
                self.assertEqual(result["content_type"], CONTENT_TYPE_FULL_TEXT)

    def test_translate_with_query_params(self):
        """Test URL translation with query parameters."""
        url = "https://books.scielo.org/id/q7gtd?lang=en&format=html"
        result = self.tm.translate(url)
        
        self.assertIsInstance(self.tm.translator, URLTranslatorBooksSite)
        self.assertEqual(result['book_id'], 'q7gtd')
        self.assertEqual(result['media_language'], 'en')

    def test_translate_uses_source_and_document_metadata_contract(self):
        sources_metadata = [
            {
                'source_type': 'book',
                'source_id': 'q7gtd',
                'title': 'Book Title',
                'access_type': 'open_access',
                'publication_year': '2023',
                'identifiers': {'book_id': 'q7gtd', 'isbn': '9788578791889'},
                'publisher_name': ['SciELO Books'],
                'extra_data': {'city': 'Rio de Janeiro', 'country': 'BR'},
            }
        ]
        documents_metadata = [
            {
                'document_type': 'book',
                'document_id': 'book:q7gtd',
                'pid_generic': 'book:q7gtd',
                'default_lang': 'pt',
                'publication_date': '2023-01-01',
                'publication_year': '2023',
                'source_type': 'book',
                'source_id': 'q7gtd',
                'title': 'Book Title',
                'identifiers': {'book_id': 'q7gtd', 'isbn': '9788578791889'},
                'files': {},
            },
            {
                'document_type': 'chapter',
                'document_id': 'book:q7gtd/chapter:03',
                'pid_generic': 'book:q7gtd/chapter:03',
                'default_lang': 'en',
                'publication_date': '2023-01-01',
                'publication_year': '2023',
                'source_type': 'book',
                'source_id': 'q7gtd',
                'title': 'Chapter Title',
                'identifiers': {'book_id': 'q7gtd', 'chapter_id': '03'},
                'files': {},
            },
        ]
        tm = URLTranslationManager(sources_metadata, documents_metadata)

        result = tm.translate("https://books.scielo.org/id/q7gtd/03")

        self.assertEqual(result['book_title'], 'Book Title')
        self.assertEqual(result['chapter_title'], 'Chapter Title')
        self.assertEqual(result['isbn'], '9788578791889')
        self.assertEqual(result['year_of_publication'], '2023')
        self.assertEqual(result['media_language'], 'en')
        self.assertEqual(result['source_type'], 'book')
        self.assertEqual(result['source_id'], 'q7gtd')
        self.assertEqual(result['document_type'], 'chapter')
        self.assertEqual(result['source_access_type'], 'open_access')
        self.assertEqual(result['source_publisher_name'], ['SciELO Books'])
        self.assertEqual(result['source_city'], 'Rio de Janeiro')
        self.assertEqual(result['source_country'], 'BR')

    def test_translate_whole_book_pdf_exposes_c2248_segments(self):
        sources_metadata = [
            {
                'source_type': 'book',
                'source_id': 'c2248',
                'title': 'Freitas Book',
                'publication_year': '2018',
                'identifiers': {'book_id': 'c2248', 'isbn': '9788599662830'},
            }
        ]
        documents_metadata = [
            {
                'document_type': 'book',
                'document_id': 'book:c2248',
                'pid_generic': 'book:c2248',
                'default_lang': 'pt',
                'publication_date': '2018-01-01',
                'publication_year': '2018',
                'source_type': 'book',
                'source_id': 'c2248',
                'title': 'Freitas Book',
                'identifiers': {'book_id': 'c2248', 'isbn': '9788599662830'},
                'files': {},
            },
            {
                'document_type': 'chapter',
                'document_id': 'book:c2248/chapter:00',
                'pid_generic': 'book:c2248/chapter:00',
                'default_lang': 'pt',
                'publication_date': '2018-01-01',
                'publication_year': '2018',
                'source_type': 'book',
                'source_id': 'c2248',
                'title': 'Introducao',
                'identifiers': {'book_id': 'c2248', 'chapter_id': '00'},
                'files': {},
            },
            {
                'document_type': 'chapter',
                'document_id': 'book:c2248/chapter:03',
                'pid_generic': 'book:c2248/chapter:03',
                'default_lang': 'pt',
                'publication_date': '2018-01-01',
                'publication_year': '2018',
                'source_type': 'book',
                'source_id': 'c2248',
                'title': 'Capitulo 03',
                'identifiers': {'book_id': 'c2248', 'chapter_id': '03'},
                'files': {},
            },
            {
                'document_type': 'chapter',
                'document_id': 'book:c2248/chapter:10',
                'pid_generic': 'book:c2248/chapter:10',
                'default_lang': 'pt',
                'publication_date': '2018-01-01',
                'publication_year': '2018',
                'source_type': 'book',
                'source_id': 'c2248',
                'title': 'Capitulo 10',
                'identifiers': {'book_id': 'c2248', 'chapter_id': '10'},
                'files': {},
            },
        ]
        tm = URLTranslationManager(sources_metadata, documents_metadata)

        result = tm.translate(
            "https://books.scielo.org/id/c2248/pdf/freitas-9788599662830.pdf"
        )

        self.assertEqual(result['pid_generic'], 'BOOK:C2248')
        self.assertEqual(result['title_pid_generic'], 'BOOK:C2248')
        self.assertEqual(
            result['segment_pid_generics'],
            [
                'BOOK:C2248/CHAPTER:00',
                'BOOK:C2248/CHAPTER:03',
                'BOOK:C2248/CHAPTER:10',
            ],
        )
        self.assertEqual(result['media_format'], MEDIA_FORMAT_PDF)
        self.assertEqual(result['content_type'], CONTENT_TYPE_FULL_TEXT)
        self.assertEqual(
            result['access_url'],
            '/id/c2248/pdf/freitas-9788599662830.pdf',
        )
        self.assertEqual(
            result['normalized_url'],
            '/id/c2248/pdf/freitas-9788599662830.pdf',
        )

    def test_translate_whole_book_epub_exposes_segments(self):
        sources_metadata = [
            {
                'source_type': 'book',
                'source_id': 'k3w36',
                'title': 'Daza Book',
                'publication_year': '2022',
                'identifiers': {'book_id': 'k3w36', 'isbn': '9789978105689'},
            }
        ]
        documents_metadata = [
            {
                'document_type': 'book',
                'document_id': 'book:k3w36',
                'pid_generic': 'book:k3w36',
                'default_lang': 'es',
                'publication_date': '2022-01-01',
                'publication_year': '2022',
                'source_type': 'book',
                'source_id': 'k3w36',
                'title': 'Daza Book',
                'identifiers': {'book_id': 'k3w36', 'isbn': '9789978105689'},
                'files': {},
            },
            {
                'document_type': 'chapter',
                'document_id': 'book:k3w36/chapter:01',
                'pid_generic': 'book:k3w36/chapter:01',
                'default_lang': 'es',
                'publication_date': '2022-01-01',
                'publication_year': '2022',
                'source_type': 'book',
                'source_id': 'k3w36',
                'title': 'Capitulo 01',
                'identifiers': {'book_id': 'k3w36', 'chapter_id': '01'},
                'files': {},
            },
            {
                'document_type': 'chapter',
                'document_id': 'book:k3w36/chapter:02',
                'pid_generic': 'book:k3w36/chapter:02',
                'default_lang': 'es',
                'publication_date': '2022-01-01',
                'publication_year': '2022',
                'source_type': 'book',
                'source_id': 'k3w36',
                'title': 'Capitulo 02',
                'identifiers': {'book_id': 'k3w36', 'chapter_id': '02'},
                'files': {},
            },
        ]
        tm = URLTranslationManager(sources_metadata, documents_metadata)

        result = tm.translate("/id/k3w36/epub/daza-9789978105689.epub")

        self.assertEqual(result['pid_generic'], 'BOOK:K3W36')
        self.assertEqual(result['title_pid_generic'], 'BOOK:K3W36')
        self.assertEqual(
            result['segment_pid_generics'],
            ['BOOK:K3W36/CHAPTER:01', 'BOOK:K3W36/CHAPTER:02'],
        )
        self.assertEqual(result['media_format'], MEDIA_FORMAT_EPUB)
        self.assertEqual(result['content_type'], CONTENT_TYPE_FULL_TEXT)
        self.assertEqual(
            result['access_url'],
            '/id/k3w36/epub/daza-9789978105689.epub',
        )

    def test_translate_chapter_xhtml_variants_are_full_text(self):
        test_cases = [
            ("https://books.scielo.org/id/p8kpd/Text/12.xhtml", "p8kpd", "12"),
            ("https://books.scielo.org/id/cwcpz/epub/07.xhtml", "cwcpz", "07"),
            ("https://books.scielo.org/id/c2248/epub/03.html", "c2248", "03"),
        ]

        for url, expected_book_id, expected_chapter_id in test_cases:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertEqual(result['book_id'], expected_book_id)
                self.assertEqual(result['chapter_id'], expected_chapter_id)
                self.assertEqual(result['media_format'], MEDIA_FORMAT_HTML)
                self.assertEqual(result['content_type'], CONTENT_TYPE_FULL_TEXT)

    def test_translate_uses_chapter_key_to_avoid_title_collisions(self):
        sources_metadata = [
            {
                'source_type': 'book',
                'source_id': 'q7gtd',
                'title': 'Book One',
                'publication_year': '2023',
                'identifiers': {'book_id': 'q7gtd', 'isbn': '9788578791889'},
            },
            {
                'source_type': 'book',
                'source_id': 'vdywc',
                'title': 'Book Two',
                'publication_year': '2024',
                'identifiers': {'book_id': 'vdywc', 'isbn': '9788575413593'},
            },
        ]
        documents_metadata = [
            {
                'document_type': 'chapter',
                'document_id': 'book:q7gtd/chapter:03',
                'pid_generic': 'book:q7gtd/chapter:03',
                'default_lang': 'en',
                'publication_date': '2023-01-01',
                'publication_year': '2023',
                'source_type': 'book',
                'source_id': 'q7gtd',
                'title': 'First Book Chapter',
                'identifiers': {'book_id': 'q7gtd', 'chapter_id': '03'},
                'files': {},
            },
            {
                'document_type': 'chapter',
                'document_id': 'book:vdywc/chapter:03',
                'pid_generic': 'book:vdywc/chapter:03',
                'default_lang': 'es',
                'publication_date': '2024-01-01',
                'publication_year': '2024',
                'source_type': 'book',
                'source_id': 'vdywc',
                'title': 'Second Book Chapter',
                'identifiers': {'book_id': 'vdywc', 'chapter_id': '03'},
                'files': {},
            },
        ]
        tm = URLTranslationManager(sources_metadata, documents_metadata)

        result = tm.translate("https://books.scielo.org/id/q7gtd/03")

        self.assertEqual(result['book_title'], 'Book One')
        self.assertEqual(result['chapter_title'], 'First Book Chapter')
        self.assertEqual(result['media_language'], 'en')

    def test_translate_keeps_source_isbn_when_book_document_has_no_isbn(self):
        sources_metadata = [
            {
                'source_type': 'book',
                'source_id': 'q7gtd',
                'title': 'Book Title',
                'publication_year': '2023',
                'identifiers': {'book_id': 'q7gtd', 'isbn': '9788578791889'},
            }
        ]
        documents_metadata = [
            {
                'document_type': 'book',
                'document_id': 'book:q7gtd',
                'pid_generic': 'book:q7gtd',
                'default_lang': 'pt',
                'publication_date': '2023-01-01',
                'publication_year': '2023',
                'source_type': 'book',
                'source_id': 'q7gtd',
                'title': 'Book Title',
                'identifiers': {'book_id': 'q7gtd'},
                'files': {},
            },
        ]
        tm = URLTranslationManager(sources_metadata, documents_metadata)

        result = tm.translate("https://books.scielo.org/id/q7gtd")

        self.assertEqual(result['isbn'], '9788578791889')

    def test_translate_returns_none_for_missing_ids(self):
        """Test that missing book/chapter IDs return None."""
        # Create translator instance directly with a malformed URL
        translator = URLTranslatorBooksSite(
            self.sources_metadata,
            self.documents_metadata
        )
        
        book_id, chapter_id, filename = translator.extract_identifiers("/invalid/path")
        self.assertIsNone(book_id)
        self.assertIsNone(chapter_id)
        self.assertIsNone(filename)

    def test_direct_translator_instantiation(self):
        """Test direct instantiation and use of URLTranslatorBooksSite.
        
        Note: When calling translator directly (not via URLTranslationManager),
        PIDs are not standardized to uppercase.
        """
        translator = URLTranslatorBooksSite(
            {'acronym_to_scielo_issn': {}, 'issn_to_title': {}},
            {'pid_v2_to_default_lang': {}, 'pid_generic_to_publication_date': {}}
        )
        
        result = translator.pipeline_translate("https://books.scielo.org/id/abc123")
        
        self.assertEqual(result['book_id'], 'abc123')
        self.assertIsNone(result['chapter_id'])
        # Direct translator call returns lowercase PIDs (not standardized)
        self.assertEqual(result['pid_generic'], 'book:abc123')
        self.assertEqual(result['media_format'], MEDIA_FORMAT_HTML)
        self.assertEqual(result['content_type'], CONTENT_TYPE_ABSTRACT)

    def test_extract_identifiers_priority(self):
        """Test that PDF patterns take priority over chapter and book patterns."""
        translator = URLTranslatorBooksSite({}, {})
        
        # PDF pattern should match first
        book_id, chapter_id, filename = translator.extract_identifiers("/id/y742k/pdf/magalhaes-9788578791889-18.pdf")
        self.assertEqual(book_id, "y742k")
        self.assertEqual(chapter_id, "18")
        self.assertEqual(filename, "magalhaes-9788578791889-18.pdf")
        
        # Chapter pattern
        book_id, chapter_id, filename = translator.extract_identifiers("/id/vdywc/03")
        self.assertEqual(book_id, "vdywc")
        self.assertEqual(chapter_id, "03")
        self.assertIsNone(filename)
        
        # Book-only pattern
        book_id, chapter_id, filename = translator.extract_identifiers("/id/q7gtd")
        self.assertEqual(book_id, "q7gtd")
        self.assertIsNone(chapter_id)
        self.assertIsNone(filename)
    
    def test_pdf_chapter_extraction_from_filename(self):
        """Test that chapter numbers are extracted from PDF filenames."""
        translator = URLTranslatorBooksSite({}, {})
        
        test_cases = [
            ("/id/y742k/pdf/magalhaes-9788578791889-18.pdf", "18"),
            ("/id/yjxdq/pdf/mororo-9788574554938-01.pdf", "01"),
            ("/id/4ndgv/pdf/paim-9788575413593-05.pdf", "05"),
            ("/id/3yd/pdf/02.pdf", "02"),
            ("/id/82r9t/pdf/sadek-9788579820342.pdf", None),  # No chapter number
        ]
        
        for url, expected_chapter in test_cases:
            with self.subTest(url=url):
                book_id, chapter_id, filename = translator.extract_identifiers(url)
                self.assertEqual(chapter_id, expected_chapter)

    def test_translate_real_books_urls_extracted_from_logs(self):
        urls = [
            '/id/xjcw9',
            '/id/h8pyf/08',
            '/id/3hs/pdf/sampaio-9788523206277.pdf',
            '/id/hd5d8/epub/gelamo-9788598605951.epub',
            'https://books.scielo.org/id/96spq',
            'https://books.scielo.org/id/3dqnm/10',
            'http://books.scielo.org/id/htnbt/pdf/caldeira-9788579830419-10.pdf',
            'https://books.scielo.org/id/wg88m/epub/ortigoza-9788579831287.epub',
            'https://books.scielo.org/id/p8kpd/Text/12.xhtml',
        ]
        for url, expected in zip(urls, BOOKS_LOG_EXPECTED):
            with self.subTest(url=url):
                result = self.tm.translate(url)

                self.assertIsInstance(self.tm.translator, URLTranslatorBooksSite)
                self.assertEqual(result['book_id'], expected['book_id'])
                self.assertEqual(result.get('chapter_id'), expected['chapter_id'])
                self.assertEqual(result['pid_generic'], expected['pid_generic'])
                self.assertEqual(result['media_format'], expected['media_format'])
                self.assertEqual(result['content_type'], expected['content_type'])

    def test_resolves_numeric_chapter_order_to_alphanumeric_chapter_id(self):
        sources_metadata = [
            {
                'source_type': 'book',
                'source_id': 'c5nm2',
                'title': 'Politicas e sistema de saude',
                'publication_year': '2012',
                'identifiers': {'book_id': 'c5nm2', 'isbn': '9788575413494'},
            }
        ]
        documents_metadata = [
            {
                'document_type': 'book',
                'document_id': 'book:c5nm2',
                'pid_generic': 'book:c5nm2',
                'default_lang': 'pt',
                'source_type': 'book',
                'source_id': 'c5nm2',
                'title': 'Politicas e sistema de saude',
                'identifiers': {'book_id': 'c5nm2', 'isbn': '9788575413494'},
            },
            {
                'document_type': 'chapter',
                'document_id': 'book:c5nm2/chapter:br4m5',
                'pid_generic': 'book:c5nm2/chapter:br4m5',
                'default_lang': 'pt',
                'source_type': 'book',
                'source_id': 'c5nm2',
                'title': 'Capitulo 09',
                'identifiers': {'book_id': 'c5nm2', 'chapter_id': 'br4m5'},
                'extra_data': {'order': '09'},
            },
        ]
        tm = URLTranslationManager(sources_metadata, documents_metadata)

        result = tm.translate(
            "https://books.scielo.org/id/c5nm2/pdf/giovanella-9788575413494-09.pdf"
        )

        self.assertEqual(result['book_id'], 'c5nm2')
        self.assertEqual(result['chapter_id'], 'br4m5')
        self.assertEqual(result['pid_generic'], 'BOOK:C5NM2/CHAPTER:BR4M5')
        self.assertEqual(result['document_type'], 'chapter')


if __name__ == '__main__':
    unittest.main()
