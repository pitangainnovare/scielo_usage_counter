import logging
import re
import tempfile


def load_robots(robots_list: None, robots_path: None):
    """
    Load robots from a list or a file path.
    This function attempts to load robots from the provided list first. 
    If the list is not provided or is empty, it then attempts to load 
    robots from the provided file path. If neither is provided, it logs 
    a warning and returns an empty set.
    
    Parameters:
    -----------
        robots_list (list or None): A list of robots. This parameter has precedence over robots_path.
        robots_path (str or None): A file path to load robots from.
        
    Returns:
    --------
        set: A set of robots loaded from the list or file path.
    """
    if robots_list:
        return load_robots_from_list(robots_list)
    
    elif robots_path:
        return load_robots_from_path(robots_path)
    
    else:
        logging.warning('No robots provided.')
        return set()


def load_robots_from_list(robots: list):
    return set([compile_pattern(r) for r in robots])


def load_robots_from_path(path: str):
    robots = set()
    
    with open(path) as fin:
        for r in fin:
            robots.add(compile_pattern(r))
    
    return robots


def compile_pattern(pattern):
    return re.compile(pattern.strip(), re.IGNORECASE)


def load_mmdb(mmdb_data: bytes=None, mmdb_path: str=None):
    """
    Load the MMDB data from a file or a bytes object.
    
    Parameters:
    -----------
        mmdb_data (bytes or None): The MMDB data as bytes.
        mmdb_path (str or None): The file path to the MMDB data.
        
    Returns:
    --------
        bytes: The MMDB data as bytes.
    """
    if mmdb_data:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(mmdb_data)
            return temp_file.name
    
    elif mmdb_path:
        return mmdb_path
    
    else:
        logging.warning('No MMDB data provided.')
        return None
