import shelve
from pathlib import Path
from typing import Optional

from cache.base import Cache
from chainmodel.base_model import Block, Receipt, Code
from config import Config


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

        self._shelve = shelve.open(str(file_path))

    def add_block(self, block: Block, block_src: str):
        self._shelve[f'b{block.number}'] = block_src

    def get_block(self, block_cls, block_number: int):
        block_src = self._shelve.get(f'b{block_number}')
        if block_src is None:
            return None, None

        # noinspection PyTypeChecker
        block_src = dict(block_src)
        return block_cls(block_src), block_src

    def add_transaction_receipt(self, receipt: Receipt, receipt_src: str):
        self._shelve['r' + receipt.transactionHash] = receipt_src

    def get_transaction_receipt(self, receipt_cls, transaction_hash):
        receipt_src = self._shelve.get('r' + transaction_hash)
        if receipt_src is None:
            return None, None

        # noinspection PyTypeChecker
        receipt_src = dict(receipt_src)
        return receipt_cls(receipt_src), receipt_src

    def add_code(self, code: Code, code_bytes: str):
        self._shelve['c' + code.address] = code_bytes

    def get_code(self, contract_cls, contract_address):
        contract_src = self._shelve.get(f'c{contract_address}')
        if contract_src is None:
            return None, None

        return Code(contract_address, contract_src), contract_src

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
