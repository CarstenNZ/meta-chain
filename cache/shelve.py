import shelve
from pathlib import Path

from chainmodel.base import Block
from cache.base import DbCache


# noinspection PyUnresolvedReferences
class ShelveCache(DbCache):
    def __init__(self, file_path, clear=False):
        if clear:
            Path(file_path).unlink(missing_ok=True)

        self._shelve = shelve.open(file_path)

    def add_block(self, block: Block):
        self._shelve['b' + block.number] = block

    def get_block(self, block_number):
        assert block_number.startswith('0x')
        return self._shelve.get('b' + block_number)

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
