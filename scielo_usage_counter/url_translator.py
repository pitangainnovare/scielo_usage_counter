import logging
import re

from urllib.parse import urlparse

from  scielo_usage_counter.translator.classic import URLTranslatorClassicSite
from  scielo_usage_counter.translator.opac import URLTranslatorOPACSite
from  scielo_usage_counter.translator.opac_alpha import URLTranslatorOPACAlphaSite
from  scielo_usage_counter.translator.dataverse import URLTranslatorDataverseSite
from  scielo_usage_counter.translator.preprints import URLTranslatorPreprintsSite
from  scielo_usage_counter.translator.books import URLTranslatorBooksSite


# Patterns to support identify a URL as a Classic Site URL
PATTERNS_CLASSIC_SITE = [
    re.compile(r'/scielo.php', re.IGNORECASE),
    re.compile(r'/scieloorg/php/', re.IGNORECASE),
    re.compile(r'/popup/', re.IGNORECASE),
    re.compile(r'/google_metrics/', re.IGNORECASE),
    re.compile(r'/pdf/.*\.pdf', re.IGNORECASE),
]

#  Patterns to support identify a URL as a Dataverse Site URL
PATTERNS_DATAVERSE_SITE = [
    re.compile(r'api/datasets', re.IGNORECASE),
    re.compile(r'api/access/datafile', re.IGNORECASE),
    re.compile(r'dataset.xhtml', re.IGNORECASE),
    re.compile(r'dataverse', re.IGNORECASE),
    re.compile(r'file.xhtml', re.IGNORECASE),
    re.compile(r'logingpage.xhtml', re.IGNORECASE),
]

# Patterns to support identify a URL as a OPAC Alpha Site URL
PATTERNS_OPAC_ALPHA_SITE = [
    re.compile(r'/?j/[^/]+/', re.IGNORECASE),
    re.compile(r'/?article/[\w]+/[^/]+/[^/]+', re.IGNORECASE),
    re.compile(r'/?pdf/[^/]+/[^/]+/', re.IGNORECASE),
]

# Patterns to support identify a URL as a OPAC Site URL
PATTERNS_OPAC_SITE = [
    re.compile(r'/?j/[^/]+/', re.IGNORECASE),
    re.compile(r'/citation/export/', re.IGNORECASE),
    re.compile(r'/article/ssm/content/raw/.*', re.IGNORECASE),
]

# Patterns to support identify a URL as a Preprints Site URL
PATTERNS_PREPRINTS_SITE = [
    re.compile(r'/?preprint/view/', re.IGNORECASE),
    re.compile(r'/?preprint/download/', re.IGNORECASE),
    re.compile(r'/?(index.php)?/?documents/article/(download|view)/', re.IGNORECASE),
    re.compile(r'/?index.php/scielo/preprint/', re.IGNORECASE),
    re.compile(r'/?plugins/generic/(hypothesis|pdfJsViewer)/', re.IGNORECASE),
]

# Patterns to support identify a URL as a Books Site URL
PATTERNS_BOOKS_SITE = [
    re.compile(r'/?b/\w+', re.IGNORECASE),
    re.compile(r'/?book/\w+', re.IGNORECASE),
    re.compile(r'/?c/\w+/\w+', re.IGNORECASE),
    re.compile(r'/?chapter/\w+/\w+', re.IGNORECASE),
    re.compile(r'/?pdf/\w+', re.IGNORECASE),
    re.compile(r'/?epub/\w+', re.IGNORECASE),
    re.compile(r'/?download/\w+', re.IGNORECASE),
]


