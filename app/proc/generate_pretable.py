import argparse
import csv
import ipaddress
import logging
import os

from app.utils.file import (
    check_dir,
    create_backup,
    create_file_with_header,
    generate_filepath_with_filename,
)
from app.values import PRETABLE_FILE_HEADER


LOGGING_LEVEL = os.environ.get(
    'GENERATE_PRETABLE_LOGGING_LEVEL',
    'INFO'
)

OUTPUT_DIRECTORY = os.environ.get(
    'OUTPUT_DIRECTORY',
    'data/pretables/'
)


def read_processed_log(filepath, delimiter='\t'):
    """
    Lê um arquivo de log processado e organizada os dados por dia.

    Parameters
    ----------
    filepath : str
        Nome do arquivo contendo dados de log processados
    delimiter: str
        Separador de colunas do arquivo de log processado

    Returns
    -------
    dict
        Um dicionário contendo dados de acesso processados e organizados por dia
            [
                ...,
                '2021-10-01': [...],
                '2021-10-02': [...],
                ...,
            ]
    """
    data = {}

    with open(filepath) as fin:
        logging.info('Lendo %s' % filepath)
        csv_reader = csv.DictReader(fin, delimiter=delimiter)
        
        for line in csv_reader:
            ymd = line.get('serverTime').split(' ')[0]
            
            if ymd not in data:
                data[ymd] = []
            
            data[ymd].append(line)

    return data


def read_pretable(filepath, delimiter='\t', ignore_header=True):
    """
    Lê arquivo de pré-tabela.

    Parameters
    ----------
    filepath : str
        Nome do arquivo contendo dados de pré-tabela
    delimiter: str
        Separador de colunas do arquivo de log processado
    ignore_header: boolean
        Ignora primeira linha se True

    Returns
    -------
    list
        Uma lista de lista (com dados de acesso nos moldes de pré-tabela)
            [
                ['2021-05-20 09:48:53','CM','90.0.4430.210','1.0.102.87','34.4002','132.475','/scielo.php?script=sci_arttext&pid=S0100-85872017000300173'],
                ...,
            ]
    """
    with open(filepath) as fin:
        if ignore_header:
            fin.readline()
        return [d.strip().split(delimiter) for d in fin]
