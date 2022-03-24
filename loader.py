from typing import Optional, Sequence, Dict

from cache.base import DbCache
from chainmodel.base import Block
from datasource.base import DataSource


class Loader:
    """ smart loader, tries memory cache, DB cache and then all the provided data sources
        - if used for all loads (no direct DB or data source calls) then only a single instance
          will exist for each distinct chain object
    """

    def __init__(self, data_sources: Sequence[DataSource], db_cache: Optional[DbCache] = None):
        self.db_cache = db_cache
        self.data_sources = tuple(data_sources)

        self._blocks: Dict[str, Block] = {}

    def close(self):
        """ only useful for testing """
        if self.db_cache:
            self.db_cache.close()
            self.db_cache = None

        [ds.close() for ds in self.data_sources]
        self.data_sources = []

    def get_block(self, block_number):
        def add_memCache():
            self._blocks[block.number] = block
            return block
        # <def

        # mem cache
        block = self._blocks.get(block_number)
        if block:
            return block

        # DB cache
        if self.db_cache:
            block = self.db_cache.get_block(block_number)
            if block:
                return add_memCache()

        # from data sources
        for ds in self.data_sources:
            block = ds.get_block(block_number)
            if block:
                break

        if not block:
            return None

        # write to DB cache
        if self.db_cache:
            self.db_cache.add_block(block)

        return add_memCache()

