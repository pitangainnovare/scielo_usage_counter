import unittest

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.translator.opac_alpha import URLTranslatorOPACAlphaSite


class TestTranslatorOPACAlpha(unittest.TestCase):
    def setUp(self):
        self.journals_metadata = [
            {
                'acronym': 'resp',
                'scielo_issn': '2965-3827',
                'issns': ['2965-3827',],
                'title': 'Revista de Epidemiologia e Saúde Pública',
            },
            {
                'acronym': 'psoc',
                'scielo_issn': '1807-0310',
                'issns': ['1807-0310',],
                'title': 'Psicologia & Sociedade',
            },
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
                'pid_v3': '',
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

    def test_issn_html(self):
        for url in [
            "article/resp/2009.v83n1/109-121/es/",
            "/article/resp/2009.v83n1/109-121/es/",
        ]:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertEqual(result['scielo_issn'], '2965-3827')
                self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_issn_pdf(self):
        for url in [
            "pdf/resp/2001.v75n5/459-466/es",
            "/pdf/resp/2001.v75n5/459-466/es",
        ]:
            with self.subTest(url=url):
                result = self.tm.translate(url)
                self.assertEqual(result['scielo_issn'], '2965-3827')
                self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_issn_pdf_with_language(self):
        url = "pdf/psoc/v37n2/en_7890-1234-psoc-37-02-0789.pdf"
        result = self.tm.translate(url)
        self.assertEqual(result['scielo_issn'], '1807-0310')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_issn_undefined_file(self):
        url = "media/assets/neco/2021/v29n3/unknown_file.xyz"
        result = self.tm.translate(url)
        self.assertEqual(result['scielo_issn'], '0103-6351')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_issn_html_with_language(self):
        url = "article/wimj/2017/v66n6/es"
        result = self.tm.translate(url)
        self.assertEqual(result['scielo_issn'], '0043-3144')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_issn_pdf_with_default_language(self):
        url = "pdf/neco/v29n3/1234-5678-neco-29-03-0123.pdf"
        result = self.tm.translate(url)
        self.assertEqual(result['scielo_issn'], '0103-6351')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_media_language_html(self):
        url = "article/psoc/2019/v37n2/es"
        result = self.tm.translate(url)
        self.assertEqual(result['media_language'], 'es')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_media_language_pdf(self):
        url = "pdf/rbz/v47n4/5678-1234-rbz-47-04-0456.pdf"
        result = self.tm.translate(url)
        self.assertEqual(result['media_language'], 'en')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_media_language_pdf_with_language(self):
        url = "pdf/psoc/v37n2/en_7890-1234-psoc-37-02-0789.pdf"
        result = self.tm.translate(url)
        self.assertEqual(result['media_language'], 'en')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_media_language_undefined(self):
        url = "media/assets/neco/2021/v29n3/unknown_file.xyz"
        result = self.tm.translate(url)
        self.assertIsNone(result['media_language'])
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_media_language_html_with_default_language(self):
        url = "article/neco/2021/v29n3"
        result = self.tm.translate(url)
        self.assertEqual(result['media_language'], 'pt')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_media_language_pdf_with_default_language(self):
        url = "pdf/neco/v29n3/1234-5678-neco-29-03-0123.pdf"
        result = self.tm.translate(url)
        self.assertEqual(result['media_language'], 'pt')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_media_format_html(self):
        url = "article/psoc/2019/v37n2/en"
        result = self.tm.translate(url)
        self.assertEqual(result['media_format'], 'html')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_media_format_pdf(self):
        url = "pdf/rbz/v47n4/5678-1234-rbz-47-04-0456.pdf"
        result = self.tm.translate(url)
        self.assertEqual(result['media_format'], 'pdf')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_media_format_pdf_with_language(self):
        url = "pdf/psoc/v37n2/en_7890-1234-psoc-37-02-0789.pdf"
        result = self.tm.translate(url)
        self.assertEqual(result['media_format'], 'pdf')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_media_format_undefined(self):
        url = "media/assets/neco/2021/v29n3/unknown_file.xyz"
        result = self.tm.translate(url)
        self.assertIsNone(result['media_format'])
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_media_format_html_with_language(self):
        url = "article/wimj/2017/v66n6/es"
        result = self.tm.translate(url)
        self.assertEqual(result['media_format'], 'html')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_pid_v3_html(self):
        url = "article/psoc/2019/v37n2/es"
        result = self.tm.translate(url)
        self.assertEqual(result['pid_v3'], 'psoc:2019:v37n2:es')
        self.assertEqual(result['scielo_issn'], '1807-0310')
        self.assertEqual(result['media_format'], 'html')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_pid_v3_pdf(self):
        url = "pdf/rbz/v47n4/5678-1234-rbz-47-04-0456.pdf"
        result = self.tm.translate(url)
        self.assertEqual(result['pid_v3'], 'rbz:2020:v47n4:5678-1234-rbz-47-04-0456')
        self.assertEqual(result['scielo_issn'], '1516-3598')
        self.assertEqual(result['media_format'], 'pdf')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_pid_v3_pdf_with_language(self):
        url = "pdf/psoc/v37n2/en_7890-1234-psoc-37-02-0789.pdf"
        result = self.tm.translate(url)
        self.assertEqual(result['pid_v3'], 'psoc:2019:v37n2:7890-1234-psoc-37-02-0789')
        self.assertEqual(result['media_language'], 'en')
        self.assertEqual(result['scielo_issn'], '1807-0310')
        self.assertEqual(result['media_format'], 'pdf')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_pid_v3_undefined_file(self):
        url = "media/assets/neco/2021/v29n3/unknown_file.xyz"
        result = self.tm.translate(url)
        self.assertEqual(result['pid_v3'], 'neco:2021:v29n3:unknown_file.xyz')
        self.assertEqual(result['scielo_issn'], '0103-6351')
        self.assertIsNone(result['media_format'])
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_content_type_html(self):
        url = "article/wimj/2017/v66n6/en"
        result = self.tm.translate(url)
        self.assertEqual(result['media_format'], 'html')
        self.assertEqual(result['scielo_issn'], '0043-3144')
        self.assertEqual(result['pid_v3'], 'wimj:2017:v66n6:en')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_content_type_pdf(self):
        url = "pdf/wimj/2017/v66n6/2309-5830-wimj-66-06-0634.pdf"
        result = self.tm.translate(url)
        self.assertEqual(result['media_format'], 'pdf')
        self.assertEqual(result['scielo_issn'], '0043-3144')
        self.assertEqual(result['pid_v3'], 'wimj:2017:v66n6:2309-5830-wimj-66-06-0634')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_content_type_pdf_with_language(self):
        url = "pdf/neco/v29n3/en_1234-5678-neco-29-03-0123.pdf"
        result = self.tm.translate(url)
        self.assertEqual(result['media_format'], 'pdf')
        self.assertEqual(result['media_language'], 'en')
        self.assertEqual(result['scielo_issn'], '0103-6351')
        self.assertEqual(result['pid_v3'], 'neco:2021:v29n3:1234-5678-neco-29-03-0123')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_content_type_undefined(self):
        url = "media/assets/wimj/2017/v66n6/unknown_file.xyz"
        result = self.tm.translate(url)
        self.assertIsNone(result['media_format'])
        self.assertEqual(result['scielo_issn'], '0043-3144')
        self.assertEqual(result['pid_v3'], 'wimj:2017:v66n6:unknown_file.xyz')
        self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)