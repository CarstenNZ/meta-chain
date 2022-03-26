import shelve
from pathlib import Path
from typing import Optional

from config import Config
from std_format import Hex
from chainmodel.base import Block
from cache.base import Cache


# noinspection PyUnresolvedReferences
class ShelveCache(Cache):
    def __init__(self, config: Optional[Config], clear=False, explicit_path=None):
        """
            - explicit_path overrides config (config can be Null in this case)
            - clear creates an empty cache
        """

        file_path = explicit_path or config.get_cache_path()
        if clear:
            Path(file_path).unlink(missing_ok=True)

        self._shelve = shelve.open(file_path)

    def add_block(self, block: Block):
        self._shelve['b' + Hex.fmt(block.number)] = block

    def get_block(self, block_number):
        return self._shelve.get('b' + Hex.fmt(block_number))

    def close(self):
        if self._shelve:
            self._shelve.close()
            self._shelve = None

    def __enter__(self):
        assert self._shelve is not None
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.close()

    def __del__(self):
        self.close()
