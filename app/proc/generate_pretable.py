import argparse
import csv
import logging
import os
import shlex
import subprocess

from app import values
from app.lib import db, file, exceptions


LOGGING_LEVEL = os.environ.get(
    'GENERATE_PRETABLE_LOGGING_LEVEL',
    'INFO'
)

PROCESSED_LOGS_DIRECTORY = os.environ.get(
    'GENERATE_PRETABLE_PROCESSED_LOGS_DIRECTORY',
    'data/processed/'
)

OUTPUT_DIRECTORY = os.environ.get(
    'OUTPUT_DIRECTORY',
    'data/pretables/'
)

UNSORTED_POSFIX = os.environ.get(
    'GENERATE_PRETABLE_UNSORTED_POSFIX',
    'unsorted'
)

COLLECTION = os.environ.get(
    'GENERATE_PRETABLE_PARSE_LOG_COLLECTION',
    'scl'
)

STR_CONNECTION = os.environ.get(
    'GENERATE_PRETABLE_PARSE_LOG_STR_CONNECTION',
    'mysql://user:pass@localhost:3306/usage'
)

UNSORTED_PRETABLES_DIRECTORY = os.environ.get(
    'GENERATE_PRETABLE_UNSORTED_PRETABLES_DIRECTORY',
    'data/unsorted_pretables/'
)


def _args_to_param(args, ignore):
    params = {}
    for k, v in args.__dict__.items():
        if k not in ignore:
            params[k] = v
    return params


def extract_values(data, header, delimiter):
    """Método auxiliar para extrair valores de um dicionário usando chaves indicadas em um header.

    Parameters
    ----------
    data : dict
        Dicionário de dados
    header : list
        Chaves cujos valores serão usados para extrair os dados
    delimiter: str
        Caractere utilizado para agrupar itens em uma string

    Yields
    ------
    str
        Uma string delimitada por join_char que representa os valores obtidos de data
    """
    return delimiter.join([data.get(h) for h in header])


def generate_pretables(input_file, output_directory, header, extension='tsv', delimiter='\t'):
    """
    Gera arquivo(s) com os dados de log processados.
    Grava um arquivo por dia.

    Parameters
    ----------
    input_file : str
        Nome do arquivo contendo dados de log processados
    output_directory : str
        Caminho no disco em que o arquivo será gravado
    header : list
        Lista de nomes de campos a serem gravados no arquivo de pré-tabela
    extension : str
        Extensão do nome dos arquivos a serem gerados
    delimiter : str
        Separador de colunas dos arquivos a serem gerados
    """
    logging.info('Lendo %s' % input_file)
    with open(input_file) as fin:
        output_files = {}

        csv_reader = csv.DictReader(fin, delimiter=delimiter)

        try:
            for row in csv_reader:
                # obtém yyyy-mm-dd do acesso
                ymd = row.get('serverTime').split(' ')[0]

                # gera nome de arquivo relacionado a ymd
                ymd_output_path = generate_filepath_with_filename(
                    directory=output_directory,
                    filename=ymd,
                    posfix=UNSORTED_POSFIX,
                    extension=extension,
                )

                # verifica se arquivo já existe
                if not os.path.exists(ymd_output_path):
                    logging.info('Criado arquivo %s' % ymd_output_path)
                    create_file_with_header(ymd_output_path, header)

                # abre arquivo em modo append, caso ainda não esteja aberto. adiciona em dicionário uma referência ao arquivo
                if ymd not in output_files:
                    output_files[ymd] = open(ymd_output_path, 'a')

                # obtém uma linha moldada ao formato pré-tabela
                fmt_values = extract_values(row, header, delimiter)

                # grava linha no arquivo de data correta
                output_files[ymd].write(fmt_values + '\n')

        finally:
            # garante fechamento dos arquivos
            for v in output_files.values():
                v.close()


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

    generate_pretables(
        input_file=params.input_file,
        output_directory=params.output_directory,
        header=PRETABLE_FILE_HEADER,
        extension='tsv',
        delimiter='\t',
    )
