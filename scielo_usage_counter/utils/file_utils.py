import bz2
import datetime
import magic
import os
import gzip
import shutil

from scielo_usage_counter import exceptions, values


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


def open_bz2(file_path, mode):
    return bz2.open(file_path, mode)


def extract_gzip(file_path, path_output):
    with gzip.open(file_path, 'rb') as fin:
        with open(path_output, 'wb') as fout:
            shutil.copyfileobj(fin, fout)


def get_mimetype(file_path):
    with open(file_path, 'rb') as fin:
        return magic.from_buffer(fin.read(2048), mime=True)


def open_logfile(file_path):
    file_mime = get_mimetype(file_path)

    if file_mime in ('application/gzip', 'application/x-gzip'):
        return open_gzip(file_path, 'rb')
    elif file_mime in ('application/x-bzip2',):
        return open_bz2(file_path, 'rb')
    elif file_mime in ('application/text', 'text/plain'):
        return open(file_path, 'r')
    else:
        raise exceptions.InvalidLogFileMimeError(f'Arquivo de log inválido: {file_path}')


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


def _filename_contains_dates(filename, dates):
    for d in dates:
        if d in filename or d.replace('-', '') in filename:
            return True
    return False


def get_processed_files(date, processed_logs_directory: str, extension='tsv'):
    all_days = [date]
    
    for i in range(1, 3):
        all_days.append(date + datetime.timedelta(days=-i))
        all_days.append(date + datetime.timedelta(days=+i))

    all_days_str = [d.strftime('%Y-%m-%d') for d in all_days]
    files = [f for f in os.listdir(processed_logs_directory) if f.endswith(extension)]

    return [os.path.join(processed_logs_directory, f) for f in files if _filename_contains_dates(f, all_days_str)]


def translate_date_to_output_path(date, output_directory, posfix='', extension='tsv'):
    str_date = date.strftime('%Y-%m-%d')
    if posfix:
        output_filename = f'{str_date}.{posfix}.{extension}'
    else:
        output_filename = f'{str_date}.{extension}'
    return os.path.join(output_directory, output_filename)


def is_valid_path(path):
    return os.path.exists(path)


def translate_path(path):
    for p in values.LOG_PATH_TRANSLATOR.keys():
        if path.startswith(p):
            return path.replace(p, values.LOG_PATH_TRANSLATOR[p])    
    return path