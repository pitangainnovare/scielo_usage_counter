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


class TestIsRequest(unittest.TestCase):
    def test_is_request_full_text(self):
        content_type = 'full_text'
        self.assertTrue(is_request(content_type))

    def test_is_request_data(self):
        content_type = 'data'
        self.assertTrue(is_request(content_type))

    def test_is_request_non_request_type(self):
        content_type = 'abstract'
        self.assertFalse(is_request(content_type))

    def test_is_request_empty_content_type(self):
        content_type = ''
        self.assertFalse(is_request(content_type))

    def test_is_request_custom_request_types(self):
        content_type = 'custom_type'
        custom_request_types = ['custom_type', 'another_type']
        self.assertTrue(is_request(content_type, custom_request_types))

    def test_is_request_custom_request_types_non_matching(self):
        content_type = 'non_matching_type'
        custom_request_types = ['custom_type', 'another_type']
        self.assertFalse(is_request(content_type, custom_request_types))

    def test_is_request_case_sensitivity(self):
        content_type = 'Full_Text'
        self.assertTrue(is_request(content_type))

    def test_is_request_none_content_type(self):
        content_type = None
        self.assertFalse(is_request(content_type))
