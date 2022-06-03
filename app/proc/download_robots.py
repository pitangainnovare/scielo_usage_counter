#!/usr/env python
import argparse
import logging
import os
import requests

from time import sleep


LOGGING_LEVEL = os.environ.get(
    'COUNTER_ROBOTS_LOGGING_LEVEL',
    'INFO'
)

MAX_RETRIES = int(os.environ.get(
    'COUNTER_ROBOTS_MAX_RETRIES',
    5
))

COUNTER_ROBOTS_URL = os.environ.get(
    'COUNTER_ROBOTS_URL',
    'https://raw.githubusercontent.com/atmire/COUNTER-Robots/master/COUNTER_Robots_list.json'
)

SLEEP_TIME = int(os.environ.get(
    'COUNTER_ROBOTS_URL_SLEEP_TIME',
    30
))


class FileRobotsWasNotDownloadError(Exception):
    ...


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
    for t in range(1, MAX_RETRIES + 1):
        response = requests.get(url)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.warning(
                'Não foi possível coletar dados de %s. Aguardando %d segundos para tentativa %d de %d' % (
                    url, 
                    SLEEP_TIME, 
                    t, 
                    MAX_RETRIES
                )
            )
            sleep(SLEEP_TIME)
        else:
            return response.json()


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
        help='URL da lista de robôs',
    )

    parser.add_argument(
        '--path_output',
        required=True,
        help='Arquivo de saída',
    )

    params = parser.parse_args()

    logging.basicConfig(
        level=LOGGING_LEVEL,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%d/%b/%Y %H:%M:%S'
    )

    try:

    data = get_robots(params.url)

    save(data, params.output)
