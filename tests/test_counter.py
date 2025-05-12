import unittest

from scielo_usage_counter.counter import get_valid_clicks, is_request


class TestGetValidClicks(unittest.TestCase):
    def test_valid_clicks_within_00_10_20(self):
        clicks = {'00:00': 1, '00:10': 1, '00:20': 1}
        expected_clicks = 1
        obtained_clicks = get_valid_clicks(clicks)
        self.assertEqual(expected_clicks, obtained_clicks)

    def test_valid_clicks_with_min_gap(self):
        clicks = {'00:00': 1, '00:31': 1, '01:02': 1}
        expected_clicks = 3
        obtained_clicks = get_valid_clicks(clicks)
        self.assertEqual(expected_clicks, obtained_clicks)

    def test_valid_clicks_multiple_within_30_seconds(self):
        clicks = {'00:00': 1, '00:15': 2, '00:25': 1}
        expected_clicks = 1
        obtained_clicks = get_valid_clicks(clicks)
        self.assertEqual(expected_clicks, obtained_clicks)

    def test_valid_clicks_no_clicks(self):
        clicks = {}
        expected_clicks = 0
        obtained_clicks = get_valid_clicks(clicks)
        self.assertEqual(expected_clicks, obtained_clicks)

    def test_valid_clicks_single_click(self):
        clicks = {'00:00': 1}
        expected_clicks = 1
        obtained_clicks = get_valid_clicks(clicks)
        self.assertEqual(expected_clicks, obtained_clicks)

    def test_valid_clicks_single_click_twice(self):
        clicks = {'00:00': 2}
        expected_clicks = 1
        obtained_clicks = get_valid_clicks(clicks)
        self.assertEqual(expected_clicks, obtained_clicks)

    def test_valid_clicks_edge_case_30_seconds(self):
        clicks = {'00:00': 1, '00:30': 1, '01:00': 1}
        expected_clicks = 1
        obtained_clicks = get_valid_clicks(clicks)
        self.assertEqual(expected_clicks, obtained_clicks)

    def test_valid_clicks_large_gap(self):
        clicks = {'00:00': 1, '01:00': 1, '02:00': 1}
        expected_clicks = 3
        obtained_clicks = get_valid_clicks(clicks)
        self.assertEqual(expected_clicks, obtained_clicks)

    def test_valid_clicks_multiple_clicks(self):
        clicks = {'00:00': 3, '00:15': 2, '01:45': 1}
        expected_clicks = 2
        obtained_clicks = get_valid_clicks(clicks)
        self.assertEqual(expected_clicks, obtained_clicks)

