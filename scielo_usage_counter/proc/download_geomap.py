import argparse
import datetime
import logging
import requests
import os

from scielo_usage_counter.utils import file_utils


_now = datetime.date.today()
_last_month = _now.replace(day=1) - datetime.timedelta(days=1)

CURRENT_YEAR = _last_month.year
PAST_MONTH = f"{_last_month.month:02d}"

MMDB_CITY_URL_FORMAT = 'https://download.db-ip.com/free/dbip-city-lite-{0}-{1}.mmdb.gz'
MMDB_COUNTRY_URL_FORMAT = 'https://download.db-ip.com/free/dbip-country-lite-{0}-{1}.mmdb.gz'

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
        raise FileMMDBWasNotDownloadError('Geolocation file was not collected')

    with open(path_output,'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

    return True


def _generate_mmdb_url_from_date(default_mmdb_route, year, month):
    if not year or not month:
        year = CURRENT_YEAR
        month = PAST_MONTH

    str_month = str(month).zfill(2)

    return default_mmdb_route.format(year, str_month)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--year',
        default='',
        help='Geolocation map year (yyyy)',
    )

    parser.add_argument(
        '--month',
        default='',
        help='Geolocation map month (mm)',
    )

    parser.add_argument(
        '--url',
        help='URL of the mmdb.gz map',
    )

    parser.add_argument(
        '--subset',
        choices=['city', 'country'],
        default='city',
    )

    parser.add_argument(
        '--path_output',
        required=True,
        help='Geolocation map file path',
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
        if params.subset == 'country':
            mmdb_url = _generate_mmdb_url_from_date(MMDB_COUNTRY_URL_FORMAT, params.year, params.month)
        else:
            mmdb_url = _generate_mmdb_url_from_date(MMDB_CITY_URL_FORMAT, params.year, params.month)
    else:
        route = MMDB_COUNTRY_URL_FORMAT if params.subset == 'country' else MMDB_CITY_URL_FORMAT
        mmdb_url = _generate_mmdb_url_from_date(route, CURRENT_YEAR, PAST_MONTH)

    try:
        logging.info('Collecting MMDB file from %s' % mmdb_url)
        download_mmdb(mmdb_url, params.path_output)
    except FileMMDBWasNotDownloadError:
        logging.warning('MMDB file is not available at %s' % mmdb_url)
        exit(1)

    logging.info('Extracting data from %s' % params.path_output)
    file_utils.extract_gzip(params.path_output, params.path_output.replace('.gz', ''))
