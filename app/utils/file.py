import datetime
import magic
import os
import gzip
import shutil


def check_dir(output):
    if not os.path.isdir(output):
        dirname = os.path.dirname(output)
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

    if file_mime == 'application/gzip':
        return open_gzip(file_path, 'rb')
    elif file_mime == 'application/text':
        return open(file_path, 'r')


def generate_filepath_with_date(directory, date, extension='tsv'):
    try:
        date_str = date.strftime('%Y-%m-%d')
    except ValueError:
        raise

    filename = f'{date_str}.{datetime.datetime.utcnow().timestamp()}.{extension}'

    return os.path.join(directory, filename)
def generate_filepath_with_filename(directory, filename, extension='tsv'):
    return os.path.join(directory, f'{filename}.{extension}')
