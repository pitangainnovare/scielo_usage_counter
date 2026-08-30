from scielo_usage_counter.cache import BoundedLRUCache


def test_evicts_least_recently_used_entry():
    cache = BoundedLRUCache(max_size=2)
    cache.set("first", 1)
    cache.set("second", 2)

    assert cache.get("first") == (True, 1)

    cache.set("third", 3)

    assert cache.get("second") == (False, None)
    assert cache.get("first") == (True, 1)
    assert cache.get("third") == (True, 3)


def test_distinguishes_cached_none_from_missing_value():
    cache = BoundedLRUCache(max_size=1)
    cache.set("missing-country", None)

    assert cache.get("missing-country") == (True, None)
