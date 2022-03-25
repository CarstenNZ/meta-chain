from std_format import Hex
from cache.base import Cache
from chainmodel.base import Block


# noinspection PyUnresolvedReferences
class MemCache(Cache):
    def __init__(self):
        self._blocks = {}

    def add_block(self, block: Block):
        self._blocks[Hex.fmt(block.number)] = block

    def get_block(self, block_number):
        return self._blocks.get(Hex.fmt(block_number))

    def close(self):
        pass