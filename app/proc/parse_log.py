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


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', '--collection',
        default=COLLECTION,
        help='Acrônimo de coleção',
    )

    parser.add_argument(
        '-f', '--file',
        required=True,
        help='Arquivo de log de acesso',
    )

    parser.add_argument(
        '-o',
        '--output_directory',
        default=OUTPUT_DIRECTORY,
        help='Diretório de saída',
    )

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

    params = parser.parse_args()

    logging.basicConfig(
        level=LOGGING_LEVEL,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%d/%b/%Y %H:%M:%S',
    )

    logging.info(f'Validação iniciada para arquivo {params.file}')
    validation_results = validate(
        params.file,
        [_validate_path, _validate_content],
        sample_size=0.05,
    )

    if validation_results.get('is_valid', {}).get('all', False):
        output_filepath = generate_filepath(params.output_directory, params.file)

        lp = LogParser(params.mmdb, params.robots)
        lp.logfile = params.file
        lp.output = output_filepath
        lp.stats.output = output_filepath + '.summary'

        logging.info(f'Processamento iniciado para arquivo {params.file} com saída em {output_filepath}')
        data = lp.parse()
        lp.save(data)

        logging.info(f'Arquivo {params.file} foi processado em {lp.total_time} segundos')

    else:
        logging.warning(f'Arquivo {params.file} não é válido')
