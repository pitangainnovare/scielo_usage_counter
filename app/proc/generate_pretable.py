import argparse
import csv
import logging
import os

from app.utils.file import (
    check_dir,
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

UNSORTED_POSFIX = os.environ.get(
    'UNSORTED_POSFIX',
    'unsorted'
)


def read_processed_log(filepath, delimiter='\t'):
    """
    Lê um arquivo de log processado e organiza os dados por dia.

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
        for d in fin:
            yield d.strip().split(delimiter)


def _get_formatted_data(data, header, join_char):
    """Método auxiliar para extrair dados de dicionário.

    Parameters
    ----------
    data : dict
        Dicionário de dados
    header : list
        Chaves cujos valores serão usados para extrair os dados
    join_char: str
        Caractere utilizado para agrupar itens em uma string

    Yields
    ------
    str
        Uma string delimitada por join_char que representa os valores obtidos de data
    """
    for d in data:
        els = [d.get(h) for h in header]
        yield join_char.join(els)


def write_pretable(filepath, header, data, delimiter='\t'):
    """
    Grava arquivo de pré-tabela não ordenado.
    Caso arquivo já exista, acrescenta nele os dados novos.

    Parameters
    ----------
    filepath : str
        Nome do arquivo de pré-tabela
    header: list
        Lista de strings que representam o cabeçalho do arquivo de saída
    data: dict
        Dicionário contendo valores de acesso
    delimiter: str
        Separador de colunas do arquivo de pré-tabela

    Returns
    -------
    str
        Caminho do arquivo de pré-tabela gravado
    """
    if not os.path.exists(filepath):
        create_file_with_header(filepath, header)

    outfile = open(filepath, 'a')

    for fd in _get_formatted_data(data, header, delimiter):
        outfile.write(fd + '\n')

    return filepath


def generate_pretables(filepath, output_directory, extension='tsv', delimiter='\t'):
    """
    Gera arquivo(s) com os dados de log processados.
    Grava um arquivo por dia.

    Parameters
    ----------
    filepath : str
        Nome do arquivo contendo dados de log processados
    output_directory : str
        Caminho no disco em que o arquivo será gravado
    extension: str
        Extensão do nome dos arquivos a serem gerados
    delimiter: str
        Separador de colunas dos arquivos a serem gerados
    """
    ymd_to_data = read_processed_log(filepath)

    for ymd, d in ymd_to_data.items():
        pretable_filepath = generate_filepath_with_filename(
            directory=output_directory,
            filename=ymd,
            posfix=UNSORTED_POSFIX,
            extension=extension,
        )

        write_pretable(
            filepath=pretable_filepath,
            header=PRETABLE_FILE_HEADER,
            data=d,
            delimiter=delimiter,
        )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f', '--input_file',
        required=True,
        help='Arquivo de log pré-processado',
    )

    parser.add_argument(
        '-o',
        '--output_directory',
        default=OUTPUT_DIRECTORY,
        help='Diretório de saída',
    )

    params = parser.parse_args()

    logging.basicConfig(
        level=LOGGING_LEVEL,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%d/%b/%Y %H:%M:%S',
    )

    check_dir(params.output_directory)

    generate_pretables(params.input_file, params.output_directory)
