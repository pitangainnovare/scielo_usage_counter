import argparse
import datetime
import logging
import requests
import os

from scielo_usage_counter.utils import file_utils


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

    if params.url:
        mmdb_url = params.url

    elif params.year and params.month:
        mmdb_url = _generate_mmdb_url_from_date(MMDB_DEFAULT_URL_FORMAT, params.year, params.month)

    try:
        logging.info('Coletando arquivo MMDB de %s' % mmdb_url)
        download_mmdb(mmdb_url, params.path_output)
    except FileMMDBWasNotDownloadError:
        logging.warning('Arquivo MMDB não está disponível em %s' % mmdb_url)
        exit(1)

    logging.info('Extraindo dados de %s' % params.path_output)
    file_utils.extract_gzip(params.path_output, params.path_output.replace('mmdb.gz', 'mmdb'))
