from cache.base import Cache
from chainmodel.base import Block


# noinspection PyUnresolvedReferences
class MemCache(Cache):
    def __init__(self):
        self._blocks = {}

    def add_block(self, block: Block):
        assert block.number.startswith('0x')
        self._blocks[block.number] = block

    def get_block(self, block_number):
        assert block_number.startswith('0x')
        return self._blocks.get(block_number)

    def close(self):
        pass