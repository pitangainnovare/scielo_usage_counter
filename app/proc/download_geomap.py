import argparse
import datetime
import logging
import requests
import os

from app.utils.file import (
    check_dir,
    extract_gzip,
)


DEFAULT_URL = 'https://download.db-ip.com/free/dbip-city-lite-{0}-{1}.mmdb.gz'

LOGGING_LEVEL = os.environ.get(
    'GEOIP_LOGGING_LEVEL',
    'INFO'
)

OUTPUT_FILENAME = os.environ.get(
    'GEOIP_OUTPUT_FILENAME',
    'data/map.mmdb.gz'
)


def _download(url, output, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(output, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)
    return output


def download_mmdb_from_date(year, month, output):
    if year == '' or month == '':
        today = datetime.date.today()

        year = today.year
        month = today.month

    return _download(DEFAULT_URL.format(year, month), output)


def download_mmdb_from_url(url, output):
    return _download(url, output)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--year',
        default='',
        help='Ano do mapa de geolocalização (yyyy)'
    )

    parser.add_argument(
        '--month',
        default='',
        help='Mês do mapa de geolocalização (mm)'
    )

    parser.add_argument(
        '--url',
        help='URL do mapa em formato mmdb.gz'
    )

    parser.add_argument(
        '-o',
        '--output',
        default=OUTPUT_FILENAME,
        help='Arquivo do mapa de geolocalizações'
    )

    params = parser.parse_args()

    logging.basicConfig(
        level=LOGGING_LEVEL,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%d/%b/%Y %H:%M:%S'
    )

    check_dir(params.output)
    output = ''

    if params.url:
        logging.info('Coletando dados...')
        output = download_mmdb_from_url(params.url, params.output)

    elif params.year and params.month:
        logging.info('Coletando dados a partir de data e ano: (%s, %s)' % (params.year, params.month))
        output = download_mmdb_from_date(params.year, params.month, params.output)

    if output:
        logging.info('Extraindo dados...')
        extract_gzip(output)
