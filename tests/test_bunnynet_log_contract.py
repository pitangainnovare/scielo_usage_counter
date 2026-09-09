import re
import unittest

from scielo_usage_counter import log, values


class TestBunnyNetLogContract(unittest.TestCase):
    def setUp(self):
        self.parser = log.LogParser.__new__(log.LogParser)

    def test_formats_timestamp_in_seconds(self):
        self.assertEqual(
            '2026-08-04 23:59:59',
            self.parser.format_date_from_timestamp('1785887999'),
        )

    def test_formats_timestamp_in_milliseconds(self):
        self.assertEqual(
            '2026-08-04 23:59:59',
            self.parser.format_date_from_timestamp('1785887999998'),
        )

    def test_rejects_ambiguous_timestamp_lengths(self):
        for timestamp in ['17858879999', '178588799999']:
            self.assertIsNone(
                self.parser.format_date_from_timestamp(timestamp)
            )

    def test_uses_last_field_as_country_code(self):
        line = (
            'HIT|200|1785887999998|5432|4339610|186.225.0.1|-|'
            'https://www.scielo.br/j/neco/a/test/|IQ2|Mozilla/5.0|'
            '8dbbeef65a64c5235f863868a7c94d70|US'
        )

        match = re.match(values.PATTERN_BUNNY, line)

        self.assertIsNotNone(match)
        self.assertEqual('IQ2', match.groupdict()['edge_location'])
        self.assertEqual('US', match.groupdict()['country_code'])


if __name__ == '__main__':
    unittest.main()
