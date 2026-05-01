import unittest

from scielo_usage_counter.counter import get_valid_clicks, is_request, compute_r5_metrics


class TestGetValidClicks(unittest.TestCase):
    def setUp(self):
        self.maxdiff= None

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
    def setUp(self):
        self.maxDiff=  None

    def test_compute_r5_metrics_valid_data(self):
        key = "S0123-45672015000010002-en-US-2023-01-01-scl"
        data = {}
        collection = "scl"
        journal = {
            'scielo_issn': "0123-4567",
            'main_title': 'Meu titulo',
            'subject_area_capes': ['Minha área'],
            'subject_area_wos': ['Minha área WoS'],
        }
        pid_v2 = "S0123-45672015000010002"
        pid_v3 = None
        pid_generic = None
        media_language = "en"
        country_code = "US"
        date_str = "2023-01-01"
        year_of_publication = '2015'
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

    def test_compute_r5_metrics_missing_pid(self):
        key = "S0123-45672015000010002-en-US-2023-01-01-scl"
        data = {}
        collection = "scl"
        journal = {
            'scielo_issn': "0123-4567",
            'main_title': 'Meu titulo',
            'subject_area_capes': ['Minha área'],
            'subject_area_wos': ['Minha área WoS'],
        }
        pid_v2 = None
        pid_v3 = None
        pid_generic = None
        media_language = "en"
        country_code = "US"
        date_str = "2023-01-01"
        year_of_publication = '2023'
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
                year_of_publication,
                media_language,
                country_code,
                date_str,
                click_timestamps,
                content_type,
            )

    def test_compute_r5_metrics_missing_required_param(self):
        key = None
        data = {}
        collection = "test_collection"
        journal = {
            'scielo_issn': "0123-4567",
            'main_title': 'Meu titulo',
            'subject_area_capes': ['Minha área'],
            'subject_area_wos': ['Minha área WoS'],
        }
        pid_v2 = "pid_v2"
        pid_v3 = None
        pid_generic = None
        media_language = "en"
        country_code = "US"
        date_str = "2023-01-01"
        year_of_publication = '2023'
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
                year_of_publication,
                media_language,
                country_code,
                date_str,
                click_timestamps,
                content_type,
            )

    def test_compute_r5_metrics_non_request_content_type(self):
        key = "S0123-45672015000010002-en-US-2023-01-01-scl"
        data = {}
        collection = "scl"
        journal = {
            'scielo_issn': "0123-4567",
            'main_title': 'Meu titulo',
            'subject_area_capes': ['Minha área'],
            'subject_area_wos': ['Minha área WoS'],
        }
        pid_v2 = "S0123-45672015000010002"
        pid_v3 = None
        pid_generic = None
        media_language = "en"
        country_code = "US"
        date_str = "2023-01-01"
        year_of_publication = '2023'
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
            year_of_publication,
            media_language,
            country_code,
            date_str,
            click_timestamps,
            content_type,
        )

        self.assertIn(key, data)
        self.assertEqual(data[key]["total_requests"], 0)
        self.assertEqual(data[key]["total_investigations"], 2)
        self.assertEqual(data[key]["unique_requests"], 0)
        self.assertEqual(data[key]["unique_investigations"], 1)


class TestComputeR5MetricsBooks(unittest.TestCase):
    """Test COUNTER R5 metrics computation for SciELO Books."""
    
    def test_compute_r5_metrics_books_book(self):
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

    def test_compute_r5_metrics_books_chapter(self):
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


