import unittest

from scielo_usage_counter.counter import get_valid_clicks, is_request, compute_r5_metrics


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


class TestComputeR5Metrics(unittest.TestCase):
    def test_compute_r5_metrics_valid_data(self):
        key = "S0123-45672015000010002-en-US-2023-01-01-scl"
        data = {}
        collection = "scl"
        journal = "S0123-4567"
        pid_v2 = "S0123-45672015000010002"
        pid_v3 = None
        pid_generic = None
        media_language = "en"
        country_code = "US"
        date_str = "2023-01-01"
        year = 2023
        month = 1
        day = 1
        click_timestamps = {"00:00": 1, "00:31": 1}
        content_type = "full_text"

        compute_r5_metrics(
            key,
            data,
            collection,
            journal,
            pid_v2,
            pid_v3,
            pid_generic,
            media_language,
            country_code,
            date_str,
            year,
            month,
            day,
            click_timestamps,
            content_type,
        )

        self.assertIn(key, data)
        self.assertEqual(data[key]["total_requests"], 2)
        self.assertEqual(data[key]["total_investigations"], 2)
        self.assertEqual(data[key]["unique_requests"], 1)
        self.assertEqual(data[key]["unique_investigations"], 1)

    def test_compute_r5_metrics_missing_pid(self):
        key = "S0123-45672015000010002-en-US-2023-01-01-scl"
        data = {}
        collection = "scl"
        journal = "S0123-4567"
        pid_v2 = None
        pid_v3 = None
        pid_generic = None
        media_language = "en"
        country_code = "US"
        date_str = "2023-01-01"
        year = 2023
        month = 1
        day = 1
        click_timestamps = {"00:00": 1}
        content_type = "full_text"

        with self.assertRaises(ValueError):
            compute_r5_metrics(
                key,
                data,
                collection,
                journal,
                pid_v2,
                pid_v3,
                pid_generic,
                media_language,
                country_code,
                date_str,
                year,
                month,
                day,
                click_timestamps,
                content_type,
            )

    def test_compute_r5_metrics_missing_required_param(self):
        key = None
        data = {}
        collection = "test_collection"
        journal = "test_journal"
        pid_v2 = "pid_v2"
        pid_v3 = None
        pid_generic = None
        media_language = "en"
        country_code = "US"
        date_str = "2023-01-01"
        year = 2023
        month = 1
        day = 1
        click_timestamps = {"00:00": 1}
        content_type = "full_text"

        with self.assertRaises(ValueError):
            compute_r5_metrics(
                key,
                data,
                collection,
                journal,
                pid_v2,
                pid_v3,
                pid_generic,
                media_language,
                country_code,
                date_str,
                year,
                month,
                day,
                click_timestamps,
                content_type,
            )

    def test_compute_r5_metrics_non_request_content_type(self):
        key = "S0123-45672015000010002-en-US-2023-01-01-scl"
        data = {}
        collection = "scl"
        journal = "S0123-4567"
        pid_v2 = "S0123-45672015000010002"
        pid_v3 = None
        pid_generic = None
        media_language = "en"
        country_code = "US"
        date_str = "2023-01-01"
        year = 2023
        month = 1
        day = 1
        click_timestamps = {"00:00": 1, "00:31": 1}
        content_type = "abstract"

        compute_r5_metrics(
            key,
            data,
            collection,
            journal,
            pid_v2,
            pid_v3,
            pid_generic,
            media_language,
            country_code,
            date_str,
            year,
            month,
            day,
            click_timestamps,
            content_type,
        )

        self.assertIn(key, data)
        self.assertEqual(data[key]["total_requests"], 0)
        self.assertEqual(data[key]["total_investigations"], 2)
        self.assertEqual(data[key]["unique_requests"], 0)
        self.assertEqual(data[key]["unique_investigations"], 1)


class TestComputeR5MetricsLivros(unittest.TestCase):
    """Test COUNTER R5 metrics computation for SciELO Livros (Books)."""
    
    def test_compute_r5_metrics_livros_book(self):
        """Test R5 metrics computation for a book landing page."""
        key = "BOOK:BOOK001-un-US-2023-01-01-scl"
        data = {}
        collection = "scl"
        journal = {"scielo_issn": "0000-0000"}
        pid_v2 = None
        pid_v3 = None
        pid_generic = "BOOK:BOOK001"
        year_of_publication = None
        media_language = "un"
        country_code = "US"
        date_str = "2023-01-01"
        click_timestamps = {"00:00": 1}
        content_type = "abstract"

        compute_r5_metrics(
            key,
            data,
            collection,
            journal,
            pid_v2,
            pid_v3,
            pid_generic,
            year_of_publication,
            media_language,
            country_code,
            date_str,
            click_timestamps,
            content_type,
        )

        self.assertIn(key, data)
        self.assertEqual(data[key]["total_requests"], 0)
        self.assertEqual(data[key]["total_investigations"], 1)
        self.assertEqual(data[key]["unique_requests"], 0)
        self.assertEqual(data[key]["unique_investigations"], 1)
        self.assertEqual(data[key]["pid_generic"], "BOOK:BOOK001")

    def test_compute_r5_metrics_livros_chapter(self):
        """Test R5 metrics computation for a book chapter."""
        key = "BOOK:BOOK002/CHAPTER:CHAP01-en-BR-2023-01-02-scl"
        data = {}
        collection = "scl"
        journal = {"scielo_issn": "0000-0000"}
        pid_v2 = None
        pid_v3 = None
        pid_generic = "BOOK:BOOK002/CHAPTER:CHAP01"
        year_of_publication = None
        media_language = "en"
        country_code = "BR"
        date_str = "2023-01-02"
        click_timestamps = {"00:00": 1, "00:31": 1}
        content_type = "full_text"

        compute_r5_metrics(
            key,
            data,
            collection,
            journal,
            pid_v2,
            pid_v3,
            pid_generic,
            year_of_publication,
            media_language,
            country_code,
            date_str,
            click_timestamps,
            content_type,
        )

        self.assertIn(key, data)
        self.assertEqual(data[key]["total_requests"], 2)
        self.assertEqual(data[key]["total_investigations"], 2)
        self.assertEqual(data[key]["unique_requests"], 1)
        self.assertEqual(data[key]["unique_investigations"], 1)
        self.assertEqual(data[key]["pid_generic"], "BOOK:BOOK002/CHAPTER:CHAP01")

