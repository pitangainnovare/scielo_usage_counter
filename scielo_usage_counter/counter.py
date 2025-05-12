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

