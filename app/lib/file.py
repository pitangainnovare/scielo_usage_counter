import datetime
import magic
import os
import gzip
import shutil

from app.lib.exceptions import (
    InvalidLogFileMimeError,
)


def check_dir(output, force_tail=False):
    if not force_tail:
        if not os.path.isdir(output):
            dirname = os.path.dirname(output)
        else:
            dirname = output
    else:
        dirname = output

    if not os.path.exists(dirname):
        os.makedirs(dirname)


def open_gzip(file_path, mode):
    return gzip.GzipFile(file_path, mode)


def extract_gzip(file_path):
    with gzip.open(file_path, 'rb') as fin:
        with open(file_path.replace('.gz', ''), 'wb') as fout:
            shutil.copyfileobj(fin, fout)


def get_mimetype(file_path):
    with open(file_path, 'rb') as fin:
        return magic.from_buffer(fin.read(2048), mime=True)


def open_logfile(file_path):
    file_mime = get_mimetype(file_path)

    if file_mime in ('application/gzip', 'application/x-gzip'):
        return open_gzip(file_path, 'rb')
    elif file_mime in ('application/text', 'text/plain'):
        return open(file_path, 'r')
    else:
        raise InvalidLogFileMimeError(f'Arquivo de log inválido: {file_path}')


def generate_filepath(output_directory, input_filepath, extension='tsv'):
    filename = os.path.basename(input_filepath)
    output_filename = f'{filename}.{datetime.datetime.utcnow().timestamp()}.{extension}'

    return os.path.join(output_directory, output_filename)


def generate_filepath_with_filename(directory, filename, posfix, extension='tsv'):
    if posfix:
        return os.path.join(directory, f'{filename}.{posfix}.{extension}')
    return os.path.join(directory, f'{filename}.{extension}')


def create_file_with_header(path, header=[], delimiter='\t'):
    with open(path, 'w') as fout:
        fout.write(delimiter.join(header) + '\n')
