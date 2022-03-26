from std_format import Hex
from cache.base import Cache
from chainmodel.base import Block, Receipt


# noinspection PyUnresolvedReferences
class MemCache(Cache):
    def __init__(self):
        self._blocks = {}
        self._receipts = {}

    def add_block(self, block: Block):
        self._blocks[Hex.fmt(block.number)] = block

    def get_block(self, block_number):
        return self._blocks.get(Hex.fmt(block_number))

    def add_transaction_receipt(self, receipt: Receipt):
        self._receipts[Hex.fmt(receipt.transactionHash)] = receipt

    def get_transaction_receipt(self, transaction_hash):
        return self._receipts.get(Hex.fmt(transaction_hash))

    def close(self):
        pass