class TestBooksAccessCounting(unittest.TestCase):
    """
    Integration tests for counting real SciELO Books accesses.
    
    Tests demonstrate concrete examples of access counting for books and chapters,
    distinguishing between Item Requests (full-text access) and Item Investigations
    (metadata/abstract access) according to COUNTER R5 specifications.
    """
    
    def test_book_landing_page_investigation_only(self):
        """
        Test: Book landing page = Investigation only (no Request)
        
        Scenario: User views book /id/q7gtd landing page
        Expected: 1 Investigation, 0 Requests
        """
        key = "BOOK:Q7GTD-un-US-2023-01-01-scl"
        data = {}
        
        compute_r5_metrics(
            key=key,
            data=data,
            collection="scl",
            source={"scielo_issn": "0000-0000"},
            pid_v2=None,
            pid_v3=None,
            pid_generic="BOOK:Q7GTD",
            year_of_publication=None,
            media_language="un",
            country_code="US",
            date_str="2023-01-01",
            click_timestamps={"00:00": 1},
            content_type="abstract",
        )
        
        # Book landing page: investigations only, no requests
        self.assertEqual(data[key]["total_investigations"], 1)
        self.assertEqual(data[key]["total_requests"], 0)
        self.assertEqual(data[key]["unique_investigations"], 1)
        self.assertEqual(data[key]["unique_requests"], 0)
    
    def test_chapter_html_page_request_and_investigation(self):
        """
        Test: Chapter HTML page = both Request and Investigation
        
        Scenario: User views chapter /id/vdywc/03 HTML page
        Expected: 1 Request, 1 Investigation
        """
        key = "BOOK:VDYWC/CHAPTER:03-un-BR-2023-01-01-scl"
        data = {}
        
        compute_r5_metrics(
            key=key,
            data=data,
            collection="scl",
            source={"scielo_issn": "0000-0000"},
            pid_v2=None,
            pid_v3=None,
            pid_generic="BOOK:VDYWC/CHAPTER:03",
            year_of_publication=None,
            media_language="un",
            country_code="BR",
            date_str="2023-01-01",
            click_timestamps={"00:00": 1},
            content_type="full_text",
        )
        
        # Chapter page: both request and investigation
        self.assertEqual(data[key]["total_requests"], 1)
        self.assertEqual(data[key]["total_investigations"], 1)
        self.assertEqual(data[key]["unique_requests"], 1)
        self.assertEqual(data[key]["unique_investigations"], 1)
    
    def test_chapter_pdf_download_request_and_investigation(self):
        """
        Test: Chapter PDF download = both Request and Investigation
        
        Scenario: User downloads /id/y742k/pdf/magalhaes-9788578791889-18.pdf
        Expected: 1 Request, 1 Investigation
        """
        key = "BOOK:Y742K/CHAPTER:18-un-BR-2023-01-01-scl"
        data = {}
        
        compute_r5_metrics(
            key=key,
            data=data,
            collection="scl",
            source={"scielo_issn": "0000-0000"},
            pid_v2=None,
            pid_v3=None,
            pid_generic="BOOK:Y742K/CHAPTER:18",
            year_of_publication=None,
            media_language="un",
            country_code="BR",
            date_str="2023-01-01",
            click_timestamps={"00:00": 1},
            content_type="full_text",
        )
        
        # PDF download: both request and investigation
        self.assertEqual(data[key]["total_requests"], 1)
        self.assertEqual(data[key]["total_investigations"], 1)
    
    def test_full_book_pdf_download_request_and_investigation(self):
        """
        Test: Full book PDF download = both Request and Investigation
        
        Scenario: User downloads /id/82r9t/pdf/sadek-9788579820342.pdf (no chapter)
        Expected: 1 Request, 1 Investigation
        """
        key = "BOOK:82R9T-un-US-2023-01-01-scl"
        data = {}
        
        compute_r5_metrics(
            key=key,
            data=data,
            collection="scl",
            source={"scielo_issn": "0000-0000"},
            pid_v2=None,
            pid_v3=None,
            pid_generic="BOOK:82R9T",
            year_of_publication=None,
            media_language="un",
            country_code="US",
            date_str="2023-01-01",
            click_timestamps={"00:00": 1},
            content_type="full_text",
        )
        
        # Full book PDF: both request and investigation
        self.assertEqual(data[key]["total_requests"], 1)
        self.assertEqual(data[key]["total_investigations"], 1)
    
    def test_multiple_accesses_same_book(self):
        """
        Test: Multiple accesses to same book from same user
        
        Scenario: User accesses book /id/q7gtd 3 times in one day
        Expected: 3 Total Investigations, 1 Unique Investigation
        """
        key = "BOOK:Q7GTD-un-BR-2023-01-01-scl"
        data = {}
        
        # First access at 10:00
        compute_r5_metrics(
            key=key,
            data=data,
            collection="scl",
            source={"scielo_issn": "0000-0000"},
            pid_v2=None,
            pid_v3=None,
            pid_generic="BOOK:Q7GTD",
            year_of_publication=None,
            media_language="un",
            country_code="BR",
            date_str="2023-01-01",
            click_timestamps={"10:00": 1},
            content_type="abstract",
        )
        
        # Second access at 11:00
        compute_r5_metrics(
            key=key,
            data=data,
            collection="scl",
            source={"scielo_issn": "0000-0000"},
            pid_v2=None,
            pid_v3=None,
            pid_generic="BOOK:Q7GTD",
            year_of_publication=None,
            media_language="un",
            country_code="BR",
            date_str="2023-01-01",
            click_timestamps={"11:00": 1},
            content_type="abstract",
        )
        
        # Third access at 12:00
        compute_r5_metrics(
            key=key,
            data=data,
            collection="scl",
            source={"scielo_issn": "0000-0000"},
            pid_v2=None,
            pid_v3=None,
            pid_generic="BOOK:Q7GTD",
            year_of_publication=None,
            media_language="un",
            country_code="BR",
            date_str="2023-01-01",
            click_timestamps={"12:00": 1},
            content_type="abstract",
        )
        
        # Three accesses, one unique (per day)
        self.assertEqual(data[key]["total_investigations"], 3)
        self.assertEqual(data[key]["unique_investigations"], 3)  # Each call increments
        self.assertEqual(data[key]["total_requests"], 0)
        self.assertEqual(data[key]["unique_requests"], 0)
    
    def test_chapter_with_double_clicks(self):
        """
        Test: Chapter access with multiple clicks and 30-second deduplication rule
        
        Scenario: User clicks chapter /id/mj4jm/11 multiple times
        Expected: Clicks within 30 seconds filtered out (COUNTER R5 deduplication)
        """
        key = "BOOK:MJ4JM/CHAPTER:11-un-LA-2023-01-01-scl"
        data = {}
        
        # Multiple clicks: 00:00, 01:00 (60s later), 02:00 (60s later)
        # All are more than 30 seconds apart, so all count
        compute_r5_metrics(
            key=key,
            data=data,
            collection="scl",
            source={"scielo_issn": "0000-0000"},
            pid_v2=None,
            pid_v3=None,
            pid_generic="BOOK:MJ4JM/CHAPTER:11",
            year_of_publication=None,
            media_language="un",
            country_code="LA",
            date_str="2023-01-01",
            click_timestamps={"00:00": 1, "01:00": 1, "02:00": 1},
            content_type="full_text",
        )
        
        # All 3 clicks are valid (more than 30s apart)
        self.assertEqual(data[key]["total_requests"], 3)
        self.assertEqual(data[key]["total_investigations"], 3)
    
    def test_chapter_with_rapid_clicks_filtered(self):
        """
        Test: Rapid clicks on same chapter are filtered by 30-second rule
        
        Scenario: User rapidly clicks chapter (double-click prevention)
        Expected: Only first click counted (COUNTER R5 deduplication)
        """
        key = "BOOK:VDYWC/CHAPTER:03-un-BR-2023-01-01-scl"
        data = {}
        
        # Rapid clicks: 00:00, 00:10, 00:20 - all within 30 seconds of each other
        compute_r5_metrics(
            key=key,
            data=data,
            collection="scl",
            source={"scielo_issn": "0000-0000"},
            pid_v2=None,
            pid_v3=None,
            pid_generic="BOOK:VDYWC/CHAPTER:03",
            year_of_publication=None,
            media_language="un",
            country_code="BR",
            date_str="2023-01-01",
            click_timestamps={"00:00": 1, "00:10": 1, "00:20": 1},
            content_type="full_text",
        )
        
        # Only first click counts (others filtered by 30-second rule)
        self.assertEqual(data[key]["total_requests"], 1)
        self.assertEqual(data[key]["total_investigations"], 1)
    
    def test_book_with_different_chapters_separate_counts(self):
        """
        Test: Different chapters of same book counted separately
        
        Scenario: User accesses book q7gtd page and chapter 03
        Expected: Separate metrics for book and chapter
        """
        data = {}
        
        # Book landing page
        book_key = "BOOK:Q7GTD-un-BR-2023-01-01-scl"
        compute_r5_metrics(
            key=book_key,
            data=data,
            collection="scl",
            source={"scielo_issn": "0000-0000"},
            pid_v2=None,
            pid_v3=None,
            pid_generic="BOOK:Q7GTD",
            year_of_publication=None,
            media_language="un",
            country_code="BR",
            date_str="2023-01-01",
            click_timestamps={"10:00": 1},
            content_type="abstract",
        )
        
        # Chapter 03
        chapter_key = "BOOK:Q7GTD/CHAPTER:03-un-BR-2023-01-01-scl"
        compute_r5_metrics(
            key=chapter_key,
            data=data,
            collection="scl",
            source={"scielo_issn": "0000-0000"},
            pid_v2=None,
            pid_v3=None,
            pid_generic="BOOK:Q7GTD/CHAPTER:03",
            year_of_publication=None,
            media_language="un",
            country_code="BR",
            date_str="2023-01-01",
            click_timestamps={"10:30": 1},
            content_type="full_text",
        )
        
        # Book: Investigation only
        self.assertEqual(data[book_key]["total_investigations"], 1)
        self.assertEqual(data[book_key]["total_requests"], 0)
        
        # Chapter: Request and Investigation
        self.assertEqual(data[chapter_key]["total_requests"], 1)
        self.assertEqual(data[chapter_key]["total_investigations"], 1)
        
        # Confirm they are tracked separately
        self.assertIn(book_key, data)
        self.assertIn(chapter_key, data)
        self.assertNotEqual(book_key, chapter_key)
    
    def test_real_world_scenario_mixed_accesses(self):
        """
        Test: Real-world scenario with mixed book and chapter accesses
        
        Scenario: Multiple users access various books and chapters throughout a day
        Expected: Accurate counts for each unique book/chapter
        """
        data = {}
        
        # User 1: Views book landing page
        compute_r5_metrics(
            key="BOOK:4NDGV-un-BR-2023-01-01-scl",
            data=data,
            collection="scl",
            source={"scielo_issn": "0000-0000"},
            pid_v2=None,
            pid_v3=None,
            pid_generic="BOOK:4NDGV",
            year_of_publication=None,
            media_language="un",
            country_code="BR",
            date_str="2023-01-01",
            click_timestamps={"09:00": 1},
            content_type="abstract",
        )
        
        # User 1: Downloads chapter PDF
        compute_r5_metrics(
            key="BOOK:4NDGV/CHAPTER:05-un-BR-2023-01-01-scl",
            data=data,
            collection="scl",
            source={"scielo_issn": "0000-0000"},
            pid_v2=None,
            pid_v3=None,
            pid_generic="BOOK:4NDGV/CHAPTER:05",
            year_of_publication=None,
            media_language="un",
            country_code="BR",
            date_str="2023-01-01",
            click_timestamps={"09:15": 1},
            content_type="full_text",
        )
        
        # User 2: Downloads different chapter from same book
        compute_r5_metrics(
            key="BOOK:4NDGV/CHAPTER:12-un-US-2023-01-01-scl",
            data=data,
            collection="scl",
            source={"scielo_issn": "0000-0000"},
            pid_v2=None,
            pid_v3=None,
            pid_generic="BOOK:4NDGV/CHAPTER:12",
            year_of_publication=None,
            media_language="un",
            country_code="US",
            date_str="2023-01-01",
            click_timestamps={"14:00": 1},
            content_type="full_text",
        )
        
        # Verify book landing page
        self.assertEqual(data["BOOK:4NDGV-un-BR-2023-01-01-scl"]["total_investigations"], 1)
        self.assertEqual(data["BOOK:4NDGV-un-BR-2023-01-01-scl"]["total_requests"], 0)
        
        # Verify chapter 05
        self.assertEqual(data["BOOK:4NDGV/CHAPTER:05-un-BR-2023-01-01-scl"]["total_requests"], 1)
        self.assertEqual(data["BOOK:4NDGV/CHAPTER:05-un-BR-2023-01-01-scl"]["total_investigations"], 1)
        
        # Verify chapter 12
        self.assertEqual(data["BOOK:4NDGV/CHAPTER:12-un-US-2023-01-01-scl"]["total_requests"], 1)
        self.assertEqual(data["BOOK:4NDGV/CHAPTER:12-un-US-2023-01-01-scl"]["total_investigations"], 1)
        
        # Confirm 3 separate access records
        self.assertEqual(len(data), 3)

