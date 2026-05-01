import logging

from .common import clean_value, empty_sources_metadata


def build_sources_metadata(data):
    logging.info('Loading sources metadata...')

    sources_metadata = empty_sources_metadata()

    count = 0
    for source in data or []:
        count += 1
        _load_source_record(sources_metadata, source)

    logging.info(f'Loaded {count} sources metadata.')
    return sources_metadata


def _load_source_record(sources_metadata, source):
    source_id = clean_value(source.get('source_id'))
    source_type = clean_value(source.get('source_type')) or _infer_source_type(source)
    scielo_issn = clean_value(source.get('scielo_issn'))
    acronym = clean_value(source.get('acronym'))
    title = clean_value(source.get('title'))
    identifiers = source.get('identifiers') or {}
    issns = _collect_issns(source.get('issns'), identifiers, scielo_issn)

    if acronym and scielo_issn:
        sources_metadata['acronym_to_scielo_issn'][acronym] = scielo_issn

    if source_id:
        sources_metadata['source_id_to_title'][source_id] = title
        sources_metadata['source_id_to_type'][source_id] = source_type
        sources_metadata['source_id_to_identifiers'][source_id] = identifiers
        sources_metadata['source_id_to_default_lang'][source_id] = clean_value(source.get('default_lang'))
        sources_metadata['source_id_to_publication_date'][source_id] = clean_value(source.get('publication_date'))
        sources_metadata['source_id_to_publication_year'][source_id] = clean_value(source.get('publication_year'))
        sources_metadata['source_id_to_publisher_name'][source_id] = source.get('publisher_name')
        sources_metadata['source_id_to_access_type'][source_id] = clean_value(source.get('access_type'))
        sources_metadata['source_id_to_city'][source_id] = clean_value((source.get('extra_data') or {}).get('city'))
        sources_metadata['source_id_to_country'][source_id] = clean_value((source.get('extra_data') or {}).get('country'))

    if source_type == 'book' and source_id:
        sources_metadata['book_id_to_title'][source_id] = title
        sources_metadata['book_id_to_isbn'][source_id] = identifiers.get('isbn') or identifiers.get('eisbn')
        sources_metadata['book_id_to_year_of_publication'][source_id] = clean_value(source.get('publication_year'))
        sources_metadata['book_id_to_access_type'][source_id] = clean_value(source.get('access_type'))

    for issn in issns:
        sources_metadata['issn_to_title'][issn] = source.get('title')
        sources_metadata['issn_to_subject_area_capes'][issn] = source.get('subject_areas')
        sources_metadata['issn_to_subject_area_wos'][issn] = source.get('wos_subject_areas')
        sources_metadata['issn_to_publisher_name'][issn] = source.get('publisher_name')
        sources_metadata['issn_set'].add(issn)
        sources_metadata['issn_to_acronym'][issn] = acronym


def _collect_issns(issns, identifiers, scielo_issn):
    normalized_issns = set()

    if isinstance(issns, dict):
        normalized_issns.update(value for value in issns.values() if value)
    elif isinstance(issns, (list, set, tuple)):
        normalized_issns.update(value for value in issns if value)

    if isinstance(identifiers, dict):
        for key, value in identifiers.items():
            if value and 'issn' in str(key).lower():
                normalized_issns.add(value)

    if scielo_issn:
        normalized_issns.add(scielo_issn)

    return normalized_issns


def _infer_source_type(source):
    if source.get('issns') or source.get('scielo_issn') or source.get('acronym'):
        return 'journal'
    if source.get('source_id') or (source.get('identifiers') or {}).get('book_id'):
        return 'book'
    return None
