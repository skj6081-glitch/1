"""Week 3 · Task 3 — A Local DNS Cache"""

class BaselineCache:
    """The baseline cache always fetches from upstream."""
    def __init__(self, upstream):
        self.upstream = upstream

    def lookup(self, name, now):
        address, ttl = self.upstream(name)
        return address

    def stats(self):
        return {"entries": 0}


class YourCache:
    """Your cache.

    Same interface: __init__(upstream), lookup(name, now) -> address, stats().
    `upstream(name)` costs a network round trip and returns (address, ttl).
    The TTL is in seconds and it is the authoritative answer's own TTL -
    the baseline throws it away.
    """

    def __init__(self, upstream):
        self.upstream = upstream
        # Dictionary to store cached records for O(1) lookups
        # Format: { 'domain_name': (address, expires_at) }
        self.cache = {}

    def lookup(self, name, now):
        # 1. Check if the name is in cache and has NOT expired
        if name in self.cache:
            address, expires_at = self.cache[name]
            if now < expires_at:
                return address # Cache Hit (Fresh)
            # If expired, we naturally fall through to fetch a new one
            
        # 2. Cache Miss or Expired: Fetch from upstream
        address, ttl = self.upstream(name)
        
        # 3. Store in cache with the correct expiration time based on ACTUAL TTL
        self.cache[name] = (address, now + ttl)
        
        return address

    def stats(self):
        return {"entries": len(self.cache)}
