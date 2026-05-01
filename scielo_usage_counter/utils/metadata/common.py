def empty_documents_metadata():
    return {
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
        'pid_generic_to_default_lang': {},
        'pid_generic_to_default_format': {},
        'pid_generic_to_title': {},
        'pid_generic_to_source_id': {},
        'pid_generic_to_source_type': {},
        'pid_generic_to_document_type': {},
        'book_pid_generic_to_chapter_pid_generics': {},
        'file_id_to_pid_generic': {},
        'document_id_to_title': {},
        'document_id_to_document_type': {},
        'document_set': set(),
        'pid_set': set(),
    }


def empty_sources_metadata():
    return {
        'acronym_to_scielo_issn': {},
        'issn_to_title': {},
        'issn_to_subject_area_capes': {},
        'issn_to_subject_area_wos': {},
        'issn_to_publisher_name': {},
        'issn_to_acronym': {},
        'source_id_to_title': {},
        'source_id_to_type': {},
        'source_id_to_identifiers': {},
        'source_id_to_default_lang': {},
        'source_id_to_publication_date': {},
        'source_id_to_publication_year': {},
        'source_id_to_publisher_name': {},
        'source_id_to_access_type': {},
        'source_id_to_city': {},
        'source_id_to_country': {},
        'book_id_to_isbn': {},
        'book_id_to_title': {},
        'book_id_to_year_of_publication': {},
        'book_id_to_access_type': {},
        'book_id_to_chapter_pid_generics': {},
        'book_id_and_order_to_chapter_pid_generic': {},
        'chapter_id_to_title': {},
        'chapter_key_to_title': {},
        'pid_generic_to_default_lang': {},
        'pid_generic_to_default_format': {},
        'issn_set': set(),
    }


def clean_value(value):
    if value in ('', [], {}, ()):
        return None
    return value


def iter_files(files):
    if isinstance(files, dict):
        for fid, file_data in files.items():
            if isinstance(file_data, dict):
                yield fid, file_data
        return

    if isinstance(files, list):
        for file_data in files:
            if isinstance(file_data, dict):
                yield None, file_data


def normalize_files(files):
    if isinstance(files, (list, dict)):
        return files
    return {}


def normalize_langs(langs):
    if isinstance(langs, list):
        return langs
    if isinstance(langs, dict):
        return [key for key, value in langs.items() if value]
    if langs:
        return [langs]
    return []
