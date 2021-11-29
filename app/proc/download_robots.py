#!/usr/env python
import argparse
import logging
import os
import requests

from time import sleep
from app.utils.file import check_dir


LOGGING_LEVEL = os.environ.get(
    'COUNTER_ROBOTS_LOGGING_LEVEL',
    'INFO'
)

MAX_RETRIES = int(os.environ.get(
    'COUNTER_ROBOTS_MAX_RETRIES',
    5
))

OUTPUT_FILENAME = os.environ.get(
    'COUNTER_ROBOTS_OUTPUT_FILENAME',
    'data/counter-robots.txt'
)

COUNTER_ROBOTS_URL = os.environ.get(
    'COUNTER_ROBOTS_URL',
    'https://raw.githubusercontent.com/atmire/COUNTER-Robots/master/COUNTER_Robots_list.json'
)


def _extract_patterns(robots_json):
    for i in robots_json:
        yield i.get('pattern') + '\n'


def get_robots(url):
    """
    Obtém objeto json contendo robôs da URL informada

    Parameters
    ----------
    url : str
        Endereço da lista de robôs

    Returns
    -------
    json
        Um objeto json contendo as expressões regulares de robôs (e a data de atualização)
            [
                {
                    "pattern": "bot",
                    "last_changed": "2017-08-08"
                },
                {
                    "pattern": "^Buck\\/[0-9]",
                    "last_changed": "2019-11-19"
                },
                {
                    "pattern": "spider",
                    "last_changed": "2017-08-08"
                },
                {
                    "pattern": "crawl",
                    "last_changed": "2017-08-08"
                },
            ]
    """
    logging.info('Coletando dados...')
    try:
        for t in range(MAX_RETRIES):
            logging.debug(f'Tentativa {t + 1}')
            response = requests.get(url)

            if response.status_code != 200:
                logging.warning('Não foi possível obter a lista de robôs')
            else:
                return response.json()

            sleep(30)
    except Exception as e:
        logging.error(e)


def save(data, output):
    """
    Grava em um arquivo as expressões regulares dos robôs

    Parameters
    ----------
    data : json
        Objeto json contendo robôs
    output : str
        Arquivo destino da lista de robôs

    """
    try:
        with open(output, 'w') as fout:
            robots_patterns = _extract_patterns(data)
            fout.writelines(robots_patterns)
            logging.info('Lista de robôs obtida com sucesso: %s' % output)
    except Exception as e:
        logging.error(e)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-u',
        '--url',
        default=COUNTER_ROBOTS_URL,
        help='URL da lista de robots',
    )

    parser.add_argument(
        '-o',
        '--output',
        default=OUTPUT_FILENAME,
        help='Arquivo de saída',
    )

    params = parser.parse_args()

    logging.basicConfig(
        level=LOGGING_LEVEL,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%d/%b/%Y %H:%M:%S'
    )

    check_dir(params.output)

    data = get_robots(params.url)

    save(data, params.output)
