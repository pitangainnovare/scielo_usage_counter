from .values import DEFAULT_REQUEST_TYPES


def get_valid_clicks(clicks: dict) -> int:
    """
    Returns the number of valid clicks from a dictionary of clicks.
    A valid click is defined as a click that occurs within 30 seconds of the last click,
    and each value greater than 1 represents additional clicks (e.g., double-clicks).

    :param clicks: dictionary where keys are timestamps (minute:second) and values are click counts

    :return: number of valid clicks

    Example 1:
    >>> clicks = {'00:00': 1, '00:31': 1, '01:02': 1}
    >>> get_valid_clicks(clicks)
    3

    Example 2:
    >>> clicks = {'00:00': 1, '00:15': 2, '00:25': 1}
    >>> get_valid_clicks(clicks)
    1

    Example 3:
    >>> clicks = {'00:00': 1, '01:00': 1, '02:00': 1}
    >>> get_valid_clicks(clicks)
    3
    """
    sorted_clicks = sorted(clicks.items(), key=lambda x: x[0])
    valid_clicks = 0
    last_timestamp = None

    for timestamp, _ in sorted_clicks:
        minutes, seconds = map(int, timestamp.split(':'))
        current_time_in_seconds = minutes * 60 + seconds

        if last_timestamp is not None:
            last_minutes, last_seconds = map(int, last_timestamp.split(':'))
            last_time_in_seconds = last_minutes * 60 + last_seconds

            if current_time_in_seconds - last_time_in_seconds <= 30:
                last_timestamp = timestamp
                continue

        valid_clicks += 1
        last_timestamp = timestamp

    return valid_clicks


def is_request(content_type: str, request_types: list=DEFAULT_REQUEST_TYPES) -> bool:
    """
    Determines if the content type represents a request. 
    A request refers to access to full content (e.g., full article text, full dataset).

    :param content_type: content type string
    :param request_types: list of request types to check against

    :return: True if the content type represents a request, False otherwise
    """
    if not content_type:
        return False
    
    if not request_types:
        request_types = DEFAULT_REQUEST_TYPES
    
    return content_type.lower() in (rt.lower() for rt in request_types)


def compute_r5_metrics(
    key,
    data,
    collection,
    journal: dict,
    pid_v2,
    pid_v3,
    pid_generic,
    year_of_publication,
    media_language,
    country_code,
    date_str,
    click_timestamps,
    content_type,
):
    """
    Computes the R5 metrics for a given key and updates the data dictionary. The R5 metrics include:
    - total_requests: Total number of requests
    - total_investigations: Total number of investigations
    - unique_requests: Unique number of requests
    - unique_investigations: Unique number of investigations

    :param key: unique identifier for the data entry
    :param data: dictionary to store the computed metrics
    :param collection: collection name
    :param journal: dictionary with journal information (scielo_issn, main_title, subject_area_capes, subject_area_wos)
    :param pid_v2: PID v2
    :param pid_v3: PID v3
    :param pid_generic: generic PID
    :param year_of_publication: year of publication
    :param media_language: language of the media
    :param country_code: country code
    :param date_str: date string in the format YYYY-MM-DD
    :param click_timestamps: dictionary of click timestamps
    :param content_type: content type string

    :raises ValueError: if any of the required parameters are None or empty
    :raises TypeError: if the click_timestamps parameter is not a dictionary
    :raises KeyError: if the key is not found in the data dictionary
    """
    if not isinstance(journal, dict):
        raise TypeError("The 'journal' parameter must be a dictionary.")
    
    if not all([key, collection, journal.get('scielo_issn'), media_language, country_code, date_str, click_timestamps, content_type]):
        raise ValueError("All parameters must be provided.")

    if not (pid_v2 or pid_v3 or pid_generic):
        raise ValueError("At least one PID (v2, v3, or generic) must be provided.")   
    
    pid = pid_v3 or pid_v2 or pid_generic

    if key not in data:
        data[key] = {
            'collection': collection,
            'journal': journal,
            'pid': pid,
            'pid_v2': pid_v2,
            'pid_v3': pid_v3,
            'pid_generic': pid_generic,
            'year_of_publication': year_of_publication,
            'media_language': media_language,
            'country_code': country_code,
            'date': date_str,
            'total_requests': 0, 
            'total_investigations': 0, 
            'unique_requests': 0, 
            'unique_investigations': 0,
        }

    number_of_clicks = get_valid_clicks(click_timestamps)

    data[key]['total_investigations'] += number_of_clicks
    data[key]['unique_investigations'] += 1

    if is_request(content_type):
        data[key]['total_requests'] += number_of_clicks
        data[key]['unique_requests'] += 1
