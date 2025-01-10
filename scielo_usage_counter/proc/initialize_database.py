#!/usr/env python
import argparse
import logging
import os

from scielo_usage_counter.database.controller import create_tables


LOGGING_LEVEL = os.environ.get(
    'INITIALIZE_DATABASE_LOGGING_LEVEL',
    'INFO'
)

STR_CONNECTION = os.environ.get(
    'INITIALIZE_DATABASE_STR_CONNECTION',
    'mysql://user:pass@localhost:3306/usage'
)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-s', '--str_connection',
        default=STR_CONNECTION,
        help='String de conexão com banco de dados (mysql://user:pass@host:port/database)',
    )

    params = parser.parse_args()

    logging.basicConfig(
        level=LOGGING_LEVEL,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%d/%b/%Y %H:%M:%S',
    )

    logging.info('Criando tabelas...')
    create_tables(params.str_connection)
