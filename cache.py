import time

class Cache:
    def __init__(self, ttl=900):
        self.ttl = ttl
        self.cache = {}

    def set(self, key, value):
        self.cache[key] = {
            "value": value,
            "expires_at": time.monotonic() + self.ttl
        }

    def get(self, key):
        if key not in self.cache:
            return None
        if self.cache[key]["expires_at"] <= time.monotonic():
            del self.cache[key]
            return None
        return self.cache[key]["value"]
