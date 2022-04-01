from typing import Optional, Sequence, Dict

from cache.base import Cache
from cache.memcache import MemCache
from chainmodel.base import Receipt, Block
from datasource.base import DataSource
from load.loaderbase import LoaderBase


class Loader(LoaderBase):
    """ smart load, tries memory cache, DB cache and then all the provided data sources
        - if used for all loads (no direct DB or data source calls) then only a single instance
          will exist for each distinct chain object
    """

    def __init__(self, data_sources: Sequence[DataSource], db_cache: Optional[Cache] = None,
                 acc_names: Dict[str, str] = None):
        super().__init__()
        self.data_sources = tuple(data_sources)
        self.caches = [MemCache()] + ([db_cache] if db_cache else [])
        self.acc_names = acc_names or {}

    def close(self):
        """ - only useful for testing
        """
        [c.close() for c in self. caches]
        [ds.close() for ds in self.data_sources]
        self.caches = self.data_sources = ()
        super().close()

    def get_block(self, block_number: int) -> Block:
        return self.__get('block', block_number)

    def get_transaction_receipt(self, txhash) -> Optional[Receipt]:
        return self.__get('transaction_receipt', txhash)

    def _get_account_name(self, address) -> Optional[str]:
        return self.acc_names.get(address)

    def __get(self, attrib, arg):
        """ generic cache and data-source access method
        """
        def update_cache(hit_cache):
            for inner_cache in self.caches:
                if inner_cache == hit_cache:
                    return obj

                getattr(inner_cache, adder)(obj, obj_src)

            return obj
        # <def

        getter = 'get_' + attrib
        adder = 'add_' + attrib

        # check caches
        for cache in self.caches:
            obj, obj_src = getattr(cache, getter)(arg)
            if obj:
                return update_cache(cache)

        # from data sources
        for ds in self.data_sources:
            obj, obj_src = getattr(ds, getter)(arg)
            if obj:
                return update_cache(None)

        return None

