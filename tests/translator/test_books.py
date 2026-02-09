import unittest

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.translator.books import URLTranslatorBooksSite

from scielo_usage_counter.values import (
    CONTENT_TYPE_FULL_TEXT,
    CONTENT_TYPE_ABSTRACT,
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_PDF,
    DEFAULT_SCIELO_ISSN,
)


class TestTranslatorBooks(unittest.TestCase):
    """
    Test suite for the SciELO Books URL translator.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        self.journals_metadata = []
        self.articles_metadata = []
        self.tm = URLTranslationManager(self.journals_metadata, self.articles_metadata)

    def test_translate_book_id_extraction(self):
        """Test that book IDs are correctly extracted from actual SciELO Books URL formats."""
        urls_with_expected_ids = [
            ("https://books.scielo.org/id/q7gtd", "q7gtd", None),
            ("https://books.scielo.org/id/4ndgv", "4ndgv", None),
            ("/id/gbvb4", "gbvb4", None),
            ("/id/y742k", "y742k", None),
        ]
        
        for url, expected_book_id, expected_chapter_id in urls_with_expected_ids:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorBooksSite)
                self.assertEqual(result['book_id'], expected_book_id)
                self.assertEqual(result['chapter_id'], expected_chapter_id)

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

    def test_translate_issn_default(self):
        """Test that books use the default ISSN."""
        urls = [
            "https://books.scielo.org/id/q7gtd",
            "https://books.scielo.org/id/vdywc/03",
            "/id/y742k/pdf/magalhaes-9788578791889-18.pdf",
        ]
        
        for url in urls:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorBooksSite)
                self.assertEqual(result['scielo_issn'], DEFAULT_SCIELO_ISSN)

    def test_translate_with_query_params(self):
        """Test URL translation with query parameters."""
        url = "https://books.scielo.org/id/q7gtd?lang=en&format=html"
        result = self.tm.translate(url)
        
        self.assertIsInstance(self.tm.translator, URLTranslatorBooksSite)
        self.assertEqual(result['book_id'], 'q7gtd')
        self.assertEqual(result['media_language'], 'en')

    def test_translate_returns_none_for_missing_ids(self):
        """Test that missing book/chapter IDs return None."""
        # Create translator instance directly with a malformed URL
        translator = URLTranslatorBooksSite(
            self.journals_metadata, 
            self.articles_metadata
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
            ("/id/82r9t/pdf/sadek-9788579820342.pdf", None),  # No chapter number
        ]
        
        for url, expected_chapter in test_cases:
            with self.subTest(url=url):
                book_id, chapter_id, filename = translator.extract_identifiers(url)
                self.assertEqual(chapter_id, expected_chapter)


if __name__ == '__main__':
    unittest.main()
