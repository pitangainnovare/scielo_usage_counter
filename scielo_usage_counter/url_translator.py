import logging
import re

from urllib.parse import urlparse

from scielo_scholarly_data import standardizer

from scielo_usage_counter.translator.classic import URLTranslatorClassicSite
from scielo_usage_counter.translator.opac import URLTranslatorOPACSite
from scielo_usage_counter.translator.opac_alpha import URLTranslatorOPACAlphaSite
from scielo_usage_counter.translator.dataverse import URLTranslatorDataverseSite
from scielo_usage_counter.translator.preprints import URLTranslatorPreprintsSite
from scielo_usage_counter.translator.books import URLTranslatorBooksSite
from scielo_usage_counter.utils.metadata import (
    build_documents_metadata,
    build_sources_metadata,
)


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
    re.compile(r'^/id/[-\w]+/pdf/[-\w]+\.pdf', re.IGNORECASE),  # /id/{book_id}/pdf/{filename}.pdf
    re.compile(r'^/id/[-\w]+/epub/[-\w]+\.epub$', re.IGNORECASE),  # /id/{book_id}/epub/{filename}.epub
    re.compile(r'^/id/[-\w]+/(?:Text|epub)/\d+\.(?:xhtml|html)$', re.IGNORECASE),  # chapter html/xhtml
    re.compile(r'^/id/[-\w]+/(?:cover|swf)/.+$', re.IGNORECASE),  # ignored books assets
    re.compile(r'^/id/[-\w]+/\d+/?$', re.IGNORECASE),  # /id/{book_id}/{chapter_number}
    re.compile(r'^/id/[-\w]+/?$', re.IGNORECASE),  # /id/{book_id}
]


class URLTranslationManager:
    def __init__(self, sources_metadata, documents_metadata, translator=None):
        self.load_sources(sources_metadata)
        self.load_documents(documents_metadata)
        self.translator = translator
        
        self.is_translator_forced = bool(translator)
        if self.is_translator_forced:
            logging.info(f'Using {translator.__name__} as the URL translator class.')
            self.translator = translator(self.sources_metadata, self.documents_metadata)

    def load_documents(self, data):
        self.documents_metadata = build_documents_metadata(
            data,
            sources_metadata=getattr(self, 'sources_metadata', None),
        )

    def load_sources(self, data):
        self.sources_metadata = build_sources_metadata(data)

    def identify_translator_class(self, url):
        parsed_url = urlparse(url)

        for pattern, url_translator_class  in [
            (PATTERNS_BOOKS_SITE, URLTranslatorBooksSite),
            (PATTERNS_CLASSIC_SITE, URLTranslatorClassicSite),
            (PATTERNS_OPAC_SITE, URLTranslatorOPACSite),
            (PATTERNS_PREPRINTS_SITE, URLTranslatorPreprintsSite),
            (PATTERNS_OPAC_ALPHA_SITE, URLTranslatorOPACAlphaSite),
            (PATTERNS_DATAVERSE_SITE, URLTranslatorDataverseSite),
        ]:
            if any(re.search(p, parsed_url.path) for p in pattern):
                logging.debug(f'Identified URL as a {url_translator_class.__name__} URL.')
                self.translator = url_translator_class(self.sources_metadata, self.documents_metadata)
                return
        
        if not self.translator:
            logging.debug(f'Could not identify URL translator class for {url}')
            self.translator = URLTranslatorClassicSite(self.sources_metadata, self.documents_metadata)

    def translate(self, url: str):
        if not self.is_translator_forced:
            self.identify_translator_class(url)

        data = self.translator.pipeline_translate(url)
        if not data:
            return {}
        return self.standardize_fields(data)

    def standardize_fields(self, fields: dict):
        std_fields = {}
        
        for k, v in fields.items():
            if not v:
                continue

            if k in ('scielo_issn', 'pid_v2', 'pid_generic', 'title_pid_generic'):
                if v:
                    std_fields[k] = v.strip().upper()
                    continue

            if k in ('pid_v3', 'media_language', 'media_format'):
                if v:
                    std_fields[k] = v.strip()
                    continue

            if k == 'year_of_publication':
                year = standardizer.document_publication_date(v, only_year=True)
                if year:
                    std_fields[k] = str(year)
                continue

            if k == 'segment_pid_generics':
                std_fields[k] = [
                    str(item).strip().upper()
                    for item in (v or [])
                    if item
                ]
                continue
            
            std_fields[k] = v

        return std_fields

    def is_valid_code(self, code: str, available_codes: set):
        if code in available_codes:
            return True
        return False
