import argparse
import datetime
import logging
import requests
import os

from app.lib.file import extract_gzip


MMDB_DEFAULT_URL_FORMAT = 'https://download.db-ip.com/free/dbip-city-lite-{0}-{1}.mmdb.gz'

LOGGING_LEVEL = os.environ.get(
    'GEOIP_LOGGING_LEVEL',
    'INFO'
)


class FileMMDBWasNotDownloadError(Exception):
    ...


def download_mmdb(url, path_output, chunk_size=128):
    r = requests.get(url, stream=True)

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        raise FileMMDBWasNotDownloadError('Arquivo de geolocalizações não foi coletado')

    with open(path_output,'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

    return True


def _generate_mmdb_url_from_date(default_mmdb_route, year, month):
    if year == '' or month == '':
        today = datetime.date.today()

        year = today.year
        month = today.month

    return default_mmdb_route.format(year, month)


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
        '--path_output',
        required=True,
        help='Caminho do arquivo de mapa de geolocalizações'
    )

    params = parser.parse_args()

    logging.basicConfig(
        level=LOGGING_LEVEL,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%d/%b/%Y %H:%M:%S'
    )

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
