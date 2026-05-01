#!/usr/bin/env python3
import argparse
import logging
import os

from scielo_log_validator import validator
from scielo_usage_counter import log_handler, values
from scielo_usage_counter.utils import file_utils


COLLECTION = os.environ.get(
    'PARSE_LOG_COLLECTION',
    'scl'
)

LOGGING_LEVEL = os.environ.get(
    'PARSE_LOG_LOGGING_LEVEL',
    'INFO'
)

OUTPUT_DIRECTORY = os.environ.get(
    'OUTPUT_DIRECTORY',
    'data'
)


def parse_file(logfile: str, output_directory: str, mmdb: str, robots: str, sample_size=0.05, validate=True):
    validation_results = {}

    if validate:
        logging.info(f'Validation started for file {logfile}')
        validation_results = validator.pipeline_validate(
            path=logfile, 
            sample_size=sample_size
        )

    if validation_results.get('is_valid', {}).get('all', False) or not validate:
        output_filepath = file_utils.generate_filepath(output_directory, logfile)

        lp = log_handler.LogParser(mmdb_path=mmdb, robots_path=robots)
        lp.logfile = logfile
        lp.output = output_filepath
        lp.stats.output = output_filepath + '.summary'

        logging.info(f'Processing started for file {logfile} with output at {output_filepath}')
        data = [d for d in lp.parse()]
        lp.save(data)

        logging.info(f'File {logfile} processed in {lp.total_time} seconds. {len(data)} lines.')
        return values.LOG_FILE_PROCESSED
    else:
        logging.warning(f'File {logfile} was invalidated')
        return values.LOG_FILE_INVALIDATED


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-m',
        '--mmdb',
        required=True,
        help='Geolocation map file',
    )

    parser.add_argument(
        '-r',
        '--robots',
        required=True,
        help='Robots file',
    )

    parser.add_argument(
        '-o',
        '--output_directory',
        default=OUTPUT_DIRECTORY,
        help='Output directory',
    )

    parser.add_argument(
        '-f',
        '--logfile',
        help='Access log file path',
    )

    parser.add_argument(
        '--sample_size',
        default=0.05,
        help='Sample size for validation',
    )

    parser.add_argument(
        '--validate',
        default=False,
        action='store_true',
        help='Enable validation',
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=LOGGING_LEVEL,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%d/%b/%Y %H:%M:%S',
    )

    parse_file(**args.__dict__)
