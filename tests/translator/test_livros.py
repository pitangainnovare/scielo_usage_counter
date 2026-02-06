import unittest

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.translator.livros import URLTranslatorLivrosSite

from scielo_usage_counter.values import (
    CONTENT_TYPE_FULL_TEXT,
    CONTENT_TYPE_ABSTRACT,
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_PDF,
    DEFAULT_SCIELO_ISSN,
)


class TestTranslatorLivros(unittest.TestCase):
    """
    Test suite for the SciELO Livros (Books) URL translator.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        self.journals_metadata = []
        self.articles_metadata = []
        self.tm = URLTranslationManager(self.journals_metadata, self.articles_metadata)

    def test_translate_book_id_extraction(self):
        """Test that book IDs are correctly extracted from various URL formats."""
        urls_with_expected_ids = [
            ("https://books.scielo.org/b/abc123", "abc123", None),
            ("https://livros.scielo.org/book/xyz789", "xyz789", None),
            ("/b/book001", "book001", None),
            ("/book/book002", "book002", None),
            ("https://books.scielo.org/pdf/book003", "book003", None),
            ("https://books.scielo.org/epub/book004", "book004", None),
            ("https://books.scielo.org/download/book005", "book005", None),
        ]
        
        for url, expected_book_id, expected_chapter_id in urls_with_expected_ids:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorLivrosSite)
                self.assertEqual(result['book_id'], expected_book_id)
                self.assertEqual(result['chapter_id'], expected_chapter_id)

    def test_translate_chapter_id_extraction(self):
        """Test that chapter IDs are correctly extracted from URLs."""
        urls_with_expected_ids = [
            ("https://books.scielo.org/c/book001/chap01", "book001", "chap01"),
            ("https://livros.scielo.org/chapter/book002/chap02", "book002", "chap02"),
            ("/c/book003/chapter123", "book003", "chapter123"),
            ("/chapter/book004/ch999", "book004", "ch999"),
            ("https://books.scielo.org/pdf/book005/chap05", "book005", "chap05"),
            ("https://books.scielo.org/download/book006/chap06", "book006", "chap06"),
        ]
        
        for url, expected_book_id, expected_chapter_id in urls_with_expected_ids:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorLivrosSite)
                self.assertEqual(result['book_id'], expected_book_id)
                self.assertEqual(result['chapter_id'], expected_chapter_id)

    def test_translate_pid_generic_generation(self):
        """Test that generic PIDs are correctly generated."""
        test_cases = [
            ("https://books.scielo.org/b/book001", "BOOK:BOOK001"),
            ("https://books.scielo.org/c/book002/chap01", "BOOK:BOOK002/CHAPTER:CHAP01"),
            ("/book/book003", "BOOK:BOOK003"),
            ("/chapter/book004/chap02", "BOOK:BOOK004/CHAPTER:CHAP02"),
        ]
        
        for url, expected_pid in test_cases:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertEqual(result['pid_generic'], expected_pid)

    def test_translate_content_type_is_abstract(self):
        """Test that book landing pages are classified as abstract."""
        urls = [
            "https://books.scielo.org/b/book001",
            "https://livros.scielo.org/book/book002",
            "/b/book003",
            "/book/book004",
        ]
        
        for url in urls:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorLivrosSite)
                self.assertEqual(result['content_type'], CONTENT_TYPE_ABSTRACT)

    def test_translate_content_type_is_full_text(self):
        """Test that PDF/EPUB/chapter pages are classified as full text."""
        urls = [
            "https://books.scielo.org/pdf/book001",
            "https://books.scielo.org/epub/book002",
            "https://books.scielo.org/download/book003",
            "https://books.scielo.org/c/book004/chap01",
            "https://livros.scielo.org/chapter/book005/chap02",
            "/pdf/book006/chap03",
            "/download/book007/chap04",
        ]
        
        for url in urls:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorLivrosSite)
                self.assertEqual(result['content_type'], CONTENT_TYPE_FULL_TEXT)

    def test_translate_media_format_html(self):
        """Test that HTML format is correctly identified."""
        urls = [
            "https://books.scielo.org/b/book001",
            "https://books.scielo.org/book/book002",
            "https://books.scielo.org/c/book003/chap01",
            "https://books.scielo.org/chapter/book004/chap02",
            "https://books.scielo.org/epub/book005",
            "/b/book006",
            "/c/book007/chap03",
        ]
        
        for url in urls:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorLivrosSite)
                self.assertEqual(result['media_format'], MEDIA_FORMAT_HTML)

    def test_translate_media_format_pdf(self):
        """Test that PDF format is correctly identified."""
        urls = [
            "https://books.scielo.org/pdf/book001",
            "https://books.scielo.org/pdf/book002/chap01",
            "https://books.scielo.org/download/book003",
            "https://books.scielo.org/download/book004/chap02",
            "/pdf/book005",
            "/download/book006",
        ]
        
        for url in urls:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorLivrosSite)
                self.assertEqual(result['media_format'], MEDIA_FORMAT_PDF)

    def test_translate_issn_default(self):
        """Test that books use the default ISSN."""
        urls = [
            "https://books.scielo.org/b/book001",
            "https://books.scielo.org/c/book002/chap01",
            "/pdf/book003",
        ]
        
        for url in urls:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorLivrosSite)
                self.assertEqual(result['scielo_issn'], DEFAULT_SCIELO_ISSN)

    def test_translate_with_query_params(self):
        """Test URL translation with query parameters."""
        url = "https://books.scielo.org/b/book001?lang=en&format=html"
        result = self.tm.translate(url)
        
        self.assertIsInstance(self.tm.translator, URLTranslatorLivrosSite)
        self.assertEqual(result['book_id'], 'book001')
        self.assertEqual(result['media_language'], 'en')

    def test_translate_returns_none_for_missing_ids(self):
        """Test that missing book/chapter IDs return None."""
        # Create translator instance directly with a malformed URL
        translator = URLTranslatorLivrosSite(
            self.journals_metadata, 
            self.articles_metadata
        )
        
        book_id, chapter_id = translator.extract_identifiers("/invalid/path")
        self.assertIsNone(book_id)
        self.assertIsNone(chapter_id)

    def test_direct_translator_instantiation(self):
        """Test direct instantiation and use of URLTranslatorLivrosSite."""
        translator = URLTranslatorLivrosSite(
            {'acronym_to_scielo_issn': {}, 'issn_to_title': {}},
            {'pid_v2_to_default_lang': {}, 'pid_generic_to_publication_date': {}}
        )
        
        result = translator.pipeline_translate("https://books.scielo.org/b/book123")
        
        self.assertEqual(result['book_id'], 'book123')
        self.assertIsNone(result['chapter_id'])
        self.assertEqual(result['pid_generic'], 'book:book123')
        self.assertEqual(result['media_format'], MEDIA_FORMAT_HTML)
        self.assertEqual(result['content_type'], CONTENT_TYPE_ABSTRACT)

    def test_extract_identifiers_priority(self):
        """Test that chapter patterns take priority over book patterns."""
        translator = URLTranslatorLivrosSite([], [])
        
        # Chapter patterns should match first
        book_id, chapter_id = translator.extract_identifiers("/c/book001/chap01")
        self.assertEqual(book_id, "book001")
        self.assertEqual(chapter_id, "chap01")
        
        # Book-only pattern
        book_id, chapter_id = translator.extract_identifiers("/b/book002")
        self.assertEqual(book_id, "book002")
        self.assertIsNone(chapter_id)


if __name__ == '__main__':
    unittest.main()
