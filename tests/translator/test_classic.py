import unittest

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.translator.classic import URLTranslatorClassicSite


class TestTranslatorClassic(unittest.TestCase):
    def setUp(self):
        self.journals_metadata = [
            {
                'acronym': 'wimj',
                'scielo_issn': '0043-3144',
                'issns': ['0043-3144',],
                'title': 'West Indian Medical Journal',
                'publisher_name': 'The University of the West Indies',
                'subject_areas': ['Health Sciences',],
                'wos_subject_areas': ['HEALTH CARE SCIENCES & SERVICES',]
            }, {
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
                'pid_v2': 'S0043-31442017000600634',
                'pid_v3': None,
                'default_lang': 'en',
                'text_langs': ['en', 'es'],
                'scielo_issn': '0043-3144',
                'publication_year': '2017',
                'pdfs': [
                    {'doi': '10.7727/wimj.2014.321', 'lang': 'en', 'path': 'pdf/wimj/v66n6/2309-5830-wimj-66-06-0634.pdf', 'checked': False},
                    {'doi': '10.7727/wimj.2014.321', 'lang': 'es', 'path': 'pdf/wimj/v66n6/es_2309-5830-wimj-66-06-0588.pdf', 'checked': False}
                ]
            },
            {
                'pid_v2': '',
                'pid_v3': '5ySvRy7VFTxsKLt35Mwsm9g',
                'default_lang': 'en',
                'text_langs': ['en', 'es'],
                'scielo_issn': '0043-3144',
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

    def test_translate_classic_site_url_scielo_php_script_sci_arttext_with_pid_and_tlng(self):
        url = 'https://westindies.scielo.org/scielo.php?script=sci_arttext&pid=S0043-31442017000600634&tlng=en'

        expected = {}
        expected['pid_v2'] = 'S0043-31442017000600634'
        expected['pid_v3'] = None
        expected['scielo_issn'] = '0043-3144'
        expected['media_format'] = 'html'
        expected['media_language'] = 'en'
        expected['content_type'] = 'request'

        obtained = self.tm.translate(url)

        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_url_scielo_php_script_sci_arttext_with_pid_tlng_and_extra_params(self):
        url = 'https://westindies.scielo.org/scielo.php?script=sci_arttext&pid=S0043-31442017000600634&lng=en&nrm=iso&tlng=en'
        expected = {}
        expected['pid_v2'] = 'S0043-31442017000600634'
        expected['pid_v3'] = None
        expected['scielo_issn'] = '0043-3144'
        expected['media_format'] = 'html'
        expected['media_language'] = 'en'
        expected['content_type'] = 'request'

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
        
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_url_pdf_path(self):
        url = 'https://westindies.scielo.org/pdf/wimj/v66n6/2309-5830-wimj-66-06-0634.pdf'
        
        expected = {}
        expected['pid_v2'] = 'S0043-31442017000600634'
        expected['pid_v3'] = None
        expected['scielo_issn'] = '0043-3144'
        expected['media_format'] = 'pdf'
        expected['media_language'] = 'en'
        expected['content_type'] = 'request'

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
        
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_url_scieloorg_php_article_xml_with_pid_and_tlng(self):
        url = 'http://westindies.scielo.org/scieloOrg/php/articleXML.php?pid=S0043-31442017000600634&tlng=en'
        
        expected = {}
        expected['pid_v2'] = 'S0043-31442017000600634'
        expected['pid_v3'] = None
        expected['scielo_issn'] = '0043-3144'
        expected['media_format'] = 'xml'
        expected['media_language'] = 'en'
        expected['content_type'] = 'request'

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
        
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_url_scielo_php_script_sci_abstract_with_pid_and_tlng(self):
        url = 'https://westindies.scielo.org/scielo.php?script=sci_abstract&pid=S0043-31442017000600634&tlng=es'
        
        expected = {}
        expected['pid_v2'] = 'S0043-31442017000600634'
        expected['pid_v3'] = None
        expected['scielo_issn'] = '0043-3144'
        expected['media_format'] = 'html'
        expected['media_language'] = 'es'
        expected['content_type'] = 'investigation'

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
        
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_url_scielo_php_script_sci_abstract_with_pid_and_tlng_invalid_value(self):
        # Invalid value `de` for tlng
        url = 'https://westindies.scielo.org/scielo.php?script=sci_abstract&pid=S0043-31442017000600634&tlng=de'
        
        expected = {}
        expected['pid_v2'] = 'S0043-31442017000600634'
        expected['pid_v3'] = None
        expected['scielo_issn'] = '0043-3144'
        expected['media_format'] = 'html'
        expected['content_type'] = 'investigation'

        # The media_language should default to 'en' because the value of tlng is invalid
        expected['media_language'] = 'en'

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
        
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_url_scielo_php_script_sci_abstract_with_pid_tlng_and_extra_params(self):
        url = 'https://westindies.scielo.org/scielo.php?script=sci_abstract&pid=S0043-31442017000600634&lng=en&nrm=iso&tlng=es'
        
        expected = {}
        expected['pid_v2'] = 'S0043-31442017000600634'
        expected['pid_v3'] = None
        expected['scielo_issn'] = '0043-3144'
        expected['media_format'] = 'html'
        expected['media_language'] = 'es'
        expected['content_type'] = 'investigation'

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
        
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_content_type_is_investigation(self):
        for url in [
            '/scielo.php?script=sci_abstract&pid=S0043-31442017000600634',
            '/scielo.php?script=sci_abstract&pid=S0043-31442017000600634&tlng=en',
            '/scielo.php?script=sci_abstract&pid=S0043-31442017000600634&tlng=en',
            '/scielo.php?script=sci_abstract&pid=S0043-31442017000600634&lng=en&nrm=iso&tlng=en',
            '/scielo.php?script=sci_abstract&pid=S0043-31442017000600634&lng=en',
        ]:
            with self.subTest(url=url):
                obtained = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
                expected = {
                    'scielo_issn': '0043-3144',
                    'pid_v2': 'S0043-31442017000600634',
                    'pid_v3': None,
                    'media_format': 'html',
                    'media_language': 'en',
                    'content_type': 'investigation',
                }
                self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_content_type_is_request(self):
        for url in [
            '/scielo.php?script=sci_arttext&pid=S0043-31442017000600634',
            '/scielo.php?script=sci_arttext&pid=S0043-31442017000600634&tlng=en',
            '/scielo.php?script=sci_arttext&pid=S0043-31442017000600634&lng=en&nrm=iso&tlng=en',
            '/pdf/wimj/v66n6/2309-5830-wimj-66-06-0634.pdf',
            '/scieloOrg/php/articleXML.php?pid=S0043-31442017000600634',
            '/scieloOrg/php/articleXML.php?pid=S0043-31442017000600634&tlng=en',
        ]:
            with self.subTest(url=url):
                obtained = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
                expected = {
                    'scielo_issn': '0043-3144',
                    'pid_v2': 'S0043-31442017000600634',
                    'pid_v3': None,
                    'media_format': 'html' if 'sci_arttext' in url else 'pdf' if 'pdf' in url else 'xml',
                    'media_language': 'en',
                    'content_type': 'request',
                }
                self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_content_type_is_undefined(self):
        for url in [
            '/scielo.php',
            '/scielo.php?script=unknown_script',
            '/unknown_path',
        ]:
            with self.subTest(url=url):
                obtained = self.tm.translate(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
                expected = {
                    'scielo_issn': None,
                    'pid_v2': '',
                    'pid_v3': None,
                    'media_format': 'html',
                    'media_language': 'un',
                    'content_type': 'und',
                }
                self.assertDictEqual(obtained, expected)
