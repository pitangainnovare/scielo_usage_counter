import logging

from .common import (
    clean_value,
    empty_documents_metadata,
    empty_sources_metadata,
    iter_files,
    normalize_files,
    normalize_langs,
)


def build_documents_metadata(data, sources_metadata=None):
    logging.info('Loading documents metadata...')

    documents_metadata = empty_documents_metadata()
    sources_metadata = sources_metadata or empty_sources_metadata()

    count = 0
    for document in data or []:
        count += 1
        _load_document_record(documents_metadata, sources_metadata, document)

    logging.info(f'Loaded {count} documents metadata.')
    return documents_metadata


def _load_document_record(documents_metadata, sources_metadata, document):
    key_pid_v2 = clean_value(document.get('pid_v2'))
    key_pid_v3 = clean_value(document.get('pid_v3'))
    key_pid_generic = clean_value(document.get('pid_generic'))
    document_id = clean_value(document.get('document_id'))
    document_type = clean_value(document.get('document_type'))
    source_id = clean_value(document.get('source_id'))
    source_type = clean_value(document.get('source_type'))
    default_lang = clean_value(document.get('default_lang'))
    publication_date = clean_value(document.get('publication_date'))
    publication_year = clean_value(document.get('publication_year'))
    default_media_format = clean_value(document.get('default_media_format'))
    title = clean_value(document.get('title'))
    text_langs = normalize_langs(document.get('text_langs'))
    files = normalize_files(document.get('files'))

    if document_id:
        documents_metadata['document_set'].add(document_id)
        documents_metadata['document_id_to_title'][document_id] = title
        documents_metadata['document_id_to_document_type'][document_id] = document_type

    if key_pid_generic:
        _load_generic_document_metadata(
            documents_metadata=documents_metadata,
            document_type=document_type,
            source_id=source_id,
            source_type=source_type,
            pid_generic=key_pid_generic,
            title=title,
            default_lang=default_lang,
            default_media_format=default_media_format,
            publication_date=publication_date,
            files=files,
        )
        _load_books_document_mappings(
            sources_metadata=sources_metadata,
            documents_metadata=documents_metadata,
            document=document,
            document_type=document_type,
            source_id=source_id,
            pid_generic=key_pid_generic,
            title=title,
            publication_year=publication_year,
            default_lang=default_lang,
            default_media_format=default_media_format,
        )

    if key_pid_v2:
        _load_pid_v2_metadata(
            documents_metadata=documents_metadata,
            document=document,
            pid_v2=key_pid_v2,
            pid_v3=key_pid_v3,
            default_lang=default_lang,
            text_langs=text_langs,
            publication_year=publication_year,
        )

    _load_document_file_mappings(
        documents_metadata=documents_metadata,
        files=files,
        pid_v2=key_pid_v2,
        pid_v3=key_pid_v3,
    )

    if key_pid_v3 and key_pid_v2:
        documents_metadata['pid_v3_to_pid_v2'][key_pid_v3] = key_pid_v2

    if key_pid_v3:
        _load_pid_v3_metadata(
            documents_metadata=documents_metadata,
            document=document,
            pid_v3=key_pid_v3,
            default_lang=default_lang,
            text_langs=text_langs,
            publication_year=publication_year,
        )


def _load_generic_document_metadata(
    documents_metadata,
    document_type,
    source_id,
    source_type,
    pid_generic,
    title,
    default_lang,
    default_media_format,
    publication_date,
    files,
):
    documents_metadata['pid_set'].add(pid_generic)
    documents_metadata['pid_generic_to_publication_date'][pid_generic] = publication_date
    documents_metadata['pid_generic_to_available_file_ids'][pid_generic] = _available_file_ids(files)
    documents_metadata['pid_generic_to_default_lang'][pid_generic] = default_lang
    documents_metadata['pid_generic_to_default_format'][pid_generic] = default_media_format
    documents_metadata['pid_generic_to_title'][pid_generic] = title
    documents_metadata['pid_generic_to_source_id'][pid_generic] = source_id
    documents_metadata['pid_generic_to_source_type'][pid_generic] = source_type
    documents_metadata['pid_generic_to_document_type'][pid_generic] = document_type

    for fid, file_data in iter_files(files):
        file_key_generic = (
            file_data.get('file_persistent_id')
            or file_data.get('file_persisent_id')
            or pid_generic
        )
        if file_key_generic:
            documents_metadata['file_id_to_pid_generic'][file_key_generic] = pid_generic

        if fid is not None:
            documents_metadata['file_id_to_pid_generic'][str(fid)] = pid_generic


