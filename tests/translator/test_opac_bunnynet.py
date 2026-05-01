import unittest

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.translator.opac_bunnynet import BunnynetOPACBridge
from scielo_usage_counter.values import (
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_PDF,
    CONTENT_TYPE_FULL_TEXT,
)


class TestBunnynetTranslator(unittest.TestCase):
    def setUp(self):
        self.journals_metadata = [
            {
                'acronym': 'neco',
                'scielo_issn': '0103-6351',
                'issns': ['0103-6351'],
                'title': 'Nova Economia',
                'publisher_name': 'Universidade Federal de Minas Gerais',
                'subject_areas': ['Economics'],
                'wos_subject_areas': ['ECONOMICS']
            },
            {
                'acronym': 'psoc',
                'scielo_issn': '1807-0310',
                'issns': ['1807-0310',],
                'title': 'Psicologia & Sociedade',
                'publisher_name': 'Universidade Federal do Rio Grande do Sul',
                'subject_areas': ['Psychology',],
                'wos_subject_areas': ['PSYCHOLOGY, SOCIAL',]
            },
            {
                'acronym': 'rbz',
                'scielo_issn': '1516-3598',
                'issns': ['1516-3598'],
                'title': 'Revista Brasileira de Zootecnia',
                'publisher_name': 'Sociedade Brasileira de Zootecnia',
                'subject_areas': ['Agricultural Sciences'],
                'wos_subject_areas': ['AGRICULTURE, DAIRY & ANIMAL SCIENCE']
            },
        ]
        self.articles_metadata = [
            {
                'pid_v2': '',
                'pid_v3': 'dqLRqnpmnncSmnzMCB8bzPG',
                'default_lang': 'pt',
                'text_langs': ['pt', 'en'],
                'scielo_issn': '0103-6351',
                'publication_year': '2021',
                'files': []
            },
            {
                'pid_v2': '',
                'pid_v3': 'hbSYnTbyNfzxcWT3FpXrL5G',
                'default_lang': 'es',
                'text_langs': ['es', 'en'],
                'scielo_issn': '1807-0310',
                'publication_year': '2019',
                'files': []
            },
            {
                'pid_v2': '',
                'pid_v3': 'cKnLLBn5NnshCX93Y6qYpHv',
                'default_lang': 'en',
                'text_langs': ['en', 'es'],
                'scielo_issn': '1516-3598',
                'publication_year': '2020',
                'files': []
            },
        ]
        self.tm = URLTranslationManager(self.journals_metadata, self.articles_metadata)
    
    def test_bunnynet_translator_article_url(self):
        url = '/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/'
        
        obtained = self.tm.translate(url)
        
        self.assertEqual(obtained['scielo_issn'], '0103-6351')
        self.assertEqual(obtained['pid_v3'], 'dqLRqnpmnncSmnzMCB8bzPG')
        self.assertEqual(obtained['media_format'], MEDIA_FORMAT_HTML)
        self.assertEqual(obtained['media_language'], 'pt')
        self.assertEqual(obtained['content_type'], CONTENT_TYPE_FULL_TEXT)
    
    def test_bunnynet_translator_article_with_lang(self):
        url = '/j/psoc/a/hbSYnTbyNfzxcWT3FpXrL5G/?lang=es'
        
        obtained = self.tm.translate(url)
        
        self.assertEqual(obtained['scielo_issn'], '1807-0310')
        self.assertEqual(obtained['pid_v3'], 'hbSYnTbyNfzxcWT3FpXrL5G')
        self.assertEqual(obtained['media_format'], MEDIA_FORMAT_HTML)
        self.assertEqual(obtained['media_language'], 'es')
        self.assertEqual(obtained['content_type'], CONTENT_TYPE_FULL_TEXT)
    
    def test_bunnynet_translator_pdf_url(self):
        url = '/j/rbz/a/cKnLLBn5NnshCX93Y6qYpHv/?format=pdf'
        
        obtained = self.tm.translate(url)
        
        self.assertEqual(obtained['scielo_issn'], '1516-3598')
        self.assertEqual(obtained['pid_v3'], 'cKnLLBn5NnshCX93Y6qYpHv')
        self.assertEqual(obtained['media_format'], MEDIA_FORMAT_PDF)
        self.assertEqual(obtained['media_language'], 'en')
        self.assertEqual(obtained['content_type'], CONTENT_TYPE_FULL_TEXT)


if __name__ == '__main__':
    unittest.main()
