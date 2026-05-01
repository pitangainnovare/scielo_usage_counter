import unittest

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.translator.classic import URLTranslatorClassicSite
from scielo_usage_counter.values import (
    MEDIA_FORMAT_HTML,
    MEDIA_FORMAT_PDF,
    MEDIA_FORMAT_XML,
    CONTENT_TYPE_FULL_TEXT,
    CONTENT_TYPE_ABSTRACT,
    CONTENT_TYPE_CITATION_EXPORT,
    CONTENT_TYPE_HOW_TO_CITE,
    CONTENT_TYPE_REFERENCES_LIST,
    CONTENT_TYPE_TRANSLATE_DOCUMENT,
    CONTENT_TYPE_UNDEFINED,
)


class TestTranslatorClassic(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.journals_metadata = [
            {
                'acronym': 'wimj',
                'scielo_issn': '0043-3144',
                'issns': ['0043-3144',],
                'title': 'West Indian Medical Journal',
                'publisher_name': 'The University of the West Indies',
                'subject_areas': ['Health Sciences',],
                'wos_subject_areas': ['HEALTH CARE SCIENCES & SERVICES',]
            },
            {
                'acronym': 'amc',
                'scielo_issn': '0001-6002',
                'issns': ['0001-6002',],
                'title': 'Acta Médica Costarricense',                
            }
        ]
        self.articles_metadata = [
            {
                'pid_v2': 'S0043-31442017000600634',
                'default_lang': 'en',
                'text_langs': ['en', 'es'],
                'scielo_issn': '0043-3144',
                'publication_year': '2017',
                'files': [
                    {'doi': '10.7727/wimj.2014.321', 'lang': 'en', 'path': 'pdf/wimj/v66n6/2309-5830-wimj-66-06-0634.pdf', 'checked': False},
                    {'doi': '10.7727/wimj.2014.321', 'lang': 'es', 'path': 'pdf/wimj/v66n6/es_2309-5830-wimj-66-06-0588.pdf', 'checked': False}
                ]
            },
            {
                'pid_v2': 'S0001-60022024000100008',
                'default_lang': 'en',
                'text_langs': ['en', 'es'],
                'scielo_issn': '0001-6002',
                'publication_year': '2024',
                'files': [
                    {'lang': 'ee', 'path': '/pdf/amc/v66n1/0001-6002-amc-66-01-8.pdf', 'checked': False},
                ]
            }
        ]
        self.tm = URLTranslationManager(self.journals_metadata, self.articles_metadata)

    def test_translate_classic_site_url_scielo_php_script_sci_arttext_with_pid_and_tlng(self):
        url = 'https://westindies.scielo.org/scielo.php?script=sci_arttext&pid=S0043-31442017000600634&tlng=en'

        expected = {}
        expected['journal_acronym'] = 'wimj'
        expected['journal_main_title'] = 'West Indian Medical Journal'
        expected['journal_publisher_name'] = 'The University of the West Indies'
        expected['journal_subject_area_capes'] = ['Health Sciences']
        expected['journal_subject_area_wos'] = ['HEALTH CARE SCIENCES & SERVICES']
        expected['year_of_publication'] = '2017'
        expected['pid_v2'] = 'S0043-31442017000600634'
        expected['scielo_issn'] = '0043-3144'
        expected['media_format'] = MEDIA_FORMAT_HTML
        expected['media_language'] = 'en'
        expected['content_type'] = CONTENT_TYPE_FULL_TEXT

        obtained = self.tm.translate(url)

        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_url_scielo_php_script_sci_arttext_with_pid_tlng_and_extra_params(self):
        url = 'https://westindies.scielo.org/scielo.php?script=sci_arttext&pid=S0043-31442017000600634&lng=en&nrm=iso&tlng=en'
        expected = {}
        expected['journal_acronym'] = 'wimj'
        expected['journal_main_title'] = 'West Indian Medical Journal'
        expected['journal_publisher_name'] = 'The University of the West Indies'
        expected['journal_subject_area_capes'] = ['Health Sciences']
        expected['journal_subject_area_wos'] = ['HEALTH CARE SCIENCES & SERVICES']
        expected['year_of_publication'] = '2017'
        expected['pid_v2'] = 'S0043-31442017000600634'
        expected['scielo_issn'] = '0043-3144'
        expected['media_format'] = MEDIA_FORMAT_HTML
        expected['media_language'] = 'en'
        expected['content_type'] = CONTENT_TYPE_FULL_TEXT

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
        
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_url_pdf_path(self):
        url = 'https://westindies.scielo.org/pdf/wimj/v66n6/2309-5830-wimj-66-06-0634.pdf'
        
        expected = {}
        expected['journal_acronym'] = 'wimj'
        expected['journal_main_title'] = 'West Indian Medical Journal'
        expected['journal_publisher_name'] = 'The University of the West Indies'
        expected['journal_subject_area_capes'] = ['Health Sciences']
        expected['journal_subject_area_wos'] = ['HEALTH CARE SCIENCES & SERVICES']
        expected['year_of_publication'] = '2017'
        expected['pid_v2'] = 'S0043-31442017000600634'
        expected['scielo_issn'] = '0043-3144'
        expected['media_format'] = MEDIA_FORMAT_PDF
        expected['media_language'] = 'en'
        expected['content_type'] = CONTENT_TYPE_FULL_TEXT

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
        
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_url_scieloorg_php_article_xml_with_pid_and_tlng(self):
        url = 'http://westindies.scielo.org/scieloOrg/php/articleXML.php?pid=S0043-31442017000600634&tlng=en'
        
        expected = {}
        expected['journal_acronym'] = 'wimj'
        expected['journal_main_title'] = 'West Indian Medical Journal'
        expected['journal_publisher_name'] = 'The University of the West Indies'
        expected['journal_subject_area_capes'] = ['Health Sciences']
        expected['journal_subject_area_wos'] = ['HEALTH CARE SCIENCES & SERVICES']
        expected['year_of_publication'] = '2017'
        expected['pid_v2'] = 'S0043-31442017000600634'
        expected['scielo_issn'] = '0043-3144'
        expected['media_format'] = MEDIA_FORMAT_XML
        expected['media_language'] = 'en'
        expected['content_type'] = CONTENT_TYPE_FULL_TEXT

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
        
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_url_scielo_php_script_sci_abstract_with_pid_and_tlng(self):
        url = 'https://westindies.scielo.org/scielo.php?script=sci_abstract&pid=S0043-31442017000600634&tlng=es'
        
        expected = {}
        expected['journal_acronym'] = 'wimj'
        expected['journal_main_title'] = 'West Indian Medical Journal'
        expected['journal_publisher_name'] = 'The University of the West Indies'
        expected['journal_subject_area_capes'] = ['Health Sciences']
        expected['journal_subject_area_wos'] = ['HEALTH CARE SCIENCES & SERVICES']
        expected['year_of_publication'] = '2017'
        expected['pid_v2'] = 'S0043-31442017000600634'
        expected['scielo_issn'] = '0043-3144'
        expected['media_format'] = MEDIA_FORMAT_HTML
        expected['media_language'] = 'es'
        expected['content_type'] = CONTENT_TYPE_ABSTRACT

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
        
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_url_scielo_php_script_sci_abstract_with_pid_and_tlng_invalid_value(self):
        # Invalid value `de` for tlng
        url = 'https://westindies.scielo.org/scielo.php?script=sci_abstract&pid=S0043-31442017000600634&tlng=de'
        
        expected = {}
        expected['journal_acronym'] = 'wimj'
        expected['journal_main_title'] = 'West Indian Medical Journal'
        expected['journal_publisher_name'] = 'The University of the West Indies'
        expected['journal_subject_area_capes'] = ['Health Sciences']
        expected['journal_subject_area_wos'] = ['HEALTH CARE SCIENCES & SERVICES']
        expected['year_of_publication'] = '2017'
        expected['pid_v2'] = 'S0043-31442017000600634'
        expected['scielo_issn'] = '0043-3144'
        expected['media_format'] = MEDIA_FORMAT_HTML
        expected['content_type'] = CONTENT_TYPE_ABSTRACT

        # The media_language should default to 'en' because the value of tlng is invalid
        expected['media_language'] = 'en'

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
        
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_url_scielo_php_script_sci_abstract_with_pid_tlng_and_extra_params(self):
        url = 'https://westindies.scielo.org/scielo.php?script=sci_abstract&pid=S0043-31442017000600634&lng=en&nrm=iso&tlng=es'
        
        expected = {}
        expected['journal_acronym'] = 'wimj'
        expected['journal_main_title'] = 'West Indian Medical Journal'
        expected['journal_publisher_name'] = 'The University of the West Indies'
        expected['journal_subject_area_capes'] = ['Health Sciences']
        expected['journal_subject_area_wos'] = ['HEALTH CARE SCIENCES & SERVICES']
        expected['year_of_publication'] = '2017'
        expected['pid_v2'] = 'S0043-31442017000600634'
        expected['scielo_issn'] = '0043-3144'
        expected['media_format'] = MEDIA_FORMAT_HTML
        expected['media_language'] = 'es'
        expected['content_type'] = CONTENT_TYPE_ABSTRACT

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)
        
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_content_type_is_abstract(self):
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
                    'journal_acronym': 'wimj',
                    'journal_main_title': 'West Indian Medical Journal',
                    'journal_publisher_name': 'The University of the West Indies',
                    'journal_subject_area_capes': ['Health Sciences'],
                    'journal_subject_area_wos': ['HEALTH CARE SCIENCES & SERVICES'],
                    'year_of_publication': '2017',
                    'scielo_issn': '0043-3144',
                    'pid_v2': 'S0043-31442017000600634',
                    'media_format': MEDIA_FORMAT_HTML,
                    'media_language': 'en',
                    'content_type': CONTENT_TYPE_ABSTRACT,
                }
                self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_content_type_is_full_text(self):
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
                    'journal_acronym': 'wimj',
                    'journal_main_title': 'West Indian Medical Journal',
                    'journal_publisher_name': 'The University of the West Indies',
                    'journal_subject_area_capes': ['Health Sciences'],
                    'journal_subject_area_wos': ['HEALTH CARE SCIENCES & SERVICES'],
                    'year_of_publication': '2017',
                    'scielo_issn': '0043-3144',
                    'pid_v2': 'S0043-31442017000600634',
                    'media_format': MEDIA_FORMAT_HTML if 'sci_arttext' in url else MEDIA_FORMAT_PDF if 'pdf' in url else MEDIA_FORMAT_XML,
                    'media_language': 'en',
                    'content_type': CONTENT_TYPE_FULL_TEXT,
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
                    'media_format': MEDIA_FORMAT_HTML,
                    'media_language': 'un',
                    'content_type': CONTENT_TYPE_UNDEFINED,
                }
                self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_content_type_is_how_to_cite(self):
        url = 'scielo.php?script=sci_isoref&pid=S0001-60022024000100008&lng=en&tlng=es'

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)

        expected = {
            'journal_acronym': 'amc',
            'journal_main_title': 'Acta Médica Costarricense',
            'year_of_publication': '2024',
            'scielo_issn': '0001-6002',
            'pid_v2': 'S0001-60022024000100008',
            'media_format': MEDIA_FORMAT_HTML,
            'media_language': 'es',
            'content_type': CONTENT_TYPE_HOW_TO_CITE,
        }
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_content_type_is_citation_export(self):
        url = '/scielo.php?download&format=EndNote&pid=S0001-60022024000100008'

        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)

        expected = {
            'journal_acronym': 'amc',
            'journal_main_title': 'Acta Médica Costarricense',
            'year_of_publication': '2024',
            'scielo_issn': '0001-6002',
            'pid_v2': 'S0001-60022024000100008',
            'media_format': MEDIA_FORMAT_HTML,
            'media_language': 'en',
            'content_type': CONTENT_TYPE_CITATION_EXPORT,
        }
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_content_type_is_references_list(self):
        url = '/scieloOrg/php/reference.php?pid=S0001-60022024000100008&caller=www.scielo.sa.cr&lang=en'
        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)

        expected = {
            'journal_acronym': 'amc',
            'journal_main_title': 'Acta Médica Costarricense',
            'year_of_publication': '2024',
            'scielo_issn': '0001-6002',
            'pid_v2': 'S0001-60022024000100008',
            'media_format': MEDIA_FORMAT_HTML,
            'media_language': 'en',
            'content_type': CONTENT_TYPE_REFERENCES_LIST,
        }
        self.assertDictEqual(obtained, expected)

    def test_translate_classic_site_content_type_is_translate(self):
        url = '/scieloOrg/php/translate.php?pid=S0001-60022024000100008&caller=www.scielo.sa.cr&lang=en&tlang=es&script=sci_arttext'
        obtained = self.tm.translate(url)
        self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)

        expected = {
            'journal_acronym': 'amc',
            'journal_main_title': 'Acta Médica Costarricense',
            'year_of_publication': '2024',
            'scielo_issn': '0001-6002',
            'pid_v2': 'S0001-60022024000100008',
            'media_format': MEDIA_FORMAT_HTML,
            'media_language': 'en',
            'content_type': CONTENT_TYPE_TRANSLATE_DOCUMENT,
        }
        self.assertDictEqual(obtained, expected)
