from app import values


def translate_path(path):
    for p in values.LOG_PATH_TRANSLATOR.keys():
        if path.startswith(p):
            return path.replace(p, values.LOG_PATH_TRANSLATOR[p])    
    return path
