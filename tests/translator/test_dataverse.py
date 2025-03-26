import unittest

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.translator.dataverse import URLTranslatorDataverseSite


class TestTranslatorDataverse(unittest.TestCase):
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

    def test_translate_dataverse_site_urls_doi_identifiers(self):
        urls = [l.strip() for l in open('tests/fixtures/urls.dat.txt')]

        expected_ids = set([
            'DOI:10.48331/SCIELODATA.025WUA', 
            'DOI:10.48331/SCIELODATA.025WUA/M8KYDB', 
            'DOI:10.48331/SCIELODATA.025WUA/NOZ9HH', 
            'DOI:10.48331/SCIELODATA.1WUQZ5', 
            'DOI:10.48331/SCIELODATA.4IBRYS', 
            'DOI:10.48331/SCIELODATA.5VSHR0', 
            'DOI:10.48331/SCIELODATA.AHD4UG', 
            'DOI:10.48331/SCIELODATA.B4L4S8', 
            'DOI:10.48331/SCIELODATA.BXKHHP', 
            'DOI:10.48331/SCIELODATA.C0OVRZ', 
            'DOI:10.48331/SCIELODATA.C4HFUF', 
            'DOI:10.48331/SCIELODATA.C4HFUF/VKTLCE', 
            'DOI:10.48331/SCIELODATA.C5OLYQ/VQRNAW', 
            'DOI:10.48331/SCIELODATA.CUTEIZ', 
            'DOI:10.48331/SCIELODATA.F7PAP0', 
            'DOI:10.48331/SCIELODATA.FA3YFA', 
            'DOI:10.48331/SCIELODATA.FDIXEJ', 
            'DOI:10.48331/SCIELODATA.FEC3AC', 
            'DOI:10.48331/SCIELODATA.FYC8LU', 
            'DOI:10.48331/SCIELODATA.GG4194', 
            'DOI:10.48331/SCIELODATA.H4WLPB', 
            'DOI:10.48331/SCIELODATA.I22LOU', 
            'DOI:10.48331/SCIELODATA.I7J5JL', 
            'DOI:10.48331/SCIELODATA.IGWTDW', 
            'DOI:10.48331/SCIELODATA.IGWTDW/ANQ2PO', 
            'DOI:10.48331/SCIELODATA.IRQIQF', 
            'DOI:10.48331/SCIELODATA.JAZSA3', 
            'DOI:10.48331/SCIELODATA.JAZSA3/NPTQ0M', 
            'DOI:10.48331/SCIELODATA.JQJBE9', 
            'DOI:10.48331/SCIELODATA.LCXGHX/6U9IHT', 
            'DOI:10.48331/SCIELODATA.LCXGHX/CEQD7D', 
            'DOI:10.48331/SCIELODATA.LCXGHX/GKNHUU', 
            'DOI:10.48331/SCIELODATA.LMAQH9/JBEGIF', 
            'DOI:10.48331/SCIELODATA.MDQAK4', 
            'DOI:10.48331/SCIELODATA.N6A5AT', 
            'DOI:10.48331/SCIELODATA.N8RZ2V', 
            'DOI:10.48331/SCIELODATA.NJ7OML', 
            'DOI:10.48331/SCIELODATA.NJ7OML/8I71PJ', 
            'DOI:10.48331/SCIELODATA.NJ7OML/O6WTVY', 
            'DOI:10.48331/SCIELODATA.NWUMDI', 
            'DOI:10.48331/SCIELODATA.O0OVEG', 
            'DOI:10.48331/SCIELODATA.O4CS0B/XZ8BMN', 
            'DOI:10.48331/SCIELODATA.P48MOJ', 
            'DOI:10.48331/SCIELODATA.Q3UFVB/KHLZHJ', 
            'DOI:10.48331/SCIELODATA.QRF50O', 
            'DOI:10.48331/SCIELODATA.RZ56KJ', 
            'DOI:10.48331/SCIELODATA.SYBBUJ/WYQQ54', 
            'DOI:10.48331/SCIELODATA.TSZQM9', 
            'DOI:10.48331/SCIELODATA.V4R3OK/VUKYLC', 
            'DOI:10.48331/SCIELODATA.VFCFCW', 
            'DOI:10.48331/SCIELODATA.VHHVGB', 
            'DOI:10.48331/SCIELODATA.WPYUK2', 
            'DOI:10.48331/SCIELODATA.XEOF5P', 
            'DOI:10.48331/SCIELODATA.XGVN3X', 
            'DOI:10.48331/SCIELODATA.Y8JBGG', 
            'DOI:10.48331/SCIELODATA.ZADXTC',
        ])

        for url in urls:
            with self.subTest(url=url):
                obtained_id = self.tm.translate(url).get('id', '')
                if not obtained_id:
                    continue

                if not obtained_id.startswith('DOI'):
                    continue

                self.assertIn(obtained_id, expected_ids)

    def test_translate_dataverse_site_urls_number_identifiers(self):
        urls = [l.strip() for l in open('tests/fixtures/urls.dat.txt')]

        expected_ids = set([
            '10105',
            '10107',
            '10108',
            '10109',
            '10113',
            '10114',
            '10217',
            '10218',
            '10222',
            '10223',
            '10224',
            '10225',
            '10227',
            '10287',
            '10343',
            '10610',
            '10613',
            '10614',
            '10615',
            '10617',
            '11807',
            '11808',
            '12528',
            '12529',
            '12530',
            '12531',
            '12532',
            '12533',
            '12534',
            '12561',
            '12574',
            '12596',
            '12609',
            '12627',
            '12669',
            '1846',
            '2255',
            '3052',
            '3054',
            '3418',
            '3419',
            '3420',
            '415',
            '4827',
            '6119',
            '7688',
            '8196',
            '8440',
            '9911',
        ])

        for url in urls:
            with self.subTest(url=url):
                obtained_id = self.tm.translate(url).get('id', '')
                if not obtained_id:
                    continue

                if obtained_id.startswith('DOI'):
                    continue

                self.assertIn(obtained_id, expected_ids)

    def test_translate_dataverse_site_content_type_is_investigation(self):
        for url, identifier in [
            ('/dataset.xhtml?persistentId=doi:10.48331/scielodata.C5OLYQ/VQRNAW', 'DOI:10.48331/SCIELODATA.C5OLYQ/VQRNAW'),
            ('/api/datasets/export?exporter=Datacite&persistentId=doi%3A10.48331/scielodata.FYC8LU', 'DOI:10.48331/SCIELODATA.FYC8LU'),
            ('/api/datasets/:persistentId?persistentId=doi:10.48331/scielodata.XEOF5P', 'DOI:10.48331/SCIELODATA.XEOF5P'),
        ]:
            with self.subTest(url=url):
                obtained = self.tm.translate(url)
                expected = {
                    'scielo_issn': None,
                    'pid_v2': None,
                    'pid_v3': None,
                    'id': identifier,
                    'content_type': 'investigation',
                    'media_format': 'und',
                    'media_language': 'un',
                }
                self.assertDictEqual(obtained, expected)
                self.assertIsInstance(self.tm.translator, URLTranslatorDataverseSite)

    def test_translate_dataverse_site_identifier_is_not_doi(self):
        for url, identifier in [
            ('/api/access/datafile/12530;jsessionid=10f3dcfc6fc3781167757d5156bc?imageThumb=true&pfdrid_c=true', '12530'),
        ]:
            with self.subTest(url=url):
                obtained = self.tm.translate(url)
                expected = {
                    'scielo_issn': None,
                    'pid_v2': None,
                    'pid_v3': None,
                    'id': identifier,
                    'content_type': 'request',
                    'media_format': 'und',
                    'media_language': 'un',
                }
                self.assertDictEqual(obtained, expected)
                self.assertIsInstance(self.tm.translator, URLTranslatorDataverseSite)

    def test_translate_dataverse_site_content_type_is_request(self):
        for url, identifier in [
            ('/api/access/datafile/12530;jsessionid=10f3dcfc6fc3781167757d5156bc?imageThumb=true&pfdrid_c=true', '12530'),
            ('/file.xhtml?persistentId=doi:10.48331/scielodata.SYBBUJ/WYQQ54', 'DOI:10.48331/SCIELODATA.SYBBUJ/WYQQ54'),
        ]:
            with self.subTest(url=url):
                obtained = self.tm.translate(url)
                expected = {
                    'scielo_issn': None,
                    'pid_v2': None,
                    'pid_v3': None,
                    'id': identifier,
                    'content_type': 'request',
                    'media_format': 'und',
                    'media_language': 'un',
                }
                self.assertDictEqual(obtained, expected)
                self.assertIsInstance(self.tm.translator, URLTranslatorDataverseSite)