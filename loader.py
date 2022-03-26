from typing import Optional, Sequence

from cache.base import Cache
from cache.memcache import MemCache
from chainmodel.base import Receipt
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
        return self.__get('block', block_number)

    def get_transaction_receipt(self, txhash) -> Optional[Receipt]:
        return self.__get('transaction_receipt', txhash)

    def __get(self, attrib, arg):
        """ generic cache and data source access method """
        def update_cache(hit_cache):
            for inner_cache in self.caches:
                if inner_cache == hit_cache:
                    return obj

                getattr(inner_cache, adder)(obj)

            return obj
        # <def

        getter = 'get_' + attrib
        adder = 'add_' + attrib

        # check caches
        for cache in self.caches:
            obj = getattr(cache, getter)(arg)
            if obj:
                return update_cache(cache)

        # from data sources
        for ds in self.data_sources:
            obj = getattr(ds, getter)(arg)
            if obj:
                return update_cache(None)

        return None