class URLTranslationManager:
    def __init__(self, journals_metadata, articles_metadata, translator=None):
        self.load_journals(journals_metadata)
        self.load_articles(articles_metadata)
        self.translator = translator
        
        self.is_translator_forced = bool(translator)
        if self.is_translator_forced:
            logging.info(f'Using {translator.__name__} as the URL translator class.')
            self.translator = translator(self.journals_metadata, self.articles_metadata)

    def load_articles(self, data):
        logging.info('Loading articles metadata...')

        self.articles_metadata = {
            'pid_v3_to_pid_v2': {},
            'pid_v3_to_default_lang': {},
            'pid_v3_to_available_langs': {},
            'pid_v3_to_scielo_issn': {},
            'pid_v3_to_publication_year': {},
            'pid_v2_to_pid_v3': {},
            'pid_v2_to_default_lang': {},
            'pid_v2_to_available_langs': {},
            'pid_v2_to_scielo_issn': {},
            'pid_v2_to_publication_year': {},
            'pdf_to_pid_v2': {},
            'pdf_to_pid_v3': {},
            'doi_to_pid_v2': {},
            'doi_to_pid_v3': {},
            'pid_generic_to_publication_date': {},
            'pid_generic_to_available_file_ids': {},
            'file_id_to_pid_generic': {},
            'pid_set': set(),
        }

        count = 0
        for art in data:
            count += 1
            key_pid_v2 = art.get('pid_v2')
            key_pid_v3 = art.get('pid_v3')
            key_pid_generic = art.get('pid_generic')

            if key_pid_generic is not None:
                self.articles_metadata['pid_set'].add(key_pid_generic)

                self.articles_metadata['pid_generic_to_publication_date'][key_pid_generic] = art.get('publication_date')

                files = art.get('files', [])
                self.articles_metadata['pid_generic_to_available_file_ids'][key_pid_generic] = set(files)

                for fid in files:
                    file_key_generic = files[fid].get('file_persistent_id') or key_pid_generic
                    # Map the persistent ID of the file to the generic PID
                    self.articles_metadata['file_id_to_pid_generic'][file_key_generic] = key_pid_generic

                    # Map the numeric ID of the file to the generic PID
                    self.articles_metadata['file_id_to_pid_generic'][fid] = key_pid_generic

                continue

            if key_pid_v2:
                self.articles_metadata['pid_set'].add(key_pid_v2)

                self.articles_metadata['pid_v2_to_pid_v3'][key_pid_v2] = key_pid_v3
                self.articles_metadata['pid_v2_to_default_lang'][key_pid_v2] = art.get('default_lang')
                self.articles_metadata['pid_v2_to_available_langs'][key_pid_v2] = art.get('text_langs')
                self.articles_metadata['pid_v2_to_scielo_issn'][key_pid_v2] = art.get('scielo_issn')
                self.articles_metadata['pid_v2_to_publication_year'][key_pid_v2] = art.get('publication_year')

            for file_data in art.get('files', []):
                file_id = file_data.get('path')
                if not file_id.startswith('/'):
                    file_id = f'/{file_id}'

                if file_id:
                    if key_pid_v3:
                        self.articles_metadata['pdf_to_pid_v3'][file_id] = key_pid_v3

                if key_pid_v2:
                    self.articles_metadata['pdf_to_pid_v2'][file_id] = key_pid_v2

                doi_key = file_data.get('doi')
                if doi_key:
                    if key_pid_v2:
                        self.articles_metadata['doi_to_pid_v2'][doi_key] = key_pid_v2

                    if key_pid_v3:
                        self.articles_metadata['doi_to_pid_v3'][doi_key] = key_pid_v3

            if key_pid_v3 and key_pid_v2:
                self.articles_metadata['pid_v3_to_pid_v2'][key_pid_v3] = key_pid_v2
    
            if key_pid_v3:     
                self.articles_metadata['pid_set'].add(key_pid_v3)
          
                self.articles_metadata['pid_v3_to_default_lang'][key_pid_v3] = art.get('default_lang')
                self.articles_metadata['pid_v3_to_available_langs'][key_pid_v3] = art.get('text_langs')
                self.articles_metadata['pid_v3_to_scielo_issn'][key_pid_v3] = art.get('scielo_issn')
                self.articles_metadata['pid_v3_to_publication_year'][key_pid_v3] = art.get('publication_year')

        logging.info(f'Loaded {count} articles metadata.')

    def load_journals(self, data):
        logging.info('Loading journals metadata...')

        self.journals_metadata = {
            'acronym_to_scielo_issn': {},
            'issn_to_title': {},
            'issn_to_subject_area_capes': {},
            'issn_to_subject_area_wos': {},
            'issn_to_publisher_name': {},
            'issn_to_acronym': {},
            'issn_set': set(),
        }

        count = 0
        for j in data:
            count += 1
            self.journals_metadata['acronym_to_scielo_issn'][j.get('acronym')] = j.get('scielo_issn')

            for issn in j.get('issns'):
                self.journals_metadata['issn_to_title'][issn] = j.get('title')
                self.journals_metadata['issn_to_subject_area_capes'][issn] = j.get('subject_areas')
                self.journals_metadata['issn_to_subject_area_wos'][issn] = j.get('wos_subject_areas')
                self.journals_metadata['issn_to_publisher_name'][issn] = j.get('publisher_name')
                self.journals_metadata['issn_set'].add(issn)
                self.journals_metadata['issn_to_acronym'][issn] = j.get('acronym')

        logging.info(f'Loaded {count} journals metadata.')

    def identify_translator_class(self, url):
        parsed_url = urlparse(url)

        for pattern, url_translator_class  in [
            (PATTERNS_CLASSIC_SITE, URLTranslatorClassicSite),
            (PATTERNS_OPAC_SITE, URLTranslatorOPACSite),
            (PATTERNS_PREPRINTS_SITE, URLTranslatorPreprintsSite),
            (PATTERNS_OPAC_ALPHA_SITE, URLTranslatorOPACAlphaSite),
            (PATTERNS_DATAVERSE_SITE, URLTranslatorDataverseSite),
            (PATTERNS_BOOKS_SITE, URLTranslatorBooksSite),
        ]:
            if any(re.search(p, parsed_url.path) for p in pattern):
                logging.debug(f'Identified URL as a {url_translator_class.__name__} URL.')
                self.translator = url_translator_class(self.journals_metadata, self.articles_metadata)
                return
        
        if not self.translator:
            logging.debug(f'Could not identify URL translator class for {url}')
            self.translator = URLTranslatorClassicSite(self.journals_metadata, self.articles_metadata)

    def translate(self, url: str):
        if not self.is_translator_forced:
            self.identify_translator_class(url)

        data = self.translator.pipeline_translate(url)
        return self.standardize_fields(data)

    def standardize_fields(self, fields: dict):
        std_fields = {}
        
        for k, v in fields.items():
            if k in ('scielo_issn', 'pid_v2', 'pid_generic',):
                if v:
                    std_fields[k] = v.strip().upper()
                    continue

            if k in ('pid_v3', 'media_language', 'media_format'):
                if v:
                    std_fields[k] = v.strip()
                    continue
            
            std_fields[k] = v

        return std_fields

    def is_valid_code(self, code: str, available_codes: set):
        if code in available_codes:
            return True
        return False
