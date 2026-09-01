import pytest

from scielo_usage_counter import log_handler


@pytest.fixture
def parser():
    return log_handler.LogParser(
        mmdb_path='tests/fixtures/map.mmdb',
        robots_path='tests/fixtures/counter-robots.txt',
        output_mode='dict',
    )


@pytest.mark.parametrize(
    ('timestamp', 'expected'),
    [
        ('1785887999', '2026-08-04 23:59:59'),
        ('1785887999998', '2026-08-04 23:59:59'),
    ],
)
def test_formats_bunnynet_timestamps_in_seconds_and_milliseconds(
    parser,
    timestamp,
    expected,
):
    assert parser.format_date(timestamp, None) == expected


@pytest.mark.parametrize('timestamp', ['17858879999', '178588799999'])
def test_rejects_ambiguous_bunnynet_timestamp_lengths(parser, timestamp):
    assert parser.format_date(timestamp, None) is None


@pytest.mark.parametrize(
    ('edge_location', 'country_code'),
    [('LA', 'US'), ('BR', 'AR'), ('IQ2', 'IQ'), ('KWI', 'KW')],
)
def test_uses_last_bunnynet_field_as_client_country(
    parser,
    edge_location,
    country_code,
):
    line = (
        'HIT|200|1785887999998|5432|4339610|186.225.0.1|-|'
        'https://www.scielo.br/j/neco/a/test/|'
        f'{edge_location}|Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/151.0.0.0 Safari/537.36|'
        f'8dbbeef65a64c5235f863868a7c94d70|{country_code}'
    )

    result = parser.parse_line(line)

    assert result['country_code'] == country_code
    assert result['local_datetime'] == '2026-08-04 23:59:59'
    assert result['is_valid'] is True
