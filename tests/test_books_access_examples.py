#!/usr/bin/env python
"""
Demonstration script showing concrete examples of SciELO Books access counting.

This script demonstrates how real accesses to SciELO Books are counted according to
COUNTER R5 specifications, distinguishing between Item Requests and Item Investigations.

Run with: python tests/test_books_access_examples.py
"""

from scielo_usage_counter.url_translator import URLTranslationManager
from scielo_usage_counter.counter import compute_r5_metrics


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_access(url, result, metrics=None):
    """Print details of an access."""
    print(f"\nURL: {url}")
    print(f"  → Book ID: {result.get('book_id')}")
    print(f"  → Chapter ID: {result.get('chapter_id')}")
    print(f"  → PID: {result.get('pid_generic')}")
    print(f"  → Content Type: {result.get('content_type')}")
    print(f"  → Media Format: {result.get('media_format')}")
    
    if metrics:
        print(f"\n  COUNTER R5 Metrics:")
        print(f"    Total Requests: {metrics['total_requests']}")
        print(f"    Total Investigations: {metrics['total_investigations']}")
        print(f"    Unique Requests: {metrics['unique_requests']}")
        print(f"    Unique Investigations: {metrics['unique_investigations']}")


def example_1_book_landing_page():
    """Example 1: Book landing page (Investigation only)."""
    print_section("Example 1: Book Landing Page Access")
    
    print("\nScenario: User views book landing page at /id/q7gtd")
    print("Expected: 1 Investigation, 0 Requests (metadata view only)")
    
    # Translate URL
    tm = URLTranslationManager([], [])
    url = "/id/q7gtd"
    result = tm.translate(url)
    
    # Compute metrics
    data = {}
    key = "BOOK:Q7GTD-un-US-2023-01-01-scl"
    compute_r5_metrics(
        key=key,
        data=data,
        collection="scl",
        journal={"scielo_issn": "0000-0000"},
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
    
    print_access(url, result, data[key])


def example_2_chapter_html():
    """Example 2: Chapter HTML page (Request + Investigation)."""
    print_section("Example 2: Chapter HTML Page Access")
    
    print("\nScenario: User views chapter 03 at /id/vdywc/03")
    print("Expected: 1 Request, 1 Investigation (full-text access)")
    
    # Translate URL
    tm = URLTranslationManager([], [])
    url = "/id/vdywc/03"
    result = tm.translate(url)
    
    # Compute metrics
    data = {}
    key = "BOOK:VDYWC/CHAPTER:03-un-BR-2023-01-01-scl"
    compute_r5_metrics(
        key=key,
        data=data,
        collection="scl",
        journal={"scielo_issn": "0000-0000"},
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
    
    print_access(url, result, data[key])


def example_3_chapter_pdf():
    """Example 3: Chapter PDF download (Request + Investigation)."""
    print_section("Example 3: Chapter PDF Download")
    
    print("\nScenario: User downloads chapter 18 PDF")
    print("URL: /id/y742k/pdf/magalhaes-9788578791889-18.pdf")
    print("Expected: 1 Request, 1 Investigation (full-text download)")
    
    # Translate URL
    tm = URLTranslationManager([], [])
    url = "/id/y742k/pdf/magalhaes-9788578791889-18.pdf"
    result = tm.translate(url)
    
    # Compute metrics
    data = {}
    key = "BOOK:Y742K/CHAPTER:18-un-BR-2023-01-01-scl"
    compute_r5_metrics(
        key=key,
        data=data,
        collection="scl",
        journal={"scielo_issn": "0000-0000"},
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
    
    print_access(url, result, data[key])


def example_4_full_book_pdf():
    """Example 4: Full book PDF download (Request + Investigation)."""
    print_section("Example 4: Full Book PDF Download")
    
    print("\nScenario: User downloads entire book PDF (no chapter number)")
    print("URL: /id/82r9t/pdf/sadek-9788579820342.pdf")
    print("Expected: 1 Request, 1 Investigation (full-text download)")
    
    # Translate URL
    tm = URLTranslationManager([], [])
    url = "/id/82r9t/pdf/sadek-9788579820342.pdf"
    result = tm.translate(url)
    
    # Compute metrics
    data = {}
    key = "BOOK:82R9T-un-US-2023-01-01-scl"
    compute_r5_metrics(
        key=key,
        data=data,
        collection="scl",
        journal={"scielo_issn": "0000-0000"},
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
    
    print_access(url, result, data[key])


def example_5_multiple_chapters():
    """Example 5: Different chapters of same book counted separately."""
    print_section("Example 5: Multiple Chapters from Same Book")
    
    print("\nScenario: User accesses book landing page, then two different chapters")
    print("Expected: Separate metrics for each book/chapter combination")
    
    tm = URLTranslationManager([], [])
    data = {}
    
    # Book landing page
    url1 = "/id/4ndgv"
    result1 = tm.translate(url1)
    key1 = "BOOK:4NDGV-un-BR-2023-01-01-scl"
    compute_r5_metrics(
        key=key1, data=data, collection="scl",
        journal={"scielo_issn": "0000-0000"},
        pid_v2=None, pid_v3=None,
        pid_generic=result1['pid_generic'],
        year_of_publication=None, media_language="un",
        country_code="BR", date_str="2023-01-01",
        click_timestamps={"09:00": 1},
        content_type=result1['content_type'],
    )
    
    # Chapter 05
    url2 = "/id/4ndgv/pdf/paim-9788575413593-05.pdf"
    result2 = tm.translate(url2)
    key2 = "BOOK:4NDGV/CHAPTER:05-un-BR-2023-01-01-scl"
    compute_r5_metrics(
        key=key2, data=data, collection="scl",
        journal={"scielo_issn": "0000-0000"},
        pid_v2=None, pid_v3=None,
        pid_generic=result2['pid_generic'],
        year_of_publication=None, media_language="un",
        country_code="BR", date_str="2023-01-01",
        click_timestamps={"09:15": 1},
        content_type=result2['content_type'],
    )
    
    # Chapter 12
    url3 = "/id/4ndgv/12"
    result3 = tm.translate(url3)
    key3 = "BOOK:4NDGV/CHAPTER:12-un-BR-2023-01-01-scl"
    compute_r5_metrics(
        key=key3, data=data, collection="scl",
        journal={"scielo_issn": "0000-0000"},
        pid_v2=None, pid_v3=None,
        pid_generic=result3['pid_generic'],
        year_of_publication=None, media_language="un",
        country_code="BR", date_str="2023-01-01",
        click_timestamps={"09:30": 1},
        content_type=result3['content_type'],
    )
    
    print_access(url1, result1, data[key1])
    print_access(url2, result2, data[key2])
    print_access(url3, result3, data[key3])
    
    print(f"\n  Total unique records: {len(data)}")
    print("  → Each book/chapter combination is tracked separately")


def example_6_deduplication():
    """Example 6: 30-second deduplication rule."""
    print_section("Example 6: COUNTER R5 Deduplication (30-second rule)")
    
    print("\nScenario: User rapidly clicks same chapter multiple times")
    print("Expected: Only valid clicks counted (30-second deduplication)")
    
    tm = URLTranslationManager([], [])
    url = "/id/mj4jm/11"
    result = tm.translate(url)
    
    data = {}
    key = "BOOK:MJ4JM/CHAPTER:11-un-LA-2023-01-01-scl"
    
    print("\nCase A: Clicks within 30 seconds (00:00, 00:10, 00:20)")
    compute_r5_metrics(
        key=key, data=data, collection="scl",
        journal={"scielo_issn": "0000-0000"},
        pid_v2=None, pid_v3=None,
        pid_generic=result['pid_generic'],
        year_of_publication=None, media_language="un",
        country_code="LA", date_str="2023-01-01",
        click_timestamps={"00:00": 1, "00:10": 1, "00:20": 1},
        content_type=result['content_type'],
    )
    
    print_access(url, result, data[key])
    print("  → Only 1 click counted (rapid clicks filtered)")
    
    data2 = {}
    print("\n\nCase B: Clicks more than 30 seconds apart (00:00, 01:00, 02:00)")
    compute_r5_metrics(
        key=key, data=data2, collection="scl",
        journal={"scielo_issn": "0000-0000"},
        pid_v2=None, pid_v3=None,
        pid_generic=result['pid_generic'],
        year_of_publication=None, media_language="un",
        country_code="LA", date_str="2023-01-01",
        click_timestamps={"00:00": 1, "01:00": 1, "02:00": 1},
        content_type=result['content_type'],
    )
    
    print(f"\n  COUNTER R5 Metrics:")
    print(f"    Total Requests: {data2[key]['total_requests']}")
    print(f"    Total Investigations: {data2[key]['total_investigations']}")
    print("  → All 3 clicks counted (sufficiently spaced)")


def main():
    """Run all examples."""
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    print("#  SciELO Books Access Counting - Concrete Examples".center(80) + "#")
    print("#  COUNTER R5 Specifications".center(80) + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80)
    
    example_1_book_landing_page()
    example_2_chapter_html()
    example_3_chapter_pdf()
    example_4_full_book_pdf()
    example_5_multiple_chapters()
    example_6_deduplication()
    
    print("\n" + "=" * 80)
    print("  Summary: Request vs Investigation")
    print("=" * 80)
    print("\n  INVESTIGATIONS ONLY (metadata/abstract view):")
    print("    • Book landing page: /id/{book_id}")
    print("\n  REQUESTS + INVESTIGATIONS (full-text access):")
    print("    • Chapter HTML page: /id/{book_id}/{chapter_number}")
    print("    • Chapter PDF: /id/{book_id}/pdf/filename-{chapter}.pdf")
    print("    • Full book PDF: /id/{book_id}/pdf/filename.pdf")
    print("\n  DEDUPLICATION:")
    print("    • Clicks within 30 seconds are filtered (COUNTER R5 rule)")
    print("    • Each book/chapter tracked separately")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
