import unittest

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.translator.opac_alpha import URLTranslatorOPACAlphaSite

from scielo_usage_counter.values import (
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_PDF,
    CONTENT_TYPE_ABSTRACT,
    CONTENT_TYPE_FULL_TEXT,
)


class TestTranslatorOPACAlpha(unittest.TestCase):
    def setUp(self):
        self.journals_metadata = [
            {
                'acronym': 'resp',
                'scielo_issn': '2173-9110',
                'issns': ['2173-9110', '1135-5727'],
                'title': 'Revista Española de Salud Pública',
            }, {
                'acronym': 'psoc',
                'scielo_issn': '1807-0310',
                'issns': ['1807-0310',],
                'title': 'Psicologia & Sociedade',
            }, {
                'acronym': 'gs',
                'title': 'Gaceta Sanitaria',
                'scielo_issn': '0213-9111',
                'issns': ['0213-9111',],
            }, {
                'acronym': 'csc',
                'title': 'Ciência & Saúde Coletiva',
                'scielo_issn': '0103-9733',
                'issns': ['0103-9733',],
            }
        ]
        self.articles_metadata = [
            {
                'pid_v2': '',
                'pid_v3': 'gs:2010:v24n3:233-240',
                'default_lang': 'es',
                'text_langs': ['es', 'en'],
                'pdfs': [
                    {'doi': '10.1016/j.gaceta.2010.01.010', 'lang': 'es', 'path': 'pdf/gs/2010.v24n3/233-240/es', 'checked': False},
                ]
            },
            {
                'pid_v2': '',
                'pid_v3': 'resp:2024:v98:e202409053',
                'default_lang': 'es',
                'text_langs': ['es', 'en'],
                'pdfs': [],
            },
            {
                'pid_v2': '',
                'pid_v3': 'resp:2005:v79n5:591-597',
                'default_lang': 'es',
                'text_langs': ['es', 'en'],
                'pdfs': [],
            },
            {
                'pid_v2': '',
                'pid_v3': 'csc:2025:v30n2:e05402023',
                'default_lang': 'pt',
                'text_langs': ['pt',],
                'pdfs': [],
            },
            {
                'pid_v2': '',
                'pid_v3': 'resp:2005:v83n1:109-121',
                'default_lang': 'es',
                'text_langs': ['es', 'en'],
                'pdfs': [
                    {'path': 'resp_83_01_0109.pdf', 'lang': 'es', 'checked': False},
                ],
            },
            {
                'pid_v2': '',
                'pid_v3': 'resp:v92:e201806033',
                'default_lang': 'es',
                'text_langs': ['es', 'en'],
                'pdfs': [
                    {'path': '1135-5727-resp-92-e201806033.pdf', 'lang': 'es', 'checked': False},
                ],
            }
        ]
        self.tm = URLTranslationManager(self.journals_metadata, self.articles_metadata)

    def test_translate_opac_alpha_url_article_journal_acronym_year_vol_issue_pages_language(self):
        for url in [
            "article/resp/2009.v83n1/109-121/es/",
            "/article/resp/2009.v83n1/109-121/es/",
        ]:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertDictEqual(
                    result,
                    {
                        'scielo_issn': '2173-9110',
                        'pid_v2': None,
                        'pid_v3': 'resp:2009:v83n1:109-121',
                        'media_format': MEDIA_FORMAT_HTML,
                        'media_language': 'es',
                        'content_type': CONTENT_TYPE_FULL_TEXT,
                    }
                )
                self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_translate_opac_alpha_url_pdf_journal_acronym_year_vol_issue_pages_language(self):
        for url in [
            "pdf/resp/2001.v75n5/459-466/es",
            "/pdf/resp/2001.v75n5/459-466/es",
        ]:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertDictEqual(
                    result,
                    {
                        'scielo_issn': '2173-9110',
                        'pid_v2': None,
                        'pid_v3': 'resp:2001:v75n5:459-466',
                        'media_format': MEDIA_FORMAT_PDF,
                        'media_language': 'es',
                        'content_type': CONTENT_TYPE_FULL_TEXT,
                    }
                )
                self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_translate_opac_alpha_url_article_journal_acronym_year_vol_issue_pages(self):
        urls = [
            '/article/gs/2010.v24n3/233-240',
            '/article/gs/2010.v24n3/233-240/',
            'article/gs/2010.v24n3/233-240',
            'article/gs/2010.v24n3/233-240/',
        ]
        for url in urls:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertDictEqual(
                    result,
                    {
                        'scielo_issn': '0213-9111',
                        'pid_v2': None,
                        'pid_v3': 'gs:2010:v24n3:233-240',
                        'media_format': MEDIA_FORMAT_HTML,
                        'media_language': 'es',
                        'content_type': CONTENT_TYPE_FULL_TEXT,
                    }
                )
                self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_translate_opac_alpha_url_article_journal_acronym_year_vol_epage_language(self):
        url = 'article/resp/2024.v98/e202409053/es/'
        result = self.tm.translate(url)
        self.assertDictEqual(
            result,
            {
                'scielo_issn': '2173-9110',
                'pid_v2': None,
                'pid_v3': 'resp:2024:v98:e202409053',
                'media_format': MEDIA_FORMAT_HTML,
                'media_language': 'es',
                'content_type': CONTENT_TYPE_FULL_TEXT,
            }
        )
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_translate_opac_alpha_url_pdf_journal_acronym_year_vol_epage_language(self):
        url = 'pdf/resp/2024.v98/e202409053/es'
        result = self.tm.translate(url)
        self.assertDictEqual(
            result,
            {
                'scielo_issn': '2173-9110',
                'pid_v2': None,
                'pid_v3': 'resp:2024:v98:e202409053',
                'media_format': MEDIA_FORMAT_PDF,
                'media_language': 'es',
                'content_type': CONTENT_TYPE_FULL_TEXT,
            })
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_translate_opac_alpha_url_article_journal_acronym_year_vol_pages_language_abstract_language(self):
        url = '/article/gs/2010.v24n3/233-240/es/?abstract_lang=es'
        result = self.tm.translate(url)
        self.assertDictEqual(
            result,
            {
                'scielo_issn': '0213-9111',
                'pid_v2': None,
                'pid_v3': 'gs:2010:v24n3:233-240',
                'media_format': MEDIA_FORMAT_HTML,
                'media_language': 'es',
                'content_type': CONTENT_TYPE_ABSTRACT,
            }
        )
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_translate_opac_alpha_url_aritcle_journal_acronym_year_vol_epage_language_abstract_language(self):
        url = '/article/csc/2025.v30n2/e05402023/pt/?abstract_lang=pt'
        result = self.tm.translate(url)
        self.assertDictEqual(
            result,
            {
                'scielo_issn': '0103-9733',
                'pid_v2': None,
                'pid_v3': 'csc:2025:v30n2:e05402023',
                'media_format': MEDIA_FORMAT_HTML,
                'media_language': 'pt',
                'content_type': CONTENT_TYPE_ABSTRACT,
            }
        )
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_translate_opac_alpha_url_pdf_journal_acronym_year_vol_issue_pages(self):
        url = 'pdf/resp/2005.v79n5/591-597'
        result = self.tm.translate(url)
        self.assertDictEqual(
            result,
            {
                'scielo_issn': '2173-9110',
                'pid_v2': None,
                'pid_v3': 'resp:2005:v79n5:591-597',
                'media_format': MEDIA_FORMAT_PDF,
                'media_language': 'es',
                'content_type': CONTENT_TYPE_FULL_TEXT,
            })
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_translate_opac_alpha_url_pdf_journal_acronym_vol_issue_file_path(self):
        # This URLs is very similar to the classic URL format
        # In this case, we have to use the OPACAlphaSite translator
        self.tm.translator = URLTranslatorOPACAlphaSite(self.tm.journals_metadata, self.tm.articles_metadata)
        self.tm.is_translator_forced = True

        url = '/pdf/resp/v83n1/109-121/resp_83_01_0109.pdf'

        result = self.tm.translate(url)

        self.assertDictEqual(
            result,
            {
                'scielo_issn': '2173-9110',
                'pid_v2': None,
                'pid_v3': 'resp:2005:v83n1:109-121',
                'media_format': MEDIA_FORMAT_PDF,
                'media_language': 'es',
                'content_type': CONTENT_TYPE_FULL_TEXT,
            })
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_translate_opac_alpha_url_resource_ssm_path(self):
        url = '/article/ssm/content/raw/?resource_ssm_path=/media/assets/resp/v92/1135-5727-resp-92-e201806033.pdf'

        # This URL is very similar to the OPAC URL format, so, we have to force the OPACAlphaSite translator
        self.tm.translator = URLTranslatorOPACAlphaSite(self.tm.journals_metadata, self.tm.articles_metadata)
        self.tm.is_translator_forced = True
        result = self.tm.translate(url)
        self.assertDictEqual(
            result,
            {
                'scielo_issn': '2173-9110',
                'pid_v2': None,
                'pid_v3': 'resp:v92:e201806033',
                'media_format': MEDIA_FORMAT_PDF,
                'media_language': 'es',
                'content_type': CONTENT_TYPE_FULL_TEXT,
            })
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_translate_opac_alpha_content_type_is_full_text(self):
        for u in [
            '/article/resp/2009.v83n1/109-121/es/' 
            '/article/csc/2025.v30n2/e05402023/pt',
            '/article/csc/2025.v30n2/e05402023', 
            'pdf/resp/2001.v75n5/459-466/es',
        ]:
            with self.subTest(u):
                result = self.tm.translate(u)
                self.assertEqual(CONTENT_TYPE_FULL_TEXT, result['content_type'])
                self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_translate_opac_alpha_content_type_is_abstract(self):
        for u in [
            '/article/resp/2009.v83n1/109-121/es/?abstract_lang=es',
            '/article/resp/2009.v83n1/109-121/pt/?abstract_lang=pt',
        ]:
            with self.subTest(u):
                result = self.tm.translate(u)
                self.assertEqual(CONTENT_TYPE_ABSTRACT, result['content_type'])
                self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)
