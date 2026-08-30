from collections import OrderedDict
from threading import Lock


class BoundedLRUCache:
    def __init__(self, max_size):
        self._data = OrderedDict()
        self._lock = Lock()
        self._max_size = max_size

    def get(self, key):
        with self._lock:
            try:
                value = self._data.pop(key)
            except KeyError:
                return False, None

            self._data[key] = value
            return True, value

    def set(self, key, value):
        with self._lock:
            self._data.pop(key, None)
            if len(self._data) >= self._max_size:
                self._data.popitem(last=False)
            self._data[key] = value

    def clear(self):
        with self._lock:
            self._data.clear()
