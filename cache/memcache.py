from std_format import Hex
from cache.base import Cache
from chainmodel.base import Block, Receipt


# noinspection PyUnresolvedReferences
class MemCache(Cache):
    def __init__(self):
        self._blocks: Dict[int, Block] = {}
        self._receipts = {}

    def add_block(self, block: Block, block_src: str):
        assert type(block.number) is int
        self._blocks[block.number] = block

    def get_block(self, block_number: int):
        return self._blocks.get(block_number)

    def add_transaction_receipt(self, receipt: Receipt, receipt_src: str):
        self._receipts[Hex.fmt(receipt.transactionHash)] = receipt

    def get_transaction_receipt(self, transaction_hash):
        return self._receipts.get(Hex.fmt(transaction_hash))

    def close(self):
        pass