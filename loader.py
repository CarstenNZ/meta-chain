from typing import Optional, Sequence

from cache.base import Cache
from cache.memcache import MemCache
from datasource.base import DataSource


class Loader:
    """ smart loader, tries memory cache, DB cache and then all the provided data sources
        - if used for all loads (no direct DB or data source calls) then only a single instance
          will exist for each distinct chain object
    """

    def __init__(self, data_sources: Sequence[DataSource], db_cache: Optional[Cache] = None):
        self.data_sources = tuple(data_sources)
        self.caches = [MemCache()] + ([db_cache] if db_cache else [])

    def close(self):
        """ only useful for testing """
        [c.close() for c in self. caches]
        [ds.close() for ds in self.data_sources]
        self.caches = self.data_sources = ()

    def get_block(self, block_number):
        def update_cache(hit_cache):
            for inner_cache in self.caches:
                if inner_cache == hit_cache:
                    return block

                inner_cache.add_block(block)

            return block
        # <def

        # check caches
        for cache in self.caches:
            block = cache.get_block(block_number)
            if block:
                return update_cache(cache)

        # from data sources
        for ds in self.data_sources:
            block = ds.get_block(block_number)
            if block:
                return update_cache(None)

        return None
