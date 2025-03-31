import unittest

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.translator.dataverse import URLTranslatorDataverseSite
from scielo_usage_counter.values import (
    MEDIA_FORMAT_DATAVERSE,
    MEDIA_FORMAT_HTML,
    MEDIA_LANGUAGE_UNDEFINED,
    CONTENT_TYPE_ABSTRACT,
    CONTENT_TYPE_FULL_TEXT,
    DEFAULT_SCIELO_ISSN,
)


class TestTranslatorDataverse(unittest.TestCase):
    def setUp(self):
        self.journals_metadata = []
        self.articles_metadata = [
            {
                'pid_generic': 'DOI:10.48331/SCIELODATA.C5OLYQ',
                'publication_date': '2023-01-01',
                'files': {
                    '12530': {
                        'url': '',
                        'name': '',
                    }
                }

            },
            {
                'pid_generic': 'DOI:10.48331/SCIELODATA.FYC8LU',
                'publication_date': '2023-02-01',
                'files': {}
            },
            {
                'pid_generic': 'DOI:10.48331/SCIELODATA.XEOF5P',
                'publication_date': '2023-03-01',
                'files': {
                    "10310": {
                        "url": "https://data.scielo.org/api//access/datafile/10310",
                        "name": "README.txt"
                    }
                }
            },
            {
                'pid_generic': '10.48331/scielodata.ITBXPQ',
                'publication_date': '2024-02-21',
                'files': {
                    "9370": {
                        "url": "https://data.scielo.org/api//access/datafile/9370", 
                        "name": "Mapeamento_de_iniciativas_de_Direito_constitucional_comparado_no_Brasil.xlsx"
                    }, 
                    "10310": {
                        "url": "https://data.scielo.org/api//access/datafile/10310", 
                        "name": "README.txt"
                    }
                }
            },
            {
                'pid_generic': '10.48331/scielodata.YFA97N',
                'publication_date': '2024-11-21',
                'files': {
                    "11944": {
                        "url": "https://data.scielo.org/api//access/datafile/11944", 
                        "name": "PB_PARECER_CONSUBSTANCIADO_CEP_5654303.pdf"
                    }, 
                    "12245": {
                        "url": "https://data.scielo.org/api//access/datafile/12245", 
                        "name": "README.docx"
                    }, 
                    "14027": {
                        "url": "https://data.scielo.org/api//access/datafile/14027", 
                        "name": "transcricao_da_roda_de_conversa_e_assembleia.pdf"
                    }, 
                    "14028": {
                        "url": "https://data.scielo.org/api//access/datafile/14028", 
                        "name": "declaracao_termo_autorização.pdf"
                    }
                }
            }
        ]
        self.tm = URLTranslationManager(self.journals_metadata, self.articles_metadata)

    def test_translate_dataverse_site_urls_doi_identifiers(self):
        urls = [l.strip() for l in open('tests/fixtures/urls.dat.txt')]

        expected_ids = set([
            'DOI:10.48331/SCIELODATA.LCXGHX',
            'DOI:10.48331/SCIELODATA.LMAQH9',
            'DOI:10.48331/SCIELODATA.O4CS0B',
            'DOI:10.48331/SCIELODATA.Q3UFVB',
            'DOI:10.48331/SCIELODATA.SYBBUJ',
            'DOI:10.48331/SCIELODATA.025WUA', 
            'DOI:10.48331/SCIELODATA.C5OLYQ',
            'DOI:10.48331/SCIELODATA.1WUQZ5', 
            'DOI:10.48331/SCIELODATA.4IBRYS', 
            'DOI:10.48331/SCIELODATA.5VSHR0', 
            'DOI:10.48331/SCIELODATA.AHD4UG', 
            'DOI:10.48331/SCIELODATA.B4L4S8', 
            'DOI:10.48331/SCIELODATA.BXKHHP', 
            'DOI:10.48331/SCIELODATA.C0OVRZ', 
            'DOI:10.48331/SCIELODATA.C4HFUF', 
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
            'DOI:10.48331/SCIELODATA.IRQIQF', 
            'DOI:10.48331/SCIELODATA.JAZSA3', 
            'DOI:10.48331/SCIELODATA.JQJBE9', 
            'DOI:10.48331/SCIELODATA.MDQAK4', 
            'DOI:10.48331/SCIELODATA.N6A5AT', 
            'DOI:10.48331/SCIELODATA.N8RZ2V', 
            'DOI:10.48331/SCIELODATA.NJ7OML', 
            'DOI:10.48331/SCIELODATA.NWUMDI', 
            'DOI:10.48331/SCIELODATA.O0OVEG', 
            'DOI:10.48331/SCIELODATA.P48MOJ', 
            'DOI:10.48331/SCIELODATA.QRF50O', 
            'DOI:10.48331/SCIELODATA.RZ56KJ', 
            'DOI:10.48331/SCIELODATA.TSZQM9',
            'DOI:10.48331/SCIELODATA.V4R3OK',
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
                obtained_id = self.tm.translate(url).get('pid_generic', '')
                if not obtained_id:
                    continue

                if not obtained_id.startswith('DOI'):
                    continue

                self.assertIn(obtained_id, expected_ids)

    def test_translate_dataverse_site_urls_file_ids(self):
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
                obtained_file_id = self.tm.translate(url).get('file_id', '')
                if not obtained_file_id:
                    continue

                self.assertIn(obtained_file_id, expected_ids)

    def test_translate_dataverse_site_content_type_is_abstract(self):
        for url, identifier, media_format in [
            ('/dataset.xhtml?persistentId=doi:10.48331/scielodata.C5OLYQ/VQRNAW', 'DOI:10.48331/SCIELODATA.C5OLYQ', MEDIA_FORMAT_HTML),
            ('/api/datasets/export?exporter=Datacite&persistentId=doi%3A10.48331/scielodata.FYC8LU', 'DOI:10.48331/SCIELODATA.FYC8LU', MEDIA_FORMAT_HTML),
            ('/api/datasets/:persistentId?persistentId=doi:10.48331/scielodata.XEOF5P', 'DOI:10.48331/SCIELODATA.XEOF5P', MEDIA_FORMAT_HTML),
        ]:
            with self.subTest(url=url):
                obtained = self.tm.translate(url)
                expected = {
                    'scielo_issn': DEFAULT_SCIELO_ISSN,
                    'pid_v2': None,
                    'pid_v3': None,
                    'file_id': None,
                    'pid_generic': identifier,
                    'content_type': CONTENT_TYPE_ABSTRACT,
                    'media_format': media_format,
                    'media_language': 'un',
                }
                self.assertDictEqual(obtained, expected)
                self.assertIsInstance(self.tm.translator, URLTranslatorDataverseSite)

    def test_translate_dataverse_site_media_format_is_dataverse(self):
        for url, file_id, identifier in [
            ('/api/access/datafile/12530;jsessionid=10f3dcfc6fc3781167757d5156bc?imageThumb=true&pfdrid_c=true', '12530', 'DOI:10.48331/SCIELODATA.C5OLYQ'),
            ('/file.xhtml?persistentId=doi:10.48331/scielodata.SYBBUJ/WYQQ54', None, 'DOI:10.48331/SCIELODATA.SYBBUJ'),
        ]:
            with self.subTest(url=url):
                obtained = self.tm.translate(url)
                expected = {
                    'scielo_issn': DEFAULT_SCIELO_ISSN,
                    'pid_v2': None,
                    'pid_v3': None,
                    'file_id': file_id,
                    'pid_generic': identifier,
                    'content_type': CONTENT_TYPE_FULL_TEXT,
                    'media_format': MEDIA_FORMAT_DATAVERSE,
                    'media_language': MEDIA_LANGUAGE_UNDEFINED,
                }
                self.assertDictEqual(obtained, expected)
                self.assertIsInstance(self.tm.translator, URLTranslatorDataverseSite)

    def test_translate_dataverse_site_identifier_is_not_doi(self):
        for url, identifier in [
            ('/api/access/datafile/12530;jsessionid=10f3dcfc6fc3781167757d5156bc?imageThumb=true&pfdrid_c=true', 'DOI:10.48331/SCIELODATA.C5OLYQ'),
        ]:
            with self.subTest(url=url):
                obtained = self.tm.translate(url)
                expected = {
                    'scielo_issn': DEFAULT_SCIELO_ISSN,
                    'pid_v2': None,
                    'pid_v3': None,
                    'file_id': '12530',
                    'pid_generic': identifier,
                    'content_type': CONTENT_TYPE_FULL_TEXT,
                    'media_format': MEDIA_FORMAT_DATAVERSE,
                    'media_language': MEDIA_LANGUAGE_UNDEFINED,
                }
                self.assertDictEqual(obtained, expected)
                self.assertIsInstance(self.tm.translator, URLTranslatorDataverseSite)

    def test_translate_dataverse_site_content_type_is_full_text(self):
        for url, file_id, identifier in [
            ('/api/access/datafile/12530;jsessionid=10f3dcfc6fc3781167757d5156bc?imageThumb=true&pfdrid_c=true', '12530', 'DOI:10.48331/SCIELODATA.C5OLYQ'),
            ('/file.xhtml?persistentId=doi:10.48331/scielodata.SYBBUJ/WYQQ54', None, 'DOI:10.48331/SCIELODATA.SYBBUJ'),
        ]:
            with self.subTest(url=url):
                obtained = self.tm.translate(url)
                expected = {
                    'scielo_issn': DEFAULT_SCIELO_ISSN,
                    'pid_v2': None,
                    'pid_v3': None,
                    'file_id': file_id,
                    'pid_generic': identifier,
                    'content_type': CONTENT_TYPE_FULL_TEXT,
                    'media_format': MEDIA_FORMAT_DATAVERSE,
                    'media_language': MEDIA_LANGUAGE_UNDEFINED,
                }
                self.assertDictEqual(obtained, expected)
                self.assertIsInstance(self.tm.translator, URLTranslatorDataverseSite)
