import unittest
from unittest.mock import patch

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.translator import opac
from scielo_usage_counter.translator.opac import URLTranslatorOPACSite
from scielo_usage_counter.values import (
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_PDF,
    MEDIA_FORMAT_XML,
    CONTENT_TYPE_FULL_TEXT,
    CONTENT_TYPE_ABSTRACT,
    CONTENT_TYPE_CITATION_EXPORT,
)


class TestTranslatorOPAC(unittest.TestCase):
    def setUp(self):
        self.journals_metadata = [
            {
                'acronym': 'psoc',
                'scielo_issn': '1807-0310',
                'issns': ['1807-0310',],
                'title': 'Psicologia & Sociedade',
                'publisher_name': 'Universidade Federal do Rio Grande do Sul',
                'subject_areas': ['Psychology',],
                'wos_subject_areas': ['PSYCHOLOGY, SOCIAL',]
            }, {
                'acronym': 'rbz',
                'scielo_issn': '1516-3598',
                'issns': ['1516-3598'],
                'title': 'Revista Brasileira de Zootecnia',
                'publisher_name': 'Sociedade Brasileira de Zootecnia',
                'subject_areas': ['Agricultural Sciences'],
                'wos_subject_areas': ['AGRICULTURE, DAIRY & ANIMAL SCIENCE']
            }, {
                'acronym': 'neco',
                'scielo_issn': '0103-6351',
                'issns': ['0103-6351'],
                'title': 'Nova Economia',
                'publisher_name': 'Universidade Federal de Minas Gerais',
                'subject_areas': ['Economics'],
                'wos_subject_areas': ['ECONOMICS']
            },
            {
                'acronym': 'smj',
                'issns': ['1806-9460'],
                'scielo_issn': '1806-9460',
                'title': 'Revista de Economia e Sociologia Rural',
            }
        ]
        self.articles_metadata = [
            {
                'pid_v2': '',
                'pid_v3': '5ySvRy7VFTxsKLt35Mwsm9g',
                'default_lang': 'en',
                'text_langs': ['en', 'es'],
                'scielo_issn': '0103-6351',
                'publication_year': '2017',
                'files': [
                    {'doi': '10.7727/neco.2014.321', 'lang': 'en', 'path': 'pdf/neco/v66n6/2309-5830-neco-66-06-0634.pdf', 'checked': False},
                    {'doi': '10.7727/neco.2014.321', 'lang': 'es', 'path': 'pdf/neco/v66n6/es_2309-5830-neco-66-06-0588.pdf', 'checked': False}
                ] 
            },
            {
                'pid_v2': '',
                'pid_v3': 'dqLRqnpmnncSmnzMCB8bzPG',
                'default_lang': 'pt',
                'text_langs': ['pt', 'en'],
                'scielo_issn': '0103-6351',
                'publication_year': '2021',
                'files': [
                    {'doi': '10.1590/neco.2021.123', 'lang': 'pt', 'path': 'pdf/neco/v29n3/1234-5678-neco-29-03-0123.pdf', 'checked': False},
                    {'doi': '10.1590/neco.2021.123', 'lang': 'en', 'path': 'pdf/neco/v29n3/en_1234-5678-neco-29-03-0123.pdf', 'checked': False}
                ]
            },
            {
                'pid_v2': '',
                'pid_v3': 'cKnLLBn5NnshCX93Y6qYpHv',
                'default_lang': 'en',
                'text_langs': ['en', 'es'],
                'scielo_issn': '1516-3598',
                'publication_year': '2020',
                'files': [
                    {'doi': '10.1590/rbz.2020.456', 'lang': 'en', 'path': 'pdf/rbz/v47n4/5678-1234-rbz-47-04-0456.pdf', 'checked': False},
                    {'doi': '10.1590/rbz.2020.456', 'lang': 'es', 'path': 'pdf/rbz/v47n4/es_5678-1234-rbz-47-04-0456.pdf', 'checked': False}
                ]
            },
            {
                'pid_v2': '',
                'pid_v3': 'hbSYnTbyNfzxcWT3FpXrL5G',
                'default_lang': 'es',
                'text_langs': ['es', 'en'],
                'scielo_issn': '1807-0310',
                'publication_year': '2019',
                'files': [
                    {'doi': '10.1590/psoc.2019.789', 'lang': 'es', 'path': 'pdf/psoc/v37n2/7890-1234-psoc-37-02-0789.pdf', 'checked': False},
                    {'doi': '10.1590/psoc.2019.789', 'lang': 'en', 'path': 'pdf/psoc/v37n2/en_7890-1234-psoc-37-02-0789.pdf', 'checked': False}
                ]
            },
            {
                'pid_v2': '',
                'pid_v3': 'YdZ7HCqnBkgxhJRPCmKrxkz',
                'default_lang': 'pt',
                'text_langs': ['pt', 'en'],
                'scielo_issn': '1806-9460',
                'files': [],
            }
        ]
        self.tm = URLTranslationManager(self.journals_metadata, self.articles_metadata)

    def test_translate_opac_site_url_journal_article_abstract(self):
        url = '/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/abstract/?lang=en'
        
        expected = {
            'journal_acronym': 'neco',
            'journal_main_title': 'Nova Economia',
            'journal_publisher_name': 'Universidade Federal de Minas Gerais',
            'journal_subject_area_capes': ['Economics'],
            'journal_subject_area_wos': ['ECONOMICS'],
            'year_of_publication': '2021',
            'scielo_issn': '0103-6351',
            'pid_v3': 'dqLRqnpmnncSmnzMCB8bzPG',
            'media_format': 'html',
            'media_language': 'en',
            'content_type': CONTENT_TYPE_ABSTRACT,
        }

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACSite)
        self.assertDictEqual(obtained, expected)

    def test_translate_opac_site_url_journal_article(self):
        url = '/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/'
        
        expected = {
            'journal_acronym': 'neco',
            'journal_main_title': 'Nova Economia',
            'journal_publisher_name': 'Universidade Federal de Minas Gerais',
            'journal_subject_area_capes': ['Economics'],
            'journal_subject_area_wos': ['ECONOMICS'],
            'year_of_publication': '2021',
            'scielo_issn': '0103-6351',
            'pid_v3': 'dqLRqnpmnncSmnzMCB8bzPG',
            'media_format': MEDIA_FORMAT_HTML,
            'media_language': 'pt',
            'content_type': CONTENT_TYPE_FULL_TEXT,
        }

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACSite)
        self.assertDictEqual(obtained, expected)

    def test_translate_opac_site_url_journal_article_with_language(self):
        url = '/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/?lang=pt'
        
        expected = {
            'journal_acronym': 'neco',
            'journal_main_title': 'Nova Economia',
            'journal_publisher_name': 'Universidade Federal de Minas Gerais',
            'journal_subject_area_capes': ['Economics'],
            'journal_subject_area_wos': ['ECONOMICS'],
            'year_of_publication': '2021',
            'scielo_issn': '0103-6351',
            'pid_v3': 'dqLRqnpmnncSmnzMCB8bzPG',
            'media_format': MEDIA_FORMAT_HTML,
            'media_language': 'pt',
            'content_type': CONTENT_TYPE_FULL_TEXT,
        }

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACSite)
        self.assertDictEqual(obtained, expected)

    def test_translate_opac_site_url_journal_article_with_format_pdf(self):
        url = '/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/?format=pdf'
        
        expected = {
            'journal_acronym': 'neco',
            'journal_main_title': 'Nova Economia',
            'journal_publisher_name': 'Universidade Federal de Minas Gerais',
            'journal_subject_area_capes': ['Economics'],
            'journal_subject_area_wos': ['ECONOMICS'],
            'year_of_publication': '2021',
            'scielo_issn': '0103-6351',
            'pid_v3': 'dqLRqnpmnncSmnzMCB8bzPG',
            'media_format': MEDIA_FORMAT_PDF,
            'media_language': 'pt',
            'content_type': CONTENT_TYPE_FULL_TEXT,
        }

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACSite)
        self.assertDictEqual(obtained, expected)

    def test_translate_opac_site_url_journal_article_with_format_xml(self):
        url = '/j/rbz/a/cKnLLBn5NnshCX93Y6qYpHv/?format=xml'
        
        expected = {
            'journal_acronym': 'rbz',
            'journal_main_title': 'Revista Brasileira de Zootecnia',
            'journal_publisher_name': 'Sociedade Brasileira de Zootecnia',
            'journal_subject_area_capes': ['Agricultural Sciences'],
            'journal_subject_area_wos': ['AGRICULTURE, DAIRY & ANIMAL SCIENCE'],
            'year_of_publication': '2020',
            'scielo_issn': '1516-3598',
            'pid_v3': 'cKnLLBn5NnshCX93Y6qYpHv',
            'media_format': MEDIA_FORMAT_XML,
            'media_language': 'en',
            'content_type': CONTENT_TYPE_FULL_TEXT,
        }

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACSite)
        self.assertDictEqual(obtained, expected)

    def test_translate_opac_site_url_journal_article_abstract_content_type_is_abstract(self):
        url = '/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/abstract/'
        
        expected = {
            'journal_acronym': 'neco',
            'journal_main_title': 'Nova Economia',
            'journal_publisher_name': 'Universidade Federal de Minas Gerais',
            'journal_subject_area_capes': ['Economics'],
            'journal_subject_area_wos': ['ECONOMICS'],
            'year_of_publication': '2021',
            'scielo_issn': '0103-6351',
            'pid_v3': 'dqLRqnpmnncSmnzMCB8bzPG',
            'media_format': MEDIA_FORMAT_HTML,
            'media_language': 'pt',
            'content_type': CONTENT_TYPE_ABSTRACT,
        }

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACSite)
        self.assertEqual(obtained['content_type'], CONTENT_TYPE_ABSTRACT)
        self.assertDictEqual(obtained, expected)

    def test_translate_opac_site_url_journal_article_content_type_is_full_text(self):
        url = '/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/'
        
        expected = {
            'journal_acronym': 'neco',
            'journal_main_title': 'Nova Economia',
            'journal_publisher_name': 'Universidade Federal de Minas Gerais',
            'journal_subject_area_capes': ['Economics'],
            'journal_subject_area_wos': ['ECONOMICS'],
            'year_of_publication': '2021',
            'scielo_issn': '0103-6351',
            'pid_v3': 'dqLRqnpmnncSmnzMCB8bzPG',
            'media_format': MEDIA_FORMAT_HTML,
            'media_language': 'pt',
            'content_type': CONTENT_TYPE_FULL_TEXT,
        }

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACSite)
        self.assertEqual(obtained['content_type'], CONTENT_TYPE_FULL_TEXT)
        self.assertDictEqual(obtained, expected)

    def test_translate_opac_site_url_journal_article_pdf_content_type_is_full_text(self):
        url = '/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/?format=pdf'
        
        expected = {
            'journal_acronym': 'neco',
            'journal_main_title': 'Nova Economia',
            'journal_publisher_name': 'Universidade Federal de Minas Gerais',
            'journal_subject_area_capes': ['Economics'],
            'journal_subject_area_wos': ['ECONOMICS'],
            'year_of_publication': '2021',
            'scielo_issn': '0103-6351',
            'pid_v3': 'dqLRqnpmnncSmnzMCB8bzPG',
            'media_format': MEDIA_FORMAT_PDF,
            'media_language': 'pt',
            'content_type': CONTENT_TYPE_FULL_TEXT,
        }

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACSite)
        self.assertEqual(obtained['content_type'], CONTENT_TYPE_FULL_TEXT)
        self.assertDictEqual(obtained, expected)

    def test_translate_opac_site_url_journal_article_xml_content_type_is_fulltext(self):
        url = '/j/rbz/a/cKnLLBn5NnshCX93Y6qYpHv/?format=xml'
        
        expected = {
            'journal_acronym': 'rbz',
            'journal_main_title': 'Revista Brasileira de Zootecnia',
            'journal_publisher_name': 'Sociedade Brasileira de Zootecnia',
            'journal_subject_area_capes': ['Agricultural Sciences'],
            'journal_subject_area_wos': ['AGRICULTURE, DAIRY & ANIMAL SCIENCE'],
            'year_of_publication': '2020',
            'scielo_issn': '1516-3598',
            'pid_v3': 'cKnLLBn5NnshCX93Y6qYpHv',
            'media_format': 'xml',
            'media_language': 'en',
            'content_type': CONTENT_TYPE_FULL_TEXT,
        }

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACSite)
        self.assertEqual(obtained['content_type'], CONTENT_TYPE_FULL_TEXT)
        self.assertDictEqual(obtained, expected)

    def test_translate_opac_site_url_citation_export_content_type_is_citation_export(self):
        urls = [
            '/citation/export/5ySvRy7VFTxsKLt35Mwsm9g/?format=bib',
            'citation/export/5ySvRy7VFTxsKLt35Mwsm9g/?format=bib',
            '/citation/export/5ySvRy7VFTxsKLt35Mwsm9g/?format=ris',
            'citation/export/5ySvRy7VFTxsKLt35Mwsm9g/?format=ris',
        ]
        for url in urls:
            with self.subTest(url=url):
                expected = {
                    'journal_acronym': 'neco',
                    'journal_main_title': 'Nova Economia',
                    'journal_publisher_name': 'Universidade Federal de Minas Gerais',
                    'journal_subject_area_capes': ['Economics'],
                    'journal_subject_area_wos': ['ECONOMICS'],
                    'year_of_publication': '2017',
                    'scielo_issn': '0103-6351',

                    'pid_v3': '5ySvRy7VFTxsKLt35Mwsm9g',
                    'media_format': MEDIA_FORMAT_HTML,
                    'media_language': 'en',
                    'content_type': CONTENT_TYPE_CITATION_EXPORT,
                }
                obtained = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorOPACSite)
                self.assertDictEqual(obtained, expected)
                
    def test_translate_opac_site_url_documentstore(self):
        url = '/article/ssm/content/raw/?resource_ssm_path=/documentstore/1806-9460/YdZ7HCqnBkgxhJRPCmKrxkz/b7e997318152c89988a6aad8b0c541d510f468f6.pdf'
        
        expected = {
            'journal_acronym': 'smj',
            'journal_main_title': 'Revista de Economia e Sociologia Rural',
            'scielo_issn': '1806-9460',
            'pid_v3': 'YdZ7HCqnBkgxhJRPCmKrxkz',
            'media_format': MEDIA_FORMAT_PDF,
            'media_language': 'pt',
            'content_type': CONTENT_TYPE_FULL_TEXT,
        }

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACSite)
        self.assertDictEqual(obtained, expected)

    def test_pid_v2_urls_use_the_article_pid_v3(self):
        pid_v2 = 'S0103-63512021000100001'
        pid_v3 = 'dqLRqnpmnncSmnzMCB8bzPG'
        article = next(
            item for item in self.articles_metadata if item['pid_v3'] == pid_v3
        )
        article['pid_v2'] = pid_v2
        manager = URLTranslationManager(
            self.journals_metadata,
            self.articles_metadata,
        )
        urls = (
            (f'/j/neco/a/{pid_v2}/', CONTENT_TYPE_FULL_TEXT, MEDIA_FORMAT_HTML),
            (f'/j/neco/a/{pid_v2.lower()}/', CONTENT_TYPE_FULL_TEXT, MEDIA_FORMAT_HTML),
            (f'/j/neco/a/{pid_v2}/abstract/?lang=en', CONTENT_TYPE_ABSTRACT, MEDIA_FORMAT_HTML),
            (f'/citation/export/{pid_v2}/?format=bib', CONTENT_TYPE_CITATION_EXPORT, MEDIA_FORMAT_HTML),
            (
                '/article/ssm/content/raw/?resource_ssm_path='
                f'/documentstore/0103-6351/{pid_v2}/file.pdf',
                CONTENT_TYPE_FULL_TEXT,
                MEDIA_FORMAT_PDF,
            ),
        )

        for url, content_type, media_format in urls:
            with self.subTest(url=url):
                result = manager.translate(url)

                self.assertEqual(result['pid_v2'], pid_v2)
                self.assertEqual(result['pid_v3'], pid_v3)
                self.assertEqual(result['scielo_issn'], '0103-6351')
                self.assertEqual(result['year_of_publication'], '2021')
                self.assertEqual(result['content_type'], content_type)
                self.assertEqual(result['media_format'], media_format)
                self.assertNotEqual(result['media_language'], 'un')

    def test_article_url_with_suffix_keeps_pid_v3(self):
        pid_v3 = 'dqLRqnpmnncSmnzMCB8bzPG'
        result = self.tm.translate(f'/j/neco/a/{pid_v3}.pdf')

        self.assertEqual(result['pid_v3'], pid_v3)
        self.assertEqual(result['content_type'], CONTENT_TYPE_FULL_TEXT)

    def test_unmapped_pid_v2_is_not_truncated(self):
        pid_v2 = 'S0103-63512021000100002'
        result = self.tm.translate(f'/j/neco/a/{pid_v2}/?lang=pt')

        self.assertEqual(result['pid_v2'], pid_v2)
        self.assertNotIn('pid_v3', result)

    def test_pipeline_parses_url_once(self):
        url = '/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/abstract/?lang=en'

        with patch.object(opac, 'urlparse', wraps=opac.urlparse) as urlparse:
            obtained = self.tm.translate(url)

        self.assertEqual(obtained['pid_v3'], 'dqLRqnpmnncSmnzMCB8bzPG')
        self.assertEqual(obtained['content_type'], CONTENT_TYPE_ABSTRACT)
        urlparse.assert_called_once_with(url)
