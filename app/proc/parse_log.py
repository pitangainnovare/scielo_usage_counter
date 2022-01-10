#!/usr/env python
import argparse
import logging
import os

from scielo_log_validator import validator
from app import utils, values
from app.lib import db, file, logparser


STR_CONNECTION = os.environ.get(
    'PARSE_LOG_STR_CONNECTION',
    'mysql://user:pass@localhost:port/database',
)

COLLECTION = os.environ.get(
    'PARSE_LOG_COLLECTION',
    'scl'
)

LOGGING_LEVEL = os.environ.get(
    'PARSE_LOG_LOGGING_LEVEL',
    'INFO'
)

STR_CONNECTION = os.environ.get(
    'PARSE_LOG_STR_CONNECTION',
    'mysql://user:pass@localhost:3306/usage'
)

OUTPUT_DIRECTORY = os.environ.get(
    'OUTPUT_DIRECTORY',
    'data'
)


def parse_file(logfile: str, output_directory: str, mmdb: str, robots: str):
    logging.info(f'Validação iniciada para arquivo {logfile}')
    validations = [validator._validate_path, validator._validate_content]
    validation_results = validator.validate(logfile, validations, sample_size=0.05)

    if validation_results.get('is_valid', {}).get('all', False):
        output_filepath = file.generate_filepath(output_directory, logfile)

        lp = logparser.LogParser(mmdb, robots)
        lp.logfile = logfile
        lp.output = output_filepath
        lp.stats.output = output_filepath + '.summary'

        logging.info(f'Processamento iniciado para arquivo {logfile} com saída em {output_filepath}')
        data = lp.parse()
        lp.save(data)

        logging.info(f'Arquivo {logfile} foi processado em {lp.total_time} segundos')        
        return values.LOGFILE_STATUS_LOADED
    else:
        logging.warning(f'Arquivo {logfile} foi invalidado')
        return values.LOGFILE_STATUS_INVALIDATED


def parse_files_db(str_connection: str, collection: str, output_directory: str, mmdb: str, robots: str):    
    non_parsed_logs = db.get_non_parsed_logs(str_connection, collection)

    for lf in non_parsed_logs:
        lf_path = utils.translate_path(lf.full_path)
        lf_status = parse_file(lf_path, output_directory, mmdb, robots)
        db.set_logfile_status(str_connection, lf.id, lf_status)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-m',
        '--mmdb',
        required=True,
        help='Arquivo de mapa de geolocalizações',
    )

    parser.add_argument(
        '-r',
        '--robots',
        required=True,
        help='Arquivo de robôs',
    )

    parser.add_argument(
        '-o',
        '--output_directory',
        default=OUTPUT_DIRECTORY,
        help='Diretório de saída',
    )

    subparsers = parser.add_subparsers(
        title='mode',
    )

    file_parser = subparsers.add_parser('file', help='Modo de caminho de arquivo')

    file_parser.add_argument(
        '-f',
        '--logfile',
        help='Caminho de arquivo de log de acesso',
    )

    database_parser = subparsers.add_parser('database', help='Modo de banco de dados')

    database_parser.add_argument(
        '-u',
        '--str_connection',
        default=STR_CONNECTION,
        help='String de conexão com banco de dados',
    )

    database_parser.add_argument(
        '-c',
        '--collection',
        default=COLLECTION,
        help='Acrônimo de coleção',
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=LOGGING_LEVEL,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%d/%b/%Y %H:%M:%S',
    )

    if getattr(args, 'logfile', None):
        logging.info('Inicializado em modo de arquivo')
        parse_file(**args.__dict__)
    elif getattr(args, 'str_connection', None):
        logging.info('Inicializado em modo de banco de dados')
        parse_files_db(**args.__dict__)
