from cache.base import Cache
from chainmodel.base_model import Block, Receipt, Code


# noinspection PyUnresolvedReferences
class MemCache(Cache):
    def __init__(self):
        self._blocks: Dict[int, Block] = {}
        self._receipts = {}
        self._codes = {}

    def add_block(self, block: Block, block_src: str):
        assert type(block.number) is int
        self._blocks[block.number] = block

    def get_block(self, block_cls, block_number: int):
        return self._blocks.get(block_number), None

    def add_transaction_receipt(self, receipt: Receipt, receipt_src: str):
        self._receipts[receipt.transactionHash] = receipt

    def get_transaction_receipt(self, receipt_cls, transaction_hash):
        return self._receipts.get(transaction_hash), None

    def add_code(self, code: Code, code_bytes: str):
        self._codes[code.address] = code

    def get_code(self, code_cls, contract_address):
        return self._codes.get(contract_address), None

    def close(self):
        pass