def _load_pid_v2_metadata(
    documents_metadata,
    document,
    pid_v2,
    pid_v3,
    default_lang,
    text_langs,
    publication_year,
):
    documents_metadata['pid_set'].add(pid_v2)
    documents_metadata['pid_v2_to_pid_v3'][pid_v2] = pid_v3
    documents_metadata['pid_v2_to_default_lang'][pid_v2] = default_lang
    documents_metadata['pid_v2_to_available_langs'][pid_v2] = text_langs
    documents_metadata['pid_v2_to_scielo_issn'][pid_v2] = document.get('scielo_issn')
    documents_metadata['pid_v2_to_publication_year'][pid_v2] = publication_year


def _load_document_file_mappings(documents_metadata, files, pid_v2, pid_v3):
    for _, file_data in iter_files(files):
        file_id = file_data.get('path')
        if file_id and not file_id.startswith('/'):
            file_id = f'/{file_id}'

        if file_id:
            if pid_v3:
                documents_metadata['pdf_to_pid_v3'][file_id] = pid_v3
            if pid_v2:
                documents_metadata['pdf_to_pid_v2'][file_id] = pid_v2

        doi_key = file_data.get('doi')
        if not doi_key:
            continue

        if pid_v2:
            documents_metadata['doi_to_pid_v2'][doi_key] = pid_v2

        if pid_v3:
            documents_metadata['doi_to_pid_v3'][doi_key] = pid_v3


def _load_pid_v3_metadata(
    documents_metadata,
    document,
    pid_v3,
    default_lang,
    text_langs,
    publication_year,
):
    documents_metadata['pid_set'].add(pid_v3)
    documents_metadata['pid_v3_to_default_lang'][pid_v3] = default_lang
    documents_metadata['pid_v3_to_available_langs'][pid_v3] = text_langs
    documents_metadata['pid_v3_to_scielo_issn'][pid_v3] = document.get('scielo_issn')
    documents_metadata['pid_v3_to_publication_year'][pid_v3] = publication_year


def _available_file_ids(files):
    file_ids = set()

    for fid, file_data in iter_files(files):
        if fid is not None:
            file_ids.add(str(fid))

        file_path = file_data.get('path')
        if file_path:
            file_ids.add(file_path)

    return file_ids


def _load_books_document_mappings(
    sources_metadata,
    documents_metadata,
    document,
    document_type,
    source_id,
    pid_generic,
    title,
    publication_year,
    default_lang,
    default_media_format,
):
    if not pid_generic:
        return

    if default_lang:
        sources_metadata['pid_generic_to_default_lang'][pid_generic] = default_lang

    if default_media_format:
        sources_metadata['pid_generic_to_default_format'][pid_generic] = default_media_format

    if document_type == 'book' and source_id:
        if title:
            sources_metadata['book_id_to_title'][source_id] = title
        if publication_year:
            sources_metadata['book_id_to_year_of_publication'][source_id] = publication_year

        identifiers = document.get('identifiers') or {}
        isbn = identifiers.get('isbn') or identifiers.get('eisbn')
        if isbn:
            sources_metadata['book_id_to_isbn'][source_id] = isbn

    if document_type != 'chapter' or not source_id:
        return

    book_pid_generic = f'book:{source_id}'
    source_chapters = sources_metadata['book_id_to_chapter_pid_generics'].setdefault(source_id, [])
    if pid_generic not in source_chapters:
        source_chapters.append(pid_generic)

    document_chapters = documents_metadata['book_pid_generic_to_chapter_pid_generics'].setdefault(
        book_pid_generic,
        [],
    )
    if pid_generic not in document_chapters:
        document_chapters.append(pid_generic)

    extra_data = document.get('extra_data') or {}
    order = extra_data.get('order')
    if order:
        sources_metadata['book_id_and_order_to_chapter_pid_generic'][
            f'{source_id}:{order}'
        ] = pid_generic

    chapter_id = _extract_chapter_id(document, pid_generic)
    if chapter_id and title:
        sources_metadata['chapter_id_to_title'][chapter_id] = title
        sources_metadata['chapter_key_to_title'][f'{source_id}:{chapter_id}'] = title


def _extract_chapter_id(document, pid_generic):
    identifiers = document.get('identifiers') or {}
    chapter_id = identifiers.get('chapter_id')
    if chapter_id:
        return str(chapter_id)

    if '/chapter:' in (pid_generic or ''):
        return pid_generic.split('/chapter:')[-1]

    return None
