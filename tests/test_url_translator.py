import unittest

from scielo_usage_counter.values import (
    MEDIA_FORMAT_HTML,
    MEDIA_LANGUAGE_UNDEFINED,
    CONTENT_TYPE_FULL_TEXT,
)

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.translator.classic import URLTranslatorClassicSite
from scielo_usage_counter.translator.books import URLTranslatorBooksSite
from scielo_usage_counter.translator.dataverse import URLTranslatorDataverseSite
from scielo_usage_counter.translator.opac import URLTranslatorOPACSite
from scielo_usage_counter.translator.opac_alpha import URLTranslatorOPACAlphaSite
from scielo_usage_counter.translator.preprints import URLTranslatorPreprintsSite


class TestURLTranslationManager(unittest.TestCase):
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
                'files': [
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
            }
        ]
        self.tm = URLTranslationManager(self.journals_metadata, self.articles_metadata)

    def test_identify_translator_class_is_classic_site(self):
        for url in [
            '/scielo.php?pid=S1981-77462017005002103&script=sci_arttext',
            '/pdf/rem/v63n4/a07v63n4.pdf',
            '/scielo.php?',
            '/scielo.php?script=sci_abstract', 
            '/scielo.php?script=sci_abstract&pid=S0043-31442017000600634',
            '/scielo.php?script=sci_abstract&pid=S0043-31442017000600634&lng=en&nrm=iso&tlng=es',
            '/scielo.php?script=sci_abstract&pid=S0043-31442017000600634&tlng=es', 
            '/scielo.php?script=sci_arttext&pid=S0043-31442017000600634&lng=en&nrm=iso&tlng=en',
            '/scielo.php?script=sci_arttext&pid=S0043-31442017000600634&tlng=en',
            '/scieloOrg/php/articleXML.php?pid=S0043-31442017000600634',
            '/scieloOrg/php/articleXML.php?pid=S0043-31442017000600634&tlng=en',
            'http://westindies.scielo.org/scieloOrg/php/articleXML.php?pid=S0043-31442017000600634',
            'http://westindies.scielo.org/scieloOrg/php/articleXML.php?pid=S0043-31442017000600634&tlng=en',
            'https://westindies.scielo.org/pdf/wimj/v66n6/2309-5830-wimj-66-06-0634.pdf',
            'https://westindies.scielo.org/scielo.php?',
            'https://westindies.scielo.org/scielo.php?script=sci_abstract', 
            'https://westindies.scielo.org/scielo.php?script=sci_abstract&pid=S0043-31442017000600634',
            'https://westindies.scielo.org/scielo.php?script=sci_abstract&pid=S0043-31442017000600634&lng=en&nrm=iso&tlng=es',
            'https://westindies.scielo.org/scielo.php?script=sci_abstract&pid=S0043-31442017000600634&tlng=es', 
            'https://westindies.scielo.org/scielo.php?script=sci_arttext&pid=S0043-31442017000600634&lng=en&nrm=iso&tlng=en',
            'https://westindies.scielo.org/scielo.php?script=sci_arttext&pid=S0043-31442017000600634&tlng=en',
            "/popup/questions_es.html",
            "/popup/whatismyip.php",
            "/scielo.php?pid=S0325-00752005000400013&script=sci_arttext&tlng=pt",
            "/scielo.php?pid=S1668-70272019000200185&script=sci_arttext",
            "/scielo.php?pid=S1668-87082021000100003&script=sci_arttext",
            "/scielo.php?pid=S1692-715X2011000200011&script=sci_arttext",
            "/scielo.php?script=sci_arttext&pid=S0034-74502009000200012",
            "/scielo.php?script=sci_arttext&pid=S0034-98872020000400542",
            "/scielo.php?script=sci_arttext&pid=S0121-07932016000200008",
            "/scielo.php?script=sci_arttext&pid=S0718-48082014000100001",
            "/scielo.php?script=sci_arttext&pid=S0718-48082018000300156",
            "/scielo.php?script=sci_arttext&pid=S1657-70272014000100004",
            "/scielo.php?script=sci_arttext&pid=S1851-17242012000100001",
            "/scielo.php?script=sci_arttext&pid=S1851-56572008000100022&lng=es&tlng=es",
            "/scielo.php?script=sci_arttext&pid=S2452-45492021000300370",
            "/scieloOrg/php/articleXML.php?pid=S1850-20672022000200227&lang=en",
            "/scieloOrg/php/articleXML.php?pid=S1851-00272020000200002&lang=en",
            "/scieloOrg/php/articleXML.php?pid=S1853-001X2019000100001&lang=en",
            "google_metrics/get_h5_m5.php?issn=0120-5307&callback=jsonp1733288396148",
            "google_metrics/get_h5_m5.php?issn=0121-0793&callback=jsonp1733288396020",
            "google_metrics/get_h5_m5.php?issn=1692-715X&callback=jsonp1733288396676",
            "google_metrics/get_h5_m5.php?issn=1851-1724&callback=jsonp1706756408454",
            "google_metrics/get_h5_m5.php?issn=1851-5657&callback=jsonp1706756408224",
            '/pdf/wimj/v66n6/2309-5830-wimj-66-06-0634.pdf',
            "/pdf/psdc/v30n2/v30n2a09.pdf",
            "/pdf/rcre/v25n4/0121-8123-rcre-25-04-00245.pdf",
            "/pdf/reus/v19n2/0124-7107-reus-19-02-00309.pdf",
        ]:
            with self.subTest(url=url):
                self.tm.identify_translator_class(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorClassicSite)

    def test_identify_translator_class_is_opac_alpha_site(self):
        for url in [
            '/article/csc/2025.v30n2/e05402023/pt/?abstract_lang=pt',
            '/article/csc/2025.v30n2/e05402023/pt/',
            '/j/csc/grid',
            '/j/csc/i/2025.v30n2/',
            '/j/ress/',
            'https://www.scielosp.org/article/csc/2025.v30n2/e05402023/pt/',
            'https://www.scielosp.org/j/csc/grid',
            'https://www.scielosp.org/j/csc/i/2025.v30n2/',
            'https://www.scielosp.org/j/ress/',
            'https://www.scielosp.org/pdf/csc/2025.v30n2/e05402023/pt',
            "/article/csp/2022.v38n3/e00095821/",
            "/article/rcsp/2017.v43n3/470-498/es/"
            "/article/rcsp/2017.v43n3/470-498/es/",
            "/article/rcsp/2017.v43n3/470-498/es/",
            "/article/ress/2021.v30nspe1/e2020663/",
            "/article/rpmesp/2018.v35n3/542-543/es/",
            "/article/rpmesp/2023.v40n1/25-33/",
            "/article/rpmesp/2023.v40n3/307-316/",
            "/article/rpsp/1999.v6n3/149-156/",
            "/article/sausoc/2022.v31n1/e200398/",
            "/article/spm/2020.v62n1/114-117/es/",
            "/j/csp/i/2013.v29n6/",
            "article/csc/2010.v15n6/2845-2857/",
            "article/rcsp/2018.v44n4/220-228/es/",
            "article/rpmesp/2022.v39n2/178-184/es/",
            "article/rpmesp/2022.v39n2/178-184/es/",
            "article/rsap/2017.v19n3/374-378/",
            "article/rsap/2017.v19n3/393-395/",
            "article/rsap/2018.v20n5/649-654/",
            "article/scol/2018.v14n2/161-177/es/",
            "article/ssm/content/raw/?resource_ssm_path=/media/assets/rcsp/v38n4/spu08412.pdf",
            "article/ssm/content/raw/?resource_ssm_path=/media/assets/resp/v71n5/recension.pdf",
            "article/ssm/content/raw/?resource_ssm_path=/media/assets/resp/v82n3/colaboracion1.pdf",
            "article/ssm/content/raw/?resource_ssm_path=/media/assets/rpsp/v24n1/v24n1a02.pdf",
            "article/ssm/content/raw/?resource_ssm_path=/media/assets/spm/v42n5/3993.pdf",
            "article/ssm/content/raw/?resource_ssm_path=/media/assets/spm/v43n4/5903.pdf",
            "pdf/rcsp/v40n4/spu02414.pdf",
            "pdf/rpsp/v12n2/11622.pdf",
            "pdf/rpsp/v9n6/5390.pdf",
            "pdf/rsap/v14n5/v14n5a09.pdf",
            "pdf/spm/v53s2/10.pdf",
            '/pdf/csc/2025.v30n2/e05402023/pt',
            'pdf/resp/2001.v75n5/459-466/es',
            '/pdf/resp/2001.v75n5/459-466/es'
        ]:
            with self.subTest(url=url):
                self.tm.identify_translator_class(url)
                if 'j/' in url:
                    # In the case of j/, the are a few URLs that are similar to the ones used in the OPAC site
                    self.assertTrue(
                        isinstance(self.tm.translator, URLTranslatorOPACAlphaSite) or
                        isinstance(self.tm.translator, URLTranslatorOPACSite)
                    )
                else:
                    self.assertIsInstance(self.tm.translator, URLTranslatorOPACAlphaSite)

    def test_loads_source_and_document_contract_for_journal_metadata(self):
        sources_metadata = [
            {
                'source_type': 'journal',
                'source_id': '0103-6351',
                'scielo_issn': '0103-6351',
                'acronym': 'neco',
                'title': 'Nova Economia',
                'issns': {'0103-6351'},
                'publisher_name': ['Universidade Federal de Minas Gerais'],
                'subject_areas': ['Economics'],
                'wos_subject_areas': ['ECONOMICS'],
                'identifiers': {'scielo_issn': '0103-6351'},
            }
        ]
        documents_metadata = [
            {
                'document_type': 'article',
                'document_id': 'dqLRqnpmnncSmnzMCB8bzPG',
                'pid_v3': 'dqLRqnpmnncSmnzMCB8bzPG',
                'default_lang': 'pt',
                'text_langs': ['pt', 'en'],
                'scielo_issn': '0103-6351',
                'publication_year': '2021',
                'source_type': 'journal',
                'source_id': '0103-6351',
                'files': [
                    {'doi': '10.1590/neco.2021.123', 'lang': 'pt', 'path': 'pdf/neco/v29n3/1234-5678-neco-29-03-0123.pdf'},
                ],
            }
        ]

        tm = URLTranslationManager(sources_metadata, documents_metadata)

        self.assertEqual(tm.sources_metadata['issn_to_title']['0103-6351'], 'Nova Economia')
        self.assertEqual(tm.sources_metadata['source_id_to_type']['0103-6351'], 'journal')
        self.assertEqual(tm.documents_metadata['pid_v3_to_default_lang']['dqLRqnpmnncSmnzMCB8bzPG'], 'pt')
        self.assertEqual(tm.documents_metadata['pid_v3_to_scielo_issn']['dqLRqnpmnncSmnzMCB8bzPG'], '0103-6351')

    def test_loads_source_and_document_contract_for_books(self):
        sources_metadata = [
            {
                'source_type': 'book',
                'source_id': 'q7gtd',
                'title': 'Book Title',
                'publication_year': '2023',
                'identifiers': {'book_id': 'q7gtd', 'isbn': '9788578791889'},
            }
        ]
        documents_metadata = [
            {
                'document_type': 'book',
                'document_id': 'book:q7gtd',
                'pid_generic': 'book:q7gtd',
                'default_lang': 'pt',
                'publication_date': '2023-01-01',
                'publication_year': '2023',
                'source_type': 'book',
                'source_id': 'q7gtd',
                'title': 'Book Title',
                'identifiers': {'book_id': 'q7gtd', 'isbn': '9788578791889'},
                'files': {},
            },
            {
                'document_type': 'chapter',
                'document_id': 'book:q7gtd/chapter:03',
                'pid_generic': 'book:q7gtd/chapter:03',
                'default_lang': 'en',
                'publication_date': '2023-01-01',
                'publication_year': '2023',
                'source_type': 'book',
                'source_id': 'q7gtd',
                'title': 'Chapter Title',
                'identifiers': {'book_id': 'q7gtd', 'chapter_id': '03'},
                'files': {},
            },
        ]

        tm = URLTranslationManager(sources_metadata, documents_metadata)
        result = tm.translate('/id/q7gtd/03')

        self.assertIsInstance(tm.translator, URLTranslatorBooksSite)
        self.assertEqual(result['book_title'], 'Book Title')
        self.assertEqual(result['chapter_title'], 'Chapter Title')
        self.assertEqual(result['year_of_publication'], '2023')
        self.assertEqual(result['media_language'], 'en')

    def test_identify_translator_class_is_opac_site(self):
        for url in [
            'https://scielo.br/j/aa/',
            "/j/neco/a/5ySvRy7VFTxsKLt35Mwsm9g/abstract/?lang=en",
            "/j/neco/a/5ySvRy7VFTxsKLt35Mwsm9g/abstract/?lang=pt",
            "/j/neco/a/5ySvRy7VFTxsKLt35Mwsm9g/abstract/?lang=it",
            "/j/neco/a/5ySvRy7VFTxsKLt35Mwsm9g/abstract/?format=xml",
            "/j/neco/a/5ySvRy7VFTxsKLt35Mwsm9g/abstract/?format=pdf",
            "/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/",
            "/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/?lang=en",
            "/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/?lang=pt",
            "/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/?lang=it",
            "/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/?format=xml",
            "/j/neco/a/dqLRqnpmnncSmnzMCB8bzPG/?format=pdf",
            "/j/jiems/a/JJRjZV3MjjdgRWk9JmfPTYd/?lang=en",
            "/j/jiems/a/JJRjZV3MjjdgRWk9JmfPTYd/?lang=pt",
            "/j/jiems/a/JJRjZV3MjjdgRWk9JmfPTYd/?lang=it",
            "/j/jiems/a/JJRjZV3MjjdgRWk9JmfPTYd/?format=xml",
            "/j/jiems/a/JJRjZV3MjjdgRWk9JmfPTYd/?format=pdf",
            "/j/cr/a/CP849wcWRp6y46zCvsyYsCb/?lang=pt",
            "/j/cr/a/CP849wcWRp6y46zCvsyYsCb/?lang=en",
            "/j/cr/a/CP849wcWRp6y46zCvsyYsCb/?lang=it",
            "/j/cr/a/CP849wcWRp6y46zCvsyYsCb/?format=xml",
            "/j/cr/a/CP849wcWRp6y46zCvsyYsCb/?format=pdf",
            "/j/esa/a/TWyHMQBS4H6tyrXPZhcWxps/",
            "/j/esa/a/TWyHMQBS4H6tyrXPZhcWxps/?lang=en",
            "/j/esa/a/TWyHMQBS4H6tyrXPZhcWxps/?lang=pt",
            "/j/esa/a/TWyHMQBS4H6tyrXPZhcWxps/?lang=it",
            "/j/esa/a/TWyHMQBS4H6tyrXPZhcWxps/?format=xml",
            "/j/esa/a/TWyHMQBS4H6tyrXPZhcWxps/?format=pdf",
            "/j/rbz/a/cKnLLBn5NnshCX93Y6qYpHv/abstract/?format=html&lang=en",
            "/j/rbz/a/cKnLLBn5NnshCX93Y6qYpHv/abstract/?format=html&lang=pt",
            "/j/rbz/a/cKnLLBn5NnshCX93Y6qYpHv/abstract/?format=html&lang=it",
            "/j/rbz/a/cKnLLBn5NnshCX93Y6qYpHv/abstract/?format=xml",
            "/j/rbz/a/cKnLLBn5NnshCX93Y6qYpHv/abstract/?format=pdf",
            "/j/psoc/a/9bZdr3zfr5YYtyb3m8c5KZS/?format=html",
            "/j/psoc/a/9bZdr3zfr5YYtyb3m8c5KZS/?format=xml",
            "/j/psoc/a/9bZdr3zfr5YYtyb3m8c5KZS/?format=pdf",
            "/j/psoc/a/hbSYnTbyNfzxcWT3FpXrL5G/?format=html&lang=es",
            "/j/psoc/a/hbSYnTbyNfzxcWT3FpXrL5G/?format=html&lang=en",
            "/j/psoc/a/hbSYnTbyNfzxcWT3FpXrL5G/?format=html&lang=pt",
            "/j/psoc/a/hbSYnTbyNfzxcWT3FpXrL5G/?format=html&lang=it",
            "/j/psoc/a/hbSYnTbyNfzxcWT3FpXrL5G/?format=xml",
            "/j/psoc/a/hbSYnTbyNfzxcWT3FpXrL5G/?format=pdf",
            "/j/asagr/a/msfBCRNfx7wtnLTJ7wTgk7L/abstract/?format=html&lang=en&stop=previous",
            "/j/asagr/a/msfBCRNfx7wtnLTJ7wTgk7L/abstract/?format=html&lang=pt&stop=previous",
            "/j/asagr/a/msfBCRNfx7wtnLTJ7wTgk7L/abstract/?format=html&lang=it&stop=previous",
            "/j/asagr/a/msfBCRNfx7wtnLTJ7wTgk7L/abstract/?format=xml",
            "/j/asagr/a/msfBCRNfx7wtnLTJ7wTgk7L/abstract/?format=pdf",
            "/j/inter/a/kJHmpQkLTrnPCbftkSNncpr/abstract/?lang=en",
            "/j/inter/a/kJHmpQkLTrnPCbftkSNncpr/abstract/?lang=pt",
            "/j/inter/a/kJHmpQkLTrnPCbftkSNncpr/abstract/?lang=it",
            "/j/inter/a/kJHmpQkLTrnPCbftkSNncpr/abstract/?format=xml",
            "/j/inter/a/kJHmpQkLTrnPCbftkSNncpr/abstract/?format=pdf",
            "/citation/export/5ySvRy7VFTxsKLt35Mwsm9g/?format=bib",
            "/article/ssm/content/raw/?resource_ssm_path=/documentstore/1806-9460/YdZ7HCqnBkgxhJRPCmKrxkz/b7e997318152c89988a6aad8b0c541d510f468f6.pdf",
        ]:
            with self.subTest(url=url):
                self.tm.identify_translator_class(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorOPACSite)

    def test_identify_translator_class_is_dataverse_site(self):
        for url in [
            '/dataset.xhtml?persistentId=doi:10.48331/scielodata.KKBWDE',
            '/dataset.xhtml?persistentId=doi:10.48331/scielodata.Q8TJ9N',
            'https://data.scielo.org/dataset.xhtml?persistentId=doi:10.48331/scielodata.KKBWDE',
            'https://data.scielo.org/dataset.xhtml?persistentId=doi:10.48331/scielodata.Q8TJ9N',
            'https://dataverse.scielo.org',
            "/api/dataverses/scielodata"
            "/api/dataverses/scielodata",
            "/dataset.xhtml;jsessionid=a36db12b30413c00ed134d710a70?fileSortField=type&persistentId=doi%3A10.48331%2Fscielodata.0P0QUN",
            "/dataset.xhtml;jsessionid=a36db12b30413c00ed134d710a70?fileSortField=type&persistentId=doi%3A10.48331%2Fscielodata.0P0QUN",
            "/dataset.xhtml;jsessionid=a94eb6d7a2c4e0acadd78746dc9c?fileAccess=Public&fileSortField=size&fileTypeGroupFacet=%22Archive%22&persistentId=doi%3A10.48331%2Fscielodata.0P0QUN",
            "/dataset.xhtml;jsessionid=a94eb6d7a2c4e0acadd78746dc9c?fileAccess=Public&fileSortField=size&fileTypeGroupFacet=%22Archive%22&persistentId=doi%3A10.48331%2Fscielodata.0P0QUN",
            "/dataset.xhtml;jsessionid=bf8c49e2abe6572528588ba0dd85?fileAccess=Public&fileSortField=size&fileTypeGroupFacet=%22Text%22&persistentId=doi%3A10.48331%2Fscielodata.0P0QUN",
            "/dataset.xhtml;jsessionid=c151b1d11582b42e52d190a31b2b?fileTypeGroupFacet=%22Archive%22&persistentId=doi%3A10.48331%2Fscielodata.0P0QUN",
            "/dataset.xhtml;jsessionid=c151b1d11582b42e52d190a31b2b?fileTypeGroupFacet=%22Archive%22&persistentId=doi%3A10.48331%2Fscielodata.0P0QUN",
            "/dataset.xhtml;jsessionid=f0a936613832b917849d84ab7e0b?fileSortField=name&fileSortOrder=desc&persistentId=doi%3A10.48331%2Fscielodata.0P0QUN",
            "/dataset.xhtml;jsessionid=f0a936613832b917849d84ab7e0b?fileSortField=name&fileSortOrder=desc&persistentId=doi%3A10.48331%2Fscielodata.0P0QUN",
            "/dataset.xhtml?persistentId=doi:10.48331/scielodata.A5MQLB",
            "/dataverse/brrbsmi;jsessionid=a7c5559f001800d9805561750dc3",
            "/dataverse/brrbsmi;jsessionid=a7c5559f001800d9805561750dc3",
            "/dataverse/brurbe;jsessionid=eebd9b2f5320007999005dc3d488/?order=asc&page=1&sort=dateSort&types=dataverses%3Adatasets",
            "/dataverse/brurbe;jsessionid=eebd9b2f5320007999005dc3d488/?order=asc&page=1&sort=dateSort&types=dataverses%3Adatasets",
            "/dataverse/preprints;jsessionid=f0ef0816c86fe784cd6f3a79ddd1",
            "/dataverse/preprints;jsessionid=f0ef0816c86fe784cd6f3a79ddd1",
            "/dataverse/scielodata;jsessionid=ad6338c2c497d4e78333870a66dc/?order=desc&page=1&sort=nameSort&types=files%3Adataverses",
            "/dataverse/scielodata;jsessionid=ad6338c2c497d4e78333870a66dc/?order=desc&page=1&sort=nameSort&types=files%3Adataverses",
            "/dataverse/scielodata;jsessionid=c1952523ada61956ecaadc330f8f/?order=asc&page=2&sort=nameSort&types=dataverses%3Adatasets",
            "/dataverse/scielodata;jsessionid=c1952523ada61956ecaadc330f8f/?order=asc&page=2&sort=nameSort&types=dataverses%3Adatasets",
            "/dataverse/scielodata;jsessionid=eb568f3c70a14b67c8c6b83483a0/?order=desc&page=2&sort=dateSort&types=dataverses%3Adatasets",
            "/dataverse/scielodata;jsessionid=eb568f3c70a14b67c8c6b83483a0/?order=desc&page=2&sort=dateSort&types=dataverses%3Adatasets",
            "/dataverse/scielodata;jsessionid=ee9dc5ad63b25d38840c68e5e202/?order=desc&page=53&sort=dateSort&types=dataverses%3Adatasets",
            "/dataverse/scielodata;jsessionid=ee9dc5ad63b25d38840c68e5e202/?order=desc&page=53&sort=dateSort&types=dataverses%3Adatasets",
            "/dataverse/scielodata;jsessionid=ef3c98c0de75e6878155fb57f917/?order=desc&page=1&sort=nameSort&types=dataverses%3Adatasets",
            "/dataverse/scielodata;jsessionid=ef3c98c0de75e6878155fb57f917/?order=desc&page=1&sort=nameSort&types=dataverses%3Adatasets",
            "/loginpage.xhtml;jsessionid=cdf021bb2b24a2931341c87e89c5?redirectPage=%2Fdataset.xhtml%3FpersistentId%3Ddoi%3A10.48331%2Fscielodata.0P0QUN",
            "/loginpage.xhtml;jsessionid=cdf021bb2b24a2931341c87e89c5?redirectPage=%2Fdataset.xhtml%3FpersistentId%3Ddoi%3A10.48331%2Fscielodata.0P0QUN",
            "/file.xhtml?persistentId=doi:10.48331/scielodata.JAZSA3/NPTQ0M&version=1.0&toolType=PREVIEW",
            "/file.xhtml?persistentId=doi:10.48331/scielodata.LCXGHX/6U9IHT&version=2.0",
            "/api/access/datafile/8196?gbrecs=true",
            "/api/access/datafile/8440?gbrecs=true",
            "/api/access/datafile/9911;jsessionid=0f4cb3efd291eae89e65a2faf59e?imageThumb=400&pfdrid_c=true",
            "/api/datasets/3417/versions/1.0",
            "/api/datasets/:persistentId?persistentId=doi:10.48331/scielodata.XEOF5P",
            "/api/datasets/export?exporter=Datacite&persistentId=doi%3A10.48331/scielodata.FYC8LU",
            "/api/datasets/export?exporter=dcterms&persistentId=doi%3A10.48331/scielodata.1WUQZ5",
            "/api/datasets/export?exporter=dcterms&persistentId=doi%3A10.48331/scielodata.FYC8LU",
            "/api/datasets/export?exporter=dcterms&persistentId=doi%3A10.48331/scielodata.NJ7OML",
        ]:
            with self.subTest(url=url):
                self.tm.identify_translator_class(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorDataverseSite)

    def test_identify_translator_class_is_preprints_site(self):
        urls = [
            # REGEX_PREPRINTS_SITE_VIEW_ABSTRACT
            "preprint/view/12345",
            # REGEX_PREPRINTS_SITE_DOCUMENT_ABSTRACT
            "documents/article/view/54321",
            # REGEX_PREPRINTS_SITE_VERSION_ABSTRACT
            "preprint/view/12345/version/1",
            # REGEX_PREPRINTS_SITE_VIEW_PDF
            "preprint/view/12345/6789",
            # REGEX_PREPRINTS_SITE_DOWNLOAD_PDF
            "preprint/download/12345/6789",
            # REGEX_PREPRINTS_SITE_DOCUMENT_DOWNLOAD_PDF
            "documents/article/download/54321/9876",
            # REGEX_PREPRINTS_SITE_VERSION_DOWNLOAD_PDF
            "preprint/download/12345/version/1/6789",
            # Additional URLs
            "index.php/scielo/preprint/view/7353/version/7787",
            "index.php/scielo/citations/get?citationsId=10.1590%2FSciELOPreprints.7353&citationsShowList=1&citationsProvider=all",
            "index.php/scielo/preprint/download/8342/15581/16158",
            "index.php/scielo/preprint/download/5485/10601/11185",
            "index.php/scielo/preprint/view/660/version/684",
            "index.php/scielo/preprint/view/660/866",
            "index.php/scielo/preprint/download/7697/14412/15009",
            "index.php/scielo/preprint/view/7353/13812",
            "plugins/generic/hypothesis/pdf.js/viewer/web/viewer.html?file=https%3A%2F%2Fpreprints.scielo.org%2Findex.php%2Fscielo%2Fpreprint%2Fdownload%2F7353%2F13812%2F14379",
            "plugins/generic/hypothesis/pdf.js/viewer/web/locale/locale.properties",
            "plugins/generic/hypothesis/pdf.js/viewer/web/locale/es-ES/viewer.properties",
            "index.php/scielo/preprint/view/7766/14506",
            "index.php/scielo/preprint/download/7766/14506/15120",
            "index.php/scielo/preprint/download/7353/13812/14379",
            "index.php/scielo/preprint/view/136/version/141",
            "index.php/scielo/preprint/view/136/160",
            "/index.php/scielo/preprint/view/7007",
            "index.php/scielo/preprint/view/786/version/844",
            "index.php/scielo/preprint/view/786/1092",
            "index.php/scielo/preprint/download/2402/4081",
            "index.php/scielo/preprint/download/631/812/843",
            "index.php/scielo/preprint/download/631/812/843",
            "index.php/scielo/preprint/view/7353/version/7787",
            "index.php/scielo",
            "index.php/scielo/preprint/view/2428/version/2569",
            "index.php/scielo/preprint/download/9505/17685/18317",
            "/index.php/scielo/preprint/download/8919/16665/17263",
            "index.php/scielo/preprint/download/8240/15397/15975",
            "index.php/scielo/preprint/download/9332/17385/17983",
            "index.php/scielo/preprint/download/8899/16624/17227tail"
            "https://preprints.scielo.org/preprint/view/1234",
            "https://preprints.scielo.org/preprint/view/1234/version/2",
            "https://preprints.scielo.org/documents/article/view/5678",
            "https://preprints.scielo.org/preprint/download/1234/5678",
            "https://preprints.scielo.org/preprint/download/1234/version/2/5678",
            "https://preprints.scielo.org/documents/article/download/5678/1234",
            "/preprint/view/1234",
            "/preprint/view/1234/version/2",
            "/documents/article/view/5678",
            "/preprint/download/1234/5678",
            "/preprint/download/1234/version/2/5678",
            "/documents/article/download/5678/1234",
            "https://preprints.scielo.org/invalid/url",
            "https://preprints.scielo.org/preprint/unknown/1234",
        ]

        for url in urls:
            with self.subTest(url=url):
                self.tm.identify_translator_class(url)
                self.assertIsInstance(self.tm.translator, URLTranslatorPreprintsSite)

    def test_initialization_with_forced_translator(self):
        forced_translator = URLTranslatorClassicSite
        tm_forced = URLTranslationManager(
            self.journals_metadata,
            self.articles_metadata,
            translator=forced_translator
        )
        self.assertTrue(tm_forced.is_translator_forced)
        self.assertIsInstance(tm_forced.translator, forced_translator)

        obtained = tm_forced.translate('/scielo.php?pid=S1981-77462017005002103&script=sci_arttext')
        expected = {
            'scielo_issn': '1981-7746', 
            'pid_v2': 'S1981-77462017005002103',
            'media_format': MEDIA_FORMAT_HTML, 
            'media_language': MEDIA_LANGUAGE_UNDEFINED, 
            'content_type': CONTENT_TYPE_FULL_TEXT
        }
        self.assertDictEqual(obtained, expected)
