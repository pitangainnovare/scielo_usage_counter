import unittest

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.counter import compute_r5_metrics


class TestCounterBooks(unittest.TestCase):

    def setUp(self):
        self.tm = URLTranslationManager([], [])
        self.default_journal = {"scielo_issn": "0000-0000"}

    def test_example_1_book_landing_page(self):
        """Example 1: Book landing page (Investigation only)."""
        url = "/id/q7gtd"
        result = self.tm.translate(url)
        
        data = {}
        key = "BOOK:Q7GTD-un-US-2023-01-01-books"
        compute_r5_metrics(
            key=key,
            data=data,
            collection="books",
            source=self.default_journal,
            pid_v2=None,
            pid_v3=None,
            pid_generic=result['pid_generic'],
            year_of_publication=None,
            media_language="un",
            country_code="US",
            date_str="2023-01-01",
            click_timestamps={"10:00": 1},
            content_type=result['content_type'],
        )
        
        metrics = data[key]
        self.assertEqual(metrics['total_requests'], 0)
        self.assertEqual(metrics['total_investigations'], 1)
        self.assertEqual(metrics['unique_requests'], 0)
        self.assertEqual(metrics['unique_investigations'], 1)

    def test_example_2_chapter_html(self):
        """Example 2: Chapter HTML page (Request + Investigation)."""
        url = "/id/vdywc/03"
        result = self.tm.translate(url)
        
        data = {}
        key = "BOOK:VDYWC/CHAPTER:03-un-BR-2023-01-01-books"
        compute_r5_metrics(
            key=key,
            data=data,
            collection="books",
            source=self.default_journal,
            pid_v2=None,
            pid_v3=None,
            pid_generic=result['pid_generic'],
            year_of_publication=None,
            media_language="un",
            country_code="BR",
            date_str="2023-01-01",
            click_timestamps={"10:00": 1},
            content_type=result['content_type'],
        )
        
        metrics = data[key]
        self.assertEqual(metrics['total_requests'], 1)
        self.assertEqual(metrics['total_investigations'], 1)

    def test_example_3_chapter_pdf(self):
        """Example 3: Chapter PDF download (Request + Investigation)."""
        url = "/id/y742k/pdf/magalhaes-9788578791889-18.pdf"
        result = self.tm.translate(url)
        
        data = {}
        key = "BOOK:Y742K/CHAPTER:18-un-BR-2023-01-01-books"
        compute_r5_metrics(
            key=key,
            data=data,
            collection="books",
            source=self.default_journal,
            pid_v2=None,
            pid_v3=None,
            pid_generic=result['pid_generic'],
            year_of_publication=None,
            media_language="un",
            country_code="BR",
            date_str="2023-01-01",
            click_timestamps={"10:00": 1},
            content_type=result['content_type'],
        )
        
        metrics = data[key]
        self.assertEqual(metrics['total_requests'], 1)
        self.assertEqual(metrics['total_investigations'], 1)

    def test_example_4_full_book_pdf(self):
        """Example 4: Full book PDF download (Request + Investigation)."""
        url = "/id/82r9t/pdf/sadek-9788579820342.pdf"
        result = self.tm.translate(url)
        
        data = {}
        key = "BOOK:82R9T-un-US-2023-01-01-books"
        compute_r5_metrics(
            key=key,
            data=data,
            collection="books",
            source=self.default_journal,
            pid_v2=None,
            pid_v3=None,
            pid_generic=result['pid_generic'],
            year_of_publication=None,
            media_language="un",
            country_code="US",
            date_str="2023-01-01",
            click_timestamps={"10:00": 1},
            content_type=result['content_type'],
        )
        
        metrics = data[key]
        self.assertEqual(metrics['total_requests'], 1)
        self.assertEqual(metrics['total_investigations'], 1)

    def test_example_5_multiple_chapters(self):
        """Example 5: Different chapters of same book counted separately."""
        data = {}
        
        # Book landing page
        url1 = "/id/4ndgv"
        result1 = self.tm.translate(url1)
        key1 = "BOOK:4NDGV-un-BR-2023-01-01-books"
        compute_r5_metrics(
            key=key1, data=data, collection="books",
            source=self.default_journal,
            pid_v2=None, pid_v3=None,
            pid_generic=result1['pid_generic'],
            year_of_publication=None, media_language="un",
            country_code="BR", date_str="2023-01-01",
            click_timestamps={"09:00": 1},
            content_type=result1['content_type'],
        )
        
        # Chapter 05
        url2 = "/id/4ndgv/pdf/paim-9788575413593-05.pdf"
        result2 = self.tm.translate(url2)
        key2 = "BOOK:4NDGV/CHAPTER:05-un-BR-2023-01-01-books"
        compute_r5_metrics(
            key=key2, data=data, collection="books",
            source=self.default_journal,
            pid_v2=None, pid_v3=None,
            pid_generic=result2['pid_generic'],
            year_of_publication=None, media_language="un",
            country_code="BR", date_str="2023-01-01",
            click_timestamps={"09:15": 1},
            content_type=result2['content_type'],
        )
        
        # Chapter 12
        url3 = "/id/4ndgv/12"
        result3 = self.tm.translate(url3)
        key3 = "BOOK:4NDGV/CHAPTER:12-un-BR-2023-01-01-books"
        compute_r5_metrics(
            key=key3, data=data, collection="books",
            source=self.default_journal,
            pid_v2=None, pid_v3=None,
            pid_generic=result3['pid_generic'],
            year_of_publication=None, media_language="un",
            country_code="BR", date_str="2023-01-01",
            click_timestamps={"09:30": 1},
            content_type=result3['content_type'],
        )

        self.assertEqual(len(data), 3)
        self.assertIn(key1, data)
        self.assertIn(key2, data)
        self.assertIn(key3, data)

    def test_example_6_deduplication(self):
        """Example 6: COUNTER R5 Deduplication (30-second rule)."""
        url = "/id/mj4jm/11"
        result = self.tm.translate(url)
        
        key = "BOOK:MJ4JM/CHAPTER:11-un-LA-2023-01-01-books"

        # Case A: Clicks within 30 seconds (same timestamp map)
        data = {}
        compute_r5_metrics(
            key=key, data=data, collection="books",
            source=self.default_journal,
            pid_v2=None, pid_v3=None,
            pid_generic=result['pid_generic'],
            year_of_publication=None, media_language="un",
            country_code="LA", date_str="2023-01-01",
            click_timestamps={"00:00": 3},  # Simulating multiple rapid clicks via count in one timestamp, or separate ones in dict keys if we were granular
            content_type=result['content_type'],
        )
        
        # If the implementation handles rapid clicks within the same bucket as 1, or filters correctly
        # Currently, the counter.py might just be doing max 1 per metric per interval if implemented as standard.
        # We'll assert total_requests based on expected R5 deduplication logic.
        # Often the dict passed to click_timestamps is just {"HH:MM": count}, and the counter handles it.
        # We expect 1 request regardless of count > 1
        self.assertEqual(data[key]['total_requests'], 1)

        # Case B: Clicks separated by more than 30 seconds (we simulate with different minutes)
        data2 = {}
        compute_r5_metrics(
            key=key, data=data2, collection="books",
            source=self.default_journal,
            pid_v2=None, pid_v3=None,
            pid_generic=result['pid_generic'],
            year_of_publication=None, media_language="un",
            country_code="LA", date_str="2023-01-01",
            click_timestamps={"00:00": 1, "01:00": 1, "02:00": 1},
            content_type=result['content_type'],
        )
        self.assertEqual(data2[key]['total_requests'], 3)
        self.assertEqual(data2[key]['total_investigations'], 3)

    def test_example_8_book_epub_is_request(self):
        url = "/id/k3w36/epub/daza-9789978105689.epub"
        result = self.tm.translate(url)

        data = {}
        key = "BOOK:K3W36-un-US-2023-01-01-books"
        compute_r5_metrics(
            key=key,
            data=data,
            collection="books",
            source=self.default_journal,
            pid_v2=None,
            pid_v3=None,
            pid_generic=result['pid_generic'],
            year_of_publication=None,
            media_language="un",
            country_code="US",
            date_str="2023-01-01",
            click_timestamps={"10:00": 1},
            content_type=result['content_type'],
        )

        metrics = data[key]
        self.assertEqual(metrics['total_requests'], 1)
        self.assertEqual(metrics['total_investigations'], 1)

    def test_example_9_chapter_xhtml_is_request(self):
        url = "/id/p8kpd/Text/12.xhtml"
        result = self.tm.translate(url)

        data = {}
        key = "BOOK:P8KPD/CHAPTER:12-un-PL-2023-01-01-books"
        compute_r5_metrics(
            key=key,
            data=data,
            collection="books",
            source=self.default_journal,
            pid_v2=None,
            pid_v3=None,
            pid_generic=result['pid_generic'],
            year_of_publication=None,
            media_language="un",
            country_code="PL",
            date_str="2023-01-01",
            click_timestamps={"10:00": 1},
            content_type=result['content_type'],
        )

        metrics = data[key]
        self.assertEqual(metrics['total_requests'], 1)
        self.assertEqual(metrics['total_investigations'], 1)

if __name__ == "__main__":
    unittest.main()
