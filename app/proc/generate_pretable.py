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


def extract_values(data, header, delimiter):
    """Método auxiliar para extrair valores de um dicionário usando chaves indicadas em um header.

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
