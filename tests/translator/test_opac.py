import unittest

from scielo_usage_counter.url_translator import URLTranslationManager
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
        ]
        self.articles_metadata = [
            {
                'pid_v2': '',
                'pid_v3': '5ySvRy7VFTxsKLt35Mwsm9g',
                'default_lang': 'en',
                'text_langs': ['en', 'es'],
                'scielo_issn': '0103-6351',
                'publication_year': '2017',
                'pdfs': [
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
                'pdfs': [
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
                'pdfs': [
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
                'pdfs': [
                    {'doi': '10.1590/psoc.2019.789', 'lang': 'es', 'path': 'pdf/psoc/v37n2/7890-1234-psoc-37-02-0789.pdf', 'checked': False},
                    {'doi': '10.1590/psoc.2019.789', 'lang': 'en', 'path': 'pdf/psoc/v37n2/en_7890-1234-psoc-37-02-0789.pdf', 'checked': False}
                ]
            }
        ]
        self.tm = URLTranslationManager(self.journals_metadata, self.articles_metadata)

    def test_translate_opac_site_url_journal_article_abstract(self):
        url = '/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/abstract/?lang=en'
        
        expected = {
            'scielo_issn': '0103-6351',
            'pid_v2': None,
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
            'scielo_issn': '0103-6351',
            'pid_v2': None,
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
            'scielo_issn': '0103-6351',
            'pid_v2': None,
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
            'scielo_issn': '0103-6351',
            'pid_v2': None,
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
            'scielo_issn': '1516-3598',
            'pid_v2': None,
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
            'scielo_issn': '0103-6351',
            'pid_v2': None,
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
            'scielo_issn': '0103-6351',
            'pid_v2': None,
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
            'scielo_issn': '0103-6351',
            'pid_v2': None,
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
            'scielo_issn': '1516-3598',
            'pid_v2': None,
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
        url = '/citation/export/5ySvRy7VFTxsKLt35Mwsm9g/?format=bib'
        expected = {
            'scielo_issn': '0103-6351',
            'pid_v2': None,
            'pid_v3': '5ySvRy7VFTxsKLt35Mwsm9g',
            'media_format': MEDIA_FORMAT_HTML,
            'media_language': 'en',
            'content_type': CONTENT_TYPE_CITATION_EXPORT,
        }
        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACSite)
        self.assertDictEqual(obtained, expected)
