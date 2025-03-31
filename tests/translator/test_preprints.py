import unittest

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.translator.preprints import URLTranslatorPreprintsSite

from scielo_usage_counter.values import (
    CONTENT_TYPE_FULL_TEXT,
    CONTENT_TYPE_ABSTRACT,
)


class TestTranslatorPreprints(unittest.TestCase):
    def setUp(self):
        self.journals_metadata = []
        self.articles_metadata = []
        self.tm = URLTranslationManager(self.journals_metadata, self.articles_metadata)

    def test_translate_preprint_id_extraction(self):
        urls_with_expected_ids = [
            ("https://preprints.scielo.org/preprint/view/1234", "1234"),
            ("https://preprints.scielo.org/preprint/view/1234/version/2", "1234"),
            ("https://preprints.scielo.org/documents/article/view/5678", "5678"),
            ("https://preprints.scielo.org/preprint/download/1234/5678", "1234"),
            ("https://preprints.scielo.org/preprint/download/1234/version/2/5678", "1234"),
            ("https://preprints.scielo.org/documents/article/download/5678/1234", "5678"),
            ("/preprint/view/1234", "1234"),
            ("/preprint/view/1234/version/2", "1234"),
            ("/documents/article/view/5678", "5678"),
            ("/preprint/download/1234/5678", "1234"),
            ("/preprint/download/1234/version/2/5678", "1234"),
            ("/documents/article/download/5678/1234", "5678"),
        ]
        for url, expected_id in urls_with_expected_ids:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorPreprintsSite)
                self.assertEqual(result['pid_generic'], expected_id)

    def test_translate_content_type_is_abstract(self):
        urls = [
            "https://preprints.scielo.org/preprint/view/1234",
            "https://preprints.scielo.org/preprint/view/1234/version/2",
            "https://preprints.scielo.org/documents/article/view/5678",
            "/preprint/view/1234",
            "/preprint/view/1234/version/2",
            "/documents/article/view/5678",
        ]
        for url in urls:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorPreprintsSite)
                self.assertEqual(result['content_type'], CONTENT_TYPE_ABSTRACT)

    def test_translate_content_type_full_text(self):
        urls = [
            "https://preprints.scielo.org/preprint/download/1234/5678",
            "https://preprints.scielo.org/preprint/download/1234/version/2/5678",
            "https://preprints.scielo.org/documents/article/download/5678/1234",
            "/preprint/download/1234/5678",
            "/preprint/download/1234/version/2/5678",
            "/documents/article/download/5678/1234",
        ]
        for url in urls:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorPreprintsSite)
                self.assertEqual(result['content_type'], CONTENT_TYPE_FULL_TEXT)
